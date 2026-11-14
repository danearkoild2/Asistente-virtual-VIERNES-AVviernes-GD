"""
Steam & Game Deal Hunter Plugin for MARK LV / Viernes.
Finds active discounts, historical low prices, and deals on PC games via CheapShark API.
"""
from __future__ import annotations
import json
import urllib.parse
import urllib.request
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "steam_deal_hunter",
    "description": (
        "Finds current discounts, cheapest stores, and pricing for PC video games across Steam and digital stores. "
        "Use when user asks 'ofertas de juegos', 'cuánto cuesta el juego...', 'está en oferta...', "
        "or 'descuentos en steam'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "game_title": {
                "type": "STRING",
                "description": "Title of the video game to search prices for (e.g. 'Cyberpunk 2077', 'Elden Ring').",
            }
        },
        "required": ["game_title"],
    },
}

PLUGIN_SETTINGS = {
    "title": "Cazador de Ofertas de Videojuegos",
    "fields": [
        {
            "key": "max_results",
            "label": "Máximo de Resultados",
            "type": "choice",
            "options": ["1", "3", "5"],
            "default": "3",
        },
    ],
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    title = str(parameters.get("game_title", "")).strip()
    if not title:
        return "Sir, dime qué videojuego deseas consultar para buscar ofertas."

    max_res = int(get_plugin_setting("steam_deal_hunter", "max_results", 3))
    url = f"https://www.cheapshark.com/api/1.0/deals?title={urllib.parse.quote(title)}&pageSize={max_res}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Viernes-GameDeals"})
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            deals = json.loads(resp.read().decode("utf-8"))

        if not deals:
            return f"No encontré ofertas activas registradas para '{title}'."

        deal_lines = []
        for d in deals[:max_res]:
            name = d.get("title")
            sale_price = d.get("salePrice")
            norm_price = d.get("normalPrice")
            savings = round(float(d.get("savings", 0)))
            rating = d.get("steamRatingText", "")
            deal_lines.append(f"🎮 {name}: ${sale_price} USD (-{savings}% de descuento, precio normal ${norm_price})")

        list_str = "\n• " + "\n• ".join(deal_lines)
        if player:
            try:
                player.write_log(f"🏷️ GAME DEALS:{list_str}")
            except Exception:
                pass

        first = deals[0]
        savings_first = round(float(first.get("savings", 0)))
        return f"Encontré {first.get('title')} por ${first.get('salePrice')} dólares con un {savings_first}% de descuento sobre su precio habitual de ${first.get('normalPrice')}."

    except Exception as e:
        return f"Sir, no pude consultar la base de datos de ofertas de videojuegos: {e}"
