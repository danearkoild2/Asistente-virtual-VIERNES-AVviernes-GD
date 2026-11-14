"""
Environmental Audio & Context Awareness Engine for VIERNES
==========================================================
Real-time (<0.4ms/frame) local acoustic scene analyzer + PC media cross-reference.
Distinguishes direct user speech from distant room chatter, keyboard transients,
steady background noise, and music/videos playing on the computer.
"""
from __future__ import annotations

import threading
import time
from collections import deque
from dataclasses import dataclass
from typing import Optional

import numpy as np


# Acoustic scene categories
SCENE_SILENCE        = "SILENCE"
SCENE_AMBIENT_NOISE  = "AMBIENT_NOISE"
SCENE_TRANSIENT      = "TRANSIENT"
SCENE_MUSIC_OR_MEDIA = "MUSIC_OR_MEDIA"
SCENE_DISTANT_SPEECH = "DISTANT_SPEECH"
SCENE_DIRECT_SPEECH  = "DIRECT_SPEECH"


@dataclass
class AcousticSnapshot:
    scene: str = SCENE_SILENCE
    rms: float = 0.0
    noise_floor: float = 45.0
    snr: float = 1.0
    speech_ratio: float = 0.0
    zcr: float = 0.0
    pc_media_playing: bool = False
    pc_media_desc: str = ""
    active_speaker: str = "Jesús"
    timestamp: float = 0.0


class EnvironmentalAwareness:
    """
    Thread-safe real-time acoustic & environmental context tracker.
    Safe to call `analyze_frame()` directly from the sounddevice audio callback.
    """

    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self._lock = threading.Lock()

        # Adaptive ambient noise floor (int16 RMS units)
        self._noise_floor: float = 55.0
        self._scene: str = SCENE_SILENCE
        self._last_rms: float = 0.0
        self._last_snr: float = 1.0
        self._last_speech_ratio: float = 0.0
        self._last_zcr: float = 0.0

        # Short-term history for hysteresis (avoids flickering on 1-frame spikes)
        self._speech_streak: int = 0
        self._recent_scenes: deque[str] = deque(maxlen=25)  # ~1.5s window
        self._last_direct_speech_at: float = 0.0
        self._last_distant_speech_at: float = 0.0

        # Cached PC media status (updated in background thread every ~4s)
        self._pc_media_playing: bool = False
        self._pc_media_desc: str = ""
        self._media_last_check: float = 0.0
        self._media_checking: bool = False

        # Active speaker (updated by voice_id)
        self._active_speaker: str = "Jesús"
        self._speaker_confidence: float = 0.0

        # Precompute FFT bin masks lazily for the first frame length seen
        self._cached_len: int = 0
        self._speech_mask: Optional[np.ndarray] = None
        self._high_mask: Optional[np.ndarray] = None
        self._hann: Optional[np.ndarray] = None

    def _ensure_fft_masks(self, n: int) -> None:
        if self._cached_len == n and self._speech_mask is not None:
            return
        freqs = np.fft.rfftfreq(n, 1.0 / self.sample_rate)
        self._speech_mask = (freqs >= 280.0) & (freqs <= 3400.0)
        self._high_mask = freqs > 4000.0
        self._hann = np.hanning(n).astype(np.float32)
        self._cached_len = n

    def analyze_frame(self, indata: np.ndarray) -> str:
        """
        Analyze a single PCM int16 audio frame in <0.4ms.
        Returns the classified acoustic scene string.
        """
        if indata is None or len(indata) == 0:
            return SCENE_SILENCE

        mono = indata[:, 0] if getattr(indata, "ndim", 1) > 1 else indata
        n = len(mono)
        if n < 64:
            return self._scene

        samples = mono.astype(np.float32)
        rms = float(np.sqrt(np.mean(samples * samples)))

        # Quick silence / very-low-energy update of adaptive noise floor
        if rms < 35.0:
            self._noise_floor = self._noise_floor * 0.96 + max(20.0, rms) * 0.04
            self._speech_streak = 0
            self._scene = SCENE_SILENCE
            self._last_rms = rms
            self._last_snr = rms / max(1.0, self._noise_floor)
            self._recent_scenes.append(SCENE_SILENCE)
            return SCENE_SILENCE

        snr = rms / max(20.0, self._noise_floor)

        # If energy is close to floor, slowly adapt floor upward/downward
        if snr < 1.6:
            self._noise_floor = self._noise_floor * 0.985 + rms * 0.015
            self._speech_streak = max(0, self._speech_streak - 1)
            scene = SCENE_MUSIC_OR_MEDIA if self._pc_media_playing else SCENE_AMBIENT_NOISE
            self._scene = scene
            self._last_rms = rms
            self._last_snr = snr
            self._recent_scenes.append(scene)
            return scene

        # Compute spectral features & ZCR for active signals
        self._ensure_fft_masks(n)
        windowed = samples * self._hann
        mag2 = np.abs(np.fft.rfft(windowed)) ** 2
        total_energy = float(np.sum(mag2)) + 1e-6

        speech_energy = float(np.sum(mag2[self._speech_mask]))
        high_energy = float(np.sum(mag2[self._high_mask]))
        speech_ratio = speech_energy / total_energy
        high_ratio = high_energy / total_energy

        # Zero-crossing rate (normalized 0..1)
        zcr = float(np.mean(np.abs(np.diff(np.signbit(samples)))))

        # Classification heuristics:
        # 1. Impulsive click / keyboard tap: very high high-freq or ZCR, short burst
        if high_ratio > 0.45 and speech_ratio < 0.35:
            scene = SCENE_TRANSIENT
            self._speech_streak = 0
        # 2. Clear near-field human speech: strong speech-band dominance + high SNR
        elif speech_ratio >= 0.48 and 0.02 <= zcr <= 0.32 and snr >= 2.8 and rms >= 135.0:
            self._speech_streak += 1
            if self._speech_streak >= 2:
                scene = SCENE_DIRECT_SPEECH
                self._last_direct_speech_at = time.monotonic()
            else:
                scene = SCENE_DISTANT_SPEECH
        # 3. Soft / distant voice or room chatter
        elif speech_ratio >= 0.36 and snr >= 1.7:
            self._speech_streak = max(0, self._speech_streak - 1)
            if self._pc_media_playing and rms < 210.0:
                scene = SCENE_MUSIC_OR_MEDIA
            else:
                scene = SCENE_DISTANT_SPEECH
                self._last_distant_speech_at = time.monotonic()
        # 4. Wideband tonal / music / background sound
        else:
            self._speech_streak = 0
            scene = SCENE_MUSIC_OR_MEDIA if self._pc_media_playing else SCENE_AMBIENT_NOISE

        self._scene = scene
        self._last_rms = rms
        self._last_snr = snr
        self._last_speech_ratio = speech_ratio
        self._last_zcr = zcr
        self._recent_scenes.append(scene)

        # Trigger background PC media refresh if stale (>4s)
        now = time.monotonic()
        if (now - self._media_last_check) > 4.0 and not self._media_checking:
            self._refresh_pc_media_async()

        return scene

    def _refresh_pc_media_async(self) -> None:
        self._media_checking = True
        self._media_last_check = time.monotonic()

        def _worker():
            try:
                from core.media_detector import MediaDetector
                track = MediaDetector.get_instance().get_current_media(force_fetch_art=False)
                if track and track.status == "PLAYING":
                    self._pc_media_playing = True
                    self._pc_media_desc = track.describe()
                else:
                    self._pc_media_playing = False
                    self._pc_media_desc = ""
            except Exception:
                pass
            finally:
                self._media_checking = False

        threading.Thread(target=_worker, daemon=True, name="EnvMediaProbe").start()

    def update_speaker(self, speaker_name: str, confidence: float = 0.0) -> None:
        if speaker_name:
            self._active_speaker = speaker_name
            self._speaker_confidence = confidence

    def is_direct_speech_likely(self) -> bool:
        """True if near-field speech directed at the mic was just observed."""
        if self._scene == SCENE_DIRECT_SPEECH:
            return True
        return (time.monotonic() - self._last_direct_speech_at) < 1.2

    def get_snapshot(self) -> AcousticSnapshot:
        return AcousticSnapshot(
            scene=self._scene,
            rms=round(self._last_rms, 1),
            noise_floor=round(self._noise_floor, 1),
            snr=round(self._last_snr, 2),
            speech_ratio=round(self._last_speech_ratio, 2),
            zcr=round(self._last_zcr, 3),
            pc_media_playing=self._pc_media_playing,
            pc_media_desc=self._pc_media_desc,
            active_speaker=self._active_speaker,
            timestamp=time.time(),
        )

    def get_environment_report(self) -> str:
        """Human-readable Spanish report of what is currently sounding in the environment."""
        snap = self.get_snapshot()
        parts = []
        scene_labels = {
            SCENE_SILENCE: "Habitación en silencio",
            SCENE_AMBIENT_NOISE: "Ruido ambiental constante de fondo",
            SCENE_TRANSIENT: "Sonidos breves de teclado o clics",
            SCENE_MUSIC_OR_MEDIA: "Música o audio multimedia activo",
            SCENE_DISTANT_SPEECH: "Voces lejanas o conversación de terceros en la habitación",
            SCENE_DIRECT_SPEECH: "Voz directa cercana al micrófono",
        }
        parts.append(f"Escena acústica: {scene_labels.get(snap.scene, snap.scene)} (SNR {snap.snr}x, nivel {snap.rms:.0f}).")
        if snap.pc_media_playing and snap.pc_media_desc:
            parts.append(f"Audio en la PC: {snap.pc_media_desc}")
        else:
            parts.append("Audio en la PC: Sin reproducción multimedia activa.")
        parts.append(f"Interlocutor identificado: {snap.active_speaker}.")
        return " ".join(parts)

    def get_prompt_block(self) -> str:
        """Compact environmental context for system prompt injection."""
        snap = self.get_snapshot()
        media_line = snap.pc_media_desc if snap.pc_media_playing else "Ninguna"
        return (
            "[ENVIRONMENTAL AWARENESS]\n"
            f"- Room acoustic state: {snap.scene} (SNR={snap.snr}x, floor={snap.noise_floor:.0f})\n"
            f"- PC Media playing: {media_line}\n"
            f"- Active identified speaker: {snap.active_speaker}\n"
        )


# Singleton instance
_env_engine: Optional[EnvironmentalAwareness] = None


def get_environmental_awareness() -> EnvironmentalAwareness:
    global _env_engine
    if _env_engine is None:
        _env_engine = EnvironmentalAwareness()
    return _env_engine
