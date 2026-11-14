"""
Ambient White Noise & Rain Generator Plugin for MARK LV / Viernes.
Synthesizes relaxing ambient noise (pink noise, rain, waves) via sounddevice.
"""
from __future__ import annotations
import threading
import time
import numpy as np
import sounddevice as sd

PLUGIN = {
    "name": "ambient_sound",
    "description": (
        "Plays relaxing ambient background soundscapes (rain, brown noise, focus sound) or stops them. "
        "Use when user asks 'pon sonido de lluvia', 'ruido blanco', 'sonido relajante', "
        "or 'para el sonido ambiental'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "'play' or 'stop'.",
            },
            "sound_type": {
                "type": "STRING",
                "description": "'rain', 'waves', or 'brown_noise'. Defaults to 'rain'.",
            },
            "duration_minutes": {
                "type": "INTEGER",
                "description": "Duration in minutes. Defaults to 30.",
            }
        },
        "required": ["action"],
    },
}

_PLAYING_EVENT = None

def _generate_rain_block(samples: int) -> np.ndarray:
    # Brown/pink noise filtered like rainfall
    white = np.random.normal(0, 1, samples)
    b_noise = np.cumsum(white)
    b_noise -= np.mean(b_noise)
    max_val = np.max(np.abs(b_noise)) or 1.0
    rain = (b_noise / max_val) * 0.12
    return rain.astype(np.float32)

def _ambient_loop(event: threading.Event, duration_sec: float):
    sr = 24000
    t_end = time.time() + duration_sec
    while event.is_set() and time.time() < t_end:
        block = _generate_rain_block(sr * 2)
        sd.play(block, sr)
        sd.wait()

def run(parameters: dict, player=None, session_memory=None) -> str:
    global _PLAYING_EVENT
    action = parameters.get("action", "play").strip().lower()
    minutes = int(parameters.get("duration_minutes", 30))

    if action in ("stop", "off", "cancel"):
        if _PLAYING_EVENT:
            _PLAYING_EVENT.clear()
            sd.stop()
            _PLAYING_EVENT = None
        msg = "Sonido ambiental detenido."
    else:
        if _PLAYING_EVENT:
            _PLAYING_EVENT.clear()
            sd.stop()

        _PLAYING_EVENT = threading.Event()
        _PLAYING_EVENT.set()
        t = threading.Thread(target=_ambient_loop, args=(_PLAYING_EVENT, minutes * 60), daemon=True)
        t.start()
        msg = f"Reproduciendo sonido ambiental relajante durante {minutes} minutos. Di 'para el sonido ambiental' cuando gustes detenerlo."

    if player:
        try:
            player.write_log(f"SYS: {msg}")
        except Exception:
            pass

    return msg
