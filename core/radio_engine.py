from __future__ import annotations

import json
import random
import re
import threading
import time
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "config" / "radio_cache"
INDEX_FILE = CACHE_DIR / "ondachannels.json"
FAV_FILE = BASE_DIR / "config" / "radio_favorites.json"

ONDACHANNELS_M3U8 = "https://www.ondachannels.com/lists/radio.m3u8"
RADIO_BROWSER_API = "https://de1.api.radio-browser.info/json/stations/search"
UA = "ViernesRadio/1.0"

_COUNTRY_CODES = {
    "costa rica": "CR", "cr": "CR",
    "mexico": "MX", "méxico": "MX", "mx": "MX",
    "colombia": "CO", "co": "CO",
    "espana": "ES", "españa": "ES", "es": "ES",
    "argentina": "AR", "ar": "AR",
    "chile": "CL", "cl": "CL",
    "peru": "PE", "perú": "PE", "pe": "PE",
    "ecuador": "EC", "ec": "EC",
    "venezuela": "VE", "ve": "VE",
    "uruguay": "UY", "uy": "UY",
    "guatemala": "GT", "gt": "GT",
    "panama": "PA", "panamá": "PA", "pa": "PA",
    "republica dominicana": "DO", "república dominicana": "DO",
    "puerto rico": "PR",
    "estados unidos": "US", "usa": "US",
}

_CURATED_LATAM: list[dict[str, Any]] = [
    {
        "name": "Bésame 89.9 FM Costa Rica",
        "country": "CR",
        "group": "Romántica · Costa Rica",
        "language": "spanish",
        "logo": "",
        "urls": ["https://playerservices.streamtheworld.com/api/livestream-redirect/BESAME_CRAAC.aac"],
        "source": "curated_latam",
    },
    {
        "name": "Columbia Estéreo 92.7 FM Costa Rica",
        "country": "CR",
        "group": "General · Costa Rica",
        "language": "spanish",
        "logo": "",
        "urls": ["https://s5.radio.co/sca838cc60/listen"],
        "source": "curated_latam",
    },
    {
        "name": "Teletica Radio Costa Rica",
        "country": "CR",
        "group": "Noticias/Deportes · Costa Rica",
        "language": "spanish",
        "logo": "",
        "urls": ["https://g2qd375ol7an-hls-live.5centscdn.com/Radio/eae835e83c0494a376229f254f7d3392.sdp/chunks.m3u8"],
        "source": "curated_latam",
    },
]

_EXTINF_ATTR_RE = re.compile(r'([a-zA-Z0-9_-]+)="([^"]*)"')


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "")
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]+", " ", text)).strip()


class RadioManager:
    """Native Radio Engine using ondachannels.com/lists/radio.m3u8 + Spanish Radio Browser fallback."""

    def __init__(self) -> None:
        self._lock = threading.RLock()

    def refresh_index(self, force: bool = False) -> list[dict[str, Any]]:
        with self._lock:
            if not force and INDEX_FILE.exists():
                age_h = (time.time() - INDEX_FILE.stat().st_mtime) / 3600
                if age_h < 12:
                    try:
                        cached = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
                        if cached.get("stations"):
                            return cached["stations"]
                    except Exception:
                        pass

            stations_map: dict[str, dict[str, Any]] = {}
            try:
                r = requests.get(ONDACHANNELS_M3U8, headers={"User-Agent": UA}, timeout=15)
                r.raise_for_status()
                lines = r.text.splitlines()
                cur_meta: dict[str, str] | None = None
                for raw in lines:
                    line = raw.strip()
                    if not line:
                        continue
                    if line.startswith("#EXTINF:"):
                        attrs = dict(_EXTINF_ATTR_RE.findall(line))
                        comma_name = line.split(",", 1)[1].strip() if "," in line else ""
                        name = attrs.get("tvg-name") or comma_name or attrs.get("tvg-id") or "Radio"
                        cur_meta = {
                            "name": name.strip(),
                            "group": (attrs.get("group-title") or "Radio").replace("_", " ").strip(),
                            "logo": attrs.get("tvg-logo", "").strip(),
                            "id": attrs.get("tvg-id", "").strip(),
                        }
                    elif not line.startswith("#") and cur_meta is not None:
                        key = _norm(cur_meta["name"])
                        if key not in stations_map:
                            stations_map[key] = {
                                "name": cur_meta["name"],
                                "group": cur_meta["group"],
                                "logo": cur_meta["logo"],
                                "country": "ES",
                                "language": "spanish",
                                "urls": [],
                                "source": "ondachannels",
                            }
                        if line not in stations_map[key]["urls"]:
                            stations_map[key]["urls"].append(line)
                        cur_meta = None
            except Exception:
                pass

            out = list(stations_map.values())
            if out:
                try:
                    CACHE_DIR.mkdir(parents=True, exist_ok=True)
                    INDEX_FILE.write_text(
                        json.dumps({"ts": time.time(), "stations": out}, ensure_ascii=False),
                        encoding="utf-8",
                    )
                except Exception:
                    pass
                return out

            try:
                return json.loads(INDEX_FILE.read_text(encoding="utf-8")).get("stations", [])
            except Exception:
                return []

    def _extract_country(self, query: str, country: str = "") -> tuple[str, str]:
        cc = _COUNTRY_CODES.get(_norm(country), country.upper() if len(country.strip()) == 2 else "")
        q_clean = _norm(query)
        for cname, code in sorted(_COUNTRY_CODES.items(), key=lambda x: -len(x[0])):
            if len(cname) <= 2:
                continue
            if re.search(rf"\b{re.escape(cname)}\b", q_clean):
                if not cc:
                    cc = code
                q_clean = re.sub(rf"\b(?:de\s+)?{re.escape(cname)}\b", " ", q_clean).strip()
        q_clean = re.sub(r"\b(?:radio|emisora|fm|am|en vivo|de)\b", " ", q_clean)
        q_clean = re.sub(r"\s+", " ", q_clean).strip()
        return q_clean, cc

    def _search_radio_browser(self, name: str = "", country_code: str = "", limit: int = 8) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"language": "spanish", "limit": limit, "order": "votes", "reverse": "true"}
        if name:
            params["name"] = name
        if country_code:
            params["countrycode"] = country_code
        try:
            r = requests.get(RADIO_BROWSER_API, params=params, headers={"User-Agent": UA}, timeout=7)
            if r.status_code != 200:
                return []
            out = []
            for s in r.json():
                u = (s.get("url_resolved") or s.get("url") or "").strip()
                if not u:
                    continue
                out.append(
                    {
                        "name": (s.get("name") or name or "Radio").strip(),
                        "group": (s.get("tags") or s.get("country") or "Español").split(",")[0].strip(),
                        "logo": s.get("favicon", ""),
                        "country": s.get("countrycode", country_code or "ES"),
                        "language": "spanish",
                        "urls": [u],
                        "source": "radio_browser",
                    }
                )
            return out
        except Exception:
            return []

    def _verify_stream(self, url: str) -> bool:
        try:
            r = requests.get(url, headers={"User-Agent": UA}, stream=True, timeout=7.0)
            ok = r.status_code < 400
            r.close()
            return ok
        except Exception:
            return False

    def search_stations(self, query: str, country: str = "", limit: int = 10) -> list[dict[str, Any]]:
        q_clean, cc = self._extract_country(query, country)
        pool = list(_CURATED_LATAM) + self.refresh_index()
        scored: list[tuple[float, dict[str, Any]]] = []
        for st in pool:
            if cc and st.get("country") and st["country"] != cc:
                continue
            n = _norm(st["name"])
            g = _norm(st.get("group", ""))
            if not q_clean:
                score = 0.8
            elif q_clean == n:
                score = 1.0
            elif q_clean in n or n in q_clean:
                score = 0.9
            elif q_clean in g:
                score = 0.78
            else:
                score = SequenceMatcher(None, q_clean, n).ratio()
            if score >= 0.62:
                scored.append((score, st))
        scored.sort(key=lambda x: -x[0])
        results = [s for _, s in scored[:limit]]
        if not results and (q_clean or cc):
            results = self._search_radio_browser(name=q_clean, country_code=cc, limit=limit)
        return results

    def resolve_working_station(self, query: str, country: str = "") -> dict[str, Any]:
        matches = self.search_stations(query, country=country, limit=8)
        if not matches and country:
            q_clean, cc = self._extract_country(query, country)
            matches = self._search_radio_browser(name=q_clean, country_code=cc, limit=8)
        for st in matches:
            for u in st.get("urls", []):
                if self._verify_stream(u):
                    return {"ok": True, "station": st, "url": u}
        return {"ok": False, "reason": f"No encontré una señal activa para '{query}'."}

    def random_spanish_station(self, genre: str = "", country: str = "") -> dict[str, Any]:
        q_clean, cc = self._extract_country(genre, country)
        if cc and cc != "ES":
            pool = [s for s in _CURATED_LATAM if s["country"] == cc] + self._search_radio_browser(
                name=q_clean, country_code=cc, limit=15
            )
        else:
            pool = self.refresh_index()
            if q_clean:
                filtered = [s for s in pool if q_clean in _norm(s.get("group", "")) or q_clean in _norm(s.get("name", ""))]
                if filtered:
                    pool = filtered
        if not pool:
            return {"ok": False, "reason": "No hay emisoras en español disponibles en este momento."}
        sample = random.sample(pool, min(len(pool), 12))
        for st in sample:
            for u in st.get("urls", []):
                if self._verify_stream(u):
                    return {"ok": True, "station": st, "url": u}
        return {"ok": False, "reason": "Ninguna emisora aleatoria respondió a tiempo."}

    def _load_favs(self) -> list[dict[str, Any]]:
        try:
            return json.loads(FAV_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []

    def add_favorite(self, name: str, url: str, group: str = "") -> dict[str, Any]:
        favs = self._load_favs()
        favs = [f for f in favs if _norm(f.get("name", "")) != _norm(name)]
        favs.insert(0, {"name": name, "url": url, "group": group})
        FAV_FILE.parent.mkdir(parents=True, exist_ok=True)
        FAV_FILE.write_text(json.dumps(favs[:40], indent=2, ensure_ascii=False), encoding="utf-8")
        return {"ok": True, "count": len(favs[:40])}

    def list_favorites(self) -> list[dict[str, Any]]:
        return self._load_favs()


_RADIO_MGR: RadioManager | None = None


def get_radio_manager() -> RadioManager:
    global _RADIO_MGR
    if _RADIO_MGR is None:
        _RADIO_MGR = RadioManager()
    return _RADIO_MGR
