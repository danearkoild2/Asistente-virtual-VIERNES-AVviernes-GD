"""
Tony-Stark-style holographic floating screens overlay for VIERNES.

Shown while a tool runs (search, channel/video, scan, files...). Three
translucent screens materialise around the avatar, fill with animated data,
and two ghost holographic hands swipe / pinch / tap them. Cheap by design:
QPainter only, 30 FPS, and the timer runs ONLY while the overlay is visible.
"""
from __future__ import annotations

import math
import random
import time

from PyQt6.QtCore import QPointF, QRectF, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QFont, QLinearGradient, QPainter, QPen
from PyQt6.QtWidgets import QWidget

# tool name -> (kind, accent RGB, title)
_KINDS = {
    "web_search": ("search", (80, 220, 255), "BÚSQUEDA GLOBAL"),
    "web_research": ("search", (80, 220, 255), "INVESTIGACIÓN"),
    "browser_control": ("search", (80, 220, 255), "NAVEGACIÓN"),
    "web_fetch": ("search", (80, 220, 255), "LECTURA WEB"),
    "iptv_player": ("channel", (255, 170, 70), "SINTONIZANDO CANAL"),
    "video_player": ("channel", (255, 170, 70), "TRANSMISIÓN"),
    "youtube_video": ("channel", (255, 170, 70), "VIDEO"),
    "gpu_taskman": ("scan", (120, 255, 170), "ESCANEO GPU"),
    "system_diagnostics": ("scan", (120, 255, 170), "DIAGNÓSTICO"),
    "file_controller": ("files", (190, 150, 255), "ARCHIVOS"),
    "file_processor": ("files", (190, 150, 255), "PROCESANDO"),
}
_DEFAULT = ("task", (90, 200, 255), "EJECUTANDO TAREA")

_HEX = "0123456789ABCDEF"


def _hexline(rng: random.Random, n: int = 14) -> str:
    return "".join(rng.choice(_HEX) for _ in range(n))


class HoloScreensOverlay(QWidget):
    start_sig = pyqtSignal(str, str)   # tool name, detail   (thread-safe entry)
    stop_sig = pyqtSignal()

    FPS_MS = 33

    def __init__(self, parent=None, gesture_cb=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        self.hide()
        self._gesture_cb = gesture_cb
        self._kind, self._rgb, self._title = _DEFAULT
        self._detail = ""
        self._t0 = 0.0
        self._closing_at = 0.0
        self._active = False
        self._rng = random.Random(7)
        self._timer = QTimer(self)
        self._timer.setInterval(self.FPS_MS)
        self._timer.timeout.connect(self._tick)
        self._last_gesture = 0.0
        self.start_sig.connect(self._on_start)
        self.stop_sig.connect(self._on_stop)

    # ── control ──────────────────────────────────────────────────────────
    def _on_start(self, tool: str, detail: str) -> None:
        self._kind, self._rgb, self._title = _KINDS.get(tool, _DEFAULT)
        self._detail = detail or ""
        self._t0 = time.monotonic()
        self._closing_at = 0.0
        self._active = True
        if self.parentWidget() is not None:
            self.setGeometry(self.parentWidget().rect())
        self.show()
        self.raise_()
        if not self._timer.isActive():
            self._timer.start()
        self._fire_gesture(force=True)

    def _on_stop(self) -> None:
        if not self._active:
            return
        # keep it visible long enough to read (min 1.6 s since start), then fade out
        elapsed = time.monotonic() - self._t0
        self._closing_at = time.monotonic() + max(0.0, 1.6 - elapsed)

    def _fire_gesture(self, force: bool = False) -> None:
        now = time.monotonic()
        if not force and now - self._last_gesture < 2.4:
            return
        self._last_gesture = now
        if self._gesture_cb:
            try:
                self._gesture_cb("GAME_SUMMON_HUD", 2.4, 1.0)
            except Exception:
                pass

    def _tick(self) -> None:
        now = time.monotonic()
        if self._closing_at and now >= self._closing_at + 0.45:
            self._active = False
            self._timer.stop()
            self.hide()
            return
        if not self.isVisible():
            self._timer.stop()
            return
        if self._active and not self._closing_at:
            self._fire_gesture()
        self.update()

    # ── drawing ──────────────────────────────────────────────────────────
    def _alpha(self, t: float) -> float:
        a = min(1.0, t / 0.55)
        if self._closing_at:
            a *= max(0.0, 1.0 - (time.monotonic() - self._closing_at) / 0.45)
        return max(0.0, a)

    def paintEvent(self, _e) -> None:
        if not self._active:
            return
        t = time.monotonic() - self._t0
        a = self._alpha(t)
        if a <= 0.01:
            return
        w, h = self.width(), self.height()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        r, g, b = self._rgb

        # Screen layout: main (right), side-top, side-bottom — float with sine bob.
        base = min(w, h)
        sw, sh = base * 0.52, base * 0.34
        cx, cy = w * 0.72, h * 0.44
        screens = [
            (QRectF(cx - sw / 2, cy - sh / 2 + math.sin(t * 1.3) * 5, sw, sh), 0, "main"),
            (QRectF(cx - sw * 0.98, cy - sh * 0.95 + math.sin(t * 1.1 + 1) * 6, sw * 0.5, sh * 0.5), 1, "side"),
            (QRectF(cx - sw * 0.92, cy + sh * 0.5 + math.sin(t * 1.5 + 2) * 6, sw * 0.5, sh * 0.5), 2, "side"),
        ]
        for rect, idx, role in screens:
            appear = max(0.0, min(1.0, (t - idx * 0.22) / 0.5))
            if appear <= 0:
                continue
            self._draw_screen(p, rect, idx, role, appear * a, t, (r, g, b))

        self._draw_hands(p, screens, t, a, (r, g, b))
        p.end()

    def _draw_screen(self, p: QPainter, rect: QRectF, idx: int, role: str,
                     a: float, t: float, rgb) -> None:
        r, g, b = rgb
        # unfold animation: vertical scale-in from the centre line
        k = 1 - (1 - a) ** 3
        rr = QRectF(rect.x(), rect.center().y() - rect.height() * k / 2,
                    rect.width(), rect.height() * k)
        grad = QLinearGradient(rr.topLeft(), rr.bottomRight())
        grad.setColorAt(0, QColor(r, g, b, int(46 * a)))
        grad.setColorAt(1, QColor(r // 3, g // 3, b // 3, int(24 * a)))
        p.setBrush(QBrush(grad))
        p.setPen(QPen(QColor(r, g, b, int(210 * a)), 1.4))
        p.drawRoundedRect(rr, 8, 8)

        # corner brackets
        p.setPen(QPen(QColor(255, 255, 255, int(230 * a)), 2))
        L = 12
        for (x, y, dx, dy) in ((rr.left(), rr.top(), 1, 1), (rr.right(), rr.top(), -1, 1),
                               (rr.left(), rr.bottom(), 1, -1), (rr.right(), rr.bottom(), -1, -1)):
            p.drawLine(QPointF(x, y), QPointF(x + dx * L, y))
            p.drawLine(QPointF(x, y), QPointF(x, y + dy * L))

        if k < 0.85:
            return
        p.setClipRect(rr.adjusted(2, 2, -2, -2))
        pad = 10
        f = QFont("Consolas", 8 if role == "side" else 9)
        f.setBold(True)
        p.setFont(f)
        p.setPen(QColor(r, g, b, int(240 * a)))
        title = self._title if idx == 0 else ("DATOS" if idx == 1 else "ESTADO")
        p.drawText(QPointF(rr.left() + pad, rr.top() + 18), title)

        # content by kind
        y = rr.top() + 32
        p.setFont(QFont("Consolas", 7))
        if idx == 0 and self._detail:
            p.setPen(QColor(255, 255, 255, int(235 * a)))
            p.drawText(QPointF(rr.left() + pad, y), f"› {self._detail}")
            y += 16
        if idx == 0 and self._kind in ("search", "task", "files"):
            rng = random.Random(int(t * 3) + idx)
            n = int((rr.height() - 50) // 14)
            for i in range(max(0, n)):
                lw = (rr.width() - 2 * pad) * (0.35 + 0.6 * rng.random())
                shown = min(1.0, max(0.0, (t * 2.2 - i * 0.35)))
                p.setPen(QPen(QColor(r, g, b, int(150 * a * shown)), 5))
                p.drawLine(QPointF(rr.left() + pad, y + i * 14),
                           QPointF(rr.left() + pad + lw * shown, y + i * 14))
        elif idx == 0 and self._kind == "channel":
            tune = (math.sin(t * 2.5) + 1) / 2
            bw = rr.width() - 2 * pad
            p.setPen(QPen(QColor(r, g, b, int(200 * a)), 1))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRect(QRectF(rr.left() + pad, y + 6, bw, 14))
            p.fillRect(QRectF(rr.left() + pad + 1, y + 7, (bw - 2) * min(1, t / 3.0), 12),
                       QColor(r, g, b, int(150 * a)))
            for i in range(24):
                hh = 6 + 22 * abs(math.sin(t * 3 + i * 0.7)) * (0.4 + tune)
                p.fillRect(QRectF(rr.left() + pad + i * (bw / 24), rr.bottom() - 16 - hh,
                                  bw / 24 - 2, hh), QColor(r, g, b, int(120 * a)))
        elif idx == 0 and self._kind == "scan":
            cxx, cyy = rr.center().x(), rr.center().y() + 8
            rad = min(rr.width(), rr.height()) * 0.28
            p.setBrush(Qt.BrushStyle.NoBrush)
            for kk in (1, 0.66, 0.33):
                p.setPen(QPen(QColor(r, g, b, int(150 * a)), 1))
                p.drawEllipse(QPointF(cxx, cyy), rad * kk, rad * kk)
            ang = t * 3
            p.setPen(QPen(QColor(r, g, b, int(240 * a)), 2))
            p.drawLine(QPointF(cxx, cyy), QPointF(cxx + math.cos(ang) * rad, cyy + math.sin(ang) * rad))
        elif idx == 1:
            rng = random.Random(int(t * 4))
            for i in range(int((rr.height() - 38) // 11)):
                p.setPen(QColor(r, g, b, int(170 * a)))
                p.drawText(QPointF(rr.left() + pad, y + i * 11), _hexline(rng))
        else:
            pct = (t * 0.28) % 1.0
            bw = rr.width() - 2 * pad
            p.setPen(QPen(QColor(r, g, b, int(200 * a)), 1))
            p.drawRect(QRectF(rr.left() + pad, y, bw, 8))
            p.fillRect(QRectF(rr.left() + pad + 1, y + 1, (bw - 2) * pct, 6),
                       QColor(r, g, b, int(190 * a)))
            p.setPen(QColor(255, 255, 255, int(220 * a)))
            p.drawText(QPointF(rr.left() + pad, y + 24), f"{int(pct * 100):02d}%  SYNC")

        # scan line
        sy = rr.top() + ((t * 0.9) % 1.0) * rr.height()
        p.setClipping(False)
        p.setPen(QPen(QColor(r, g, b, int(110 * a)), 1))
        p.drawLine(QPointF(rr.left() + 2, sy), QPointF(rr.right() - 2, sy))

    def _draw_hands(self, p: QPainter, screens, t: float, a: float, rgb) -> None:
        """Two ghost hands: right swipes the main screen, left pinches a side one."""
        if t < 0.7:
            return
        ha = a * min(1.0, (t - 0.7) / 0.4)
        main = screens[0][0]
        side = screens[1][0]
        # right hand: figure-8 swipe over main screen
        rx = main.center().x() + math.sin(t * 1.7) * main.width() * 0.30
        ry = main.center().y() + math.sin(t * 3.4) * main.height() * 0.22
        self._hand(p, QPointF(rx, ry), ha, rgb, spread=0.6 + 0.4 * math.sin(t * 3.4), flip=False)
        # left hand: pinch-and-drag on side screen
        phase = (t * 0.9) % 1.0
        lx = side.center().x() + (phase - 0.5) * side.width() * 0.5
        ly = side.center().y() + math.sin(phase * math.pi) * -10
        pinch = 0.15 if 0.35 < phase < 0.75 else 0.9
        self._hand(p, QPointF(lx, ly), ha * 0.9, rgb, spread=pinch, flip=True)

    @staticmethod
    def _hand(p: QPainter, c: QPointF, a: float, rgb, spread: float, flip: bool) -> None:
        r, g, b = rgb
        s = -1 if flip else 1
        p.save()
        p.translate(c)
        p.setBrush(QColor(r, g, b, int(40 * a)))
        p.setPen(QPen(QColor(r, g, b, int(200 * a)), 1.2))
        p.drawEllipse(QPointF(0, 8), 11, 9)               # palm
        for i in range(5):                                # fingers
            ang = math.radians(-90 + s * (i - 2) * 24 * spread - s * 6)
            ln = 20 if i not in (0, 4) else 15
            tip = QPointF(math.cos(ang) * ln, 8 + math.sin(ang) * ln)
            p.drawLine(QPointF(math.cos(ang) * 7, 8 + math.sin(ang) * 7), tip)
            p.setBrush(QColor(255, 255, 255, int(230 * a)))
            p.drawEllipse(tip, 2.2, 2.2)
        # touch ripple
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(r, g, b, int(120 * a)), 1))
        p.drawEllipse(QPointF(0, 0), 14 + 6 * spread, 14 + 6 * spread)
        p.restore()
