"""
Weather Report Action
=====================
Fetches real-time weather and forecast data in ~300ms using wttr.in JSON API.
Features a 15-minute in-memory cache for instantaneous zero-latency repeated queries.
"""

import time
import urllib.parse
import urllib.request
import json

# 15-minute cache: {city_key: (timestamp, report_string)}
_WEATHER_CACHE: dict[str, tuple[float, str]] = {}
_CACHE_TTL = 900  # 15 minutes

_TRANSLATIONS = {
    "sunny": "Soleado",
    "clear": "Despejado",
    "partly cloudy": "Parcialmente nublado",
    "cloudy": "Nublado",
    "overcast": "Completamente cubierto",
    "mist": "Neblina",
    "patchy rain possible": "Posibilidad de lluvias dispersas",
    "patchy snow possible": "Posibilidad de nieve dispersa",
    "patchy sleet possible": "Posibilidad de aguanieve",
    "patchy freezing drizzle possible": "Posibilidad de llovizna helada",
    "thundery outbreaks possible": "Posibilidad de tormentas eléctricas",
    "blowing snow": "Ventisca de nieve",
    "blizzard": "Tormenta de nieve",
    "fog": "Niebla densa",
    "freezing fog": "Niebla helada",
    "patchy light drizzle": "Llovizna ligera",
    "light drizzle": "Llovizna suave",
    "freezing drizzle": "Llovizna helada",
    "heavy freezing drizzle": "Fuerte llovizna helada",
    "patchy light rain": "Lluvias ligeras aisladas",
    "light rain": "Lluvia ligera",
    "moderate rain at times": "Lluvia moderada a intervalos",
    "moderate rain": "Lluvia moderada",
    "heavy rain at times": "Lluvia intensa por momentos",
    "heavy rain": "Lluvia torrencial",
    "light freezing rain": "Lluvia helada ligera",
    "moderate or heavy freezing rain": "Lluvia helada intensa",
    "light sleet": "Aguanieve ligera",
    "moderate or heavy sleet": "Aguanieve moderada o fuerte",
    "patchy light snow": "Nieve ligera dispersa",
    "light snow": "Nieve ligera",
    "patchy moderate snow": "Nieve moderada dispersa",
    "moderate snow": "Nieve moderada",
    "patchy heavy snow": "Nieve intensa",
    "heavy snow": "Nieve fuerte",
    "ice pellets": "Granizo",
    "light rain shower": "Chubascos ligeros",
    "moderate or heavy rain shower": "Chubascos moderados o intensos",
    "torrential rain shower": "Aguacero torrencial",
    "light sleet showers": "Chubascos de aguanieve",
    "moderate or heavy sleet showers": "Chubascos intensos de aguanieve",
    "light snow showers": "Chubascos de nieve",
    "moderate or heavy snow showers": "Nevadas intensas",
    "light showers of ice pellets": "Chubascos de granizo ligero",
    "moderate or heavy showers of ice pellets": "Chubascos de granizo fuerte",
    "patchy light rain with thunder": "Lluvia ligera con truenos",
    "moderate or heavy rain with thunder": "Lluvia intensa con tormenta eléctrica",
    "patchy light snow with thunder": "Nieve ligera con tormenta eléctrica",
    "moderate or heavy snow with thunder": "Tormenta de nieve y truenos",
}


def _translate_condition(cond: str) -> str:
    c = cond.strip().lower()
    return _TRANSLATIONS.get(c, cond.capitalize())


def weather_action(
    parameters: dict = None,
    player=None,
    session_memory=None,
) -> str:
    params = parameters or {}
    city = (params.get("city") or "").strip()
    when = (params.get("time") or "today").strip()

    cache_key = (city or "local").lower()
    now = time.time()

    # Check cache first for 0ms response
    if cache_key in _WEATHER_CACHE:
        ts, cached_msg = _WEATHER_CACHE[cache_key]
        if (now - ts) < _CACHE_TTL:
            _log(f"Cache hit: {cached_msg}", player)
            return cached_msg

    try:
        if city and city.lower() not in ("here", "aquí", "mi ciudad", "local"):
            encoded_city = urllib.parse.quote(city)
            url = f"https://wttr.in/{encoded_city}?format=j1"
            display_name = city.title()
        else:
            url = "https://wttr.in/?format=j1"
            display_name = "tu ubicación"

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "curl/7.68.0", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=2.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        curr = data["current_condition"][0]
        temp_c = curr.get("temp_C", "--")
        feels_c = curr.get("FeelsLikeC", temp_c)
        humidity = curr.get("humidity", "--")
        wind_kmh = curr.get("windspeedKmph", "--")
        raw_desc = curr.get("weatherDesc", [{}])[0].get("value", "Despejado")
        cond_es = _translate_condition(raw_desc)

        # Get chance of rain if available
        rain_chance = ""
        try:
            weather_days = data.get("weather", [])
            if weather_days:
                hourly = weather_days[0].get("hourly", [])
                if hourly:
                    chance = hourly[0].get("chanceofrain", "0")
                    if int(chance) > 0:
                        rain_chance = f", probabilidad de lluvia {chance}%"
        except Exception:
            pass

        # Try to resolve area name from response if local
        if display_name == "tu ubicación":
            try:
                area = data.get("nearest_area", [{}])[0]
                area_name = area.get("areaName", [{}])[0].get("value", "")
                if area_name:
                    display_name = area_name
            except Exception:
                pass

        msg = (
            f"En {display_name}: {temp_c}°C (sensación térmica de {feels_c}°C), "
            f"{cond_es}. Humedad: {humidity}%, viento: {wind_kmh} km/h{rain_chance}."
        )

        # Save to memory cache
        _WEATHER_CACHE[cache_key] = (now, msg)
        _log(msg, player)
        return msg

    except Exception as exc:
        fallback = f"No pude consultar el clima en tiempo real en este momento: {exc}"
        _log(fallback, player)
        return fallback


def _log(message: str, player=None) -> None:
    print(f"[Weather] {message}")
    if player:
        try:
            player.write_log(f"SYS: {message}")
        except Exception:
            pass


TOOL = {
    "name": "weather_report",
    "description": (
        "Returns the live weather report, temperature in Celsius, feels-like, condition, humidity, "
        "and wind speed for any city or user location. Call when user asks about weather, temperature, or rain."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "city": {
                "type": "STRING",
                "description": "City name (optional; leave blank or omit for user's current city)",
            }
        },
    },
    "handler": weather_action,
}
