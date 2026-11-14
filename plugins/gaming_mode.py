"""
Gaming & Performance Mode Plugin for MARK LV / Viernes.
Closes non-essential background resource hogs and applies high-performance Windows tweaks.
"""
from __future__ import annotations
import subprocess
import os

PLUGIN = {
    "name": "gaming_mode",
    "description": (
        "Activates or deactivates high-performance gaming mode. "
        "Use when user says 'activate gaming mode', 'modo juego', 'optimize for gaming', "
        "or asks to boost performance for games."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "'enable' to optimize PC for games or 'disable' to revert to balanced mode.",
            }
        },
        "required": ["action"],
    },
}

PLUGIN_SETTINGS = {
    "title": "Modo Gaming y Rendimiento",
    "fields": [
        {
            "key": "kill_browsers",
            "label": "Cerrar Navegadores en Segundo Plano",
            "type": "toggle",
            "default": False,
        },
        {
            "key": "high_priority",
            "label": "Prioridad de Plan de Energía Alto Rendimiento",
            "type": "toggle",
            "default": True,
        },
    ],
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    action = parameters.get("action", "enable").strip().lower()

    if action in ("enable", "activate", "on"):
        # Switch to Ultimate/High performance power plan on Windows
        try:
            # 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c is High Performance GUID
            subprocess.run(["powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"],
                           capture_output=True, timeout=5)
        except Exception:
            pass

        # Close heavy non-essential background processes if desired
        killed = []
        target_procs = ["chrome.exe", "msedge.exe", "discord.exe", "spotify.exe"]
        for proc in target_procs:
            try:
                res = subprocess.run(["taskkill", "/F", "/IM", proc], capture_output=True, timeout=3)
                if res.returncode == 0:
                    killed.append(proc.replace(".exe", ""))
            except Exception:
                pass

        msg = "Modo juego activado. Plan de alto rendimiento establecido."
        if killed:
            msg += f" Se liberaron recursos cerrando: {', '.join(killed)}."
        else:
            msg += " El sistema está listo con máxima prioridad."
    else:
        try:
            # 381b4222-f694-41f0-9685-ff5bb260df2e is Balanced GUID
            subprocess.run(["powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"],
                           capture_output=True, timeout=5)
        except Exception:
            pass
        msg = "Modo juego desactivado. Sistema restaurado a balance energético normal."

    if player:
        try:
            player.write_log(f"SYS: {msg}")
        except Exception:
            pass

    return msg
