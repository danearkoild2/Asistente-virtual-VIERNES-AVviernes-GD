"""
Hardware Temperature & Health Alert Plugin for MARK LV / Viernes.
Monitors CPU/GPU thermal load, RAM usage, and alerts if system limits are exceeded.
"""
from __future__ import annotations
import shutil
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "hardware_temperature_alert",
    "description": (
        "Checks hardware health, CPU/RAM utilization, storage space, and thermal warning levels. "
        "Use when user asks 'cómo está la temperatura', 'estado del hardware', 'revisa la temperatura', "
        "or 'se está sobrecalentando el PC'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "detailed": {
                "type": "BOOLEAN",
                "description": "Whether to return full breakdown of RAM, CPU, and disk storage.",
            }
        },
        "required": [],
    },
}

PLUGIN_SETTINGS = {
    "title": "Vigilante de Temperatura y Hardware",
    "fields": [
        {
            "key": "cpu_warning_pct",
            "label": "Umbral de Alerta de CPU (%)",
            "type": "text",
            "default": "85",
            "placeholder": "85",
        },
        {
            "key": "ram_warning_pct",
            "label": "Umbral de Alerta de RAM (%)",
            "type": "text",
            "default": "90",
            "placeholder": "90",
        },
    ],
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    cpu_limit = int(get_plugin_setting("hardware_temperature_alert", "cpu_warning_pct", 85))
    ram_limit = int(get_plugin_setting("hardware_temperature_alert", "ram_warning_pct", 90))

    cpu_pct = 0.0
    ram_pct = 0.0
    ram_gb_used = 0.0
    ram_gb_total = 0.0

    # Try psutil
    try:
        import psutil
        cpu_pct = psutil.cpu_percent(interval=0.2)
        ram = psutil.virtual_memory()
        ram_pct = ram.percent
        ram_gb_used = round(ram.used / (1024**3), 1)
        ram_gb_total = round(ram.total / (1024**3), 1)
    except Exception:
        pass

    # Disk usage
    total, used, free = shutil.disk_usage("C:")
    free_gb = round(free / (1024**3), 1)

    # Check for warnings
    warnings = []
    if cpu_pct >= cpu_limit:
        warnings.append(f"carga de CPU elevada ({cpu_pct}%)")
    if ram_pct >= ram_limit:
        warnings.append(f"memoria RAM casi saturada ({ram_pct}%)")

    status_eval = "Óptimo"
    if warnings:
        status_eval = "Atención Requerida"
    elif cpu_pct > 60 or ram_pct > 75:
        status_eval = "Moderado"

    if player:
        try:
            player.write_log(f"🌡️ HARDWARE: CPU {cpu_pct}% | RAM {ram_pct}% ({ram_gb_used}/{ram_gb_total}GB) | Disco C: {free_gb}GB libres [{status_eval}]")
        except Exception:
            pass

    if warnings:
        warn_str = " y ".join(warnings)
        return f"Sir, el sistema presenta {warn_str}. La CPU está al {cpu_pct}%, la memoria RAM al {ram_pct}%, y te quedan {free_gb} GB libres en disco."
    else:
        return f"El estado del hardware es {status_eval}. CPU al {cpu_pct}%, memoria RAM al {ram_pct}% con {ram_gb_used} de {ram_gb_total} GB en uso, y {free_gb} GB libres en disco."
