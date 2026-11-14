"""
actions/iptv_player.py — Live TV & IPTV player powered by iptv-org.

Plays verified live TV channels directly inside VIERNES's internal HUD
video player (with automatic audio unless the user enabled mute), checks
whether streams are online/working, searches channels by name/country/category,
manages favorites, custom M3U playlists, and EPG metadata.
"""
from __future__ import annotations

import threading
from typing import Any

from core.iptv_org import get_iptv_manager

_open_lock = threading.Lock()
_open_token = 0


def _begin_open() -> int:
    global _open_token
    with _open_lock:
        _open_token += 1
        return _open_token


def _still_wanted(token: int) -> bool:
    with _open_lock:
        return _open_token == token


def _say(player, instruction: str) -> None:
    if player is not None and hasattr(player, "request_say"):
        try:
            player.request_say(instruction)
        except Exception:
            pass


def _log(player, msg: str) -> None:
    if player is not None and hasattr(player, "write_log"):
        try:
            player.write_log(msg)
        except Exception:
            pass


def _play_channel_async(
    player,
    channel_query: str,
    country: str,
    token: int,
    fullscreen: bool = False,
    option: int = 1,
) -> None:
    try:
        from core.sports_tv import (
            is_sports_request,
            load_settings as load_sports_settings,
            resolve_channel as resolve_sports_channel,
        )
        scfg = load_sports_settings()
        routing = scfg.get("sports_routing", "sports_web")
        if routing != "iptv" and scfg.get("enabled", True) and hasattr(player, "show_sports_channel"):
            sres = resolve_sports_channel(channel_query, option=option)
            if not _still_wanted(token):
                return
            if sres.get("ok") and sres.get("url"):
                ch_name = (sres.get("channel") or {}).get("name") or channel_query
                frame_host = sres.get("frame_host", "")
                source_tag = "TV WEB" if sres.get("source") == "tvporinternet" else "TV DEPORTIVA"
                _log(
                    player,
                    f"{source_tag}: Abriendo {ch_name.upper()} (Opción {sres.get('selected_option', 1)}) con Brave AdBlock"
                    + (f" ({frame_host})" if frame_host else ""),
                )
                player.show_sports_channel(
                    sres["url"],
                    title=f"{ch_name} [EN VIVO]",
                    frame_src=sres.get("frame_src", ""),
                    frame_host=frame_host,
                    muted=None,
                    options=sres.get("options") or [],
                    selected_option=int(sres.get("selected_option", 1)),
                )
                if fullscreen and hasattr(player, "set_video_fullscreen"):
                    player.set_video_fullscreen(True)
                return
            if routing == "sports_web" and is_sports_request(channel_query):
                reason = sres.get("reason", "Canal deportivo no disponible en la fuente web.")
                _log(player, f"TV DEPORTIVA: {reason}")
                _say(
                    player,
                    "Tell the user briefly in their own language that you could not open "
                    f"'{channel_query}' from the sports web source ({reason}).",
                )
                return
    except Exception as _se:
        _log(player, f"TV DEPORTIVA: fallback por error ({_se})")

    try:
        mgr = get_iptv_manager()
        res = mgr.resolve_working_stream(channel_query, country=country)
    except Exception as exc:
        if _still_wanted(token):
            _say(
                player,
                "Tell the user briefly in their own language that the live TV "
                f"channel '{channel_query}' failed to load: {exc}",
            )
        return

    if not _still_wanted(token):
        return

    if not res.get("found"):
        _say(
            player,
            "Tell the user briefly in their own language that no live TV "
            f"channel matched '{channel_query}' in iptv-org.",
        )
        return

    ch = res.get("channel") or {}
    ch_name = ch.get("name") or channel_query
    ch_country = ch.get("country") or ""
    st = res.get("stream") or {}
    chk = res.get("check") or {}

    if res.get("online") and st.get("url"):
        title = f"📺 {ch_name}" + (f" ({ch_country})" if ch_country else "") + " [EN VIVO]"
        _log(
            player,
            f"IPTV: Reproduciendo {ch_name} ({ch_country or 'INT'}) — "
            f"{chk.get('latency_ms', 0)} ms · {st.get('quality') or 'auto'}",
        )
        if player is not None and hasattr(player, "show_video"):
            player.show_video(st["url"], title, muted=None)
            if fullscreen and hasattr(player, "set_video_fullscreen"):
                player.set_video_fullscreen(True)
        return

    tested = res.get("tested") or []
    reasons = "; ".join(
        f"{t.get('channel_name', '')}: {t.get('reason', 'offline')}"
        for t in tested[:3]
    )
    _log(player, f"IPTV: Sin stream activo para '{ch_name}' ({reasons})")
    _say(
        player,
        "Tell the user briefly in their own language that you found "
        f"'{ch_name}' in iptv-org, but none of its live streams responded "
        f"({reasons or res.get('reason', 'offline')}).",
    )


def iptv_player(parameters: dict[str, Any] = None, player=None, **_) -> str:
    params = parameters or {}
    action = str(params.get("action") or "play").strip().lower()
    channel = str(params.get("channel") or params.get("query") or "").strip()
    country = str(params.get("country") or "").strip().upper()
    category = str(params.get("category") or "").strip().lower()
    playlist_url = str(params.get("playlist_url") or params.get("source") or "").strip()

    if action in ("stop", "close", "hide"):
        _begin_open()
        if player is not None and hasattr(player, "stop_video"):
            player.stop_video()
        return "Live TV playback stopped."

    if action in ("mute", "unmute"):
        if player is None or not player.video_is_playing():
            return "No live TV or video is playing."
        muted = action == "mute"
        player.set_video_muted(muted)
        return "Live TV muted." if muted else "Live TV sound turned on."

    if action in ("fullscreen", "exit_fullscreen"):
        if player is None or not hasattr(player, "set_video_fullscreen"):
            return "Fullscreen control is not available."
        if not player.video_is_playing():
            return "No live TV or video is playing."
        want_fs = action == "fullscreen"
        player.set_video_fullscreen(want_fs)
        return "Live TV switched to fullscreen." if want_fs else "Live TV exited fullscreen."

    if action == "agenda":
        from core.sports_tv import fetch_sports_agenda
        events = fetch_sports_agenda(force=True)
        if not events:
            return "No hay partidos publicados en este momento en la agenda deportiva de futbolenvivo.top."
        lines = []
        for ev in events[:15]:
            ch_names = ", ".join(str(e.get("name") or "Canal") for e in (ev.get("embeds") or [])[:4])
            lines.append(f"- {ev.get('time', '')[:5]} | {ev.get('title', 'Evento')} [{ch_names or 'Sin canal'}]")
        return "Agenda deportiva de hoy (futbolenvivo.top):\n" + "\n".join(lines)

    mgr = get_iptv_manager()

    if action == "play":
        if not channel:
            return "Please specify which live TV channel to play."
        if player is None or not hasattr(player, "show_video"):
            return "Internal HUD video player is not available."
        fullscreen = bool(params.get("fullscreen", False))
        try:
            option = max(1, int(params.get("option", 1) or 1))
        except (TypeError, ValueError):
            option = 1
        token = _begin_open()
        threading.Thread(
            target=_play_channel_async,
            args=(player, channel, country, token, fullscreen, option),
            daemon=True,
            name="iptv-open",
        ).start()
        return f"status=opening_iptv channel={channel} fullscreen={fullscreen} option={option}"

    if action == "check":
        if not channel:
            return "Specify a channel name or stream URL to check."
        res = mgr.resolve_working_stream(channel, country=country, force_check=True)
        if not res.get("found"):
            return res.get("reason", f"No channel found for '{channel}'.")
        ch = res.get("channel") or {}
        tested = res.get("tested") or []
        lines = [
            f"Channel: {ch.get('name', channel)} ({ch.get('country', '')}) | "
            f"Status: {'ONLINE' if res.get('online') else 'OFFLINE'}"
        ]
        for t in tested[:5]:
            state = "OK" if t.get("online") else "FAIL"
            lines.append(
                f"  - [{state}] {t.get('channel_name', '')} "
                f"({t.get('quality') or 'auto'}, {t.get('latency_ms', 0)} ms): "
                f"{t.get('reason', '')}"
            )
        return "\n".join(lines)

    if action == "search":
        matches = mgr.search_channels(
            query=channel,
            country=country,
            category=category,
            only_with_streams=True,
            limit=12,
        )
        if not matches:
            return f"No live channels found matching query='{channel}' country='{country}' category='{category}'."
        lines = [f"Found {len(matches)} channels with streams:"]
        for m in matches:
            cats = ", ".join(m.get("categories") or []) or "general"
            epg = "EPG" if m.get("has_epg") else "no-EPG"
            lines.append(
                f"  - {m['name']} [{m.get('country') or 'INT'}] "
                f"({cats}, {m['stream_count']} stream(s), {epg})"
            )
        return "\n".join(lines)

    if action == "info":
        if not channel:
            return "Specify a channel name for info."
        info = mgr.get_channel_details(channel)
        if not info.get("found"):
            return info.get("reason", "Channel not found.")
        ch = info["channel"]
        streams = info["streams"]
        guides = info["guides"]
        blocked = info.get("blocked")
        parts = [
            f"Name: {ch.get('name')} ({ch.get('id')})",
            f"Country: {ch.get('country') or 'N/A'} | Network: {ch.get('network') or 'N/A'}",
            f"Categories: {', '.join(ch.get('categories') or []) or 'N/A'}",
            f"Website: {ch.get('website') or 'N/A'}",
            f"Streams available: {len(streams)}",
            f"EPG Guides: {len(guides)} ({', '.join(g.get('site', '') for g in guides[:3]) or 'none'})",
        ]
        if blocked:
            parts.append(f"BLOCKED/DMCA: {blocked.get('reason', 'yes')}")
        return "\n".join(parts)

    if action == "categories":
        cats = mgr.list_categories()
        return "iptv-org categories: " + ", ".join(c.get("id", "") for c in cats[:30])

    if action == "countries":
        countries = mgr.list_countries()
        return "Countries (sample): " + ", ".join(
            f"{c.get('code')} ({c.get('name')})" for c in countries[:35]
        )

    if action == "add_favorite":
        if not channel:
            return "Specify a channel to add to favorites."
        res = mgr.add_favorite(channel)
        if not res.get("ok"):
            return res.get("reason", "Could not add favorite.")
        ch = res["channel"]
        return (
            f"{ch['name']} is already in favorites."
            if res.get("already")
            else f"Added {ch['name']} ({ch.get('country', '')}) to IPTV favorites."
        )

    if action == "remove_favorite":
        if not channel:
            return "Specify a channel to remove from favorites."
        ok = mgr.remove_favorite(channel)
        return f"Removed '{channel}' from favorites." if ok else f"'{channel}' was not in favorites."

    if action == "list_favorites":
        favs = mgr.list_favorites()
        if not favs:
            return "No favorite IPTV channels saved yet."
        return "IPTV Favorites:\n" + "\n".join(
            f"  - {f.get('name')} [{f.get('country', '')}] ({f.get('id')})" for f in favs
        )

    if action == "add_playlist":
        if not playlist_url:
            return "Specify 'playlist_url' (HTTP URL or local .m3u/.m3u8 path)."
        res = mgr.add_custom_playlist(playlist_url, name=channel)
        return f"Added custom M3U playlist '{res['entry']['name']}' and reloaded catalog."

    if action == "refresh":
        stats = mgr.ensure_loaded(force_refresh=True)
        return (
            f"iptv-org catalog refreshed: {stats['channels']} channels, "
            f"{stats['streams']} streams, {stats['categories']} categories, "
            f"{stats['countries']} countries."
        )

    return f"Unknown iptv_player action '{action}'."


TOOL = {
    "name": "iptv_player",
    "description": (
        "Plays LIVE TV channels from iptv-org (and custom M3U/M3U8 playlists) "
        "directly inside VIERNES's internal HUD display where the avatar "
        "normally is, and checks whether TV channels/streams are online or "
        "working. Use whenever the user asks to watch a live TV channel or a "
        "live sports match (e.g., 'Ponga el partido de Costa Rica vs Ecuador', "
        "'Ponme Cartoon Network', 'Pon ESPN en vivo', 'Quiero ver CNN en español'). "
        "When the user asks for a match/game, pass the match query in 'channel' "
        "(e.g. 'Costa Rica vs Ecuador') so it resolves the broadcast channel from "
        "futbolenvivo.top's sports agenda automatically. Use action='agenda' to "
        "list today's sports matches. Plays with sound ON automatically unless the user "
        "enabled mute. When action='play' returns 'status=opening_iptv', say in "
        "one short sentence that you are tuning the channel and verifying a "
        "working stream, then do not call it again."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": (
                    "'play' (default): find, verify working stream with automatic "
                    "fallback, and play in the internal player; 'agenda': list today's "
                    "live sports matches from futbolenvivo.top; 'check': test if "
                    "a channel/URL is online (latency, HLS check); 'search': find "
                    "channels; 'info': channel metadata & EPG guides; "
                    "'categories'; 'countries'; 'add_favorite'; 'remove_favorite'; "
                    "'list_favorites'; 'add_playlist'; 'refresh'; 'stop'; 'mute'; 'unmute'; "
                    "'fullscreen'; 'exit_fullscreen'."
                ),
                "enum": [
                    "play",
                    "agenda",
                    "check",
                    "search",
                    "info",
                    "categories",
                    "countries",
                    "add_favorite",
                    "remove_favorite",
                    "list_favorites",
                    "add_playlist",
                    "refresh",
                    "stop",
                    "mute",
                    "unmute",
                    "fullscreen",
                    "exit_fullscreen",
                ],
            },
            "fullscreen": {
                "type": "BOOLEAN",
                "description": (
                    "Set true when the user asks to open or watch the channel in fullscreen "
                    "(e.g. 'en pantalla completa')."
                ),
            },
            "option": {
                "type": "INTEGER",
                "description": (
                    "Optional 1-based embed option index when a channel has multiple options "
                    "(e.g., 1 for Opción 1, 2 for Opción 2). Defaults to 1."
                ),
            },
            "channel": {
                "type": "STRING",
                "description": (
                    "Channel name or sports match in natural language (e.g. "
                    "'Costa Rica vs Ecuador', 'Cartoon Network', 'ESPN', "
                    "'Azteca 7', 'CNN en Español'), channel ID, or direct "
                    ".m3u8 stream URL."
                ),
            },
            "country": {
                "type": "STRING",
                "description": "Optional 2-letter ISO country code filter (e.g. 'MX', 'CO', 'CR', 'AR', 'ES', 'US').",
            },
            "category": {
                "type": "STRING",
                "description": "Optional iptv-org category filter (e.g. 'animation', 'kids', 'sports', 'news', 'movies', 'music').",
            },
            "playlist_url": {
                "type": "STRING",
                "description": "For action='add_playlist': HTTP URL or local path to a custom .m3u/.m3u8 playlist.",
            },
        },
        "required": ["action"],
    },
    "handler": iptv_player,
}
