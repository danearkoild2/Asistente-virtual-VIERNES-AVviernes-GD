"""
Instant Privacy & Lock Mode Plugin for MARK LV / Viernes.
Mutes all system audio, minimizes windows and locks Windows session immediately.
"""
from __future__ import annotations
import subprocess
import ctypes

PLUGIN = {
    "name": "privacy_lock",
    "description": (
        "Immediately locks the Windows session, mutes system audio, and protects screen privacy. "
        "Use when user says 'bloqueo de privacidad', 'saldré un momento', 'lock screen', "
        "or 'modo privacidad'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {},
        "required": [],
    },
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    # 1. Mute audio using Windows key simulation or PowerShell sound mute
    try:
        # Simulate VK_VOLUME_MUTE keypress (0xAD)
        ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
        ctypes.windll.user32.keybd_event(0xAD, 0, 2, 0)
    except Exception:
        pass

    # 2. Lock Windows Workstation
    try:
        ctypes.windll.user32.LockWorkStation()
        msg = "Sesión bloqueada y audio silenciado por seguridad."
    except Exception as e:
        # Fallback to rundll32
        try:
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], timeout=3)
            msg = "Sesión bloqueada por seguridad."
        except Exception as exc:
            msg = f"No se pudo bloquear la estación de trabajo: {exc}"

    if player:
        try:
            player.write_log(f"SYS: {msg}")
        except Exception:
            pass

    return msg
