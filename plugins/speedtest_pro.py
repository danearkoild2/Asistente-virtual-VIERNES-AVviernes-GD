"""
Speedtest Pro Plugin for MARK LV / Viernes.
Tests real network latency, jitter, and download speed without external heavyweight dependencies.
"""
from __future__ import annotations
import socket
import time
import urllib.request
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "speedtest_pro",
    "description": (
        "Measures real network ping latency, connection stability and download throughput. "
        "Use when user asks 'mide la velocidad de internet', 'test de velocidad', 'cuál es mi ping', "
        "or 'cómo está mi conexión'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "quick": {
                "type": "BOOLEAN",
                "description": "If true, only test ping latency. If false, test download throughput as well.",
            }
        },
        "required": [],
    },
}

PLUGIN_SETTINGS = {
    "title": "Speedtest Pro",
    "fields": [
        {
            "key": "ping_host",
            "label": "Host de Ping (DNS)",
            "type": "text",
            "default": "1.1.1.1",
            "placeholder": "1.1.1.1 o 8.8.8.8",
        },
        {
            "key": "test_download",
            "label": "Probar Descarga Completa",
            "type": "toggle",
            "default": True,
        },
    ],
}

def _measure_ping(host: str, port: int = 53, count: int = 4) -> tuple[float, float]:
    latencies = []
    for _ in range(count):
        t0 = time.perf_counter()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((host, port))
            s.close()
            dt = (time.perf_counter() - t0) * 1000.0
            latencies.append(dt)
        except Exception:
            pass
        time.sleep(0.05)
    if not latencies:
        return 999.0, 0.0
    avg_ping = sum(latencies) / len(latencies)
    jitter = max(latencies) - min(latencies)
    return round(avg_ping, 1), round(jitter, 1)

def _measure_download(url: str = "https://speed.cloudflare.com/__down?bytes=5000000", max_sec: float = 3.5) -> float:
    # Measure transfer rate using a 5MB payload chunk
    try:
        t0 = time.perf_counter()
        req = urllib.request.Request(url, headers={"User-Agent": "Viernes-Speedtest/1.0"})
        with urllib.request.urlopen(req, timeout=4.0) as resp:
            total_bytes = 0
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                total_bytes += len(chunk)
                if time.perf_counter() - t0 > max_sec:
                    break
            dt = time.perf_counter() - t0
            if dt > 0.1:
                mbps = (total_bytes * 8.0) / (dt * 1_000_000.0)
                return round(mbps, 2)
    except Exception:
        pass
    return 0.0

def run(parameters: dict, player=None, session_memory=None) -> str:
    quick = parameters.get("quick", False)
    host = get_plugin_setting("speedtest_pro", "ping_host", "1.1.1.1")
    do_dl = get_plugin_setting("speedtest_pro", "test_download", True) if not quick else False

    if player:
        try:
            player.write_log("🌐 SPEEDTEST: Iniciando diagnóstico de red...")
        except Exception:
            pass

    ping, jitter = _measure_ping(host)
    res_text = f"Ping: {ping} ms | Jitter: {jitter} ms"

    if do_dl:
        mbps = _measure_download()
        if mbps > 0:
            res_text += f" | Descarga estimada: ~{mbps} Mbps"
            quality = "excelente" if ping < 35 and mbps > 50 else ("buena" if ping < 80 else "inestable")
            report = f"Tu conexión está {quality}. Ping medio de {ping} milisegundos con fluctuación de {jitter} ms, y velocidad de descarga aproximada de {mbps} Megabits por segundo."
        else:
            report = f"Ping de {ping} milisegundos a {host} con variación de {jitter} milisegundos."
    else:
        report = f"Latencia de red: {ping} milisegundos con fluctuación de {jitter} ms."

    if player:
        try:
            player.write_log(f"🌐 SPEEDTEST: {res_text}")
        except Exception:
            pass

    return report
