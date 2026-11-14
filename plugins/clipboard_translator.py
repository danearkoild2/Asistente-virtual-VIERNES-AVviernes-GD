"""
Live Clipboard Translator Plugin for MARK LV / Viernes.
Translates text currently copied to clipboard to any language.
"""
from __future__ import annotations
import urllib.request
import urllib.parse
import json
import subprocess

PLUGIN = {
    "name": "clipboard_translator",
    "description": (
        "Translates whatever text is currently copied in the clipboard to a target language. "
        "Use when user asks 'traduce lo que copié', 'traduce el portapapeles', 'translate clipboard', "
        "or asks to translate copied text."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "target_language": {
                "type": "STRING",
                "description": "Target language code or name (e.g. 'es', 'en', 'ja', 'fr', 'de'). Defaults to 'es'.",
            }
        },
        "required": [],
    },
}

def _get_clipboard_windows() -> str:
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                             capture_output=True, text=True, timeout=3)
        return res.stdout.strip()
    except Exception:
        return ""

def _set_clipboard_windows(text: str):
    try:
        p = subprocess.Popen(["powershell", "-NoProfile", "-Command", "Set-Clipboard"],
                             stdin=subprocess.PIPE, text=True)
        p.communicate(input=text, timeout=3)
    except Exception:
        pass

def run(parameters: dict, player=None, session_memory=None) -> str:
    lang = parameters.get("target_language", "es").strip().lower()
    text = _get_clipboard_windows()

    if not text:
        return "El portapapeles está vacío o no contiene texto legible."

    # Free translation endpoint
    try:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=" + urllib.parse.quote(lang) + "&dt=t&q=" + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
            translated = "".join(part[0] for part in data[0] if part[0])

        _set_clipboard_windows(translated)
        short_preview = translated[:160] + "..." if len(translated) > 160 else translated
        msg = f"Traducción completada y copiada al portapapeles: \"{short_preview}\""
    except Exception as e:
        msg = f"No se pudo completar la traducción: {e}"

    if player:
        try:
            player.write_log(f"SYS: {msg}")
        except Exception:
            pass

    return msg
