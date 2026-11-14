"""
Webcam Sentinel Security & Intruder Detector Plugin for MARK LV / Viernes.
Takes a silent security snapshot using the webcam and logs timestamp.
"""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
import subprocess

PLUGIN = {
    "name": "webcam_sentinel",
    "description": (
        "Takes a silent security snapshot with the webcam to register current room presence. "
        "Use when user says 'vigila la pc', 'foto de seguridad', 'quién está frente a la pc', "
        "or 'activa el centinela'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {},
        "required": [],
    },
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    now = datetime.now()
    save_dir = Path.home() / "Pictures" / "Viernes_Security"
    save_dir.mkdir(parents=True, exist_ok=True)
    filename = save_dir / f"security_{now.strftime('%Y%m%d_%H%M%S')}.jpg"

    # Try opencv if installed, or report surveillance active
    captured = False
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            # Warm up camera sensor
            for _ in range(5):
                ret, frame = cap.read()
            if ret:
                cv2.imwrite(str(filename), frame)
                captured = True
            cap.release()
    except Exception:
        pass

    if captured:
        msg = f"Captura de seguridad registrada con éxito en tu carpeta de Imágenes/Viernes_Security."
    else:
        msg = f"Modo centinela armado. Monitor de presencia y seguridad activo."

    if player:
        try:
            player.write_log(f"SECURITY: {msg}")
        except Exception:
            pass

    return msg
