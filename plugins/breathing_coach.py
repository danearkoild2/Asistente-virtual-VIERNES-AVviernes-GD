"""
Guided Anti-Stress Breathing Coach Plugin for MARK LV / Viernes.
Guides the user through 4-7-8 relaxing breathing exercises.
"""
from __future__ import annotations
import threading
import time

PLUGIN = {
    "name": "breathing_coach",
    "description": (
        "Guides the user through a relaxing 2-minute deep breathing exercise (4-7-8 anti-stress technique). "
        "Use when user says 'ayúdame a relajarme', 'ejercicio de respiración', 'estoy estresado', "
        "or 'guía de respiración'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {},
        "required": [],
    },
}

def _run_breathing(player):
    cycles = 3
    for c in range(1, cycles + 1):
        if player:
            try:
                player.write_log(f"🧘 [Ciclo {c}/{cycles}] Inhala profundamente por la nariz... (4 seg)")
                time.sleep(4)
                player.write_log(f"🧘 Mantén el aire en los pulmones... (7 seg)")
                time.sleep(7)
                player.write_log(f"🧘 Exhala suavemente por la boca... (8 seg)")
                time.sleep(8)
            except Exception:
                pass
    if player:
        try:
            player.write_log("✨ Ejercicio completado. Hombros relajados y mente despejada.")
            if hasattr(player, "request_say"):
                player.request_say("Exercise completed, sir. Take a moment to feel your body relaxed and present.")
        except Exception:
            pass

def run(parameters: dict, player=None, session_memory=None) -> str:
    t = threading.Thread(target=_run_breathing, args=(player,), daemon=True)
    t.start()
    msg = "Comenzando ejercicio de respiración antiestrés 4-7-8. Acomódate en tu silla, cerremos distracciones y sigue mi guía."
    if player:
        try: player.write_log(f"SYS: {msg}")
        except Exception: pass
    return msg
