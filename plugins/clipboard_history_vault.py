"""
Clipboard History Vault Plugin for MARK LV / Viernes.
Records clipboard clips with timestamps and lets users search, inspect, or restore recent items.
"""
from __future__ import annotations
from datetime import datetime
import json
from pathlib import Path
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "clipboard_history_vault",
    "description": (
        "Maintains a secure history of recently copied text snippets and allows searching or recovering them. "
        "Use when user asks 'qué copié antes', 'busca en mi portapapeles', 'recupera lo que copié', "
        "or 'historial de portapapeles'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "query": {
                "type": "STRING",
                "description": "Optional search term to filter recent clips.",
            },
            "limit": {
                "type": "INTEGER",
                "description": "Maximum number of recent entries to return (defaults to 5).",
            }
        },
        "required": [],
    },
}

PLUGIN_SETTINGS = {
    "title": "Bóveda de Portapapeles",
    "fields": [
        {
            "key": "max_history_entries",
            "label": "Máximo de Entradas Guardadas",
            "type": "choice",
            "options": ["10", "25", "50", "100"],
            "default": "25",
        },
    ],
}

_VAULT_FILE = Path(__file__).resolve().parent.parent / "config" / "clipboard_vault.json"

def _load_vault() -> list[dict]:
    if not _VAULT_FILE.exists():
        return []
    try:
        return json.loads(_VAULT_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def _save_vault(items: list[dict]):
    try:
        _VAULT_FILE.parent.mkdir(parents=True, exist_ok=True)
        _VAULT_FILE.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

def run(parameters: dict, player=None, session_memory=None) -> str:
    query = str(parameters.get("query", "")).lower().strip()
    try:
        limit = int(parameters.get("limit", 5))
    except (TypeError, ValueError):
        limit = 5

    vault = _load_vault()

    # Capture current clipboard into vault if new
    try:
        import subprocess
        res = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                             capture_output=True, text=True, timeout=2.0)
        curr = res.stdout.strip()
        if curr and len(curr) >= 3 and (not vault or vault[0].get("text") != curr):
            vault.insert(0, {
                "time": datetime.now().strftime("%H:%M:%S"),
                "text": curr
            })
            max_entries = int(get_plugin_setting("clipboard_history_vault", "max_history_entries", 25))
            vault = vault[:max_entries]
            _save_vault(vault)
    except Exception:
        pass

    if not vault:
        return "Tu historial de portapapeles aún está vacío."

    matches = []
    for item in vault:
        t = item.get("text", "")
        if not query or query in t.lower():
            snippet = t[:60] + "..." if len(t) > 60 else t
            matches.append(f"[{item.get('time')}] {snippet}")
        if len(matches) >= limit:
            break

    if not matches:
        return f"No encontré elementos en el portapapeles que coincidan con '{query}'."

    list_str = "\n• " + "\n• ".join(matches)
    if player:
        try:
            player.write_log(f"📋 PORTAPAPELES ({len(matches)} items):{list_str}")
        except Exception:
            pass

    return f"Aquí tienes los elementos recientes del portapapeles:{list_str}"
