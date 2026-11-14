"""
Native iptv-org integration for VIERNES.

Provides:
- Official iptv-org API catalog sync & disk caching (channels, streams, guides,
  categories, countries, languages, blocklist).
- Custom M3U/M3U8 playlist parsing & persistence.
- Intelligent natural-language channel matching with alias expansion,
  Latin-America/Spanish prioritization, and NSFW/blocklist filtering.
- Real-time HTTP/HLS stream health verification (status, latency, #EXTM3U
  manifest validation, variant probe, geo-block/HTML detection) with
  multi-stream automatic fallback and health caching.
- Favorites management and EPG/channel metadata inspection.
"""
from __future__ import annotations

import json
import re
import threading
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
CACHE_DIR = CONFIG_DIR / "iptv_cache"
FAVORITES_FILE = CONFIG_DIR / "iptv_favorites.json"
CUSTOM_PLAYLISTS_FILE = CONFIG_DIR / "iptv_custom_playlists.json"
HEALTH_CACHE_FILE = CACHE_DIR / "health_cache.json"

API_BASE = "https://iptv-org.github.io/api"
API_ENDPOINTS = {
    "channels": f"{API_BASE}/channels.json",
    "streams": f"{API_BASE}/streams.json",
    "guides": f"{API_BASE}/guides.json",
    "categories": f"{API_BASE}/categories.json",
    "countries": f"{API_BASE}/countries.json",
    "languages": f"{API_BASE}/languages.json",
    "blocklist": f"{API_BASE}/blocklist.json",
}

CATALOG_TTL_SECONDS = 24 * 3600
HEALTH_OK_TTL_SECONDS = 30 * 60
HEALTH_FAIL_TTL_SECONDS = 10 * 60
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

PREFERRED_COUNTRIES = ("MX", "CO", "CR", "AR", "ES", "CL", "PE", "VE", "US")
COMMON_ALIASES = {
    "cn": "cartoon network",
    "cartoon": "cartoon network",
    "natgeo": "national geographic",
    "nat geo": "national geographic",
    "dk": "discovery kids",
    "disc kids": "discovery kids",
    "nick": "nickelodeon",
    "disney": "disney channel",
    "cnn esp": "cnn en espanol",
    "cnn espanol": "cnn en espanol",
    "tnt": "tnt",
    "hbo": "hbo",
    "fx": "fx",
    "fox": "fox",
    "espn": "espn",
    "tyc": "tyc sports",
    "tv azteca": "azteca",
    "azteca 7": "azteca 7",
    "las estrellas": "las estrellas",
    "canal 5": "canal 5",
    "tve": "tve",
    "rtve": "rtve",
    "dw": "dw",
    "nhk": "nhk",
}

_QUALITY_RANK = {
    "2160p": 6,
    "1080p": 5,
    "720p": 4,
    "576p": 3,
    "480p": 2,
    "360p": 1,
}


def _normalize(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _parse_quality_score(quality: str) -> int:
    q = (quality or "").lower().strip()
    if q in _QUALITY_RANK:
        return _QUALITY_RANK[q]
    m = re.search(r"(\d{3,4})p", q)
    if m:
        val = int(m.group(1))
        if val >= 2160:
            return 6
        if val >= 1080:
            return 5
        if val >= 720:
            return 4
        if val >= 480:
            return 2
        return 1
    return 0


@dataclass
class StreamCheckResult:
    url: str
    online: bool
    status_code: int = 0
    latency_ms: int = 0
    content_type: str = ""
    is_hls: bool = False
    is_master_playlist: bool = False
    variant_count: int = 0
    requires_headers: bool = False
    reason: str = ""
    checked_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "online": self.online,
            "status_code": self.status_code,
            "latency_ms": self.latency_ms,
            "content_type": self.content_type,
            "is_hls": self.is_hls,
            "is_master_playlist": self.is_master_playlist,
            "variant_count": self.variant_count,
            "requires_headers": self.requires_headers,
            "reason": self.reason,
            "checked_at": self.checked_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StreamCheckResult:
        return cls(
            url=str(data.get("url", "")),
            online=bool(data.get("online", False)),
            status_code=int(data.get("status_code", 0)),
            latency_ms=int(data.get("latency_ms", 0)),
            content_type=str(data.get("content_type", "")),
            is_hls=bool(data.get("is_hls", False)),
            is_master_playlist=bool(data.get("is_master_playlist", False)),
            variant_count=int(data.get("variant_count", 0)),
            requires_headers=bool(data.get("requires_headers", False)),
            reason=str(data.get("reason", "")),
            checked_at=float(data.get("checked_at", 0.0)),
        )


def parse_m3u_content(text: str, source_name: str = "custom") -> list[dict[str, Any]]:
    """Parse an #EXTM3U playlist into channel/stream records."""
    entries: list[dict[str, Any]] = []
    current_meta: dict[str, Any] = {}
    current_headers: dict[str, str] = {}

    for raw_line in (text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#EXTINF:"):
            current_meta = {"source": source_name}
            current_headers = {}
            attrs = dict(re.findall(r'([a-zA-Z0-9_-]+)="([^"]*)"', line))
            comma_idx = line.rfind(",")
            title = line[comma_idx + 1:].strip() if comma_idx != -1 else ""
            current_meta["name"] = title or attrs.get("tvg-name") or "Canal sin nombre"
            current_meta["id"] = attrs.get("tvg-id") or f"custom:{_normalize(current_meta['name']).replace(' ', '_')}"
            current_meta["country"] = (attrs.get("tvg-country") or "").upper()
            current_meta["logo"] = attrs.get("tvg-logo") or ""
            group = attrs.get("group-title") or ""
            current_meta["categories"] = [c.strip().lower() for c in group.split(";") if c.strip()] if group else []
            current_meta["language"] = (attrs.get("tvg-language") or "").lower()
        elif line.startswith("#EXTVLCOPT:"):
            opt = line[len("#EXTVLCOPT:"):].strip()
            if opt.lower().startswith("http-user-agent="):
                current_headers["user_agent"] = opt.split("=", 1)[1].strip()
            elif opt.lower().startswith("http-referrer="):
                current_headers["referrer"] = opt.split("=", 1)[1].strip()
        elif not line.startswith("#") and (line.startswith("http://") or line.startswith("https://")):
            if not current_meta:
                name = urlparse(line).path.rsplit("/", 1)[-1] or "Stream"
                current_meta = {
                    "id": f"custom:{_normalize(name).replace(' ', '_')}",
                    "name": name,
                    "country": "",
                    "categories": [],
                    "source": source_name,
                }
            entries.append({
                "channel": current_meta,
                "stream": {
                    "channel": current_meta["id"],
                    "url": line,
                    "title": current_meta.get("name", ""),
                    "quality": "",
                    "user_agent": current_headers.get("user_agent", ""),
                    "referrer": current_headers.get("referrer", ""),
                    "source": source_name,
                },
            })
            current_meta = {}
            current_headers = {}
    return entries


def check_stream_health(
    url: str,
    user_agent: str = "",
    referrer: str = "",
    timeout: float = 6.0,
) -> StreamCheckResult:
    """Verify whether an IPTV stream URL actually responds with playable media/HLS."""
    t0 = time.perf_counter()
    requires_headers = bool(user_agent or referrer)
    headers = {"User-Agent": user_agent or DEFAULT_UA}
    if referrer:
        headers["Referer"] = referrer

    try:
        req = Request(url, headers=headers, method="GET")
        with urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()
            raw = resp.read(32768)
            latency_ms = int((time.perf_counter() - t0) * 1000)

        if status not in (200, 206):
            return StreamCheckResult(
                url=url, online=False, status_code=status, latency_ms=latency_ms,
                content_type=ctype, requires_headers=requires_headers,
                reason=f"HTTP {status}",
            )

        text_head = raw.decode("utf-8", errors="ignore")
        low_head = text_head.lstrip().lower()

        if low_head.startswith("<!doctype html") or low_head.startswith("<html"):
            return StreamCheckResult(
                url=url, online=False, status_code=status, latency_ms=latency_ms,
                content_type=ctype, requires_headers=requires_headers,
                reason="El servidor devolvió una página HTML en lugar de video (posible bloqueo o error)",
            )

        is_hls = (
            "#extm3u" in low_head[:256]
            or ".m3u8" in url.lower()
            or "mpegurl" in ctype
        )
        if is_hls:
            if "#extm3u" not in low_head:
                return StreamCheckResult(
                    url=url, online=False, status_code=status, latency_ms=latency_ms,
                    content_type=ctype, is_hls=True, requires_headers=requires_headers,
                    reason="Playlist HLS inválida (sin cabecera #EXTM3U)",
                )
            lines = [ln.strip() for ln in text_head.splitlines() if ln.strip()]
            is_master = any(ln.startswith("#EXT-X-STREAM-INF") for ln in lines)
            media_lines = [ln for ln in lines if not ln.startswith("#")]
            if not media_lines:
                return StreamCheckResult(
                    url=url, online=False, status_code=status, latency_ms=latency_ms,
                    content_type=ctype, is_hls=True, is_master_playlist=is_master,
                    requires_headers=requires_headers,
                    reason="Playlist HLS vacía (sin segmentos ni variantes)",
                )
            if is_master:
                first_variant = urljoin(url, media_lines[0])
                try:
                    vreq = Request(first_variant, headers=headers, method="GET")
                    with urlopen(vreq, timeout=max(3.0, timeout - 1.5)) as vresp:
                        vstatus = getattr(vresp, "status", 200)
                        vraw = vresp.read(8192).decode("utf-8", errors="ignore")
                    if vstatus not in (200, 206) or "#extm3u" not in vraw.lower():
                        return StreamCheckResult(
                            url=url, online=False, status_code=vstatus, latency_ms=latency_ms,
                            content_type=ctype, is_hls=True, is_master_playlist=True,
                            variant_count=len(media_lines), requires_headers=requires_headers,
                            reason=f"Variante HLS inaccesible (HTTP {vstatus})",
                        )
                except Exception as ve:
                    return StreamCheckResult(
                        url=url, online=False, status_code=status, latency_ms=latency_ms,
                        content_type=ctype, is_hls=True, is_master_playlist=True,
                        variant_count=len(media_lines), requires_headers=requires_headers,
                        reason=f"Variante HLS falló: {ve}",
                    )

            return StreamCheckResult(
                url=url, online=True, status_code=status, latency_ms=latency_ms,
                content_type=ctype or "application/vnd.apple.mpegurl",
                is_hls=True, is_master_playlist=is_master,
                variant_count=len(media_lines), requires_headers=requires_headers,
                reason="OK (HLS válido)",
            )

        if len(raw) == 0:
            return StreamCheckResult(
                url=url, online=False, status_code=status, latency_ms=latency_ms,
                content_type=ctype, requires_headers=requires_headers,
                reason="Stream vacío (0 bytes)",
            )

        return StreamCheckResult(
            url=url, online=True, status_code=status, latency_ms=latency_ms,
            content_type=ctype or "video/mp2t", is_hls=False,
            requires_headers=requires_headers, reason="OK (stream directo)",
        )
    except Exception as exc:
        latency_ms = int((time.perf_counter() - t0) * 1000)
        msg = str(exc)
        if "403" in msg:
            reason = "HTTP 403 Forbidden (bloqueo geográfico o de token)"
        elif "404" in msg:
            reason = "HTTP 404 Not Found (canal caído)"
        elif "timed out" in msg.lower():
            reason = "Tiempo de espera agotado (timeout)"
        else:
            reason = msg[:120]
        return StreamCheckResult(
            url=url, online=False, status_code=0, latency_ms=latency_ms,
            requires_headers=requires_headers, reason=reason,
        )


class IptvOrgManager:
    """Singleton manager for iptv-org catalogs, custom M3U playlists, health checks & favorites."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._loaded = False
        self._channels: list[dict[str, Any]] = []
        self._channels_by_id: dict[str, dict[str, Any]] = {}
        self._streams_by_channel: dict[str, list[dict[str, Any]]] = {}
        self._guides_by_channel: dict[str, list[dict[str, Any]]] = {}
        self._categories: dict[str, dict[str, Any]] = {}
        self._countries: dict[str, dict[str, Any]] = {}
        self._languages: dict[str, dict[str, Any]] = {}
        self._blocklist: dict[str, dict[str, Any]] = {}
        self._health_cache: dict[str, StreamCheckResult] = {}
        self._load_health_cache()

    # ── Disk cache helpers ───────────────────────────────────────────────────
    def _fetch_json(self, key: str, force_refresh: bool = False) -> list[dict[str, Any]]:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_path = CACHE_DIR / f"{key}.json"
        if not force_refresh and cache_path.exists():
            age = time.time() - cache_path.stat().st_mtime
            if age < CATALOG_TTL_SECONDS:
                try:
                    return json.loads(cache_path.read_text(encoding="utf-8"))
                except Exception:
                    pass

        url = API_ENDPOINTS[key]
        try:
            req = Request(url, headers={"User-Agent": DEFAULT_UA})
            with urlopen(req, timeout=45.0) as resp:
                raw = resp.read().decode("utf-8")
            data = json.loads(raw)
            if isinstance(data, list):
                cache_path.write_text(raw, encoding="utf-8")
                return data
        except Exception:
            if cache_path.exists():
                try:
                    return json.loads(cache_path.read_text(encoding="utf-8"))
                except Exception:
                    pass
        return []

    def ensure_loaded(self, force_refresh: bool = False) -> dict[str, int]:
        with self._lock:
            if self._loaded and not force_refresh and self._channels:
                return {
                    "channels": len(self._channels),
                    "streams": sum(len(v) for v in self._streams_by_channel.values()),
                    "categories": len(self._categories),
                    "countries": len(self._countries),
                }

            fetched: dict[str, list[dict[str, Any]]] = {}
            with ThreadPoolExecutor(max_workers=4) as pool:
                futs = {
                    pool.submit(self._fetch_json, key, force_refresh): key
                    for key in API_ENDPOINTS
                }
                for fut in as_completed(futs):
                    key = futs[fut]
                    try:
                        fetched[key] = fut.result()
                    except Exception:
                        fetched[key] = []

            channels = fetched.get("channels", [])
            streams = fetched.get("streams", [])
            guides = fetched.get("guides", [])
            categories = fetched.get("categories", [])
            countries = fetched.get("countries", [])
            languages = fetched.get("languages", [])
            blocklist = fetched.get("blocklist", [])

            self._channels = []
            self._channels_by_id = {}
            for ch in channels:
                cid = ch.get("id")
                if not cid:
                    continue
                self._channels.append(ch)
                self._channels_by_id[cid] = ch

            self._streams_by_channel = {}
            for st in streams:
                cid = st.get("channel")
                if cid and st.get("url"):
                    self._streams_by_channel.setdefault(cid, []).append(st)

            self._guides_by_channel = {}
            for g in guides:
                cid = g.get("channel")
                if cid:
                    self._guides_by_channel.setdefault(cid, []).append(g)

            self._categories = {c["id"]: c for c in categories if c.get("id")}
            self._countries = {c["code"].upper(): c for c in countries if c.get("code")}
            self._languages = {l["code"].lower(): l for l in languages if l.get("code")}
            self._blocklist = {b["channel"]: b for b in blocklist if b.get("channel")}

            self._merge_custom_playlists_locked()
            self._loaded = True
            return {
                "channels": len(self._channels),
                "streams": sum(len(v) for v in self._streams_by_channel.values()),
                "categories": len(self._categories),
                "countries": len(self._countries),
            }

    def _merge_custom_playlists_locked(self) -> None:
        sources = self.list_custom_playlists()
        for src in sources:
            target = src.get("source", "")
            if not target:
                continue
            try:
                if target.startswith(("http://", "https://")):
                    req = Request(target, headers={"User-Agent": DEFAULT_UA})
                    with urlopen(req, timeout=12.0) as resp:
                        txt = resp.read().decode("utf-8", errors="ignore")
                else:
                    p = Path(target)
                    if not p.exists():
                        continue
                    txt = p.read_text(encoding="utf-8", errors="ignore")
                for item in parse_m3u_content(txt, source_name=src.get("name", target)):
                    ch = item["channel"]
                    st = item["stream"]
                    cid = ch["id"]
                    if cid not in self._channels_by_id:
                        self._channels.append(ch)
                        self._channels_by_id[cid] = ch
                    self._streams_by_channel.setdefault(cid, []).append(st)
            except Exception:
                continue

    # ── Health cache ─────────────────────────────────────────────────────────
    def _load_health_cache(self) -> None:
        try:
            if HEALTH_CACHE_FILE.exists():
                raw = json.loads(HEALTH_CACHE_FILE.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    self._health_cache = {
                        k: StreamCheckResult.from_dict(v)
                        for k, v in raw.items()
                        if isinstance(v, dict)
                    }
        except Exception:
            self._health_cache = {}

    def _save_health_cache(self) -> None:
        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            now = time.time()
            trimmed = {
                k: v.to_dict()
                for k, v in self._health_cache.items()
                if (now - v.checked_at) < 3600
            }
            HEALTH_CACHE_FILE.write_text(json.dumps(trimmed, indent=2), encoding="utf-8")
        except Exception:
            pass

    def check_url(
        self,
        url: str,
        user_agent: str = "",
        referrer: str = "",
        force: bool = False,
    ) -> StreamCheckResult:
        now = time.time()
        if not force and url in self._health_cache:
            cached = self._health_cache[url]
            ttl = HEALTH_OK_TTL_SECONDS if cached.online else HEALTH_FAIL_TTL_SECONDS
            if (now - cached.checked_at) < ttl:
                return cached
        res = check_stream_health(url, user_agent=user_agent, referrer=referrer)
        with self._lock:
            self._health_cache[url] = res
            self._save_health_cache()
        return res

    # ── Search & smart resolution ────────────────────────────────────────────
    def search_channels(
        self,
        query: str = "",
        country: str = "",
        category: str = "",
        only_with_streams: bool = True,
        include_nsfw: bool = False,
        limit: int = 12,
    ) -> list[dict[str, Any]]:
        self.ensure_loaded()
        q_norm = _normalize(query)
        q_alias = COMMON_ALIASES.get(q_norm, q_norm)
        q_tokens = set(q_alias.split()) if q_alias else set()
        country_u = (country or "").strip().upper()
        cat_l = (category or "").strip().lower()

        scored: list[tuple[float, dict[str, Any]]] = []
        for ch in self._channels:
            cid = ch["id"]
            if not include_nsfw and ch.get("is_nsfw"):
                continue
            if cid in self._blocklist:
                continue
            streams = self._streams_by_channel.get(cid, [])
            if only_with_streams and not streams:
                continue
            if country_u and (ch.get("country") or "").upper() != country_u:
                continue
            ch_cats = [c.lower() for c in (ch.get("categories") or [])]
            if cat_l and cat_l not in ch_cats:
                continue

            name_norm = _normalize(ch.get("name", ""))
            alt_norms = [_normalize(a) for a in (ch.get("alt_names") or []) if a]
            all_names = [name_norm] + alt_norms

            score = 0.0
            if q_alias:
                if q_alias in all_names:
                    score += 120.0
                elif any(n.startswith(q_alias) for n in all_names):
                    score += 90.0
                elif any(q_alias in n for n in all_names):
                    score += 70.0
                else:
                    best_sim = max(
                        (SequenceMatcher(None, q_alias, n).ratio() for n in all_names if n),
                        default=0.0,
                    )
                    name_tokens = set(" ".join(all_names).split())
                    overlap = len(q_tokens & name_tokens) / max(1, len(q_tokens))
                    if overlap >= 0.5 or best_sim >= 0.62:
                        score += overlap * 45.0 + best_sim * 40.0
                    else:
                        continue
            else:
                score += 20.0

            if streams:
                score += 15.0 + min(len(streams), 5) * 1.5
            if ch.get("closed"):
                score -= 25.0
            ch_country = (ch.get("country") or "").upper()
            if not country_u and ch_country in PREFERRED_COUNTRIES:
                score += 12.0 - PREFERRED_COUNTRIES.index(ch_country) * 0.8
            if "espanol" in name_norm or "latino" in name_norm or "latam" in name_norm:
                score += 10.0

            scored.append((score, ch))

        scored.sort(key=lambda item: item[0], reverse=True)
        results: list[dict[str, Any]] = []
        for sc, ch in scored[:limit]:
            cid = ch["id"]
            results.append({
                "id": cid,
                "name": ch.get("name", cid),
                "country": ch.get("country", ""),
                "categories": ch.get("categories", []),
                "stream_count": len(self._streams_by_channel.get(cid, [])),
                "has_epg": cid in self._guides_by_channel,
                "website": ch.get("website", ""),
                "network": ch.get("network", ""),
                "score": round(sc, 1),
            })
        return results

    def _rank_streams(self, streams: list[dict[str, Any]]) -> list[dict[str, Any]]:
        def key_fn(st: dict[str, Any]) -> tuple[int, int, int]:
            no_custom_headers = 1 if not (st.get("user_agent") or st.get("referrer")) else 0
            q_score = _parse_quality_score(st.get("quality", ""))
            is_hls = 1 if ".m3u8" in (st.get("url") or "").lower() else 0
            return (no_custom_headers, q_score, is_hls)

        return sorted(streams, key=key_fn, reverse=True)

    def resolve_working_stream(
        self,
        query: str,
        country: str = "",
        force_check: bool = False,
        max_candidates: int = 8,
    ) -> dict[str, Any]:
        """Find the best matching channel and verify a working stream with automatic fallback."""
        self.ensure_loaded()

        # Direct URL playback/check support
        if query.strip().startswith(("http://", "https://")):
            chk = self.check_url(query.strip(), force=force_check)
            return {
                "found": True,
                "online": chk.online,
                "channel": {"id": "direct", "name": query.strip().rsplit("/", 1)[-1][:40], "country": ""},
                "stream": {"url": query.strip(), "quality": "", "user_agent": "", "referrer": ""},
                "check": chk.to_dict(),
                "tested": [chk.to_dict()],
            }

        matches = self.search_channels(query=query, country=country, only_with_streams=True, limit=6)
        if not matches:
            return {"found": False, "online": False, "reason": f"No se encontró ningún canal con streams para '{query}'."}

        candidates: list[tuple[dict[str, Any], dict[str, Any]]] = []
        for ch_meta in matches:
            cid = ch_meta["id"]
            for st in self._rank_streams(self._streams_by_channel.get(cid, []))[:3]:
                candidates.append((ch_meta, st))
                if len(candidates) >= max_candidates:
                    break
            if len(candidates) >= max_candidates:
                break

        tested_reports: list[dict[str, Any]] = []
        checks_by_url: dict[str, StreamCheckResult] = {}

        with ThreadPoolExecutor(max_workers=4) as pool:
            futs = {
                pool.submit(
                    self.check_url,
                    st["url"],
                    st.get("user_agent", ""),
                    st.get("referrer", ""),
                    force_check,
                ): (ch_meta, st)
                for ch_meta, st in candidates
            }
            for fut in as_completed(futs):
                ch_meta, st = futs[fut]
                try:
                    res = fut.result()
                except Exception as exc:
                    res = StreamCheckResult(url=st["url"], online=False, reason=str(exc))
                checks_by_url[st["url"]] = res
                tested_reports.append({
                    "channel_id": ch_meta["id"],
                    "channel_name": ch_meta["name"],
                    "country": ch_meta["country"],
                    "quality": st.get("quality", ""),
                    **res.to_dict(),
                })

        # Pick the highest-priority candidate that is online
        for ch_meta, st in candidates:
            chk = checks_by_url.get(st["url"])
            if chk and chk.online:
                return {
                    "found": True,
                    "online": True,
                    "channel": self._channels_by_id.get(ch_meta["id"], ch_meta),
                    "stream": st,
                    "check": chk.to_dict(),
                    "tested": tested_reports,
                }

        return {
            "found": True,
            "online": False,
            "channel": self._channels_by_id.get(matches[0]["id"], matches[0]),
            "stream": candidates[0][1] if candidates else {},
            "reason": "Se encontraron canales coincidentes, pero ningún stream respondió correctamente.",
            "tested": tested_reports,
        }

    def get_channel_details(self, query: str) -> dict[str, Any]:
        self.ensure_loaded()
        matches = self.search_channels(query=query, only_with_streams=False, limit=3)
        if not matches:
            return {"found": False, "reason": f"Canal '{query}' no encontrado en iptv-org."}
        cid = matches[0]["id"]
        ch = self._channels_by_id.get(cid, {})
        streams = self._streams_by_channel.get(cid, [])
        guides = self._guides_by_channel.get(cid, [])
        return {
            "found": True,
            "channel": ch,
            "streams": streams,
            "guides": guides,
            "blocked": self._blocklist.get(cid),
        }

    # ── Metadata listings ────────────────────────────────────────────────────
    def list_categories(self) -> list[dict[str, Any]]:
        self.ensure_loaded()
        return sorted(self._categories.values(), key=lambda c: c.get("name", ""))

    def list_countries(self) -> list[dict[str, Any]]:
        self.ensure_loaded()
        return sorted(self._countries.values(), key=lambda c: c.get("name", ""))

    # ── Favorites ────────────────────────────────────────────────────────────
    def list_favorites(self) -> list[dict[str, str]]:
        try:
            if FAVORITES_FILE.exists():
                data = json.loads(FAVORITES_FILE.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    return data
        except Exception:
            pass
        return []

    def add_favorite(self, query: str) -> dict[str, Any]:
        self.ensure_loaded()
        matches = self.search_channels(query=query, only_with_streams=False, limit=1)
        if not matches:
            return {"ok": False, "reason": f"No se encontró '{query}'."}
        ch = matches[0]
        favs = self.list_favorites()
        if any(f.get("id") == ch["id"] for f in favs):
            return {"ok": True, "already": True, "channel": ch}
        favs.append({"id": ch["id"], "name": ch["name"], "country": ch.get("country", "")})
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        FAVORITES_FILE.write_text(json.dumps(favs, indent=2, ensure_ascii=False), encoding="utf-8")
        return {"ok": True, "already": False, "channel": ch}

    def remove_favorite(self, query: str) -> bool:
        q = _normalize(query)
        favs = self.list_favorites()
        new_favs = [
            f for f in favs
            if _normalize(f.get("name", "")) != q and f.get("id", "").lower() != query.strip().lower()
        ]
        if len(new_favs) == len(favs):
            return False
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        FAVORITES_FILE.write_text(json.dumps(new_favs, indent=2, ensure_ascii=False), encoding="utf-8")
        return True

    # ── Custom M3U playlists ─────────────────────────────────────────────────
    def list_custom_playlists(self) -> list[dict[str, str]]:
        try:
            if CUSTOM_PLAYLISTS_FILE.exists():
                data = json.loads(CUSTOM_PLAYLISTS_FILE.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    return data
        except Exception:
            pass
        return []

    def add_custom_playlist(self, source: str, name: str = "") -> dict[str, Any]:
        pls = self.list_custom_playlists()
        entry = {"name": name or source.rsplit("/", 1)[-1], "source": source}
        if not any(p.get("source") == source for p in pls):
            pls.append(entry)
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            CUSTOM_PLAYLISTS_FILE.write_text(json.dumps(pls, indent=2, ensure_ascii=False), encoding="utf-8")
        self.ensure_loaded(force_refresh=True)
        return {"ok": True, "entry": entry}


_MANAGER: Optional[IptvOrgManager] = None


def get_iptv_manager() -> IptvOrgManager:
    global _MANAGER
    if _MANAGER is None:
        _MANAGER = IptvOrgManager()
    return _MANAGER
