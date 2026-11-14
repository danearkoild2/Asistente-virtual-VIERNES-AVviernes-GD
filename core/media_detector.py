"""
Viernes — Advanced Windows Media & Music Intelligence Detector
==============================================================
Monitors and interfaces with Windows Global System Media Transport Controls (GSMTC)
to detect currently playing music, videos, and media streams across Spotify,
YouTube (via Brave, Chrome, Edge, Firefox), VLC, Windows Media Player, and more.

Extracts real-time track metadata, playback status, and high-resolution album artwork.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import re
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from memory.config_manager import get_base_dir

if TYPE_CHECKING:
    from core.visual_engine import VisualCardData

logger = logging.getLogger("Viernes.MediaDetector")

MEDIA_CACHE_DIR = get_base_dir() / "config" / "media_cache"


@dataclass
class MediaTrackInfo:
    title: str
    artist: str = ""
    album: str = ""
    platform: str = "Windows Media"
    platform_key: str = "windows"
    status: str = "PLAYING"
    app_id: str = ""
    thumbnail_path: Optional[str] = None
    has_thumbnail: bool = False
    timestamp: float = field(default_factory=time.time)

    def describe(self) -> str:
        """Generates a natural, spoken Spanish description of what is playing."""
        parts = []
        if self.title:
            parts.append(f"'{self.title}'")
        if self.artist:
            parts.append(f"de {self.artist}")
        if self.album and self.album.lower() != self.title.lower():
            parts.append(f"(álbum '{self.album}')")
        
        plat_str = f"en {self.platform}"
        status_str = "reproduciéndose actualmente" if self.status == "PLAYING" else "en pausa"
        return f"Está {status_str} {' '.join(parts)} {plat_str}."


class MediaDetector:
    """
    Direct interface to Windows 10/11 GSMTC subsystem.
    """

    _instance: Optional[MediaDetector] = None
    _lock = threading.Lock()

    def __init__(self):
        MEDIA_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self._last_track: Optional[MediaTrackInfo] = None
        self._art_cache: Dict[str, Optional[str]] = {}
        self._gsmtc_available: Optional[bool] = None
        self._gsmtc_warned: bool = False

    @classmethod
    def get_instance(cls) -> MediaDetector:
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def get_current_media(self, force_fetch_art: bool = True) -> Optional[MediaTrackInfo]:
        """
        Synchronous wrapper to retrieve the current active media track.
        Safe to call from any worker thread or action handler.
        """
        try:
            return asyncio.run(self._get_current_media_async(force_fetch_art))
        except Exception as e:
            logger.debug(f"Direct asyncio.run error, falling back to new event loop: {e}")
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(self._get_current_media_async(force_fetch_art))
            finally:
                loop.close()

    async def _get_current_media_async(self, force_fetch_art: bool = True) -> Optional[MediaTrackInfo]:
        MediaManager = None
        if self._gsmtc_available is not False:
            try:
                from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as _MM
                MediaManager = _MM
                self._gsmtc_available = True
            except ImportError:
                try:
                    from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as _MM
                    MediaManager = _MM
                    self._gsmtc_available = True
                except ImportError:
                    self._gsmtc_available = False
                    if not self._gsmtc_warned:
                        self._gsmtc_warned = True
                        logger.debug("winsdk/winrt not installed; using native Win32 window media detection.")

        if MediaManager is None:
            return await self._get_win32_window_media_async(force_fetch_art)

        try:
            mgr = await MediaManager.request_async()
            if not mgr:
                return await self._get_win32_window_media_async(force_fetch_art)

            # Prioritize session that is currently PLAYING
            all_sessions = mgr.get_sessions()
            target_session = None

            # 1. Search for a playing session
            for s in all_sessions:
                try:
                    p_info = s.get_playback_info()
                    if p_info and p_info.playback_status.name == "PLAYING":
                        target_session = s
                        break
                except Exception:
                    pass

            # 2. Fall back to current active session if no session is explicitly playing
            if not target_session:
                target_session = mgr.get_current_session()

            # 3. Fall back to first available session
            if not target_session and all_sessions:
                target_session = all_sessions[0]

            if not target_session:
                return await self._get_win32_window_media_async(force_fetch_art)

            app_id = target_session.source_app_user_model_id or ""
            media_props = await target_session.try_get_media_properties_async()
            p_info = target_session.get_playback_info()
            status = p_info.playback_status.name if p_info else "PLAYING"

            if not media_props:
                return await self._get_win32_window_media_async(force_fetch_art)

            raw_title = (media_props.title or "").strip()
            raw_artist = (media_props.artist or "").strip()
            raw_album = (media_props.album_title or "").strip()

            if not raw_title and not raw_artist:
                return await self._get_win32_window_media_async(force_fetch_art)

            # Classify Platform and clean metadata
            platform, platform_key, title, artist = self._classify_platform(app_id, raw_title, raw_artist, raw_album)

            track = MediaTrackInfo(
                title=title or raw_title,
                artist=artist or raw_artist,
                album=raw_album,
                platform=platform,
                platform_key=platform_key,
                status=status,
                app_id=app_id,
            )

            # Extract or retrieve album artwork
            cache_key = f"{track.title}|{track.artist}"
            thumb_path = await self._extract_thumbnail_stream(media_props, track.title, track.artist)
            if not thumb_path and force_fetch_art:
                if cache_key in self._art_cache:
                    cached = self._art_cache[cache_key]
                    thumb_path = Path(cached) if cached else None
                else:
                    thumb_path = await self._fallback_fetch_art(track.title, track.artist, track.platform)
                    self._art_cache[cache_key] = str(thumb_path) if thumb_path else None

            if thumb_path:
                track.thumbnail_path = str(thumb_path)
                track.has_thumbnail = True

            self._last_track = track
            return track

        except Exception as e:
            logger.debug(f"Error querying Windows GSMTC: {e}")
            return await self._get_win32_window_media_async(force_fetch_art)

    async def _get_win32_window_media_async(self, force_fetch_art: bool = True) -> Optional[MediaTrackInfo]:
        """
        Zero-dependency native Windows Win32 media detector via EnumWindows + psutil.
        Detects active Spotify and YouTube playback without requiring winsdk.
        """
        if os.name != "nt":
            return None
        try:
            import ctypes
            from ctypes import wintypes
            import psutil

            user32 = ctypes.windll.user32
            WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

            candidates: List[Tuple[str, str]] = []  # (proc_name, window_title)
            pid_cache: Dict[int, str] = {}

            def _enum_cb(hwnd, _lparam):
                if not user32.IsWindowVisible(hwnd):
                    return True
                length = user32.GetWindowTextLengthW(hwnd)
                if length <= 0:
                    return True
                buf = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buf, length + 1)
                w_title = buf.value.strip()
                if not w_title:
                    return True
                pid = wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                p_val = int(pid.value)
                if p_val not in pid_cache:
                    try:
                        pid_cache[p_val] = psutil.Process(p_val).name().lower()
                    except Exception:
                        pid_cache[p_val] = ""
                pname = pid_cache[p_val]
                if pname in ("spotify.exe", "brave.exe", "chrome.exe", "msedge.exe", "firefox.exe", "opera.exe"):
                    candidates.append((pname, w_title))
                return True

            user32.EnumWindows(WNDENUMPROC(_enum_cb), 0)

            track: Optional[MediaTrackInfo] = None

            # 1. Check Spotify first
            for pname, w_title in candidates:
                if pname == "spotify.exe":
                    low_t = w_title.lower()
                    if low_t in ("spotify", "spotify free", "spotify premium", "spotify miniplayer") or low_t.startswith("spotify "):
                        continue
                    if " - " in w_title:
                        artist_part, title_part = w_title.split(" - ", 1)
                        track = MediaTrackInfo(
                            title=title_part.strip(),
                            artist=artist_part.strip(),
                            platform="Spotify",
                            platform_key="spotify",
                            status="PLAYING",
                            app_id="Spotify.exe",
                        )
                        break

            # 2. Check YouTube / YouTube Music across browsers
            if track is None:
                browser_suffixes = (
                    (" - Brave", "YouTube (Brave)"),
                    (" - Google Chrome", "YouTube (Chrome)"),
                    (" - Microsoft​ Edge", "YouTube (Edge)"),
                    (" - Microsoft Edge", "YouTube (Edge)"),
                    (" — Mozilla Firefox", "YouTube (Firefox)"),
                    (" - Mozilla Firefox", "YouTube (Firefox)"),
                    (" - Opera", "YouTube (Opera)"),
                )
                for pname, w_title in candidates:
                    if pname == "spotify.exe":
                        continue
                    clean_w = w_title
                    plat_label = "YouTube"
                    for suf, plabel in browser_suffixes:
                        if clean_w.endswith(suf):
                            clean_w = clean_w[: -len(suf)].strip()
                            plat_label = plabel
                            break
                    yt_Match = False
                    for yt_suf in (" - YouTube Music", " - YouTube", " • YouTube"):
                        if clean_w.endswith(yt_suf):
                            clean_w = clean_w[: -len(yt_suf)].strip()
                            yt_Match = True
                            break
                    if not yt_Match:
                        continue
                    clean_w = re.sub(r"^\(\d+\)\s*", "", clean_w).strip()
                    if not clean_w or clean_w.lower() in ("youtube", "youtube music", "home", "inicio"):
                        continue
                    if " - " in clean_w:
                        art_p, tit_p = clean_w.split(" - ", 1)
                        t_title = tit_p.strip()
                        t_artist = art_p.strip()
                    else:
                        t_title = clean_w
                        t_artist = "YouTube"
                    track = MediaTrackInfo(
                        title=t_title,
                        artist=t_artist,
                        platform=plat_label,
                        platform_key="youtube",
                        status="PLAYING",
                        app_id=pname,
                    )
                    break

            if track is None:
                return None

            cache_key = f"{track.title}|{track.artist}"
            if force_fetch_art:
                if cache_key in self._art_cache:
                    cached = self._art_cache[cache_key]
                    if cached:
                        track.thumbnail_path = cached
                        track.has_thumbnail = True
                else:
                    thumb_path = await self._fallback_fetch_art(track.title, track.artist, track.platform)
                    self._art_cache[cache_key] = str(thumb_path) if thumb_path else None
                    if thumb_path:
                        track.thumbnail_path = str(thumb_path)
                        track.has_thumbnail = True

            self._last_track = track
            return track
        except Exception as e:
            logger.debug(f"Win32 media detection fallback error: {e}")
            return None

    def _classify_platform(self, app_id: str, title: str, artist: str, album: str) -> Tuple[str, str, str, str]:
        """
        Determines the exact service / application playing the media.
        Identifies Spotify, YouTube (via any browser), Brave, VLC, WMP, etc.
        """
        app_lower = (app_id or "").lower()
        title_lower = (title or "").lower()
        artist_lower = (artist or "").lower()
        album_lower = (album or "").lower()

        # Clean title & artist if browser/YouTube added artifacts
        clean_title = title
        clean_artist = artist

        # 1. Spotify
        if "spotify" in app_lower:
            return ("Spotify", "spotify", clean_title, clean_artist)

        # 2. YouTube detection across browsers
        is_youtube = (
            "youtube" in title_lower or
            "youtube" in artist_lower or
            "youtube" in album_lower or
            title.endswith("- YouTube") or
            title.endswith("• YouTube") or
            "music.youtube.com" in title_lower
        )

        if title.endswith("- YouTube"):
            clean_title = title[:-9].strip()
        elif title.endswith("• YouTube"):
            clean_title = title[:-9].strip()

        # Check browser container
        if "brave" in app_lower:
            if is_youtube:
                return ("YouTube (Brave)", "youtube", clean_title, clean_artist or "YouTube Music")
            return ("Brave Browser", "brave", clean_title, clean_artist)

        if "chrome" in app_lower:
            if is_youtube:
                return ("YouTube (Chrome)", "youtube", clean_title, clean_artist or "YouTube Music")
            return ("Google Chrome", "chrome", clean_title, clean_artist)

        if "msedge" in app_lower or "edge" in app_lower:
            if is_youtube:
                return ("YouTube (Edge)", "youtube", clean_title, clean_artist or "YouTube Music")
            return ("Microsoft Edge", "edge", clean_title, clean_artist)

        if "firefox" in app_lower:
            if is_youtube:
                return ("YouTube (Firefox)", "youtube", clean_title, clean_artist or "YouTube Music")
            return ("Mozilla Firefox", "firefox", clean_title, clean_artist)

        if is_youtube:
            return ("YouTube", "youtube", clean_title, clean_artist or "YouTube")

        # 3. VLC Media Player
        if "vlc" in app_lower:
            return ("VLC Media Player", "vlc", clean_title, clean_artist)

        # 4. Windows Media Player / Groove
        if "wmplayer" in app_lower or "zunemusic" in app_lower or "media.player" in app_lower or "zune" in app_lower:
            return ("Windows Media Player", "windows_media", clean_title, clean_artist)

        # 5. Apple Music / iTunes
        if "itunes" in app_lower or "applemusic" in app_lower:
            return ("Apple Music", "apple_music", clean_title, clean_artist)

        # 6. Generic Windows App
        clean_app = app_id.split("!")[-1].replace(".exe", "").title() if app_id else "Windows Media"
        return (clean_app, "windows", clean_title, clean_artist)

    async def _extract_thumbnail_stream(self, media_props, title: str, artist: str) -> Optional[Path]:
        """Extracts the album artwork bytes directly from Windows GSMTC stream."""
        if not getattr(media_props, "thumbnail", None):
            return None

        try:
            from winsdk.windows.storage.streams import DataReader
            stream = await media_props.thumbnail.open_read_async()
            if not stream or stream.size == 0:
                return None

            reader = DataReader(stream)
            await reader.load_async(stream.size)
            buffer = reader.read_buffer(stream.size)
            raw_bytes = bytes(buffer)

            if len(raw_bytes) < 200:
                return None

            hash_key = hashlib.md5(f"{title}_{artist}_{len(raw_bytes)}".encode("utf-8")).hexdigest()[:10]
            out_file = MEDIA_CACHE_DIR / f"art_{hash_key}.png"
            out_file.write_bytes(raw_bytes)
            return out_file

        except Exception as e:
            logger.debug(f"Failed extracting GSMTC thumbnail stream: {e}")
            return None

    async def _fallback_fetch_art(self, title: str, artist: str, platform: str) -> Optional[Path]:
        """Fall back to image search for the album artwork if not provided by GSMTC."""
        try:
            from core.visual_engine import VisualEngine
            ve = VisualEngine.get_instance()
            search_query = f"{artist} {title} album cover" if artist else f"{title} cover artwork"
            items = ve._fetch_ddg_images(search_query, max_results=2)
            if not items:
                items = ve._fetch_ddg_images(f"{title} portada", max_results=1)

            if items:
                img_info = ve._download_and_cache_image(
                    topic=f"media_{title[:20]}",
                    index=0,
                    main_url=items[0].link,
                    thumb_url=items[0].thumbnail or items[0].link,
                    title=title,
                    source=platform
                )
                if img_info and img_info.get("local_path"):
                    return Path(img_info["local_path"])
        except Exception as e:
            logger.debug(f"Fallback art fetch error: {e}")
        return None

    def build_visual_card(self, track: MediaTrackInfo) -> VisualCardData:
        """
        Creates an elegant, high-impact VisualCardData to show in EdithVisualPanel.
        Includes platform-tailored badge, artwork, and full track metadata.
        """
        # Category Badge with iconic emoji
        if track.platform_key == "spotify":
            category = "SPOTIFY 🎵"
        elif track.platform_key == "youtube":
            category = "YOUTUBE 🔴"
        elif track.platform_key == "brave":
            category = "BRAVE BROWSER 🦁"
        elif track.platform_key == "vlc":
            category = "VLC MEDIA PLAYER 🎬"
        elif track.platform_key == "windows_media":
            category = "WINDOWS MEDIA PLAYER 📻"
        else:
            category = f"{track.platform.upper()} 🎧"

        # Summary text
        summary_lines = []
        if track.artist:
            summary_lines.append(f"Artista: {track.artist}")
        if track.album and track.album.lower() != track.title.lower():
            summary_lines.append(f"Álbum: {track.album}")
        status_esp = "Reproduciendo en alta fidelidad" if track.status == "PLAYING" else "En pausa"
        summary_lines.append(f"Estado: {status_esp}")
        summary_lines.append(f"Aplicación: {track.platform} (Windows)")
        summary = "\n".join(summary_lines)

        # Interesting fact pill
        fact = f"Pista activa detectada en {track.platform}. Sonido transmitido por el subsistema multimedia de Windows."

        # Images structure
        images = []
        if track.thumbnail_path and Path(track.thumbnail_path).exists():
            images.append({
                "local_path": track.thumbnail_path,
                "local_thumb": track.thumbnail_path,
                "url": "",
                "thumb": "",
                "title": f"{track.title} - {track.artist}",
                "source": track.platform
            })

        from core.visual_engine import VisualCardData
        return VisualCardData(
            topic=track.title,
            category=category,
            summary=summary,
            interesting_fact=fact,
            images=images,
            source=f"{track.platform} • Windows GSMTC",
            query=track.title
        )
