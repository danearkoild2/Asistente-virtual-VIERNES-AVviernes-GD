"""
Safe Mode Subsystem for VIERNES
================================
Enforces the principle of least privilege, preventing unintended, dangerous,
or destructive operations without explicit interactive user confirmation.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

_CONFIG_FILE = Path(__file__).resolve().parent.parent / "config" / "api_keys.json"

_CRITICAL_ACTIONS = {
    "DELETE_FILES": "Esta acción puede eliminar archivos permanentemente.",
    "SYSTEM_SHUTDOWN": "Esta acción apagará o reiniciará el equipo.",
    "KILL_PROCESS": "Detener este proceso podría desestabilizar el sistema.",
    "SMART_LOCK_UNLOCK": "Esta acción desbloqueará una cerradura física de seguridad.",
    "FINANCIAL_TRANSFER": "Las operaciones financieras con dinero real requieren confirmación estricta.",
    "SYSTEM_SETTING_CHANGE": "Esta acción modificará la configuración del sistema operativo.",
}

# In-memory safe mode cache (default: True)
_SAFE_MODE_ENABLED = True


def is_safe_mode() -> bool:
    global _SAFE_MODE_ENABLED
    try:
        if _CONFIG_FILE.exists():
            cfg = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
            return cfg.get("safe_mode", True)
    except Exception:
        pass
    return _SAFE_MODE_ENABLED


def set_safe_mode(enabled: bool) -> None:
    global _SAFE_MODE_ENABLED
    _SAFE_MODE_ENABLED = bool(enabled)
    try:
        if _CONFIG_FILE.exists():
            cfg = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
            cfg["safe_mode"] = _SAFE_MODE_ENABLED
            _CONFIG_FILE.write_text(json.dumps(cfg, indent=4, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print(f"[SafeMode] Error saving safe mode configuration: {e}")


def check_action_confirmation(action_name: str, target: str = "") -> Tuple[bool, str]:
    """
    Returns (needs_confirmation, warning_message).
    If Safe Mode is enabled, checks critical action list.
    """
    action_key = action_name.upper()
    if action_key in _CRITICAL_ACTIONS:
        reason = _CRITICAL_ACTIONS[action_key]
        if target:
            reason += f" Objetivo: {target}."
        return True, reason

    if is_safe_mode():
        # Any action modifying state in safe mode can require approval
        if any(verb in action_key for verb in ("DELETE", "REMOVE", "DROP", "WIPE", "FORMAT", "UNLOCK", "SHUTDOWN")):
            return True, f"Modo Seguro activo: La acción '{action_name}' requiere autorización explícita."

    return False, ""
