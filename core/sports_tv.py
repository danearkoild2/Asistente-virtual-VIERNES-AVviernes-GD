"""
Sports TV backend for VIERNES (futbolenvivo.top integration).

* Settings persisted in config/sports_tv.json (edited from the settings dialog).
* Channel index scraped from the site (cards + sitemap) and cached.
* Natural-language channel matching ("ESPN 2", "fox sports premium", "tudn").
* Brave adblock engine (adblock-rust via the ``adblock`` package) with cached
  filter lists, serialized engine, per-thread instances and a built-in fallback.

The player itself (core/sports_web_view.py) loads the ORIGINAL channel page so
the origin/referrer are genuine, then isolates the site's player frame and
removes everything else (ads, banners, overlays). No headers are spoofed.
"""
from __future__ import annotations

import json
import re
import threading
import time
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse
from urllib.request import Request, urlopen

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
SETTINGS_FILE = CONFIG_DIR / "sports_tv.json"
CACHE_DIR = CONFIG_DIR / "sports_tv_cache"
ADBLOCK_DIR = CONFIG_DIR / "adblock"
INDEX_FILE = CACHE_DIR / "channels.json"
TVPORINTERNET_URL = "https://www.tvporinternet.org"
TVPORINTERNET_INDEX_FILE = CACHE_DIR / "tvporinternet_channels.json"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

DEFAULT_SETTINGS: dict[str, Any] = {
    "enabled": True,
    "source_url": "https://futbolenvivo.top",
    # sports_web = only the web source | iptv = only IPTV-org | sports_web_then_iptv = fallback
    "sports_routing": "sports_web",
    "adblock_enabled": True,
    "block_popups": True,
    "isolate_player": True,
    "autoplay": True,
    "extra_blocked_hosts": "rtxt.org",
    "extra_filter_lists": "",
    "index_ttl_hours": 6,
    "lists_ttl_days": 3,
}

FILTER_LISTS = {
    "easylist": "https://easylist.to/easylist/easylist.txt",
    "easylist_es": "https://easylist-downloads.adblockplus.org/easylistspanish.txt",
    "easyprivacy": "https://easylist.to/easylist/easyprivacy.txt",
    "brave_specific": "https://raw.githubusercontent.com/brave/adblock-lists/master/brave-lists/brave-specific.txt",
    "brave_unbreak": "https://raw.githubusercontent.com/brave/adblock-lists/master/brave-unbreak.txt",
}

SPORTS_KEYWORDS = (
    "espn", "fox sports", "foxsports", "tudn", "sky sports", "dazn", "tnt sports",
    "directv sports", "dsports", "win sports", "gol tv", "golt", "bein", "movistar deportes",
    "deportes", "futbol", "fútbol", "liga", "champions", "nba", "nfl", "mlb", "ufc",
    "canal de deportes", "tyc sports", "claro sports", "azteca deportes", "vix deportes",
)

ALIASES = {
    "espn": "espn 1", "espn uno": "espn 1", "espn dos": "espn 2", "espn tres": "espn 3",
    "fox sports": "fox sports 1", "fox deportes": "fox sports 1", "fox sports premium": "fox sports premium",
    "tudn": "tudn mx", "univision deportes": "tudn mx",
}

_lock = threading.RLock()


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]+", " ", text)).strip()


# ── settings ────────────────────────────────────────────────────────────────
def load_settings() -> dict[str, Any]:
    data = dict(DEFAULT_SETTINGS)
    try:
        raw = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            data.update({k: raw[k] for k in DEFAULT_SETTINGS if k in raw})
    except Exception:
        pass
    data["source_url"] = (str(data["source_url"]).strip() or DEFAULT_SETTINGS["source_url"]).rstrip("/")
    if data["sports_routing"] not in ("sports_web", "iptv", "sports_web_then_iptv"):
        data["sports_routing"] = "sports_web"
    return data


def save_settings(values: dict[str, Any]) -> dict[str, Any]:
    cur = load_settings()
    cur.update({k: v for k, v in values.items() if k in DEFAULT_SETTINGS})
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        SETTINGS_FILE.write_text(json.dumps(cur, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    return load_settings()


def _http_get(url: str, timeout: float = 15.0) -> str:
    req = Request(url, headers={"User-Agent": UA, "Accept-Language": "es,en;q=0.8"})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "ignore")


# ── channel index ───────────────────────────────────────────────────────────
_CARD_RE = re.compile(
    r'<a[^>]*data-name="([^"]*)"[^>]*data-category="([^"]*)"[^>]*href="([^"]*en-vivo/[^"]+)"', re.I)
_CARD_RE2 = re.compile(
    r'<a[^>]*href="([^"]*en-vivo/[^"]+)"[^>]*data-name="([^"]*)"[^>]*data-category="([^"]*)"', re.I)


def _slug_of(href: str) -> str:
    return href.rstrip("/").rsplit("/", 1)[-1]


def refresh_index(force: bool = False) -> list[dict[str, str]]:
    cfg = load_settings()
    base = cfg["source_url"]
    with _lock:
        if not force and INDEX_FILE.exists():
            age_h = (time.time() - INDEX_FILE.stat().st_mtime) / 3600
            if age_h < float(cfg["index_ttl_hours"]):
                try:
                    cached = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
                    if cached.get("base") == base and cached.get("channels"):
                        return cached["channels"]
                except Exception:
                    pass
        channels: dict[str, dict[str, str]] = {}
        try:
            html = _http_get(base + "/")
            for name, cat, href in _CARD_RE.findall(html):
                channels[_slug_of(href)] = {"name": name.strip(), "category": cat.strip(), "slug": _slug_of(href)}
            for href, name, cat in _CARD_RE2.findall(html):
                channels.setdefault(_slug_of(href), {"name": name.strip(), "category": cat.strip(), "slug": _slug_of(href)})
        except Exception:
            pass
        try:
            xml = _http_get(base + "/sitemap.xml")
            for slug in re.findall(r"/en-vivo/([a-z0-9-]+)/?<", xml):
                channels.setdefault(slug, {"name": slug.replace("-", " "), "category": "", "slug": slug})
        except Exception:
            pass
        if channels:
            out = list(channels.values())
            try:
                CACHE_DIR.mkdir(parents=True, exist_ok=True)
                INDEX_FILE.write_text(json.dumps({"base": base, "ts": time.time(), "channels": out},
                                                 ensure_ascii=False), encoding="utf-8")
            except Exception:
                pass
            return out
        try:
            return json.loads(INDEX_FILE.read_text(encoding="utf-8")).get("channels", [])
        except Exception:
            return []


def list_channels() -> list[dict[str, str]]:
    return refresh_index()


def match_channel(query: str) -> Optional[dict[str, Any]]:
    q = _norm(query)
    if not q:
        return None
    q = _norm(ALIASES.get(q, q))
    best: tuple[float, Optional[dict[str, str]]] = (0.0, None)
    for ch in refresh_index():
        n = _norm(ch["name"])
        slug_n = _norm(ch["slug"])
        if q in (n, slug_n):
            score = 1.0
        elif q in n or n in q:
            score = 0.88
        else:
            score = SequenceMatcher(None, q, n).ratio()
        if score > best[0]:
            best = (score, ch)
    if best[1] is not None and best[0] >= 0.72:
        return dict(best[1], score=round(best[0], 2))
    return None


def is_match_query(query: str) -> bool:
    q = _norm(query)
    if not q:
        return False
    return bool(
        re.search(r"\b(?:vs|versus|contra)\b", q)
        or any(w in q for w in ("partido", "juego", "encuentro", "hoy juega", "seleccion"))
    )


def is_sports_request(query: str) -> bool:
    cfg = load_settings()
    if not cfg["enabled"]:
        return False
    if is_match_query(query):
        return True
    q = _norm(query)
    if any(_norm(k) in q for k in SPORTS_KEYWORDS):
        return True
    m = match_channel(query)
    return bool(m and "deport" in _norm(m.get("category", "")))


def channel_url(slug: str) -> str:
    return f"{load_settings()['source_url']}/en-vivo/{slug}/"


_IFRAME_RE = re.compile(r'<iframe[^>]*id="embedIframe"[^>]*src="([^"]+)"|<iframe[^>]*src="([^"]+)"[^>]*id="embedIframe"', re.I)
_TVI_CARD_RE = re.compile(
    r'<a[^>]*href="(https?://(?:www\.)?tvporinternet\.org/([a-z0-9-]+-en-vivo-online\.php)|/?([a-z0-9-]+-en-vivo-online\.php))"[^>]*>(.*?)</a>',
    re.I | re.S,
)
_TVI_OPT_RE = re.compile(
    r'<button[^>]*class="[^"]*\boption\b[^"]*"[^>]*data-src="([^"]+)"[^>]*>(.*?)</button>',
    re.I | re.S,
)
_TVI_OPT_RE2 = re.compile(
    r'<button[^>]*data-src="([^"]+)"[^>]*class="[^"]*\boption\b[^"]*"[^>]*>(.*?)</button>',
    re.I | re.S,
)
_TVI_IFRAME_RE = re.compile(r'<iframe[^>]+(?:data-src|src)="([^"]+)"', re.I)


def _clean_tvi_name(raw_html: str, slug: str) -> str:
    txt = re.sub(r"<[^>]+>", " ", raw_html or "")
    txt = re.sub(r"\s+", " ", txt).strip()
    txt = re.sub(r"^EN\s*VIVO\s*\d*\s*", "", txt, flags=re.I)
    txt = re.sub(r"[▶►]+\s*$", "", txt).strip()
    if not txt:
        txt = slug.replace("-en-vivo-online.php", "").replace("-", " ").title()
    return txt


def refresh_tvporinternet_index(force: bool = False) -> list[dict[str, str]]:
    cfg = load_settings()
    with _lock:
        if not force and TVPORINTERNET_INDEX_FILE.exists():
            age_h = (time.time() - TVPORINTERNET_INDEX_FILE.stat().st_mtime) / 3600
            if age_h < float(cfg["index_ttl_hours"]):
                try:
                    cached = json.loads(TVPORINTERNET_INDEX_FILE.read_text(encoding="utf-8"))
                    if cached.get("channels"):
                        return cached["channels"]
                except Exception:
                    pass
        channels: dict[str, dict[str, str]] = {}
        try:
            html = _http_get(TVPORINTERNET_URL + "/")
            for href, slug1, slug2, inner in _TVI_CARD_RE.findall(html):
                slug = (slug1 or slug2 or "").strip()
                if not slug:
                    continue
                full_url = href if href.startswith("http") else f"{TVPORINTERNET_URL}/{slug.lstrip('/')}"
                channels[slug] = {
                    "name": _clean_tvi_name(inner, slug),
                    "slug": slug,
                    "url": full_url,
                    "category": "tvporinternet",
                }
        except Exception:
            pass
        if channels:
            out = list(channels.values())
            try:
                CACHE_DIR.mkdir(parents=True, exist_ok=True)
                TVPORINTERNET_INDEX_FILE.write_text(
                    json.dumps({"base": TVPORINTERNET_URL, "ts": time.time(), "channels": out}, ensure_ascii=False),
                    encoding="utf-8",
                )
            except Exception:
                pass
            return out
        try:
            return json.loads(TVPORINTERNET_INDEX_FILE.read_text(encoding="utf-8")).get("channels", [])
        except Exception:
            return []


def match_tvporinternet_channel(query: str) -> Optional[dict[str, Any]]:
    q = _norm(query)
    if not q:
        return None
    q = _norm(ALIASES.get(q, q))
    best: tuple[float, Optional[dict[str, str]]] = (0.0, None)
    for ch in refresh_tvporinternet_index():
        n = _norm(ch["name"])
        slug_n = _norm(ch["slug"].replace("-en-vivo-online.php", ""))
        if q in (n, slug_n):
            score = 1.0
        elif q in n or n in q:
            score = 0.88
        else:
            score = SequenceMatcher(None, q, n).ratio()
        if score > best[0]:
            best = (score, ch)
    if best[1] is not None and best[0] >= 0.72:
        return dict(best[1], score=round(best[0], 2))
    return None


def resolve_tvporinternet_channel(query: str, option: int = 1) -> dict[str, Any]:
    """Resolve a channel from tvporinternet.org with all available embed options (Opción 1, 2, 3...)."""
    cfg = load_settings()
    if not cfg["enabled"]:
        return {"ok": False, "reason": "El módulo de TV web está desactivado en Ajustes."}
    ch = match_tvporinternet_channel(query)
    if ch is None:
        return {"ok": False, "reason": f"No encontré '{query}' en tvporinternet.org."}
    url = ch["url"]
    try:
        html = _http_get(url)
    except Exception as exc:
        return {"ok": False, "reason": f"La página del canal no respondió ({exc})", "channel": ch, "url": url}

    options: list[dict[str, str]] = []
    seen_urls: set[str] = set()
    for src, lbl_html in _TVI_OPT_RE.findall(html) + _TVI_OPT_RE2.findall(html):
        u = src.strip()
        if not u or u in seen_urls:
            continue
        if not u.startswith("http"):
            u = f"{TVPORINTERNET_URL}/{u.lstrip('/')}"
        seen_urls.add(u)
        lbl = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", lbl_html)).strip() or f"Opción {len(options) + 1}"
        options.append({"label": lbl, "url": u})

    if not options:
        for src in _TVI_IFRAME_RE.findall(html):
            if "chat.php" in src.lower():
                continue
            u = src.strip()
            if not u.startswith("http"):
                u = f"{TVPORINTERNET_URL}/{u.lstrip('/')}"
            options.append({"label": "Opción 1", "url": u})
            break

    idx = max(0, min(int(option or 1) - 1, len(options) - 1)) if options else 0
    frame_src = options[idx]["url"] if options else ""
    return {
        "ok": True,
        "source": "tvporinternet",
        "channel": ch,
        "url": url,
        "frame_src": frame_src,
        "frame_host": urlparse(frame_src).netloc if frame_src else "",
        "options": options,
        "selected_option": idx + 1,
        "has_player": bool(frame_src),
    }


_AGENDA_LOCK = threading.Lock()
_AGENDA_CACHE: dict[str, Any] = {"ts": 0.0, "events": []}
_AGENDA_STOPWORDS = {
    "partido", "el", "la", "los", "las", "de", "del", "en", "vivo",
    "ver", "ponme", "ponga", "pon", "quiero", "juego", "encuentro",
    "hoy", "por", "favor", "canal", "transmision",
}


def fetch_sports_agenda(force: bool = False) -> list[dict[str, Any]]:
    """Fetch live sports agenda events & channel embeds from futbolenvivo.top/api/agenda."""
    cfg = load_settings()
    base = cfg["source_url"].rstrip("/")
    with _AGENDA_LOCK:
        now = time.time()
        if not force and _AGENDA_CACHE["events"] and (now - _AGENDA_CACHE["ts"]) < 120.0:
            return list(_AGENDA_CACHE["events"])
    try:
        r = requests.get(
            f"{base}/api/agenda",
            headers={"User-Agent": UA, "Referer": f"{base}/"},
            timeout=10,
        )
        if r.status_code == 200:
            events = r.json().get("events") or []
            if isinstance(events, list):
                with _AGENDA_LOCK:
                    _AGENDA_CACHE["ts"] = time.time()
                    _AGENDA_CACHE["events"] = events
                return list(events)
    except Exception:
        pass
    with _AGENDA_LOCK:
        return list(_AGENDA_CACHE["events"])


def _clean_match_tokens(text: str) -> list[str]:
    return [w for w in _norm(text).split() if w and w not in _AGENDA_STOPWORDS]


def match_agenda_event(query: str, force: bool = False) -> Optional[dict[str, Any]]:
    """Find best matching live match in futbolenvivo.top/api/agenda."""
    q_norm = _norm(query)
    if not q_norm:
        return None
    parts = re.split(r"\b(?:vs|versus|contra)\b", q_norm)
    team_a = " ".join(_clean_match_tokens(parts[0])) if parts else ""
    team_b = " ".join(_clean_match_tokens(parts[1])) if len(parts) > 1 else ""
    all_tokens = _clean_match_tokens(q_norm.replace("vs", " ").replace("versus", " ").replace("contra", " "))
    if not all_tokens:
        return None

    events = fetch_sports_agenda(force=force)
    best: tuple[float, Optional[dict[str, Any]]] = (0.0, None)
    for ev in events:
        title = str(ev.get("title") or "")
        tn = _norm(title)
        if not tn:
            continue
        score = 0.0
        if team_a and team_b:
            has_a = team_a in tn
            has_b = team_b in tn
            if has_a and has_b:
                score = 1.0
            elif has_a or has_b:
                score = 0.72
        else:
            hits = sum(1 for tok in all_tokens if tok in tn)
            if hits == len(all_tokens):
                score = 0.94
            elif hits > 0:
                score = 0.55 + 0.35 * (hits / len(all_tokens))
        if score < 0.65:
            ratio = SequenceMatcher(None, " ".join(all_tokens), tn).ratio()
            score = max(score, ratio)
        if score > best[0]:
            best = (score, ev)

    if best[1] is not None and best[0] >= 0.65:
        return dict(best[1], _score=round(best[0], 2))
    return None


def resolve_agenda_match(query: str, option: int = 1) -> dict[str, Any]:
    """Resolve a match (e.g. 'Costa Rica vs Ecuador') from futbolenvivo.top agenda to its channel embed."""
    cfg = load_settings()
    if not cfg["enabled"]:
        return {"ok": False, "reason": "El módulo de TV deportiva está desactivado en Ajustes."}

    ev = match_agenda_event(query, force=False)
    if ev is None:
        ev = match_agenda_event(query, force=True)
    if ev is None:
        return {"ok": False, "reason": f"No encontré el partido '{query}' en la agenda deportiva de hoy."}

    embeds = list(ev.get("embeds") or [])
    # Prioritize Spanish streams first while keeping original order otherwise
    embeds.sort(key=lambda e: 0 if "espanol" in _norm(str(e.get("lang", ""))) else 1)

    options: list[dict[str, str]] = []
    seen: set[str] = set()
    for emb in embeds:
        cname = str(emb.get("name") or "Canal").strip()
        clang = str(emb.get("lang") or "").strip()
        iframe = str(emb.get("iframe") or "").strip()
        if not iframe and cname:
            # Fallback: resolve channel page on futbolenvivo.top if agenda omitted iframe URL
            m_ch = match_channel(cname)
            if m_ch:
                try:
                    html = _http_get(channel_url(m_ch["slug"]))
                    m = _IFRAME_RE.search(html)
                    iframe = (m.group(1) or m.group(2)) if m else ""
                except Exception:
                    iframe = ""
        if not iframe or iframe in seen:
            continue
        seen.add(iframe)
        lbl = f"{cname} ({clang})" if clang else cname
        options.append({"label": lbl, "url": iframe, "channel_name": cname})

    if not options:
        return {
            "ok": False,
            "reason": f"Encontré '{ev.get('title')}' en la agenda, pero aún no tiene canales/enlaces activos.",
            "event": ev,
        }

    idx = max(0, min(int(option or 1) - 1, len(options) - 1))
    sel = options[idx]
    frame_src = sel["url"]
    ch_display = f"{ev.get('title', query)} · {sel.get('channel_name') or sel['label']}"
    return {
        "ok": True,
        "source": "futbolenvivo_agenda",
        "channel": {"name": ch_display, "slug": "agenda", "category": "Agenda Deportiva"},
        "url": cfg["source_url"].rstrip("/") + "/",
        "frame_src": frame_src,
        "frame_host": urlparse(frame_src).netloc if frame_src else "",
        "options": [{"label": o["label"], "url": o["url"]} for o in options],
        "selected_option": idx + 1,
        "has_player": bool(frame_src),
        "event": ev,
    }


def resolve_channel(query: str, option: int = 1) -> dict[str, Any]:
    """Match, fetch the original page and report the player frame host (for the ad-block allow list)."""
    cfg = load_settings()
    if not cfg["enabled"]:
        return {"ok": False, "reason": "El módulo de TV deportiva está desactivado en Ajustes."}

    if is_match_query(query):
        ag = resolve_agenda_match(query, option=option)
        if ag.get("ok"):
            return ag

    if not is_sports_request(query):
        tvi = resolve_tvporinternet_channel(query, option=option)
        if tvi.get("ok"):
            return tvi

    ch = match_channel(query)
    if ch is None:
        slug = re.sub(r"\s+", "-", _norm(query))
        if slug:
            try:
                _http_get(channel_url(slug))
                ch = {"name": query.strip().title(), "slug": slug, "category": "", "score": 0.5}
            except Exception:
                pass
    if ch is None:
        ag = resolve_agenda_match(query, option=option)
        if ag.get("ok"):
            return ag
        tvi = resolve_tvporinternet_channel(query, option=option)
        if tvi.get("ok"):
            return tvi
        return {"ok": False, "reason": f"No encontré '{query}' en la agenda ni en {urlparse(cfg['source_url']).netloc}."}
    url = channel_url(ch["slug"])
    try:
        html = _http_get(url)
    except Exception as exc:
        tvi = resolve_tvporinternet_channel(query, option=option)
        if tvi.get("ok"):
            return tvi
        return {"ok": False, "reason": f"La página del canal no respondió ({exc})", "channel": ch, "url": url}
    m = _IFRAME_RE.search(html)
    frame_src = (m.group(1) or m.group(2)) if m else ""
    return {
        "ok": True, "source": "futbolenvivo", "channel": ch, "url": url,
        "frame_src": frame_src,
        "frame_host": urlparse(frame_src).netloc if frame_src else "",
        "options": [{"label": "Opción 1", "url": frame_src}] if frame_src else [],
        "selected_option": 1,
        "has_player": bool(frame_src),
    }


# ── ad blocking (Brave adblock-rust) ───────────────────────────────────────
class AdBlocker:
    """Thread-safe wrapper: engine bytes shared, one Engine instance per thread."""

    _TYPES = {
        "mainframe": "document", "subframe": "subdocument", "stylesheet": "stylesheet",
        "script": "script", "image": "image", "fontresource": "font", "font": "font",
        "media": "media", "xhr": "xmlhttprequest", "ping": "ping", "websocket": "websocket",
        "object": "object", "favicon": "image", "csp": "other",
    }

    def __init__(self) -> None:
        self._tls = threading.local()
        self._blob: Optional[bytes] = None
        self._lists_text: Optional[str] = None
        self.rule_count = 0
        self.backend = "none"
        self.last_update = 0.0
        self._ready = threading.Event()
        self._allow_frame_hosts: set[str] = set()
        self._extra_hosts: set[str] = set()

    # lists
    def _list_paths(self) -> dict[str, Path]:
        return {name: ADBLOCK_DIR / f"{name}.txt" for name in FILTER_LISTS}

    def update_lists(self, force: bool = False) -> int:
        cfg = load_settings()
        ADBLOCK_DIR.mkdir(parents=True, exist_ok=True)
        ttl = float(cfg["lists_ttl_days"]) * 86400
        urls = dict(FILTER_LISTS)
        for i, u in enumerate([x.strip() for x in str(cfg["extra_filter_lists"]).splitlines() if x.strip().startswith("http")]):
            urls[f"extra_{i}"] = u
        got = 0
        for name, url in urls.items():
            path = ADBLOCK_DIR / f"{name}.txt"
            if not force and path.exists() and (time.time() - path.stat().st_mtime) < ttl:
                got += 1
                continue
            try:
                path.write_text(_http_get(url, timeout=30.0), encoding="utf-8")
                got += 1
            except Exception:
                pass
        self.last_update = time.time()
        return got

    def _custom_rules(self) -> str:
        cfg = load_settings()
        hosts = [h.strip().lower() for h in re.split(r"[\s,;]+", str(cfg["extra_blocked_hosts"])) if h.strip()]
        self._extra_hosts = set(hosts)
        return "\n".join(f"||{h}^" for h in hosts)

    def build(self, force_download: bool = False) -> bool:
        """(Re)build the engine. Safe to call from a worker thread."""
        try:
            import adblock  # Brave's adblock-rust bindings
        except Exception:
            self.backend = "fallback"
            self._ready.set()
            return False
        try:
            self.update_lists(force=force_download)
            fs = adblock.FilterSet()
            total = 0
            for path in ADBLOCK_DIR.glob("*.txt"):
                try:
                    txt = path.read_text(encoding="utf-8", errors="ignore")
                    fs.add_filter_list(txt)
                    total += txt.count("\n")
                except Exception:
                    continue
            custom = self._custom_rules()
            if custom:
                fs.add_filter_list(custom)
            engine = adblock.Engine(fs)
            try:
                self._blob = engine.serialize()
            except Exception:
                self._blob = None
            self._tls = threading.local()
            self._tls.engine = engine
            self._source_engine_thread = threading.get_ident()
            self.rule_count = total
            self.backend = "brave-adblock"
            self._ready.set()
            return True
        except Exception:
            self.backend = "fallback"
            self._ready.set()
            return False

    def build_async(self, force_download: bool = False) -> None:
        threading.Thread(target=self.build, args=(force_download,), daemon=True, name="adblock-build").start()

    def _engine(self):
        eng = getattr(self._tls, "engine", None)
        if eng is not None:
            return eng
        if self._blob is None:
            return None
        try:
            import adblock
            eng = adblock.Engine(adblock.FilterSet())
            eng.deserialize(self._blob)
            self._tls.engine = eng
            return eng
        except Exception:
            return None

    def allow_frame_host(self, host: str) -> None:
        if host:
            self._allow_frame_hosts.add(host.lower())

    def should_block(self, url: str, source_url: str, rtype: str) -> bool:
        host = urlparse(url).netloc.lower()
        src_host = urlparse(source_url).netloc.lower()
        rtype = self._TYPES.get(rtype.lower(), "other")
        if host and host == src_host and rtype == "document":
            return False
        if rtype in ("document", "subdocument") and any(host == h or host.endswith("." + h) for h in self._allow_frame_hosts):
            return False
        if any(host == h or host.endswith("." + h) for h in self._extra_hosts):
            return True
        eng = self._engine()
        if eng is None:
            return host in _FALLBACK_HOSTS or any(host.endswith("." + h) for h in _FALLBACK_HOSTS)
        try:
            res = eng.check_network_urls(url, source_url or url, rtype)
            return bool(res.matched) and not bool(getattr(res, "exception", None))
        except Exception:
            return False

    def cosmetic_css(self, url: str) -> str:
        eng = self._engine()
        if eng is None:
            return ""
        try:
            res = eng.url_cosmetic_resources(url)
            sels = list(res.hide_selectors)[:4000]
            return ",".join(sels) + "{display:none!important}" if sels else ""
        except Exception:
            return ""

    def status(self) -> dict[str, Any]:
        try:
            import adblock  # noqa: F401
            installed = True
        except Exception:
            installed = False
        return {"installed": installed, "backend": self.backend, "rules": self.rule_count,
                "ready": self._ready.is_set(), "last_update": self.last_update}


_FALLBACK_HOSTS = {
    "doubleclick.net", "googlesyndication.com", "adservice.google.com", "adsterra.com",
    "popads.net", "propellerads.com", "exoclick.com", "juicyads.com", "trafficjunky.com",
    "onclickads.net", "rtxt.org", "adnxs.com", "taboola.com", "outbrain.com", "histats.com",
}

_ADBLOCKER: Optional[AdBlocker] = None


def get_adblocker() -> AdBlocker:
    global _ADBLOCKER
    if _ADBLOCKER is None:
        _ADBLOCKER = AdBlocker()
        _ADBLOCKER.build_async()
    return _ADBLOCKER
