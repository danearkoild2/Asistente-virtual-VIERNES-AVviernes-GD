"""
Gaming Decision & Random Picker Plugin for MARK LV / Viernes.
Helps the user pick what game to play or choose between options.
"""
from __future__ import annotations
import random

PLUGIN = {
    "name": "game_decider",
    "description": (
        "Picks a random game or decides between options provided by the user. "
        "Use when user asks 'qué juego hoy', 'elige qué jugar', 'decide entre X o Y', "
        "or 'dame una opción al azar'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "options": {
                "type": "STRING",
                "description": "Comma-separated list of games or choices. If omitted, uses popular gaming picks.",
            }
        },
        "required": [],
    },
}

POPULAR_GAMES = ["Cyberpunk 2077", "Elden Ring", "Valorant", "Minecraft", "Grand Theft Auto V", "League of Legends", "Rocket League", "The Witcher 3"]

def run(parameters: dict, player=None, session_memory=None) -> str:
    raw_opt = parameters.get("options", "").strip()
    if raw_opt:
        items = [i.strip() for i in raw_opt.replace(" o ", ",").split(",") if i.strip()]
    else:
        items = POPULAR_GAMES

    if not items:
        items = POPULAR_GAMES

    choice = random.choice(items)
    phrases = [
        f"Mi recomendación para hoy es: {choice}. ¡Que tengas una excelente partida!",
        f"El destino ha elegido: {choice}. Hora de demostrar tu nivel.",
        f"Definitivamente deberías jugar {choice} hoy.",
    ]
    msg = random.choice(phrases)
    if player:
        try: player.write_log(f"SYS: [Decider] {msg}")
        except Exception: pass
    return msg
