"""
core/speech_animation.py — Speech Animation & Semantic Intent Controller.
Coordinates natural semantic gestures, postural shifts, and holographic floating
with real-time Gemini speech output, tools, and conversational states.
"""

from __future__ import annotations

import re
import time
from typing import Any, Callable, Dict, List, Optional, Tuple


class SpeechAnimationController:
    """
    Analyzes live transcript chunks and assistant states to trigger
    expressive body gestures and semantic intents on the Live2D avatar.
    """

    def __init__(self, dispatch_fn: Optional[Callable[[str, Dict[str, Any]], None]] = None):
        """
        Args:
            dispatch_fn: Callback taking (intent_name, metadata_dict)
        """
        self._dispatch = dispatch_fn
        self._last_gesture_time = 0.0
        self._min_gesture_interval = 3.2  # Seconds between semantic gestures to prevent spamming
        self._speech_start_time = 0.0
        self._phrase_buffer = ""
        self._last_intent = ""
        self._explanation_side = "left"

        # Regex patterns for fast, sub-millisecond intent extraction
        self._patterns: List[Tuple[str, re.Pattern, float, str]] = [
            # (intent, compiled_regex, duration, intensity)
            (
                "emphasize",
                re.compile(
                    r"\b(importante|fundamental|clave|definitivamente|exactamente|ojo|ten en cuenta|crucial|imprescindible|crítico)\b",
                    re.IGNORECASE
                ),
                2.6,
                1.0
            ),
            (
                "present",
                re.compile(
                    r"\b(aquí tienes|estas son|te muestro|en pantalla|los resultados|las opciones|te presento|aquí está)\b",
                    re.IGNORECASE
                ),
                4.0,
                1.0
            ),
            (
                "confirm",
                re.compile(
                    r"\b(entendido|por supuesto|de acuerdo|perfecto|comprendido|así es|cuenta con ello|afirmativo|desde luego|listo)\b",
                    re.IGNORECASE
                ),
                2.8,
                0.9
            ),
            (
                "warn",
                re.compile(
                    r"\b(cuidado|advertencia|peligro|riesgo|alerta|precaución|error|fallo)\b",
                    re.IGNORECASE
                ),
                3.0,
                1.0
            ),
            (
                "apologize",
                re.compile(
                    r"\b(lo siento|disculpa|perdón|lamento|me equivoqué|disculpas)\b",
                    re.IGNORECASE
                ),
                3.2,
                0.85
            ),
            (
                "discover",
                re.compile(
                    r"\b(increíble|excelente|fantástico|maravilloso|genial|eureka|sorprendente)\b",
                    re.IGNORECASE
                ),
                3.2,
                1.1
            ),
            (
                "greet",
                re.compile(
                    r"\b(hola|buenos días|buenas tardes|buenas noches|qué tal|un gusto)\b",
                    re.IGNORECASE
                ),
                3.2,
                0.9
            ),
            (
                "farewell",
                re.compile(
                    r"\b(hasta luego|adiós|nos vemos|hasta pronto|que tengas un buen día|buenas noches)\b",
                    re.IGNORECASE
                ),
                3.4,
                0.85
            ),
            (
                "explain",
                re.compile(
                    r"\b(porque|debido a|en primer lugar|por ejemplo|consiste en|significa que|básicamente|la razón|se divide en|de esta manera|por lo tanto)\b",
                    re.IGNORECASE
                ),
                3.4,
                0.95
            ),
        ]

    def set_dispatcher(self, fn: Callable[[str, Dict[str, Any]], None]) -> None:
        self._dispatch = fn

    def on_speech_start(self) -> None:
        """Called as soon as TTS/audio output starts playing."""
        self._speech_start_time = time.monotonic()
        self._phrase_buffer = ""
        # Slight opening nod / posture prep
        now = time.monotonic()
        if (now - self._last_gesture_time) >= 2.0 and self._dispatch:
            self._dispatch("explain", {"side": "left", "duration": 2.8, "intensity": 0.75})
            self._last_gesture_time = now

    def on_speech_end(self) -> None:
        """Called when audio output has completely finished."""
        self._phrase_buffer = ""

    def process_text_chunk(self, chunk: str) -> Optional[str]:
        """
        Analyzes an incoming transcript segment from the model and dispatches
        an appropriate semantic body gesture if interval allows.
        """
        if not chunk or not self._dispatch:
            return None

        self._phrase_buffer += " " + chunk
        now = time.monotonic()

        # Enforce natural spacing between body gestures
        if (now - self._last_gesture_time) < self._min_gesture_interval:
            return None

        # Check patterns in order of priority (emphasis & warnings take precedence over generic explanation)
        matched_intent = None
        matched_dur = 3.0
        matched_intensity = 1.0

        for intent, pattern, dur, intensity in self._patterns:
            if pattern.search(chunk) or pattern.search(self._phrase_buffer[-80:]):
                matched_intent = intent
                matched_dur = dur
                matched_intensity = intensity
                break

        # Fallback for prolonged speech (> 6s since last gesture) without explicit keywords:
        # trigger a gentle explanatory arm alternation so she doesn't stay rigid
        if not matched_intent and (now - self._last_gesture_time) >= 6.5:
            matched_intent = "explain"
            matched_dur = 3.2
            matched_intensity = 0.8

        if matched_intent:
            metadata: Dict[str, Any] = {
                "duration": matched_dur,
                "intensity": matched_intensity,
            }
            if matched_intent == "explain":
                # Alternate arms
                self._explanation_side = "right" if self._explanation_side == "left" else "left"
                metadata["side"] = self._explanation_side
            elif matched_intent == "present":
                metadata["side"] = "left"  # Orient towards contextual panel

            self._dispatch(matched_intent, metadata)
            self._last_gesture_time = now
            self._last_intent = matched_intent
            self._phrase_buffer = ""
            return matched_intent

        return None

    def on_tool_start(self, tool_name: str) -> None:
        """Trigger reflective / analytical posture when a background action starts."""
        if not self._dispatch:
            return
        intent = "search" if ("search" in tool_name or "web" in tool_name or "fetch" in tool_name) else "think"
        self._dispatch(intent, {"duration": 4.5, "intensity": 0.9})
        self._last_gesture_time = time.monotonic()

    def on_tool_success(self, tool_name: str) -> None:
        """Trigger positive discovery / celebration gesture when a tool succeeds."""
        if not self._dispatch:
            return
        self._dispatch("discover", {"duration": 3.2, "intensity": 1.0})
        self._last_gesture_time = time.monotonic()

    def on_tool_error(self, tool_name: str) -> None:
        """Trigger cautious or apologetic posture on error."""
        if not self._dispatch:
            return
        self._dispatch("apologize", {"duration": 3.0, "intensity": 0.85})
        self._last_gesture_time = time.monotonic()
