"""
Screen Night Light & Warmth Plugin for MARK LV / Viernes.
Adjusts monitor color temperature and blue-light filtering to prevent eye strain.
"""
from __future__ import annotations
import ctypes
from ctypes import wintypes
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "screen_color_night_light",
    "description": (
        "Controls monitor color temperature, blue-light filter and night warmth level. "
        "Use when user asks 'activa la luz nocturna', 'modo lectura en pantalla', 'pantalla más cálida', "
        "or 'restaura el color de la pantalla'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "mode": {
                "type": "STRING",
                "description": "'warm' (amber night light), 'ultra_warm' (candlelight/sleep), or 'normal' (reset colors).",
            }
        },
        "required": ["mode"],
    },
}

PLUGIN_SETTINGS = {
    "title": "Luz Nocturna y Calidez de Pantalla",
    "fields": [
        {
            "key": "night_warmth",
            "label": "Nivel de Calidez Nocturna",
            "type": "choice",
            "options": ["Suave (4500K)", "Media (3400K)", "Ultra Cálida (2400K)"],
            "default": "Media (3400K)",
        },
    ],
}

# Gamma Ramp structure
class RAMP(ctypes.Structure):
    _fields_ = [
        ("Red", wintypes.WORD * 256),
        ("Green", wintypes.WORD * 256),
        ("Blue", wintypes.WORD * 256),
    ]

def _apply_gamma(red_scale: float, green_scale: float, blue_scale: float) -> bool:
    try:
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        hdc = user32.GetDC(None)
        if not hdc:
            return False

        ramp = RAMP()
        for i in range(256):
            v = i * 256
            ramp.Red[i]   = min(65535, int(v * red_scale))
            ramp.Green[i] = min(65535, int(v * green_scale))
            ramp.Blue[i]  = min(65535, int(v * blue_scale))

        ok = gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(ramp))
        user32.ReleaseDC(None, hdc)
        return bool(ok)
    except Exception:
        return False

def run(parameters: dict, player=None, session_memory=None) -> str:
    mode = str(parameters.get("mode", "warm")).lower().strip()

    if mode in ("normal", "reset", "dia", "day", "desactivar", "off"):
        ok = _apply_gamma(1.0, 1.0, 1.0)
        report = "Luz nocturna desactivada. Colores originales restaurados."
    elif mode in ("ultra_warm", "candle", "dormir", "sleep"):
        ok = _apply_gamma(1.0, 0.72, 0.40)
        report = "Modo ultra cálido (filtro anti-luz azul intenso) activado para proteger tu vista."
    else: # warm / lectura
        ok = _apply_gamma(1.0, 0.84, 0.65)
        report = "Luz nocturna cálida activada para reducir fatiga visual."

    if not ok:
        report = "No se pudo modificar la rampa de color directamente (puede requerir permisos del controlador de pantalla)."

    if player:
        try:
            player.write_log(f"🌙 NIGHT LIGHT: {report}")
        except Exception:
            pass

    return report
