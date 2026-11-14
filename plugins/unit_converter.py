"""
Unit & Currency Voice Converter Plugin for MARK LV / Viernes.
Converts length, weight, temperature, and international currencies.
"""
from __future__ import annotations
import urllib.request
import json

PLUGIN = {
    "name": "unit_converter",
    "description": (
        "Converts between currencies (USD, EUR, MXN, ARS, COP, GBP...) or measurement units (kg/lbs, km/miles, C/F). "
        "Use when user asks 'convierte 50 dólares a pesos mexicanos', 'cuántos kilos son 150 libras', "
        "or 'conversión de monedas / unidades'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "amount": {
                "type": "NUMBER",
                "description": "The numeric amount to convert.",
            },
            "from_unit": {
                "type": "STRING",
                "description": "Source unit or currency (e.g. 'usd', 'eur', 'mxn', 'lbs', 'kg', 'km', 'miles').",
            },
            "to_unit": {
                "type": "STRING",
                "description": "Target unit or currency.",
            }
        },
        "required": ["amount", "from_unit", "to_unit"],
    },
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    amount = float(parameters.get("amount", 1.0))
    u_from = parameters.get("from_unit", "").strip().lower()
    u_to = parameters.get("to_unit", "").strip().lower()

    # Unit math
    if u_from in ("lbs", "libras") and u_to in ("kg", "kilos", "kilogramos"):
        res = amount * 0.453592
        return f"{amount} libras equivalen a {res:.2f} kilogramos."
    elif u_from in ("kg", "kilos", "kilogramos") and u_to in ("lbs", "libras"):
        res = amount * 2.20462
        return f"{amount} kilogramos equivalen a {res:.2f} libras."
    elif u_from in ("km", "kilometros") and u_to in ("millas", "miles"):
        res = amount * 0.621371
        return f"{amount} kilómetros son {res:.2f} millas."
    elif u_from in ("millas", "miles") and u_to in ("km", "kilometros"):
        res = amount * 1.60934
        return f"{amount} millas son {res:.2f} kilómetros."

    # Currencies via free Open Exchange Rates / Frankfurter
    try:
        cur_from = u_from.upper().replace("DOLARES", "USD").replace("DÓLARES", "USD").replace("EUROS", "EUR")
        cur_to = u_to.upper().replace("PESOS MEXICANOS", "MXN").replace("PESOS", "MXN")
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={cur_from}&to={cur_to}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            val = data["rates"].get(cur_to)
            if val is not None:
                msg = f"{amount} {cur_from} equivalen a aproximadamente {val:,.2f} {cur_to} al tipo de cambio actual."
                if player: player.write_log(f"SYS: [Converter] {msg}")
                return msg
    except Exception:
        pass

    return f"No se pudo completar la conversión de {amount} {u_from} a {u_to}."
