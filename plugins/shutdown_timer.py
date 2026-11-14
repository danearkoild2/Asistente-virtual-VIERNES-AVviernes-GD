"""
Scheduled Shutdown & Sleep Timer Plugin for MARK LV / Viernes.
Allows user to schedule PC shutdown, restart, or cancel scheduled timers.
"""
from __future__ import annotations
import subprocess

PLUGIN = {
    "name": "shutdown_timer",
    "description": (
        "Schedules or cancels an automatic shutdown or restart timer for the computer. "
        "Use when user says 'apaga la PC en X minutos', 'shut down in 30 minutes', "
        "or 'cancela el apagado programado'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "'schedule' to set timer or 'cancel' to abort pending shutdown.",
            },
            "minutes": {
                "type": "INTEGER",
                "description": "Number of minutes before shutdown. Defaults to 30.",
            },
            "mode": {
                "type": "STRING",
                "description": "'shutdown' or 'restart'. Defaults to 'shutdown'.",
            }
        },
        "required": ["action"],
    },
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    action = parameters.get("action", "schedule").strip().lower()
    minutes = int(parameters.get("minutes", 30))
    mode = parameters.get("mode", "shutdown").strip().lower()

    if action in ("cancel", "abort"):
        try:
            subprocess.run(["shutdown", "/a"], capture_output=True, timeout=5)
            msg = "El temporizador de apagado automático ha sido cancelado con éxito."
        except Exception as e:
            msg = f"No se pudo cancelar el apagado: {e}"
    else:
        seconds = max(10, minutes * 60)
        flag = "/r" if mode == "restart" else "/s"
        try:
            # Cancel any previous first
            subprocess.run(["shutdown", "/a"], capture_output=True, timeout=3)
            res = subprocess.run(["shutdown", flag, "/t", str(seconds)], capture_output=True, timeout=5)
            if res.returncode == 0:
                op_name = "reinicio" if mode == "restart" else "apagado"
                msg = f"Temporizador configurado: el equipo se programó para {op_name} en {minutes} minutos."
            else:
                msg = f"Error al programar el apagado: {res.stderr.decode(errors='replace')}"
        except Exception as e:
            msg = f"Error al ejecutar comando de apagado: {e}"

    if player:
        try:
            player.write_log(f"SYS: {msg}")
        except Exception:
            pass
    return msg
