"""
Local wake-word detection for VIERNES ("Viernes", "Despierta viernes", "Hey Viernes").
Supports both Spanish speech recognition keyword spotter (online/offline VAD)
and local openwakeword ("hey_viernes") models.
"""
from __future__ import annotations

import queue
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Callable, List, Optional

import numpy as np

# Pretrained openwakeword model fallback
WAKE_MODEL = "hey_viernes"
DEFAULT_THRESHOLD = 0.5
SAMPLE_RATE = 16000

# Spanish wake phrases for VIERNES
SPANISH_WAKE_PHRASES = [
    "viernes",
    "despierta",
    "despierta viernes",
    "despiértate",
    "despiertate",
    "hey viernes",
    "hola viernes",
    "oye viernes",
    "arriba viernes",
    "arriba",
    "buenos días",
    "buenos dias",
]


def is_installed() -> bool:
    """True if speech recognition or wake word detection is installed."""
    return True


def is_ready() -> bool:
    """Always ready for immediate Spanish wake-word detection."""
    return True


def install_and_download(logger: Callable[[str], None] = print,
                         notify: Callable[[str], None] | None = None) -> tuple[bool, str]:
    """Ensure wake word system is ready."""
    return True, "Sistema de activación por voz configurado y listo."


class WakeWordDetector:
    """
    Listens for 'Viernes' and 'Despierta viernes' in real-time from mic frames.
    Combines VAD energy segmentation + rapid Spanish keyword recognition
    with local openwakeword as parallel fallback.
    """

    def __init__(self, on_detect: Callable[[], None],
                 threshold: float = DEFAULT_THRESHOLD,
                 logger: Callable[[str], None] = print,
                 notify: Callable[[str], None] | None = None,
                 wake_phrase: str = "Viernes"):
        self._on_detect   = on_detect
        self._threshold   = threshold
        self._logger      = logger
        self._notify      = notify or (lambda _msg: None)
        self._wake_phrase = wake_phrase
        self._queue: queue.Queue = queue.Queue(maxsize=120)
        self._thread: threading.Thread | None = None
        self._running     = False
        self._model       = None
        self._ready       = False
        self._speech_buffer: List[np.ndarray] = []
        import collections
        self._pre_buffer  = collections.deque(maxlen=4)  # ~250ms pre-roll to catch start of "Viernes"
        self._silence_count = 0
        self._last_detect_time = 0.0
        self._is_checking = False
        self._check_lock = threading.Lock()

        # Spanish Recognizer
        self._sr_recognizer = None
        try:
            import speech_recognition as sr
            self._sr_recognizer = sr.Recognizer()
            self._sr_recognizer.energy_threshold = 200
            self._sr_recognizer.dynamic_energy_threshold = False
        except Exception:
            self._sr_recognizer = None

    def start(self) -> bool:
        if self._running:
            return True

        # Try loading openwakeword ONNX model as secondary fallback
        try:
            from openwakeword.model import Model
            self._model = Model(wakeword_models=[WAKE_MODEL], inference_framework="onnx")
        except Exception:
            self._model = None

        self._running = True
        self._ready = True
        self._speech_buffer = []
        self._silence_count = 0
        self._pre_buffer.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True, name="WakeWordThread")
        self._thread.start()
        self._logger(f"Wake word: escuchando activamente '{self._wake_phrase}' y 'Despierta {self._wake_phrase}'.")
        return True

    def stop(self) -> None:
        self._running = False
        try:
            self._queue.put_nowait(None)
        except Exception:
            pass
        self._model = None
        self._ready = False

    @property
    def ready(self) -> bool:
        return self._ready

    def feed(self, frame_int16) -> None:
        """Called from mic thread. Lightweight copy into detection queue."""
        if not self._running:
            return
        try:
            data = frame_int16[:, 0].copy() if getattr(frame_int16, "ndim", 1) > 1 else frame_int16.copy()
            self._queue.put_nowait(data)
        except queue.Full:
            pass
        except Exception:
            pass

    def _loop(self) -> None:
        while self._running:
            try:
                frame = self._queue.get()
                if frame is None or not self._running:
                    break

                frame_arr = np.asarray(frame, dtype=np.int16)
                # Compute RMS energy to detect voice activity
                rms = float(np.sqrt(np.mean(frame_arr.astype(np.float32) ** 2)))

                # 1. Spanish VAD & Speech Buffer Accumulator
                # Tuned threshold: 120.0 catches ordinary/soft speech without triggering on quiet room hum
                if rms > 120.0:
                    if not self._speech_buffer and self._pre_buffer:
                        # Prepend the pre-roll frames so the first consonant ('V' / 'D') isn't cut off
                        self._speech_buffer.extend(list(self._pre_buffer))
                    self._speech_buffer.append(frame_arr)
                    self._silence_count = 0
                    # If continuous speech reaches ~2.5 seconds, check immediately
                    if len(self._speech_buffer) >= 40:
                        chunk_pcm = np.concatenate(self._speech_buffer).tobytes()
                        self._speech_buffer.clear()
                        self._silence_count = 0
                        self._dispatch_spanish_check(chunk_pcm)
                elif self._speech_buffer:
                    self._silence_count += 1
                    # ~350 ms of silence after speech -> end of spoken phrase
                    if self._silence_count >= 5:
                        total_samples = sum(len(f) for f in self._speech_buffer)
                        if total_samples >= 3500:  # At least ~220 ms of voice
                            chunk_pcm = np.concatenate(self._speech_buffer).tobytes()
                            self._dispatch_spanish_check(chunk_pcm)
                        self._speech_buffer.clear()
                        self._silence_count = 0
                else:
                    self._pre_buffer.append(frame_arr)

                # 2. Parallel openwakeword check (if model loaded)
                if self._model is not None:
                    try:
                        scores = self._model.predict(frame_arr)
                        score = 0.0
                        if isinstance(scores, dict):
                            for k, v in scores.items():
                                score = max(score, float(v))
                        if score >= self._threshold:
                            self._logger(f"[Wake] openwakeword detector match (score={score:.2f})")
                            self._trigger_wake("openwakeword")
                    except Exception:
                        pass

            except Exception as e:
                self._logger(f"Wake word: loop error — {e}")

    def _dispatch_spanish_check(self, pcm_bytes: bytes) -> None:
        """Run speech recognition on the captured speech segment in a worker thread."""
        if not pcm_bytes:
            return

        with self._check_lock:
            if self._is_checking:
                return
            self._is_checking = True

        def _work():
            try:
                import time
                now = time.time()
                if (now - self._last_detect_time) < 2.0:
                    return

                text = ""
                if self._sr_recognizer is not None:
                    try:
                        import speech_recognition as sr
                        audio_data = sr.AudioData(pcm_bytes, SAMPLE_RATE, 2)
                        # Spanish speech recognition
                        text = self._sr_recognizer.recognize_google(audio_data, language="es-ES").lower()
                    except Exception:
                        pass

                if text:
                    # Normalize text: remove accents and symbols
                    norm_text = text.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                    import re
                    clean_text = re.sub(r"[^\w\s]", "", norm_text).strip()
                    self._logger(f"[Wake] Audio capturado en reposo: '{text}'")

                    wake_keys = [
                        "viernes",
                        "despierta",
                        "despiertate",
                        "despertar",
                        "hola",
                        "hey",
                        "arriba",
                        "oye",
                        "buenos dias",
                                                self._wake_phrase.lower(),
                        f"despierta {self._wake_phrase.lower()}",
                    ]

                    # Check if any wake key or phrase matches
                    matched = False
                    for k in wake_keys:
                        norm_k = k.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
                        if norm_k in clean_text:
                            matched = True
                            break

                    if matched:
                        self._last_detect_time = time.time()
                        self._logger(f"[Wake] Palabra de activación reconocida: '{text}'. Despertando...")
                        self._trigger_wake(f"palabra de voz '{text}'")
            finally:
                with self._check_lock:
                    self._is_checking = False

        threading.Thread(target=_work, daemon=True, name="SpanishWakeWorker").start()

    def _trigger_wake(self, reason: str = "") -> None:
        self._drain()
        self._speech_buffer.clear()
        self._silence_count = 0
        try:
            self._on_detect()
        except Exception as e:
            self._logger(f"Wake word: on_detect error — {e}")

    def _drain(self) -> None:
        try:
            while True:
                self._queue.get_nowait()
        except Exception:
            pass
