"""
Holographic AI head for the HUD centre — the thing that used to be a ring stack
with the assistant's name in the middle.

Design notes
------------
* **The face is real human geometry.** `core.avatar_mesh` builds the head around
  MediaPipe's canonical face model, so eyelids, nostrils, lips and cheekbones
  are measured anatomy rather than fitted curves. This renderer's whole job is
  to light it, pose it and animate it.
* **Software rendered, on purpose.** Everything is QPainter, so there is no
  OpenGL context, no shader compile, no GPU driver to disagree with us and no
  new pip dependency. It looks the same on a gaming rig, a 2013 laptop, a VM
  and a remote desktop session.
* **Lip-sync comes from the audio pipeline, not from the avatar.** `main.py`
  already computes a real RMS level off the PCM (`_pcm_level`) for both the mic
  and VIERNES's own output. The avatar just consumes that number, so there is no
  second audio path to fall out of sync. The mouth only tracks the level while
  VIERNES is *speaking* — during listening the same level drives the aura, so the
  head never lip-syncs to the user's voice.

The renderer is theme-agnostic: `paint()` takes its colours as arguments, which
is what lets the HueWheel accent picker retint the avatar for free.
"""

from __future__ import annotations

from pathlib import Path
import math
import random

import numpy as np
from PyQt6.QtCore import QLineF, QPointF, QRectF, Qt
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen, QPolygonF, QRadialGradient, QLinearGradient, QPixmap, QTransform, QFont

from core.avatar_mesh import JAW_MAX, JAW_PIVOT, get_head_mesh

# Perspective camera distance in head-half-heights. Large enough that the nose
# does not balloon, small enough to keep a sense of depth.
_CAM_D = 4.6

# Wireframe opacity buckets, so the whole lattice draws in a handful of batched
# drawLines() calls instead of one call per line.
_BUCKETS = 4
_MIN_ALPHA = 0.05

# Resolution of the surface-shading colour ramp. Banding across a filled facet
# is far more visible than banding in line alpha, so this is fine-grained — and
# being a lookup it costs nothing per face.
_LUT_N = 192

# How far the brows travel at full lift, in head-half-heights. Derived, not
# tuned: the brow-to-eye gap is 0.198 and a real raise covers about a third of
# it, then the drawn landmarks only carry half the rig weight.
_BROW_LIFT = 0.14

# Mouth timing, as time constants in seconds rather than per-frame fractions.
# A fixed per-frame lerp silently changes speed with the frame rate: the HUD
# runs at 60 Hz here, throttles its paint to 30, and drops to 20 when idle, so
# the same constant meant three different mouths. These do not.
#
# Shutting is the fastest of the three, and it is measured rather than chosen.
# A short closure occupies a single 20 ms schedule frame, so the mouth has one
# step to reach it: at 20 ms the jaw got a third of the way and the closure
# vanished, at 12 ms it arrives, and going below that changes nothing because
# the analysis window is then the limit, not the smoothing. Halving it doubled
# the closures the mouth visibly makes across a test paragraph, 5 of 21 to 10,
# with no loss of opening on the vowels. Only the return to rest, once talking
# has actually stopped, is leisurely.
_TAU_OPEN = 0.022     # jaw dropping toward a vowel
_TAU_SHUT = 0.012     # lips closing on a consonant, mid-word
_TAU_REST = 0.055     # settling back to rest after speech ends
_TAU_SHAPE = 0.018    # viseme openness following the schedule

# Only the microphone path needs a level floor: it has one coarse RMS and no way
# to tell speech from room tone. VIERNES's own voice arrives as a per-20 ms
# schedule whose silences are already silent, so it needs no floor and must not
# have one — a floor there swallows the gaps between words.
_MIC_FLOOR = 0.14

# How far below this voice's own loud level counts as a closure: -20 dB, which
# is what a stop consonant actually drops to. Expressed as a ratio so it holds
# at any speaker volume.
_CLOSE_FRAC = 0.10


def _rate(dt: float, tau: float) -> float:
    """Per-frame lerp factor for an exponential approach with time constant
    `tau`. Frame-rate independent: the motion takes the same wall-clock time at
    20, 30 or 60 fps, and a long frame catches up instead of stalling."""
    return 1.0 - math.exp(-dt / tau)


def _c(col: QColor, a: float) -> QColor:
    """Copy of `col` at alpha `a` (0-255, clamped)."""
    q = QColor(col)
    q.setAlpha(int(max(0.0, min(255.0, a))))
    return q


def _blend(bg: QColor, col: QColor, a: float) -> QColor:
    """`col` at alpha `a` pre-mixed onto `bg`, returned fully **opaque**.

    Qt's raster engine has a fast path for opaque antialiased lines and a much
    slower blended path for everything else — measured at 1.0 ms versus 2.9 ms
    for the same 780 lines. The HUD paints a flat background behind the avatar,
    so mixing the alpha in by hand is visually equivalent and three times cheaper.
    """
    f = max(0.0, min(1.0, a / 255.0))
    return QColor(int(bg.red() + (col.red() - bg.red()) * f),
                  int(bg.green() + (col.green() - bg.green()) * f),
                  int(bg.blue() + (col.blue() - bg.blue()) * f))


class _MeshAvatar:
    """Animated holographic head. One instance per HUD canvas.

    Lifecycle:
        av = HoloAvatar()
        av.step(dt, amp, speaking=..., muted=...)          # once per tick
        av.paint(painter, cx, cy, r, primary, accent, bg)  # once per frame
    """

    # Look: True paints a lit, solid head with a wireframe over it; False is a
    # see-through glass wireframe. Flip here, or per instance.
    shaded = True

    def __init__(self) -> None:
        mesh = get_head_mesh()
        self._v0 = mesh["verts"]
        self._n0 = mesh["normals"]
        self._jaw = mesh["jaw"]
        self._brow_w = mesh["brow"]
        self._lips_w = mesh["lips"]
        self._lip_c = mesh["lip_centre"]
        self._fade = mesh["fade"]
        self._f = mesh["faces"]
        self._fgroup = mesh["face_group"]
        self._fa, self._fb, self._fc = (self._f[:, i] for i in range(3))
        self._e0 = mesh["edges"][:, 0]
        self._e1 = mesh["edges"][:, 1]
        self._lm = mesh["landmarks"]
        # The inner-lip ring runs lower-lip left→right, then upper-lip back.
        # Splitting it lets the upper arc anchor a strip of teeth, which is what
        # keeps an open mouth from reading as a hole punched in the face.
        lips_in = mesh["landmarks"]["lips_in"]
        self._lip_up = np.concatenate([lips_in[10:], lips_in[:1]])

        # Crown (+1.0) down to the bottom of the neck, in head-half-heights.
        # Callers size the head to the room they have with this.
        self.SPAN = mesh["span"][0] - mesh["span"][1]

        self._lut_cache: list = []
        self._lut_key = None

        n = self._v0.shape[0]
        self._v = np.empty((n, 3), dtype=np.float32)

        self._t = 0.0
        self._sway = 0.0           # integrated sway phase — see step()
        self._yaw = 0.0
        self._pitch = 0.0
        self._mouth = 0.0          # 0..1 smoothed jaw opening
        self._glow = 0.0           # 0..1 smoothed overall energy
        self._scan = -1.6          # vertical position of the energy sweep
        self._blink = 0.0          # 0 = open, 1 = shut
        self._blink_at = 3.0

        # ── expression ──────────────────────────────────────────────────────
        # Speech is not just a moving jaw. Brows ride the loudness envelope,
        # eyes widen with the brows, and the gaze flicks between fixation
        # points — those three are what make it read as talking rather than as
        # a puppet chewing.
        self._amp_slow = 0.0
        self._expr = 0.0
        self._expr_tgt = 0.0
        self._expr_at = 0.0
        self._brow = 0.0           # smoothed brow lift, -0.4 .. 1.2
        self._emph = 0.0           # syllable emphasis, drives the head nod
        self._gaze = [0.0, 0.0]
        self._gaze_tgt = [0.0, 0.0]
        self._gaze_at = 0.0

        # ── state expression ────────────────────────────────────────────────
        # The face is the fastest status indicator in the app: you read a gaze
        # before you read a word. Saccades orbit a bias that the assistant's
        # state moves — eyes off to the side while it thinks, back on you while
        # it listens, lids low while it sleeps.
        self._gaze_bias = [0.0, 0.0]
        self._bias_tgt = [0.0, 0.0]
        self._bias_at = 0.0
        self._lids = 1.0           # 1 = wide, 0 = shut; low while asleep
        self._brow_bias = 0.0      # concentration pulls the brows down
        self._glance = None        # (dx, dy, until_t) — a deliberate look

        # ── viseme ──────────────────────────────────────────────────────────
        # Loudness alone only answers "how far open", which is why an RMS-driven
        # mouth flaps rather than speaks. These two carry the *shape*: how open
        # the jaw is for this sound, and whether the lips are spread (/i/) or
        # rounded (/u/). They come from a formant read of the audio actually
        # being played — see `_pcm_visemes` in main.py.
        self._v_open = 1.0
        self._v_wide = 0.0
        self._wide = 0.0           # smoothed lip spread, -1 round .. +1 spread
        self._v_peak = 0.18        # running estimate of this voice's loud level

    # ── animation ───────────────────────────────────────────────────────────

    def _mouth_step(self, dt: float, amp: float, live: bool,
                    v_open: float | None, v_level: float | None) -> None:
        """One increment of the jaw. Called once per viseme frame while VIERNES
        speaks, once per rendered frame otherwise."""
        if v_open is None:
            shape = 1.0
        else:
            self._v_open += (v_open - self._v_open) * _rate(dt, _TAU_SHAPE)
            shape = self._v_open

        if v_level is None:
            gated = max(0.0, (amp - _MIC_FLOOR) / (1.0 - _MIC_FLOOR))
            drive = (gated ** 0.6) * (shape ** 0.75)
        else:
            # Speech RMS spends most of its time well below full scale, so the
            # raw value alone would only ever half-open the jaw. Normalise it
            # against a running estimate of this voice's own loud level rather
            # than a constant: it then reads the same whether the user has the
            # volume low or the model happens to be speaking softly.
            self._v_peak = max(v_level, self._v_peak - dt * 0.55)
            ref = max(0.18, self._v_peak)
            # The floor is a fraction of this voice's own loud level, not a
            # fixed number, so it means the same thing at any volume and in any
            # language. A stop consonant drops 20 dB or more below the vowels
            # around it, which is this ratio — so a real closure lands at
            # exactly zero rather than at some small positive value the curve
            # would otherwise lift back up. That lift is what kept the mouth
            # from ever quite shutting between words.
            q = (v_level - _CLOSE_FRAC * ref) / (ref * (1.0 - _CLOSE_FRAC))
            drive = max(0.0, min(1.0, q)) ** 0.85 * (shape ** 0.75)

        target = min(1.0, drive) if live else 0.0
        if target > self._mouth:
            tau = _TAU_OPEN
        elif live:
            tau = _TAU_SHUT      # mid-word: a consonant, and it must shut now
        else:
            tau = _TAU_REST      # speech is over; settle, don't snap
        self._mouth += (target - self._mouth) * _rate(dt, tau)
        if self._mouth < 0.002:
            self._mouth = 0.0

    def step(self, dt: float, amp: float, speaking: bool = False,
             muted: bool = False, state: str = "",
             v_open: float | None = None, v_wide: float = 0.0,
             v_level: float | None = None,
             v_seq: list | None = None, v_hop: float = 0.02) -> None:
        """Advance the animation.

        `amp` is the 0..1 display audio level. `v_open` / `v_wide` / `v_level`
        are the viseme schedule's shape and true level for this instant; passing
        None falls back to loudness-only articulation, which is what the
        microphone path uses. `v_seq` is every schedule frame the last rendered
        frame spanned, so no closure is lost when the paint rate drops.
        """
        dt = max(0.001, min(0.10, float(dt)))
        self._t += dt
        t = self._t
        amp = max(0.0, min(1.0, float(amp)))
        live = speaking and not muted

        # Idle sway. The phase is *integrated* rather than taken as
        # sin(t * rate * speed): multiplying absolute time by a speed that
        # changes when VIERNES starts or stops talking jumps the phase by
        # t * rate * delta, which after a minute of uptime is several radians
        # and visibly teleports the head the instant a sentence ends.
        speed = (1.0 if not muted else 0.55) * (1.25 if live else 1.0)
        self._sway += dt * speed
        s = self._sway
        self._yaw = 0.26 * math.sin(s * 0.31) + 0.09 * math.sin(s * 0.73 + 1.3)
        self._pitch = (0.060 * math.sin(s * 0.23 + 0.7)
                       + 0.024 * math.sin(s * 0.61))

        # Mouth. Which level is driving it matters more than any rate here.
        #
        # `v_level` is this 20 ms frame's own RMS, taken from the very audio
        # about to be heard, so its silences are real silences. `amp` is the
        # waveform display's level, and that one is a *peak hold*: it keeps the
        # loudest value it has seen and decays gently, on purpose, so the bars
        # do not stutter between audio chunks. Driving a mouth from a peak hold
        # is why the gaps between words never closed — the hold spans exactly
        # the consonant it was supposed to reveal. So the schedule drives the
        # jaw whenever there is one, and `amp` is left to the microphone path,
        # which has nothing better.
        # Advance the mouth once per *schedule* frame rather than once per
        # rendered frame. A bilabial closure lasts around 40 ms — two frames of
        # a 50 Hz schedule — and the HUD throttles its paint to 30 fps and to 20
        # when idle. Point-sampling at 20 fps steps 50 ms at a time, so a whole
        # closure can fall between two samples and simply never be seen; that is
        # information loss no smoothing constant can recover. Sub-stepping costs
        # a few float operations per frame and makes the mouth identical at 20,
        # 30 and 60 fps.
        # An empty list is meaningful and is not the same as None: it says a
        # schedule is playing but this tick landed inside a frame already
        # spoken. The mouth's clock is the schedule's, so the right thing then
        # is to do nothing. Re-stepping the same frame — which is what a
        # truthiness test here would do — advances the jaw twice for one 20 ms
        # of audio, and at 60 fps that alone made the mouth behave differently
        # than at 20.
        if v_seq is not None:
            for lv, op, _wd in v_seq:
                self._mouth_step(v_hop, amp, live, op, lv)
        else:
            self._mouth_step(dt, amp, live, v_open, v_level)

        # Syllable emphasis. Applied unconditionally: `_emph` decays to zero on
        # its own once the mouth closes, whereas gating it on `live` deleted the
        # whole offset in a single frame and snapped the head at sentence end.
        self._emph += (self._mouth - self._emph) * _rate(
            dt, 0.055 if self._mouth > self._emph else 0.32)
        self._pitch -= self._emph * 0.028
        self._yaw += 0.018 * math.sin(t * 1.7) * self._emph

        # Loudness envelope, deliberately lazier than the mouth: brows track the
        # shape of a phrase, not individual syllables.
        env = amp if live else 0.0
        self._amp_slow += (env - self._amp_slow) * _rate(
            dt, 0.16 if env > self._amp_slow else 0.36)

        if live:
            if t >= self._expr_at:
                self._expr_tgt = random.uniform(-0.35, 1.0)
                self._expr_at = t + 1.1 + 2.0 * random.random()
        else:
            self._expr_tgt = 0.0
            self._expr_at = t + 0.8
        self._expr += (self._expr_tgt - self._expr) * 0.075

        brow_t = 0.55 * self._amp_slow + 0.60 * self._expr + self._brow_bias
        self._brow += (max(-0.4, min(1.2, brow_t)) - self._brow) * 0.20

        # ── what the state does to the face ─────────────────────────────────
        st = (state or "").upper()
        thinking = st in ("THINKING", "PROCESSING")
        asleep = st in ("SLEEPING", "STANDBY", "OFFLINE")

        if thinking:
            # People look away to think, and hold it. The direction re-rolls
            # slowly so it reads as thought rather than as scanning.
            if t >= self._bias_at:
                self._bias_tgt = [random.choice((-1.0, 1.0)) * random.uniform(0.45, 0.8),
                                  random.uniform(0.25, 0.55)]
                self._bias_at = t + 1.4 + 1.6 * random.random()
            brow_bias, lid_tgt = -0.28, 0.94
        elif asleep:
            self._bias_tgt = [0.0, -0.25]
            brow_bias, lid_tgt = -0.05, 0.22
        else:
            # LISTENING / idle / speaking: eyes come back to the user.
            self._bias_tgt = [0.0, 0.0]
            self._bias_at = 0.0
            brow_bias = 0.10 if st == "LISTENING" else 0.0
            lid_tgt = 1.0

        for i in (0, 1):
            self._gaze_bias[i] += (self._bias_tgt[i] - self._gaze_bias[i]) * 0.06
        self._lids += (lid_tgt - self._lids) * 0.08
        self._brow_bias += (brow_bias - self._brow_bias) * 0.06

        # Gaze: saccades are near-instant jumps between fixations, and they get
        # more frequent when there is something to say. While thinking they slow
        # right down — a darting eye reads as nervous, not thoughtful.
        if t >= self._gaze_at:
            reach = 0.9 if live else (0.35 if thinking else 0.55)
            self._gaze_tgt = [random.uniform(-1.0, 1.0) * reach,
                              random.uniform(-1.0, 1.0) * reach * 0.55]
            if live:
                self._gaze_at = t + 0.55 + 1.7 * random.random()
            elif thinking:
                self._gaze_at = t + 1.8 + 2.4 * random.random()
            else:
                self._gaze_at = t + 1.3 + 2.8 * random.random()

        # A deliberate glance (something appeared on screen) overrides the
        # wandering for a moment, then hands control back.
        if self._glance is not None:
            gx, gy, until = self._glance
            if t < until:
                self._gaze_tgt = [gx, gy]
            else:
                self._glance = None

        for i, b in enumerate(self._gaze_bias):
            tgt = max(-1.0, min(1.0, self._gaze_tgt[i] + b))
            self._gaze[i] += (tgt - self._gaze[i]) * 0.30

        # Lips lead the jaw slightly in real speech, so they track a touch
        # faster; they also relax to neutral the moment the voice stops.
        wide_t = v_wide if (live and v_open is not None) else 0.0
        self._wide += (max(-1.0, min(1.0, wide_t)) - self._wide) * _rate(dt, 0.030)

        self._glow += ((0.0 if muted else amp) - self._glow) * (
            0.35 if (0.0 if muted else amp) > self._glow else 0.10)

        self._scan += dt * (0.55 + 1.5 * self._glow)
        if self._scan > 1.35:
            self._scan = -1.75

        if self._blink > 0.0:
            self._blink = max(0.0, self._blink - dt * 8.5)
        elif t >= self._blink_at:
            # Concentration suppresses blinking; a sleeping face has no need of
            # it at all, since the lids are already down.
            if asleep:
                self._blink_at = t + 6.0
            else:
                self._blink = 1.0
                gap = 5.5 if thinking else 3.4
                self._blink_at = t + gap + 3.1 * random.random()

    def glance(self, dx: float, dy: float, hold: float = 1.1) -> None:
        """Look deliberately somewhere for `hold` seconds, then wander again.

        Used when something appears on screen: a face that looks at what just
        showed up tells the user it landed, without a word being spoken.
        """
        self._glance = (max(-1.0, min(1.0, float(dx))),
                        max(-1.0, min(1.0, float(dy))),
                        self._t + max(0.1, float(hold)))

    # ── posing ──────────────────────────────────────────────────────────────

    def _pose(self):
        """Jaw drop, brow lift and head rotation, applied to the real geometry."""
        v = self._v
        np.copyto(v, self._v0)

        if self._brow > 0.004 or self._brow < -0.004:
            # The brow-to-eye gap is 0.198 head-half-heights and a real raise
            # moves a third of it. The old 0.045 — halved again by the landmark
            # weights, which average 0.5 — worked out to six pixels on a 250 px
            # head, which is to say invisible.
            v[:, 1] += self._brow_w * (self._brow * _BROW_LIFT)

        if abs(self._wide) > 0.01 and self._mouth > 0.0:
            # Spread pulls the corners out and flattens the lips back; rounding
            # draws them in and pushes them forward into a purse.
            k = self._lips_w * (self._wide * self._mouth)
            v[:, 0] += k * (v[:, 0] - self._lip_c[0]) * 0.55
            v[:, 1] += k * (v[:, 1] - self._lip_c[1]) * 0.30
            v[:, 2] -= k * 0.055

        if self._mouth > 0.004:
            px, py, pz = JAW_PIVOT
            ang = self._jaw * (self._mouth * JAW_MAX)
            ca, sa = np.cos(ang), np.sin(ang)
            dy = v[:, 1] - py
            dz = v[:, 2] - pz
            v[:, 1] = py + dy * ca - dz * sa
            v[:, 2] = pz + dy * sa + dz * ca

        cy, sy = math.cos(self._yaw), math.sin(self._yaw)
        cp, sp = math.cos(self._pitch), math.sin(self._pitch)
        m = np.array([
            [cy, 0.0, sy],
            [sp * sy, cp, -sp * cy],
            [-cp * sy, sp, cp * cy],
        ], dtype=np.float32)

        return v @ m.T, self._n0 @ m.T

    # ── rendering ───────────────────────────────────────────────────────────

    def _lut(self, bg: QColor, primary: QColor):
        """Cached ramp of opaque surface brushes from `bg` to `primary`."""
        key = (bg.rgb(), primary.rgb())
        if self._lut_key != key:
            self._lut_cache = [QBrush(_blend(bg, primary, 255.0 * (i + 0.5) / _LUT_N))
                               for i in range(_LUT_N)]
            self._lut_key = key
        return self._lut_cache

    def paint(self, p: QPainter, cx: float, cy: float, r: float,
              primary: QColor, accent: QColor, bg: QColor | None = None) -> None:
        """Draw the avatar with its head centre at (cx, cy).

        `r` is the head's half-height in pixels — the caller owns the layout, so
        the HUD can fit the head to whatever room the status line leaves it.
        """
        if bg is None:
            bg = QColor(0, 0, 0)
        amp = self._glow
        verts, norms = self._pose()

        # ── aura ────────────────────────────────────────────────────────────
        ar = r * 1.95
        grad = QRadialGradient(cx, cy, ar)
        grad.setColorAt(0.00, _c(primary, 34 + 66 * amp))
        grad.setColorAt(0.38, _c(primary, 20 + 40 * amp))
        grad.setColorAt(1.00, _c(primary, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(grad))
        p.drawEllipse(QRectF(cx - ar, cy - ar, ar * 2, ar * 2))

        # ── project ─────────────────────────────────────────────────────────
        w = _CAM_D - verts[:, 2]
        np.maximum(w, 0.35, out=w)
        k = (_CAM_D / w) * r
        xs = cx + verts[:, 0] * k
        ys = cy - verts[:, 1] * k

        if self.shaded:
            self._paint_surface(p, xs, ys, norms, verts, primary, bg, amp)
        self._paint_wire(p, xs, ys, norms, verts, primary, bg, amp)
        self._paint_features(p, xs, ys, norms, r, primary, accent, bg, amp)

    def _paint_surface(self, p: QPainter, xs, ys, norms, verts,
                       primary: QColor, bg: QColor, amp: float) -> None:
        """Fill the camera-facing triangles so the head reads as a lit volume."""
        a, b, c = self._fa, self._fb, self._fc

        # Flat normals, taken from each triangle's own posed geometry — NOT the
        # averaged vertex normals. Averaging smears the nose, lips and brow
        # relief into their neighbours and renders the face as a blank egg;
        # per-facet normals are exactly what makes the anatomy visible.
        fn = np.cross(verts[b] - verts[a], verts[c] - verts[a])
        fn /= np.maximum(np.linalg.norm(fn, axis=1, keepdims=True), 1e-9)

        # Point them outwards by agreeing with the vertex normals, which were
        # oriented at build time. Flipping on the sign of n_z instead would
        # negate x and y as well and scramble the lighting into moiré.
        ref = norms[a] + norms[b] + norms[c]
        fn *= np.sign((fn * ref).sum(1))[:, None]

        nz = fn[:, 2]
        area = np.abs((xs[b] - xs[a]) * (ys[c] - ys[a])
                      - (xs[c] - xs[a]) * (ys[b] - ys[a]))
        vis = np.flatnonzero((nz > 0.015) & (area > 3.0))
        if vis.size == 0:
            return
        fn = fn[vis]
        nz = nz[vis]

        ax, ay = xs[a][vis], ys[a][vis]
        bx, by = xs[b][vis], ys[b][vis]
        cxx, cyy = xs[c][vis], ys[c][vis]

        # A rim term for the glass edge plus a key light high on the left. The
        # light leans off-axis on purpose: weight it towards the camera and
        # every front-facing facet returns the same value, which is a flat mask.
        fres = np.clip(1.0 - nz, 0.0, 2.0) ** 1.7
        lam = np.clip(fn[:, 0] * -0.55 + fn[:, 1] * 0.50 + nz * 0.52, 0.0, 1.0)
        bright = 0.26 + 0.20 * fres + 0.66 * lam ** 1.05
        bright *= (self._fade[a][vis] + self._fade[b][vis] + self._fade[c][vis]) / 3.0
        bright *= 0.88 + 0.24 * amp

        idx = np.clip((bright * _LUT_N).astype(np.int32), 0, _LUT_N - 1)

        # Far facets first: the neck passes behind the jaw and the head is not
        # convex around the chin.
        # Sort far-to-near, but group first: neck facets all draw before head
        # facets, because the two meshes interpenetrate and a pure depth sort
        # interleaves them into a torn seam.
        fz = (verts[a, 2][vis] + verts[b, 2][vis] + verts[c, 2][vis]) * (1.0 / 3.0)
        order = np.argsort(self._fgroup[vis] * 1000.0 + fz, kind="stable")
        tris = np.stack([ax, ay, bx, by, cxx, cyy], axis=1)[order].tolist()
        shade = idx[order].tolist()
        lut = self._lut(bg, primary)

        # Aliased fills: adjacent antialiased polygons leave hairline seams, and
        # the interior of a tiled surface has no silhouette worth smoothing —
        # the antialiased wireframe drawn afterwards covers the outline.
        p.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        p.setPen(Qt.PenStyle.NoPen)
        for q, sh in zip(tris, shade):
            p.setBrush(lut[sh])
            p.drawPolygon(QPolygonF([QPointF(q[0], q[1]), QPointF(q[2], q[3]),
                                     QPointF(q[4], q[5])]))
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    def _paint_wire(self, p: QPainter, xs, ys, norms, verts,
                    primary: QColor, bg: QColor, amp: float) -> None:
        nz = norms[:, 2]
        fres = np.abs(1.0 - np.abs(nz)) ** 1.5
        if self.shaded:
            # The lit surface underneath is opaque, so back-facing edges would
            # float on top of the face — cull them and let the wire read as
            # structure lines over skin.
            front = nz > -0.05
            va = np.where(front, 0.10 + 0.42 * fres, 0.0)
            va += 0.30 * np.exp(-((verts[:, 1] - self._scan) / 0.13) ** 2) * front
        else:
            va = np.where(nz < 0.0, 0.13 + 0.26 * fres, 0.28 + 0.72 * fres)
            va += 0.42 * np.exp(-((verts[:, 1] - self._scan) / 0.13) ** 2)
        va *= self._fade * (0.80 + 0.45 * amp)

        ea = 0.5 * (va[self._e0] + va[self._e1])
        keep = np.flatnonzero(ea > _MIN_ALPHA)
        if keep.size == 0:
            return

        # Sort by opacity bucket once so each bucket is a contiguous *slice* of
        # one QLineF list; masking and rebuilding per bucket cost more than the
        # drawing itself.
        bucket = np.clip((ea[keep] * _BUCKETS).astype(np.int32), 0, _BUCKETS - 1)
        order = np.argsort(bucket, kind="stable")
        keep = keep[order]
        bounds = np.searchsorted(bucket[order], np.arange(_BUCKETS + 1))

        e0, e1 = self._e0[keep], self._e1[keep]
        quad = np.stack([xs[e0], ys[e0], xs[e1], ys[e1]], axis=1).tolist()
        lines = [QLineF(q[0], q[1], q[2], q[3]) for q in quad]

        skin = _blend(bg, primary, 132) if self.shaded else bg
        p.setBrush(Qt.BrushStyle.NoBrush)
        for b in range(_BUCKETS):
            lo, hi = int(bounds[b]), int(bounds[b + 1])
            if hi <= lo:
                continue
            seg = lines[lo:hi]
            a = 255.0 * min(1.0, (b + 0.5) / _BUCKETS)
            if self.shaded:
                # These sit on lit skin, so pre-mix against a representative
                # *skin* tone rather than the background — same fast opaque
                # path, and the lines still read as highlights over the face.
                p.setPen(QPen(_blend(skin, primary, a * 0.75), 1.0))
            else:
                p.setPen(QPen(_blend(bg, primary, a), 1.0))
            p.drawLines(seg)

    # ── face ────────────────────────────────────────────────────────────────

    def _ring(self, xs, ys, idx) -> QPolygonF:
        return QPolygonF([QPointF(float(x), float(y))
                          for x, y in zip(xs[idx], ys[idx])])

    def _paint_features(self, p: QPainter, xs, ys, norms, r: float,
                        primary: QColor, accent: QColor, bg: QColor,
                        amp: float) -> None:
        """Eyes, brows and the mouth cavity, drawn from the real landmark rings.

        The canonical model's eyes and lips are closed skin — the geometry gives
        the *shape* of the lids and mouth but no opening, so the openings are
        painted here, exactly on the landmarks that bound them.
        """
        face = max(0.0, math.cos(self._yaw) * math.cos(self._pitch)) ** 2
        if face < 0.02:
            return

        lm = self._lm
        vis = 1.0 - self._blink

        # ── eyes ────────────────────────────────────────────────────────────
        for key in ("eye_l", "eye_r"):
            idx = lm[key]
            ex, ey = xs[idx], ys[idx]
            mid_y = float(ey.mean())
            if vis < 0.999:
                ey = mid_y + (ey - mid_y) * max(0.04, vis)
            poly = QPolygonF([QPointF(float(a), float(b)) for a, b in zip(ex, ey)])

            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(_blend(bg, primary, 22)))       # socket shadow
            p.drawPolygon(poly)
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.setPen(QPen(_c(primary, 210 * face), 1.3))      # lid line
            p.drawPolygon(poly)

            if vis > 0.35:
                br = poly.boundingRect()
                gx = br.center().x() + self._gaze[0] * br.width() * 0.16
                gy = br.center().y() + self._gaze[1] * br.height() * 0.20
                cpt = QPointF(gx, gy)
                rad = min(br.height() * 0.62, br.width() * 0.20)
                p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(QBrush(_c(accent, (70 + 60 * amp) * face * vis)))
                p.drawEllipse(cpt, rad, rad * vis)            # iris
                p.setBrush(QBrush(_c(accent, 245 * face * vis)))
                p.drawEllipse(cpt, rad * 0.42, rad * 0.42 * vis)   # pupil

        # ── brows ───────────────────────────────────────────────────────────
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(_c(primary, 150 * face), 1.7))
        for key in ("brow_l", "brow_r"):
            idx = lm[key]
            p.drawPolyline(self._ring(xs, ys, idx))

        # ── mouth ───────────────────────────────────────────────────────────
        inner = self._ring(xs, ys, lm["lips_in"])
        open_h = inner.boundingRect().height()

        p.setPen(Qt.PenStyle.NoPen)
        if self._mouth > 0.02:
            # The cavity is dark but never pure black — a black oval on a glowing
            # head reads as a hole, not a mouth. Tinting it with the theme keeps
            # it part of the hologram.
            p.setBrush(QBrush(_blend(bg, primary, 16 + 26 * self._mouth)))
            p.drawPolygon(inner)

            # Upper teeth: a bright strip hanging from the upper lip. It is the
            # single cheapest thing that makes an open mouth look like speech.
            ux, uy = xs[self._lip_up], ys[self._lip_up]
            th = open_h * 0.30
            pts = [QPointF(float(x), float(y)) for x, y in zip(ux, uy)]
            pts += [QPointF(float(x), float(y) + th)
                    for x, y in zip(ux[::-1], uy[::-1])]
            p.setBrush(QBrush(_blend(bg, primary, 150 + 60 * self._mouth)))
            p.drawPolygon(QPolygonF(pts))

            # A warm pool at the back of the throat, strongest when wide open.
            p.setBrush(QBrush(_c(accent, 40 * self._mouth * face)))
            p.drawPolygon(inner)

        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(_c(primary, (150 + 70 * self._mouth) * face), 1.3))
        p.drawPolygon(inner)                       # lip edge
        p.setPen(QPen(_c(primary, 110 * face), 1.1))
        p.drawPolygon(self._ring(xs, ys, lm["lips_out"]))


class ViernesAvatar:
    """Live animated avatar using the Viernes Live2D character model.

    Features:
    * 23 ultra-high fidelity pre-rendered Live2D emotion & phoneme frames
    * Dual-buffer alpha cross-dissolve frame morphing (zero popping/stepping)
    * 2nd-order spring-damper 3D physics for Head Yaw, Pitch & Roll with organic inertia
    * Secondary spring physics for Melusine ears bounce and hair lag
    * 3D perspective projection with trapezoidal foreshortening & multiplane depth
    * Autonomous lifelike stand-by engine: spontaneous smiles, winks, curiosity,
      perked ears, attentive listening, thoughtful thinking, and fluid speech cadence
    * Cybernetic 3D Gyro Orbitals & reactive holographic atmospheric effects
    """

    SPAN: float = 1.85
    shaded: bool = True

    def __init__(self) -> None:
        self._t = 0.0
        self._mouth = 0.0
        self._target_mouth = 0.0
        self._speaking = False
        self._muted = False
        self._state = "IDLE"
        self._glow = 0.0

        # Look / Glance tracking
        self._look_x = 0.0
        self._look_y = 0.0
        self._target_look_x = 0.0
        self._target_look_y = 0.0
        self._glance_until = 0.0

        # ── 3D Spring-Damper Inertia Physics ───────────────────────────────────
        self.yaw = 0.0             # Horizontal head turn (-25 to +25 deg)
        self._yaw_v = 0.0
        self._target_yaw = 0.0

        self.pitch = 0.0           # Vertical nod (-18 to +18 deg)
        self._pitch_v = 0.0
        self._target_pitch = 0.0

        self.roll = 0.0            # Lateral head tilt (-15 to +15 deg)
        self._roll_v = 0.0
        self._target_roll = 0.0

        # Melusine ear secondary bounce spring
        self.ear_bounce = 0.0
        self._ear_bounce_v = 0.0

        # ── Dual-Buffer Alpha Cross-Dissolve Morphing Engine ───────────────────
        self._curr_frame_key: str = "idle"
        self._target_frame_key: str = "idle"
        self._blend_progress: float = 1.0  # 1.0 = fully transitioned
        self._blend_rate: float = 14.0     # ~70ms smooth cross-fade

        # ── Natural Blinking State Machine ────────────────────────────────────
        self._blink_timer = 0.0
        self._next_blink = 3.2 + random.random() * 2.5
        self._blink_stage = 0              # 0: idle, 1: half, 2: closed, 3: opening half
        self._blink_stage_t = 0.0
        self._is_double_blink = False
        self._double_blink_pending = False

        # ── Stand-by Autonomous Life Engine ───────────────────────────────────
        self._idle_time = 0.0
        self._standby_action = "none"
        self._standby_timer = 0.0
        self._standby_duration = 2.0
        self._next_standby = 3.5 + random.random() * 3.5

        # Load all high-fidelity rendered frames from viernes directory
        base_dir = Path(__file__).resolve().parent.parent
        frames_dir = base_dir / "viernes" / "frames"

        self._frames: dict[str, QPixmap] = {}
        if frames_dir.exists():
            for p in frames_dir.glob("*.png"):
                pm = QPixmap(str(p))
                if not pm.isNull():
                    self._frames[p.stem] = pm

        if "idle" in self._frames:
            self._aspect = self._frames["idle"].width() / max(1, self._frames["idle"].height())
        else:
            self._aspect = 700.0 / 800.0

        self._was_speaking = False

        # Fallback to mesh avatar if frames are missing
        self._fallback: _MeshAvatar | None = None
        if not self._frames:
            try:
                self._fallback = _MeshAvatar()
            except Exception:
                self._fallback = None

        # ── Sleep & Cyberpunk Glitch Transition Engine ────────────────────────
        self._is_sleeping: bool = False
        self._glitch_active: bool = False
        self._glitch_t: float = 0.0
        self._glitch_duration: float = 0.52
        self._glitch_to_sleep: bool = False
        self._aspect_dormida: float = 1536.0 / 1024.0
        if "dormida" in self._frames:
            self._aspect_dormida = self._frames["dormida"].width() / max(1, self._frames["dormida"].height())
        self._zzz_timer: float = 0.0
        self._zzz_particles: list[dict] = []

        # ── Drowsy Periodic Stir Cycle (Parece que despierta pero vuelve a dormir) ─
        self._sleep_stir_timer: float = 0.0
        self._next_sleep_stir: float = 12.0 + random.random() * 8.0
        self._is_stirring: bool = False
        self._stir_t: float = 0.0
        self._stir_duration: float = 4.2

    @property
    def is_sleeping(self) -> bool:
        return self._is_sleeping

    def trigger_glitch(self, to_sleep: bool) -> None:
        """Trigger cybernetic holographic glitch transition between awake and dormida."""
        self._glitch_active = True
        self._glitch_t = 0.0
        self._glitch_to_sleep = bool(to_sleep)
        if to_sleep:
            self._standby_action = "none"

    def sleep(self) -> None:
        """Put avatar into dormida sleep mode with cyberpunk glitch transition."""
        if not self._is_sleeping or not self._glitch_active:
            self.trigger_glitch(to_sleep=True)

    def wake(self) -> None:
        """Wake avatar from dormida sleep mode with cyberpunk glitch transition."""
        if self._is_sleeping or not self._glitch_active:
            self.trigger_glitch(to_sleep=False)

    def toggle_sleep(self) -> None:
        """Toggle sleep state with cyberpunk glitch transition."""
        self.trigger_glitch(to_sleep=not self._is_sleeping)

    def glance(self, dx: float, dy: float, hold: float = 1.1) -> None:
        if self._fallback:
            self._fallback.glance(dx, dy, hold)
            return
        self._target_look_x = max(-1.0, min(1.0, float(dx)))
        self._target_look_y = max(-1.0, min(1.0, float(dy)))
        self._glance_until = self._t + max(0.2, float(hold))

    def play_action(self, action_name: str, duration: float = 2.4) -> None:
        """Trigger an expressive action animation with organic head/ear dynamics."""
        if self._fallback:
            return
        preset_transforms = {
            "greeting_wave": (5.0, 0.0, -6.0),
            "blush_shy": (-6.0, -5.0, -7.0),
            "pout": (-4.0, 0.0, 6.0),
            "proud_smug": (0.0, 7.0, 3.0),
            "excited_sparkle": (0.0, 4.0, -2.0),
            "giggle": (0.0, 3.0, 6.5),
            "dizzy": (0.0, -4.0, 8.0),
            "crying_tears": (0.0, -6.0, -2.0),
            "apology_bow": (0.0, -16.0, 0.0),
            "shocked_gasp": (0.0, 4.0, 0.0),
            "sleepy_yawn": (0.0, -3.0, 5.0),
            "nod_yes": (0.0, 8.0, 0.0),
            "shake_no": (-16.0, 0.0, 5.5),
            "listen_attentive": (4.5, -6.5, -4.0),
            "curious": (6.0, 2.0, -6.5),
            "happy_cheer": (0.0, 3.0, 1.8),
            "wink_left": (-2.0, 1.0, -3.0),
            "wink_right": (2.0, 1.0, 3.0),
            "ear_perk": (0.0, 2.5, 0.0),
            "idle_smile": (0.0, 1.0, -1.5),
        }
        tyaw, tpitch, troll = preset_transforms.get(action_name, (0.0, 0.0, 0.0))
        self._standby_action = action_name
        self._standby_duration = max(0.5, float(duration))
        self._standby_timer = 0.0
        self._target_yaw = tyaw
        self._target_pitch = tpitch
        self._target_roll = troll
        self._set_target_frame(action_name)

    def _set_target_frame(self, key: str, fast: bool = False) -> None:
        if key not in self._frames:
            key = "idle"
        if key == self._target_frame_key:
            return
        if self._blend_progress >= 1.0:
            self._curr_frame_key = self._target_frame_key
            self._target_frame_key = key
            self._blend_progress = 0.0
            self._blend_rate = 24.0 if fast else 14.0
        else:
            # Re-direct mid-blend smoothly without any jump
            self._curr_frame_key = self._target_frame_key
            self._target_frame_key = key
            self._blend_progress = max(0.0, 1.0 - self._blend_progress)
            self._blend_rate = 24.0 if fast else 14.0

    def step(self, dt: float, amp: float, speaking: bool = False,
             muted: bool = False, state: str = "",
             v_open: float | None = None, v_wide: float = 0.0,
             v_level: float | None = None,
             v_seq: list | None = None, v_hop: float = 0.02) -> None:
        if self._fallback:
            self._fallback.step(dt, amp, speaking=speaking, muted=muted, state=state,
                                v_open=v_open, v_wide=v_wide, v_level=v_level,
                                v_seq=v_seq, v_hop=v_hop)
            return

        dt = max(0.001, min(0.05, float(dt)))
        self._t += dt
        self._speaking = bool(speaking)
        self._muted = bool(muted)
        new_state = str(state or "IDLE").upper()

        # State transition detection for cyberpunk glitch
        if new_state == "SLEEPING" and not self._is_sleeping and not self._glitch_active:
            self.trigger_glitch(to_sleep=True)
        elif new_state != "SLEEPING" and self._is_sleeping and not self._glitch_active:
            self.trigger_glitch(to_sleep=False)
        self._state = new_state

        # Wake automatically if speaking begins while sleeping
        if speaking and not muted and self._is_sleeping and not self._glitch_active:
            self.trigger_glitch(to_sleep=False)

        # ── Glitch Transition Progression ─────────────────────────────────────
        if self._glitch_active:
            self._glitch_t += dt
            if self._glitch_t >= (self._glitch_duration * 0.38) and self._is_sleeping != self._glitch_to_sleep:
                self._is_sleeping = self._glitch_to_sleep
                if self._is_sleeping:
                    self._curr_frame_key = "dormida"
                    self._target_frame_key = "dormida"
                    self._blend_progress = 1.0
                else:
                    self._curr_frame_key = "idle"
                    self._target_frame_key = "idle"
                    self._blend_progress = 1.0
            if self._glitch_t >= self._glitch_duration:
                self._glitch_active = False
                self._is_sleeping = self._glitch_to_sleep
                if self._is_sleeping:
                    self._curr_frame_key = "dormida"
                    self._target_frame_key = "dormida"

        # ── Sleeping Mode Particle & Breathing Updates ────────────────────────
        if self._is_sleeping and not self._glitch_active:
            self._curr_frame_key = "dormida"
            self._target_frame_key = "dormida"
            self._target_mouth = 0.0
            self._mouth = 0.0
            self._target_pitch = 0.0
            self._target_yaw = 0.0
            self._target_roll = 0.0
            self._standby_action = "none"

            # Periodic drowsy stir cycle (appears to wake up, stirs, stretches, and falls back asleep)
            self._sleep_stir_timer += dt
            if not self._is_stirring:
                if self._sleep_stir_timer >= self._next_sleep_stir:
                    self._is_stirring = True
                    self._stir_t = 0.0
                    self._stir_duration = random.uniform(3.8, 4.6)
                    self._sleep_stir_timer = 0.0
                    self._next_sleep_stir = random.uniform(14.0, 24.0)
            else:
                self._stir_t += dt
                if self._stir_t >= self._stir_duration:
                    self._is_stirring = False
                    self._stir_t = 0.0
                    # Emit a big satisfied Zzz when settling back to deep sleep
                    self._zzz_particles.append({
                        "t": 0.0,
                        "duration": 3.2,
                        "dx": 0.0,
                        "drift_rot": -8.0,
                        "size": 22.0,
                        "glyph": "Zzz...",
                    })

            # Procedural floating 'Zzz' particles (pause spawning during restless awakening stir)
            if not (self._is_stirring and self._stir_t < self._stir_duration * 0.65):
                self._zzz_timer += dt
                if self._zzz_timer >= 0.95:
                    self._zzz_timer = 0.0
                    self._zzz_particles.append({
                        "t": 0.0,
                        "duration": 2.8,
                        "dx": random.uniform(-10.0, 10.0),
                        "drift_rot": random.uniform(-18.0, 18.0),
                        "size": random.uniform(13.0, 21.0),
                        "glyph": random.choice(["z", "Z", "zZ"]),
                    })
            for p_z in list(self._zzz_particles):
                p_z["t"] += dt
                if p_z["t"] >= p_z["duration"]:
                    self._zzz_particles.remove(p_z)
            return

        # Update frame blend transition
        if self._blend_progress < 1.0:
            self._blend_progress = min(1.0, self._blend_progress + dt * self._blend_rate)
            if self._blend_progress >= 1.0:
                self._curr_frame_key = self._target_frame_key

        # Ambient aura glow reacts smoothly to state
        target_glow = 1.0 if speaking else (0.75 if self._state in ("LISTENING", "THINKING") else 0.35)
        self._glow += (target_glow - self._glow) * min(1.0, dt * 5.0)

        # Check transition from speaking -> stopped speaking (natural conversational reaction)
        if self._was_speaking and not (speaking and not muted):
            reaction = random.choices(
                ["nod_yes", "idle_smile", "proud_smug", "happy_cheer"],
                weights=[0.35, 0.35, 0.15, 0.15]
            )[0]
            self.play_action(reaction, duration=1.8)
        self._was_speaking = bool(speaking and not muted)

        # ── 1. Speech & Lip Sync ──────────────────────────────────────────────
        if speaking and not muted:
            target_mouth = v_open if v_open is not None else (float(amp) * 1.55)
            self._target_mouth = max(0.0, min(1.0, target_mouth))
            self._mouth += (self._target_mouth - self._mouth) * min(1.0, dt * 24.0)
            self._idle_time = 0.0
            self._standby_action = "none"

            # Speech cadence: rhythmic organic nodding & tilt
            speech_nod = math.sin(self._t * 7.5) * (self._mouth * 3.5)
            self._target_pitch = speech_nod - 1.5
            self._target_roll = math.cos(self._t * 3.8) * 2.2
            self._target_yaw = math.sin(self._t * 2.1) * 3.0

            # Viseme frame selection with smooth morphing
            if self._mouth > 0.65:
                self._set_target_frame("mouth_3", fast=True)
            elif self._mouth > 0.35:
                self._set_target_frame("mouth_2", fast=True)
            elif self._mouth > 0.12:
                self._set_target_frame("mouth_1", fast=True)
            else:
                self._set_target_frame("talk_smile" if "talk_smile" in self._frames else "smile", fast=True)

        else:
            self._target_mouth = 0.0
            self._mouth += (0.0 - self._mouth) * min(1.0, dt * 14.0)
            self._idle_time += dt

            # ── 2. Interactive States (Listening, Thinking, Muted) ───────────
            if self._muted:
                self._target_pitch = -4.0
                self._target_yaw = 0.0
                self._target_roll = 0.0
                self._set_target_frame("blink_half" if "blink_half" in self._frames else "idle")

            elif self._state == "LISTENING":
                # Attentive perk: lean forward, attentive eyes, ears perked
                self._target_pitch = -5.5
                self._target_yaw = self._look_x * 12.0
                self._target_roll = -2.0
                self._set_target_frame("listen_attentive" if "listen_attentive" in self._frames else "listening")

            elif self._state in ("THINKING", "PROCESSING"):
                # Pensive look: gaze upward-right, thoughtful head tilt
                self._target_pitch = 12.0
                self._target_yaw = 10.0 + math.sin(self._t * 1.5) * 4.0
                self._target_roll = 5.5
                self._set_target_frame("thinking")

            else:
                # ── 3. Autonomous Stand-By Life Cycle (19 Rich Actions) ───────
                self._standby_timer += dt

                # Check if it's time to choose a new spontaneous action
                if self._standby_action == "none":
                    if self._standby_timer >= self._next_standby:
                        actions = [
                            ("idle_smile", 2.2, 0.0, 1.0, -1.5),
                            ("curious", 2.5, 6.0, 2.0, -6.5),
                            ("happy_cheer", 2.0, 0.0, 3.0, 1.8),
                            ("wink_left", 1.8, -2.0, 1.0, -3.0),
                            ("wink_right", 1.8, 2.0, 1.0, 3.0),
                            ("ear_perk", 2.0, 0.0, 2.5, 0.0),
                            ("look_left", 2.4, -20.0, 0.0, 4.0),
                            ("look_right", 2.4, 20.0, 0.0, -4.0),
                            ("look_up", 2.2, 0.0, 16.0, 0.0),
                            ("look_down", 2.2, 0.0, -14.0, 1.0),
                            ("blush_shy", 2.5, -6.0, -5.0, -7.0),
                            ("pout", 2.2, -4.0, 0.0, 6.0),
                            ("proud_smug", 2.4, 0.0, 7.0, 3.0),
                            ("excited_sparkle", 2.2, 0.0, 4.0, -2.0),
                            ("greeting_wave", 2.5, 5.0, 0.0, -6.0),
                            ("sleepy_yawn", 2.8, 0.0, -3.0, 5.0),
                            ("giggle", 2.0, 0.0, 3.0, 6.5),
                            ("dizzy", 2.2, 0.0, -4.0, 8.0),
                            ("nod_yes", 1.8, 0.0, 7.0, 0.0),
                        ]
                        weights = [
                            0.12, 0.10, 0.08, 0.06, 0.06, 0.08,
                            0.06, 0.06, 0.04, 0.04, 0.06, 0.05,
                            0.05, 0.05, 0.04, 0.03, 0.05, 0.02, 0.05
                        ]
                        act, dur, tyaw, tpitch, troll = random.choices(actions, weights=weights)[0]
                        self._standby_action = act
                        self._standby_duration = dur
                        self._standby_timer = 0.0
                        self._target_yaw = tyaw
                        self._target_pitch = tpitch
                        self._target_roll = troll
                        self._set_target_frame(act)
                else:
                    # Action active — return smoothly to idle upon completion
                    if self._standby_timer >= self._standby_duration:
                        self._standby_action = "none"
                        self._standby_timer = 0.0
                        self._target_yaw = 0.0
                        self._target_pitch = 0.0
                        self._target_roll = 0.0
                        self._next_standby = 3.2 + random.random() * 3.8
                        self._set_target_frame("idle")

        # ── 4. Natural Multi-Stage Blinking (Overlaid) ─────────────────────────
        if self._state not in ("SLEEPING",) and not self._muted:
            self._blink_timer += dt
            if self._blink_stage == 0:
                if self._blink_timer >= self._next_blink:
                    self._blink_stage = 1  # Enter half-blink
                    self._blink_stage_t = 0.0
                    self._is_double_blink = (random.random() < 0.25)
            elif self._blink_stage == 1:
                # Half-blink closing (~35ms)
                self._set_target_frame("blink_half", fast=True)
                self._blink_stage_t += dt
                if self._blink_stage_t >= 0.035:
                    self._blink_stage = 2
                    self._blink_stage_t = 0.0
            elif self._blink_stage == 2:
                # Fully closed (~60ms)
                self._set_target_frame("blink", fast=True)
                self._blink_stage_t += dt
                if self._blink_stage_t >= 0.060:
                    self._blink_stage = 3
                    self._blink_stage_t = 0.0
            elif self._blink_stage == 3:
                # Half-blink opening (~35ms)
                self._set_target_frame("blink_half", fast=True)
                self._blink_stage_t += dt
                if self._blink_stage_t >= 0.035:
                    if self._is_double_blink and not self._double_blink_pending:
                        # Start quick second blink flutter
                        self._double_blink_pending = True
                        self._blink_stage = 1
                        self._blink_stage_t = 0.0
                    else:
                        self._blink_stage = 0
                        self._blink_timer = 0.0
                        self._double_blink_pending = False
                        self._next_blink = 2.8 + random.random() * 3.2
                        # Return to active state frame
                        target_key = self._standby_action if self._standby_action != "none" else "idle"
                        self._set_target_frame(target_key, fast=True)

        # ── 5. User Glance Tracking Integration ───────────────────────────────
        if self._t > self._glance_until:
            self._target_look_x = 0.0
            self._target_look_y = 0.0
        self._look_x += (self._target_look_x - self._look_x) * min(1.0, dt * 7.0)
        self._look_y += (self._target_look_y - self._look_y) * min(1.0, dt * 7.0)

        # Incorporate glance into target yaw & pitch
        eff_target_yaw = self._target_yaw + (self._look_x * 20.0)
        eff_target_pitch = self._target_pitch + (self._look_y * 14.0)
        eff_target_roll = self._target_roll

        # ── 6. 2nd-Order Spring-Damper Physics Integration ────────────────────
        # Critically damped anime mass spring: natural overshoot and soft settle
        w = 9.8      # Natural frequency (rad/s)
        zeta = 0.82  # Damping ratio

        # Yaw
        dyaw = self.yaw - eff_target_yaw
        ayaw = -2.0 * zeta * w * self._yaw_v - (w * w) * dyaw
        self._yaw_v += ayaw * dt
        self.yaw += self._yaw_v * dt

        # Pitch
        dpitch = self.pitch - eff_target_pitch
        apitch = -2.0 * zeta * w * self._pitch_v - (w * w) * dpitch
        self._pitch_v += apitch * dt
        self.pitch += self._pitch_v * dt

        # Roll
        droll = self.roll - eff_target_roll
        aroll = -2.0 * zeta * w * self._roll_v - (w * w) * droll
        self._roll_v += aroll * dt
        self.roll += self._roll_v * dt

        # Secondary Spring Physics: Melusine ear bounce reacting to head roll & yaw
        ear_w = 16.0
        ear_zeta = 0.62
        ear_force = (aroll * 0.075 + ayaw * 0.040)
        a_ear = -2.0 * ear_zeta * ear_w * self._ear_bounce_v - (ear_w * ear_w) * self.ear_bounce + ear_force
        self._ear_bounce_v += a_ear * dt
        self.ear_bounce += self._ear_bounce_v * dt

    def _calc_standing_geom(self, cx: float, cy: float, r: float,
                            canvas_w: float, canvas_h: float, zen_mode: bool) -> tuple[float, float, float, float]:
        sway_x = math.sin(self._t * 0.85) * 3.2 + math.sin(self._t * 0.38) * 1.6
        breath = math.sin(self._t * 2.2)
        breath_y = breath * (r * 0.016)
        if zen_mode:
            target_h = canvas_h if canvas_h > 0 else (r * 3.5)
            target_w = canvas_w if canvas_w > 0 else (r * 2.5)
            draw_h = min(target_h * 0.92, target_w * 0.85 / self._aspect)
            draw_w = draw_h * self._aspect
            feet_y = target_h * 0.965
            center_x = cx + (self.yaw * 0.16) + sway_x
            center_y = feet_y - (draw_h * 0.5) + breath_y
        else:
            if canvas_h > 0 and canvas_w > 0:
                fw = min(canvas_w, canvas_h)
                status_y = (canvas_h / 2.0) + fw * 0.40
                max_h = max(120.0, status_y - 20.0)
                draw_h = min(max_h, canvas_w * 0.72 / self._aspect)
                draw_w = draw_h * self._aspect
                feet_y = status_y - 8.0
                center_x = cx + (self.yaw * 0.12) + (sway_x * 0.6)
                center_y = feet_y - (draw_h * 0.5) + breath_y
            else:
                draw_h = r * 3.2
                draw_w = draw_h * self._aspect
                center_x = cx + (self.yaw * 0.12)
                center_y = cy + (r * 0.3) + breath_y
        return center_x, center_y, draw_w, draw_h

    def _calc_sleeping_geom(self, cx: float, cy: float, r: float,
                            canvas_w: float, canvas_h: float, zen_mode: bool) -> tuple[float, float, float, float]:
        aspect = getattr(self, "_aspect_dormida", 1.50)
        sleep_breath = math.sin(self._t * 1.35)
        breath_y = -sleep_breath * 2.5
        if zen_mode:
            target_h = canvas_h if canvas_h > 0 else (r * 3.5)
            target_w = canvas_w if canvas_w > 0 else (r * 2.5)
            draw_w = min(target_w * 0.62, target_h * 0.58 * aspect)
            draw_h = draw_w / aspect
            feet_y = target_h * 0.94
            center_x = cx
            center_y = feet_y - (draw_h * 0.5) + breath_y
        else:
            if canvas_h > 0 and canvas_w > 0:
                fw = min(canvas_w, canvas_h)
                status_y = (canvas_h / 2.0) + fw * 0.40
                max_h = max(120.0, status_y - 20.0)
                draw_w = min(canvas_w * 0.56, max_h * 0.62 * aspect)
                draw_h = draw_w / aspect
                feet_y = status_y - 12.0
                center_x = cx
                center_y = feet_y - (draw_h * 0.5) + breath_y
            else:
                draw_w = r * 2.4
                draw_h = draw_w / aspect
                center_x = cx
                center_y = cy + (r * 0.28) + breath_y
        return center_x, center_y, draw_w, draw_h

    def _paint_standing(self, p: QPainter, cx: float, cy: float, r: float,
                        primary: QColor, accent: QColor, bg: QColor | None,
                        canvas_w: float, canvas_h: float, zen_mode: bool) -> None:
        frame_curr = self._frames.get(self._curr_frame_key, self._frames.get("idle"))
        frame_target = self._frames.get(self._target_frame_key, self._frames.get("idle"))
        if not frame_target or frame_target.isNull():
            return

        breath = math.sin(self._t * 2.2)
        scale_x = 1.0 + (breath * 0.008) + (self.ear_bounce * 0.010)
        scale_y = 1.0 + (breath * 0.015)
        sway_tilt = math.cos(self._t * 0.85) * 0.40

        center_x, center_y, draw_w, draw_h = self._calc_standing_geom(cx, cy, r, canvas_w, canvas_h, zen_mode)
        torso_cy = center_y - (draw_h * 0.16)

        # ── Realistic Floor Contact Shadow (Anchors character into the bedroom floor) ──
        feet_y = center_y + (draw_h * 0.485)
        shadow_rx = draw_w * 0.36
        shadow_ry = draw_h * 0.042
        shadow_rect = QRectF(center_x - shadow_rx, feet_y - shadow_ry, shadow_rx * 2, shadow_ry * 2)

        p.save()
        p.setPen(Qt.PenStyle.NoPen)
        sh_grad = QRadialGradient(shadow_rect.center(), shadow_rx)
        sh_grad.setColorAt(0.00, QColor(8, 12, 18, 175))
        sh_grad.setColorAt(0.42, QColor(10, 14, 22, 105))
        sh_grad.setColorAt(0.75, QColor(15, 18, 26, 35))
        sh_grad.setColorAt(1.00, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(sh_grad))
        p.drawEllipse(shadow_rect)
        p.restore()

        # ── Soft Room Ambient Bounce (Warm backlight matching bedroom lighting) ──
        bounce_r = draw_w * 0.75
        bounce_grad = QRadialGradient(center_x, torso_cy, bounce_r)
        bounce_alpha = int(14 + 18 * self._glow)
        bounce_grad.setColorAt(0.00, QColor(255, 235, 205, bounce_alpha))
        bounce_grad.setColorAt(0.50, QColor(255, 215, 175, int(bounce_alpha * 0.45)))
        bounce_grad.setColorAt(1.00, QColor(255, 215, 175, 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(bounce_grad))
        p.drawEllipse(QRectF(center_x - bounce_r, torso_cy - bounce_r, bounce_r * 2, bounce_r * 2))

        # ── 3D Transformed Character Rendering (Smooth Morphing) ──────────────
        shear_x = (self.yaw / 30.0) * 0.028

        p.save()
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        trans = QTransform()
        trans.translate(center_x, center_y)
        trans.rotate(self.roll + sway_tilt)
        trans.shear(shear_x, 0.0)
        trans.scale(scale_x, scale_y)
        p.setTransform(trans, True)

        dst_rect = QRectF(-draw_w * 0.5, -draw_h * 0.5, draw_w, draw_h)

        if self._blend_progress < 1.0 and frame_curr and not frame_curr.isNull() and frame_curr != frame_target:
            s = self._blend_progress * self._blend_progress * (3.0 - 2.0 * self._blend_progress)
            alpha_target = s
            alpha_curr = 1.0 - s

            p.setOpacity(alpha_curr)
            p.drawPixmap(dst_rect, frame_curr, QRectF(frame_curr.rect()))

            p.setOpacity(alpha_target)
            p.drawPixmap(dst_rect, frame_target, QRectF(frame_target.rect()))
            p.setOpacity(1.0)
        else:
            p.setOpacity(1.0)
            p.drawPixmap(dst_rect, frame_target, QRectF(frame_target.rect()))

        p.restore()

    def _paint_sleeping(self, p: QPainter, cx: float, cy: float, r: float,
                        primary: QColor, accent: QColor, bg: QColor | None,
                        canvas_w: float, canvas_h: float, zen_mode: bool) -> None:
        frame_dormida = self._frames.get("dormida", self._frames.get("idle"))
        if not frame_dormida or frame_dormida.isNull():
            return

        center_x, center_y, draw_w, draw_h = self._calc_sleeping_geom(cx, cy, r, canvas_w, canvas_h, zen_mode)

        # ── Soothing Lunar & Dream Ambient Aura ───────────────────────────────
        ar = draw_w * 0.65
        glow_grad = QRadialGradient(center_x, center_y, ar)
        glow_pulse = 0.5 + 0.5 * math.sin(self._t * 1.35)
        glow_alpha = int(24 + 18 * glow_pulse)
        glow_grad.setColorAt(0.00, QColor(accent.red(), accent.green(), accent.blue(), glow_alpha))
        glow_grad.setColorAt(0.40, QColor(primary.red(), primary.green(), primary.blue(), int(glow_alpha * 0.45)))
        glow_grad.setColorAt(1.00, QColor(primary.red(), primary.green(), primary.blue(), 0))
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(glow_grad))
        p.drawEllipse(QRectF(center_x - ar, center_y - ar, ar * 2, ar * 2))

        # ── Realistic Floor Contact Shadow under Beanbag ──────────────────────
        sh_w = draw_w * 0.90
        sh_h = draw_h * 0.17
        sh_y = center_y + (draw_h * 0.44)
        sh_rect = QRectF(center_x - sh_w * 0.5, sh_y - sh_h * 0.5, sh_w, sh_h)
        p.save()
        p.setPen(Qt.PenStyle.NoPen)
        sh_grad = QRadialGradient(sh_rect.center(), sh_w * 0.5)
        sh_grad.setColorAt(0.00, QColor(6, 10, 16, 205))
        sh_grad.setColorAt(0.40, QColor(10, 14, 22, 130))
        sh_grad.setColorAt(0.72, QColor(15, 18, 26, 45))
        sh_grad.setColorAt(1.00, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(sh_grad))
        p.drawEllipse(sh_rect)
        p.restore()

        # ── Dynamic Stir / Cozy Waking & Snuggling Physics (No Text Popups) ──
        stir_x = 0.0
        stir_y = 0.0
        stir_rot = 0.0
        stir_scale_x = 1.0
        stir_scale_y = 1.0
        p_stir = 0.0

        if self._is_stirring:
            p_stir = min(1.0, max(0.0, self._stir_t / max(0.1, self._stir_duration)))
            if p_stir < 0.28:
                # Stage 1: Soft drowsy shift and gentle nuzzle
                frac = p_stir / 0.28
                stir_twitch = math.sin(self._stir_t * 12.0) * math.exp(-frac * 2.2) * 2.4
                stir_x = stir_twitch
                stir_rot = math.sin(self._stir_t * 8.0) * 1.0
            elif p_stir < 0.70:
                # Stage 2: Sweet lazy stretch & cozy yawn
                frac = (p_stir - 0.28) / 0.42
                arc = math.sin(frac * math.pi)
                stir_scale_x = 1.0 + (arc * 0.035)
                stir_scale_y = 1.0 + (arc * 0.046)
                stir_y = -7.0 * arc
                stir_rot = -1.6 * arc
            else:
                # Stage 3: Soft relaxed sigh, settling cozily deeper into the beanbag
                frac = (p_stir - 0.70) / 0.30
                settle = math.sin(frac * (math.pi / 2.0))
                stir_y = (1.0 - settle) * -2.0 + math.sin(frac * math.pi) * 1.2
                stir_rot = (1.0 - frac) * -1.0

        # ── Organic Sleep Respiration (Natural Inhale / Exhale Curve) ─────────
        # Human slumber cycle: 38% gentle inhalation, 62% slow relaxed exhalation into cushion
        b_cycle = (self._t * 0.26) % 1.0
        if b_cycle < 0.38:
            breath_p = math.sin((b_cycle / 0.38) * (math.pi / 2.0))
        else:
            breath_p = math.cos(((b_cycle - 0.38) / 0.62) * (math.pi / 2.0))

        scale_x = (1.0 + (breath_p * 0.010) - (breath_p * 0.003)) * stir_scale_x
        scale_y = (1.0 + (breath_p * 0.022)) * stir_scale_y
        breathe_lift = -breath_p * 2.8

        p.save()
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        trans = QTransform()
        trans.translate(center_x + stir_x, center_y + stir_y + breathe_lift)
        trans.rotate(stir_rot)
        trans.scale(scale_x, scale_y)
        p.setTransform(trans, True)

        dst_rect = QRectF(-draw_w * 0.5, -draw_h * 0.5, draw_w, draw_h)
        p.drawPixmap(dst_rect, frame_dormida, QRectF(frame_dormida.rect()))

        # Drowsy cheek blush / cozy dream warmth during stretch attempt
        if self._is_stirring and 0.28 <= p_stir < 0.70:
            blush_alpha = int(85 * math.sin((p_stir - 0.28) / 0.42 * math.pi))
            head_spot = QPointF(-draw_w * 0.14, -draw_h * 0.18)
            blush_grad = QRadialGradient(head_spot, draw_w * 0.20)
            blush_grad.setColorAt(0.0, QColor(255, 140, 185, blush_alpha))
            blush_grad.setColorAt(1.0, QColor(255, 140, 185, 0))
            p.setCompositionMode(QPainter.CompositionMode.CompositionMode_Screen)
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(blush_grad))
            p.drawEllipse(head_spot, draw_w * 0.20, draw_w * 0.20)

        p.restore()

        # ── Gentle Procedural Floating 'Zzz' Dream Particles (Cozy Styling) ───
        head_x = center_x + stir_x - (draw_w * 0.08)
        head_y = center_y + stir_y + breathe_lift - (draw_h * 0.22)
        for p_z in self._zzz_particles:
            prog = p_z["t"] / p_z["duration"]
            alpha = int(210.0 * math.sin(prog * math.pi))
            cur_x = head_x + p_z["dx"] + math.sin(prog * 4.0) * 12.0
            cur_y = head_y - (prog * draw_h * 0.36)
            font_sz = max(9, int(p_z["size"] * (0.8 + 0.45 * prog)))
            p.save()
            p.translate(cur_x, cur_y)
            p.rotate(p_z["drift_rot"] + prog * 8.0)
            p.setFont(QFont("Segoe UI", font_sz, QFont.Weight.Bold))
            # Soft warm pastel glow
            p.setPen(QPen(QColor(255, 205, 225, int(alpha * 0.55))))
            p.drawText(QRectF(-20, -20, 60, 40), Qt.AlignmentFlag.AlignCenter, p_z["glyph"])
            # Pure soothing cream text
            p.setPen(QPen(QColor(255, 250, 245, alpha)))
            p.drawText(QRectF(-20, -20, 60, 40), Qt.AlignmentFlag.AlignCenter, p_z["glyph"])
            p.restore()

    def _paint_glitch_transition(self, p: QPainter, cx: float, cy: float, r: float,
                                 primary: QColor, accent: QColor, bg: QColor | None,
                                 canvas_w: float, canvas_h: float, zen_mode: bool) -> None:
        st_cx, st_cy, st_w, st_h = self._calc_standing_geom(cx, cy, r, canvas_w, canvas_h, zen_mode)
        sl_cx, sl_cy, sl_w, sl_h = self._calc_sleeping_geom(cx, cy, r, canvas_w, canvas_h, zen_mode)

        progress = min(1.0, max(0.0, self._glitch_t / self._glitch_duration))
        # Smooth S-curve easing
        blend_s = progress * progress * (3.0 - 2.0 * progress)

        pm_stand = self._frames.get("idle", self._frames.get("smile"))
        pm_sleep = self._frames.get("dormida", self._frames.get("idle"))

        # Transition floor contact shadow smoothly
        p.save()
        p.setPen(Qt.PenStyle.NoPen)
        sh_alpha = 180
        if self._glitch_to_sleep:
            sh_w = st_w * 0.72 + (sl_w * 0.90 - st_w * 0.72) * blend_s
            sh_h = st_h * 0.08 + (sl_h * 0.17 - st_h * 0.08) * blend_s
            sh_cx = st_cx + (sl_cx - st_cx) * blend_s
            sh_cy = (st_cy + st_h * 0.485) + ((sl_cy + sl_h * 0.44) - (st_cy + st_h * 0.485)) * blend_s
        else:
            sh_w = sl_w * 0.90 + (st_w * 0.72 - sl_w * 0.90) * blend_s
            sh_h = sl_h * 0.17 + (st_h * 0.08 - sl_h * 0.17) * blend_s
            sh_cx = sl_cx + (st_cx - sl_cx) * blend_s
            sh_cy = (sl_cy + sl_h * 0.44) + ((st_cy + st_h * 0.485) - (sl_cy + sl_h * 0.44)) * blend_s

        sh_rect = QRectF(sh_cx - sh_w * 0.5, sh_cy - sh_h * 0.5, sh_w, sh_h)
        sh_grad = QRadialGradient(sh_rect.center(), sh_w * 0.5)
        sh_grad.setColorAt(0.00, QColor(6, 10, 16, int(sh_alpha)))
        sh_grad.setColorAt(0.45, QColor(10, 14, 22, int(sh_alpha * 0.6)))
        sh_grad.setColorAt(1.00, QColor(0, 0, 0, 0))
        p.setBrush(QBrush(sh_grad))
        p.drawEllipse(sh_rect)
        p.restore()

        # Smooth crossfade between standing and sleeping poses
        p.save()
        p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        if self._glitch_to_sleep:
            alpha_from = 1.0 - blend_s
            alpha_to = blend_s
            rect_from = QRectF(st_cx - st_w * 0.5, st_cy - st_h * 0.5, st_w, st_h)
            rect_to = QRectF(sl_cx - sl_w * 0.5, sl_cy - sl_h * 0.5, sl_w, sl_h)
            pm_from = pm_stand
            pm_to = pm_sleep
        else:
            alpha_from = 1.0 - blend_s
            alpha_to = blend_s
            rect_from = QRectF(sl_cx - sl_w * 0.5, sl_cy - sl_h * 0.5, sl_w, sl_h)
            rect_to = QRectF(st_cx - st_w * 0.5, st_cy - st_h * 0.5, st_w, st_h)
            pm_from = pm_sleep
            pm_to = pm_stand

        if pm_from and not pm_from.isNull() and alpha_from > 0.01:
            p.setOpacity(alpha_from)
            p.drawPixmap(rect_from, pm_from, QRectF(pm_from.rect()))

        if pm_to and not pm_to.isNull() and alpha_to > 0.01:
            p.setOpacity(alpha_to)
            p.drawPixmap(rect_to, pm_to, QRectF(pm_to.rect()))

        p.restore()

    def paint(self, p: QPainter, cx: float, cy: float, r: float,
              primary: QColor, accent: QColor, bg: QColor | None = None,
              canvas_w: float = 0.0, canvas_h: float = 0.0,
              zen_mode: bool = False) -> None:
        if self._fallback:
            self._fallback.paint(p, cx, cy, r, primary, accent, bg)
            return

        if self._glitch_active:
            self._paint_glitch_transition(p, cx, cy, r, primary, accent, bg, canvas_w, canvas_h, zen_mode)
            return

        if self._is_sleeping:
            self._paint_sleeping(p, cx, cy, r, primary, accent, bg, canvas_w, canvas_h, zen_mode)
            return

        self._paint_standing(p, cx, cy, r, primary, accent, bg, canvas_w, canvas_h, zen_mode)


HoloAvatar = ViernesAvatar
