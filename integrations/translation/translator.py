"""
Real-Time Translation Engine for VIERNES
=========================================
Supports automatic language detection, cross-lingual translation,
and live translation session mode.
"""
from __future__ import annotations

import json
import urllib.parse
from typing import Any, Dict, Optional, Tuple

import requests
from core.notifications import notify, LEVEL_INFO

# ISO 639-1 code to human readable names
LANGUAGE_NAMES = {
    "es": "Español",
    "en": "Inglés",
    "fr": "Francés",
    "de": "Alemán",
    "it": "Italiano",
    "pt": "Portugués",
    "ja": "Japonés",
    "zh": "Chino",
    "ru": "Ruso",
    "ko": "Coreano",
}


class TranslationEngine:
    """Multi-engine real-time neural translation subsystem."""

    def __init__(self):
        self._last_translation: Dict[str, Any] = {}

    def translate(
        self,
        text: str,
        target_lang: str = "en",
        source_lang: str = "auto",
    ) -> Dict[str, Any]:
        """
        Translate text with automatic source language detection.
        Returns: {
            "source_lang_code": "es",
            "source_lang_name": "Español",
            "target_lang_code": "en",
            "target_lang_name": "Inglés",
            "original_text": "...",
            "translated_text": "...",
            "engine": "google_neural"
        }
        """
        clean_text = text.strip()
        if not clean_text:
            return {"error": "Texto vacío para traducir."}

        target_code = target_lang.lower().strip()
        # Handle names like 'ingles' -> 'en', 'espanol' -> 'es'
        for code, name in LANGUAGE_NAMES.items():
            if target_code in name.lower() or target_code == code:
                target_code = code
                break

        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": source_lang,
            "tl": target_code,
            "dt": "t",
            "q": clean_text,
        }

        try:
            resp = requests.get(url, params=params, timeout=5.0)
            if resp.status_code == 200:
                data = resp.json()
                # Parse translation segments
                translated_parts = [segment[0] for segment in data[0] if segment and segment[0]]
                translated_text = "".join(translated_parts)
                detected_sl = data[2] if len(data) > 2 else "auto"

                sl_name = LANGUAGE_NAMES.get(detected_sl, detected_sl.upper())
                tl_name = LANGUAGE_NAMES.get(target_code, target_code.upper())

                result = {
                    "source_lang_code": detected_sl,
                    "source_lang_name": sl_name,
                    "target_lang_code": target_code,
                    "target_lang_name": tl_name,
                    "original_text": clean_text,
                    "translated_text": translated_text,
                    "engine": "neural_live",
                }
                self._last_translation = result
                notify(
                    "Traducción en Tiempo Real",
                    f"{sl_name} ➔ {tl_name}: '{translated_text[:40]}...'",
                    LEVEL_INFO,
                    "TRANSLATION"
                )
                return result
        except Exception as e:
            print(f"[Translator] API error: {e}")

        # Fallback echo if offline
        return {
            "source_lang_code": "auto",
            "source_lang_name": "Desconocido",
            "target_lang_code": target_code,
            "target_lang_name": target_code.upper(),
            "original_text": clean_text,
            "translated_text": f"[Traducción sin conexión ({target_code})]: {clean_text}",
            "engine": "fallback",
        }

    def format_live_card(self, translation_res: Dict[str, Any]) -> str:
        """Render the structured live translation card specified in Section 4."""
        sl_name = translation_res.get("source_lang_name", "Desconocido")
        tl_name = translation_res.get("target_lang_name", "Inglés")
        orig = translation_res.get("original_text", "")
        trans = translation_res.get("translated_text", "")

        return (
            f"🌐 [MODO TRADUCCIÓN EN VIVO]\n"
            f"┌─ IDIOMA DETECTADO: {sl_name.upper()}\n"
            f"│  TRANSCRIPCIÓN: \"{orig}\"\n"
            f"└─► TRADUCCIÓN ({tl_name.upper()}):\n"
            f"    \"{trans}\""
        )


# Global Translator singleton
translator = TranslationEngine()
