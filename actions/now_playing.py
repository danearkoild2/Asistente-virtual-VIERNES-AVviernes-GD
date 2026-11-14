"""
Viernes — Action: now_playing
=============================
Detects what song, video, or audio is currently playing on Windows across
Spotify, YouTube (via Brave, Chrome, Edge, Firefox), VLC, Windows Media Player,
and desktop media players.

Extracts real-time metadata (title, artist, album, platform), retrieves the album
artwork, triggers the visual card next to Edith, and returns a natural description
for Viernes to speak aloud.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from core.media_detector import MediaDetector

logger = logging.getLogger("Viernes.Actions.NowPlaying")


def now_playing(
    parameters: Optional[Dict[str, Any]] = None,
    player=None,
    speak=None,
    **kwargs,
) -> str:
    """
    Identifies the active media stream on the computer, displays the visual card
    with album art, and returns the track details.
    """
    logger.info("Executing now_playing check...")
    detector = MediaDetector.get_instance()
    track = detector.get_current_media(force_fetch_art=True)

    if not track:
        msg = (
            "En este momento no se detecta ninguna reproducción de música o video activa "
            "en el sistema (Spotify, YouTube, VLC, navegador o reproductores están pausados o cerrados)."
        )
        if player and hasattr(player, "write_log"):
            player.write_log("🎵 [Audio] No hay reproducción activa en el sistema.")
        return msg

    # Display visual card beside Edith Live2D
    card = detector.build_visual_card(track)
    if player and hasattr(player, "show_visual_card"):
        try:
            player.show_visual_card(card)
        except Exception as e:
            logger.warning(f"Error displaying media visual card: {e}")

    if player and hasattr(player, "write_log"):
        player.write_log(f"🎵 [Música en vivo] {track.title} — {track.artist} ({track.platform})")

    # Build clear, helpful text for Gemini's voice response
    details = []
    if track.artist:
        details.append(f"de {track.artist}")
    if track.album and track.album.lower() != track.title.lower():
        details.append(f"del álbum '{track.album}'")

    status_str = "reproduciéndose actualmente" if track.status == "PLAYING" else "en pausa"
    desc_str = f"'{track.title}' " + " ".join(details) if details else f"'{track.title}'"

    return (
        f"Actualmente está {status_str} {desc_str} en {track.platform}. "
        f"He desplegado la tarjeta con su información y portada oficial en pantalla."
    )


TOOL = {
    "name": "now_playing",
    "description": (
        "Detects and identifies what song, video, or audio is currently playing on the computer "
        "across Spotify, YouTube (in Brave, Chrome, Edge, Firefox), VLC, Windows Media Player, and other desktop apps. "
        "MANDATORY: Call this tool whenever the user asks '¿qué está sonando?', '¿qué canción es?', "
        "'¿qué música está puesta?', '¿qué se está reproduciendo?', '¿qué canción suena?', or asks about currently playing music/media."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {},
        "required": [],
    },
    "handler": now_playing,
}
