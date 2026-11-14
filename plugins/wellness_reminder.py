"""
Hydration & Ergonomic Posture Reminder Plugin for MARK LV / Viernes.
Schedules periodic voice alerts to stay hydrated and stretch.
"""
from __future__ import annotations
import threading
import time

PLUGIN = {
    "name": "wellness_reminder",
    "description": (
        "Starts or stops health reminders for drinking water and checking posture. "
        "Use when user says 'recuérdame tomar agua', 'recordatorio de postura', "
        "or 'detén los recordatorios de salud'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "'start' or 'stop'.",
            },
            "interval_minutes": {
                "type": "INTEGER",
                "description": "Minutes between reminders. Defaults to 45.",
            }
        },
        "required": ["action"],
    },
}

_WELLNESS_EVENT = None

def _wellness_loop(event: threading.Event, interval_sec: float, player):
    tips = [
        "Señor, recuerde tomar un sorbo de agua y relajar los hombros.",
        "Pausa ergonómica: estire la espalda y mire a un punto lejano para descansar la vista.",
        "Un recordatorio de hidratación para mantener la mente despejada y productiva."
    ]
    idx = 0
    while event.is_set():
        time.sleep(interval_sec)
        if not event.is_set():
            break
        msg = tips[idx % len(tips)]
        idx += 1
        if player:
            try:
                player.write_log(f"💧 SALUD: {msg}")
                if hasattr(player, "request_say"):
                    player.request_say(msg)
            except Exception:
                pass

def run(parameters: dict, player=None, session_memory=None) -> str:
    global _WELLNESS_EVENT
    action = parameters.get("action", "start").strip().lower()
    interval = int(parameters.get("interval_minutes", 45))

    if action in ("stop", "cancel"):
        if _WELLNESS_EVENT:
            _WELLNESS_EVENT.clear()
            _WELLNESS_EVENT = None
        msg = "Recordatorios de hidratación y postura desactivados."
    else:
        if _WELLNESS_EVENT:
            _WELLNESS_EVENT.clear()
        _WELLNESS_EVENT = threading.Event()
        _WELLNESS_EVENT.set()
        t = threading.Thread(target=_wellness_loop, args=(_WELLNESS_EVENT, interval * 60, player), daemon=True)
        t.start()
        msg = f"Recordatorios de bienestar activados: te avisaré cada {interval} minutos para tomar agua y cuidar tu postura."

    if player:
        try:
            player.write_log(f"SYS: {msg}")
        except Exception:
            pass

    return msg
