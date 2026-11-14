"""
Real-Time Translation Action for VIERNES
=========================================
Auto-discovered by core/action_loader.py.
Handles natural commands like:
- "Viernes, traduce esto al inglés: ..."
- "Viernes, ¿cómo se dice en alemán 'buenas tardes'?"
- "Traduce esta conversación"
"""
from __future__ import annotations

from typing import Any, Dict
from integrations.translation.translator import translator

TOOL = {
    "name": "translate_live",
    "description": (
        "Traduce texto o voz en tiempo real con detección automática de idioma. "
        "Muestra el esquema: IDIOMA DETECTADO -> TRANSCRIPCIÓN -> TRADUCCIÓN. "
        "Permite traducir hacia inglés, español, francés, alemán, italiano, japonés, etc."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "text": {
                "type": "STRING",
                "description": "Texto o frase que se desea traducir.",
            },
            "target_language": {
                "type": "STRING",
                "description": "Idioma de destino deseado (ej: 'inglés', 'español', 'alemán', 'francés', 'japonés').",
            },
            "speak_translation": {
                "type": "BOOLEAN",
                "description": "Si es True, solicita que la respuesta de voz incluya la pronunciación.",
            },
        },
        "required": ["text"],
    },
    "handler": None,
}


def translate_action(parameters: Dict[str, Any] = None, player=None, session_memory=None) -> str:
    params = parameters or {}
    text = (params.get("text") or "").strip()
    target_lang = (params.get("target_language") or "inglés").strip()

    if not text:
        return "Por favor indica qué frase o texto deseas traducir."

    res = translator.translate(text, target_lang=target_lang)
    card_view = translator.format_live_card(res)

    if player and hasattr(player, "write_log"):
        player.write_log(f"TRANS: {res.get('source_lang_name')} -> {res.get('target_lang_name')}")

    return card_view


TOOL["handler"] = translate_action
