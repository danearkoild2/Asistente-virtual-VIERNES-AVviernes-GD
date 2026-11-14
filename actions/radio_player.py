from __future__ import annotations

from typing import Any


def radio_player_action(parameters: dict[str, Any] = None, player=None, **_) -> str:
    """Reproduce radios en vivo con visualizador de espectro en el HUD de Viernes."""
    params = parameters or {}
    action = str(params.get("action") or "play").strip().lower()
    query = str(params.get("query") or params.get("station") or "").strip()
    country = str(params.get("country") or "").strip()
    genre = str(params.get("genre") or "").strip()
    muted = params.get("muted")

    if action == "stop":
        if player:
            player.stop_video()
        return "Radio detenida."

    if action == "mute":
        if player:
            player.set_video_muted(True)
        return "Radio silenciada."

    if action == "unmute":
        if player:
            player.set_video_muted(False)
        return "Sonido de la radio activado."

    from core.radio_engine import get_radio_manager

    mgr = get_radio_manager()

    if action == "refresh":
        stations = mgr.refresh_index(force=True)
        return f"Índice de radios actualizado ({len(stations)} emisoras disponibles)."

    if action == "list_favorites":
        favs = mgr.list_favorites()
        if not favs:
            return "No tienes emisoras favoritas guardadas todavía."
        lines = [f"- {f.get('name')} ({f.get('group') or 'Radio'})" for f in favs]
        return "Emisoras favoritas:\n" + "\n".join(lines)

    if action == "add_favorite":
        if not query:
            return "Indica el nombre de la emisora que deseas guardar en favoritos."
        res = mgr.resolve_working_station(query, country=country)
        if not res.get("ok"):
            return str(res.get("reason") or "No pude encontrar esa emisora para guardarla.")
        st = res["station"]
        mgr.add_favorite(st["name"], res["url"], group=st.get("group") or "")
        return f"Emisora guardada en favoritos: {st['name']}."

    if action == "search":
        if not query:
            return "Indica qué emisora o género deseas buscar."
        matches = mgr.search_stations(query, country=country, limit=8)
        if not matches:
            return f"No encontré emisoras para '{query}'."
        lines = [
            f"- {m.get('name')} ({m.get('country') or m.get('group') or m.get('source')})"
            for m in matches
        ]
        return "Emisoras encontradas:\n" + "\n".join(lines)

    if action == "random" or (
        action == "play"
        and (not query or any(k in query.lower() for k in ("random", "aleatori", "cualquiera", "sorpresa")))
    ):
        res = mgr.random_spanish_station(genre=genre, country=country)
        if not res.get("ok"):
            return str(res.get("reason") or "No se encontró ninguna radio aleatoria en español activa.")
        st = res["station"]
        sub = " · ".join([x for x in [st.get("group"), st.get("country"), "Español", st.get("source")] if x])
        if player:
            player.show_radio(
                res["url"],
                title=st.get("name") or "Radio en Español",
                subtitle=sub,
                muted=muted if isinstance(muted, bool) else None,
            )
        return f"Reproduciendo radio aleatoria en español: {st.get('name')} ({sub})."

    # Default: play specific station
    if not query:
        return "Indica el nombre de la emisora que quieres escuchar o pide una radio aleatoria."

    res = mgr.resolve_working_station(query, country=country)
    if not res.get("ok"):
        return str(res.get("reason") or f"No encontré un stream activo para '{query}'.")

    st = res["station"]
    sub = " · ".join([x for x in [st.get("group"), st.get("country"), st.get("source")] if x])
    if player:
        player.show_radio(
            res["url"],
            title=st.get("name") or query,
            subtitle=sub,
            muted=muted if isinstance(muted, bool) else None,
        )
    return f"Reproduciendo {st.get('name')} ({sub})."


TOOL = {
    "name": "radio_player",
    "description": (
        "Reproduce emisoras de radio en vivo dentro del HUD de Viernes con visualizador de espectro. "
        "Soporta emisoras de https://www.ondachannels.com/lists/radio.m3u8 y emisoras latinoamericanas/españolas "
        "(por ejemplo 'Bésame de Costa Rica', 'Cadena SER', 'LOS40'). "
        "Cuando el usuario pida una radio aleatoria/random, siempre reproduce una emisora en español."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": (
                    "Acción a ejecutar: 'play' (reproducir emisora específica), "
                    "'random' (radio aleatoria SIEMPRE en español), 'search', 'stop', "
                    "'mute', 'unmute', 'add_favorite', 'list_favorites', 'refresh'."
                ),
            },
            "query": {
                "type": "STRING",
                "description": "Nombre de la emisora (ej. 'Bésame de Costa Rica', 'Cadena SER', 'LOS40').",
            },
            "country": {
                "type": "STRING",
                "description": "País opcional para filtrar (ej. 'Costa Rica', 'España', 'México').",
            },
            "genre": {
                "type": "STRING",
                "description": "Género o tema opcional para radio aleatoria (ej. 'romántica', 'pop', 'noticias', 'rock').",
            },
            "muted": {
                "type": "BOOLEAN",
                "description": "Opcional: silenciar al iniciar (por defecto usa la preferencia del usuario).",
            },
        },
        "required": ["action"],
    },
    "handler": radio_player_action,
}
