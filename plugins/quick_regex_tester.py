"""
Quick Regex Tester & Explainer Plugin for MARK LV / Viernes.
Tests regular expressions against sample text and reports match groups and validity.
"""
from __future__ import annotations
import re
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "quick_regex_tester",
    "description": (
        "Tests a regular expression (regex) against sample text, finding matches and groups. "
        "Use when user asks 'prueba esta regex', 'valida una expresión regular', or 'busca con regex'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "pattern": {
                "type": "STRING",
                "description": "The regex pattern to test (e.g. '\\b\\d{4}-\\d{2}-\\d{2}\\b').",
            },
            "sample_text": {
                "type": "STRING",
                "description": "The text string to test the pattern against.",
            },
            "ignore_case": {
                "type": "BOOLEAN",
                "description": "Whether to perform case-insensitive matching.",
            }
        },
        "required": ["pattern", "sample_text"],
    },
}

PLUGIN_SETTINGS = {
    "title": "Probador de Regex",
    "fields": [
        {
            "key": "default_ignore_case",
            "label": "Ignorar Mayúsculas por Defecto",
            "type": "toggle",
            "default": True,
        },
    ],
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    pat_str = str(parameters.get("pattern", "")).strip()
    sample = str(parameters.get("sample_text", ""))
    
    if not pat_str:
        return "Sir, proporciona el patrón regex a verificar."

    ign = parameters.get("ignore_case")
    if ign is None:
        ign = bool(get_plugin_setting("quick_regex_tester", "default_ignore_case", True))
    flags = re.IGNORECASE if ign else 0

    try:
        compiled = re.compile(pat_str, flags)
        matches = compiled.findall(sample)
    except re.error as err:
        return f"Error en la expresión regular: {err}"

    count = len(matches)
    if count == 0:
        res = f"Patrón /{pat_str}/ válido, pero no se encontró ninguna coincidencia en el texto."
    else:
        sample_disp = str(matches[:5])
        res = f"¡Éxito! Se encontraron {count} coincidencias para /{pat_str}/. Muestras: {sample_disp}."

    if player:
        try:
            player.write_log(f"🔬 REGEX TEST: {res}")
        except Exception:
            pass

    return res
