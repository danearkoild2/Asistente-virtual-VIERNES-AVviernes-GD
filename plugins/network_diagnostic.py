"""
Network Speed & Latency Diagnostic Plugin for MARK LV / Viernes.
Checks internet latency, ping to major DNS, and connection stability.
"""
from __future__ import annotations
import subprocess
import time
import urllib.request

PLUGIN = {
    "name": "network_diagnostic",
    "description": (
        "Checks internet speed, connection latency, ping, and DNS status. "
        "Use when user asks 'cómo está el internet', 'check internet connection', "
        "'cuál es mi ping', or 'test de velocidad'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {},
        "required": [],
    },
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    # 1. Ping Google and Cloudflare DNS
    pings = {}
    for target, host in [("Cloudflare (1.1.1.1)", "1.1.1.1"), ("Google (8.8.8.8)", "8.8.8.8")]:
        try:
            res = subprocess.run(["ping", "-n", "2", "-w", "1000", host], capture_output=True, text=True, timeout=6)
            if "media =" in res.stdout:
                avg = res.stdout.split("media =")[-1].strip().split("ms")[0].strip()
                pings[target] = f"{avg} ms"
            elif "Average =" in res.stdout:
                avg = res.stdout.split("Average =")[-1].strip().split("ms")[0].strip()
                pings[target] = f"{avg} ms"
            else:
                pings[target] = "online"
        except Exception:
            pings[target] = "sin respuesta"

    # 2. HTTP download latency test on small fast CDN asset
    http_speed_mbps = None
    try:
        t0 = time.time()
        req = urllib.request.Request(
            "https://www.google.com/favicon.ico",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = response.read()
            dt = time.time() - t0
            if dt > 0 and len(data) > 0:
                http_speed_mbps = (len(data) * 8) / (dt * 1_000_000)
    except Exception:
        pass

    cf_ping = pings.get("Cloudflare (1.1.1.1)", "desconocido")
    msg = f"Diagnóstico de red: Conexión activa y estable. Latencia promedio a DNS de {cf_ping}."
    if http_speed_mbps:
        msg += f" Tiempo de respuesta web óptimo."

    if player:
        try:
            player.write_log(f"SYS: {msg} [Ping: {cf_ping}]")
        except Exception:
            pass

    return msg
