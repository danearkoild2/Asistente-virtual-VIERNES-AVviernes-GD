"""
Spotify & Media Smart Controller Plugin for MARK LV / Viernes.
Directly controls Spotify, YouTube, VLC and Windows Media playback via native OS key events.
"""
from __future__ import annotations
import ctypes
import time
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "spotify_smart_controller",
    "description": (
        "Controls music and video playback (Spotify, YouTube, VLC, Windows Media). "
        "Can play, pause, resume, skip to next song, previous song, mute, or adjust media volume. "
        "Use when user asks 'pausa la música', 'siguiente canción', 'reanuda la música', 'canción anterior', "
        "or 'baja el volumen de la música'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "'play_pause', 'next', 'previous', 'stop', 'volume_up', 'volume_down', or 'mute'.",
            }
        },
        "required": ["action"],
    },
}

PLUGIN_SETTINGS = {
    "title": "Controlador Multimedia / Spotify",
    "fields": [
        {
            "key": "preferred_app",
            "label": "Reproductor Principal",
            "type": "choice",
            "options": ["Spotify", "YouTube / Chrome", "VLC", "Windows Media"],
            "default": "Spotify",
        },
        {
            "key": "volume_steps",
            "label": "Pasos de Cambio de Volumen",
            "type": "choice",
            "options": ["2", "4", "6", "10"],
            "default": "4",
        },
    ],
}

# Windows Virtual Key Codes for Media
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_STOP       = 0xB2
VK_MEDIA_PLAY_PAUSE = 0xB3
VK_VOLUME_MUTE      = 0xAD
VK_VOLUME_DOWN      = 0xAE
VK_VOLUME_UP        = 0xAF
KEYEVENTF_KEYUP     = 0x0002

def _send_vk(vk_code: int, times: int = 1):
    user32 = ctypes.windll.user32
    for _ in range(times):
        user32.keybd_event(vk_code, 0, 0, 0)
        time.sleep(0.02)
        user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.04)

def run(parameters: dict, player=None, session_memory=None) -> str:
    raw_action = str(parameters.get("action", "play_pause")).lower().strip()
    steps = int(get_plugin_setting("spotify_smart_controller", "volume_steps", 4))

    if raw_action in ("play", "pause", "resume", "play_pause", "toggle"):
        _send_vk(VK_MEDIA_PLAY_PAUSE)
        verb = "Alternando reproducción/pausa"
    elif raw_action in ("next", "skip", "siguiente"):
        _send_vk(VK_MEDIA_NEXT_TRACK)
        verb = "Saltando a la siguiente pista"
    elif raw_action in ("prev", "previous", "anterior"):
        _send_vk(VK_MEDIA_PREV_TRACK)
        verb = "Volviendo a la pista anterior"
    elif raw_action in ("stop", "detener", "parar"):
        _send_vk(VK_MEDIA_STOP)
        verb = "Reproducción detenida"
    elif raw_action in ("vol_up", "volume_up", "subir_volumen"):
        _send_vk(VK_VOLUME_UP, times=steps)
        verb = "Subiendo volumen multimedia"
    elif raw_action in ("vol_down", "volume_down", "bajar_volumen"):
        _send_vk(VK_VOLUME_DOWN, times=steps)
        verb = "Bajando volumen multimedia"
    elif raw_action in ("mute", "silenciar"):
        _send_vk(VK_VOLUME_MUTE)
        verb = "Silenciando / activando audio"
    else:
        _send_vk(VK_MEDIA_PLAY_PAUSE)
        verb = "Reproducción modificada"

    if player:
        try:
            player.write_log(f"🎵 MEDIA: {verb}")
        except Exception:
            pass

    return f"Listo. {verb}."
