"""
Voice Pomodoro Focus Assistant Plugin for MARK LV / Viernes.
Starts focus sessions and break timers with audio and visual feedback.
"""
from __future__ import annotations
import threading
import time

PLUGIN = {
    "name": "pomodoro_timer",
    "description": (
        "Starts or stops a Pomodoro focus timer session. "
        "Use when user says 'inicia un pomodoro', 'start pomodoro', 'temporizador de concentración', "
        "or 'para el pomodoro'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "'start' to begin focus period or 'stop' to cancel.",
            },
            "work_minutes": {
                "type": "INTEGER",
                "description": "Minutes of deep work. Defaults to 25.",
            },
            "break_minutes": {
                "type": "INTEGER",
                "description": "Minutes of rest after work. Defaults to 5.",
            }
        },
        "required": ["action"],
    },
}

PLUGIN_SETTINGS = {
    "title": "Temporizador Pomodoro",
    "fields": [
        {
            "key": "default_work_minutes",
            "label": "Minutos de Enfoque",
            "type": "text",
            "default": "25",
            "placeholder": "25",
        },
        {
            "key": "default_break_minutes",
            "label": "Minutos de Descanso",
            "type": "text",
            "default": "5",
            "placeholder": "5",
        },
    ],
}

_ACTIVE_TIMER = None

def _run_pomodoro(work_min: int, break_min: int, player):
    time.sleep(work_min * 60)
    if player:
        try:
            player.write_log(f"⏰ POMODORO: ¡Tiempo de trabajo terminado! Tómate un descanso de {break_min} minutos.")
            if hasattr(player, "request_say"):
                player.request_say("Sir, the Pomodoro focus block has finished. Time for a five-minute break.")
        except Exception:
            pass

def run(parameters: dict, player=None, session_memory=None) -> str:
    global _ACTIVE_TIMER
    action = parameters.get("action", "start").strip().lower()
    work_min = int(parameters.get("work_minutes", 25))
    break_min = int(parameters.get("break_minutes", 5))

    if action in ("stop", "cancel"):
        _ACTIVE_TIMER = None
        msg = "El temporizador Pomodoro ha sido detenido."
    else:
        t = threading.Thread(target=_run_pomodoro, args=(work_min, break_min, player), daemon=True)
        t.start()
        _ACTIVE_TIMER = t
        msg = f"Sesión Pomodoro iniciada: {work_min} minutos de concentración máxima. Te avisaré cuando sea momento de descansar."

    if player:
        try:
            player.write_log(f"SYS: {msg}")
        except Exception:
            pass

    return msg
