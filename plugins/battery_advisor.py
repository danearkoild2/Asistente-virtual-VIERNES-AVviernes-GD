"""
Battery & Power Health Advisor Plugin for MARK LV / Viernes.
Inspects battery charge, plugged-in status and power metrics.
"""
from __future__ import annotations
import subprocess

PLUGIN = {
    "name": "battery_advisor",
    "description": (
        "Checks laptop battery percentage, power supply status, and estimated remaining time. "
        "Use when user asks 'cómo está la batería', 'batería restante', 'battery status', "
        "or 'está conectado el cargador'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {},
        "required": [],
    },
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    try:
        cmd = "Get-CimInstance -ClassName Win32_Battery | Select-Object EstimatedChargeRemaining, BatteryStatus"
        res = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True, timeout=5)
        lines = [l.strip() for l in res.stdout.strip().splitlines() if l.strip()]

        if len(lines) >= 3:
            parts = lines[-1].split()
            pct = parts[0]
            status_code = parts[1] if len(parts) > 1 else "2"
            plugged = "conectado a la corriente" if status_code == "2" else "operando con batería"

            advice = ""
            int_pct = int(pct)
            if int_pct >= 80 and status_code == "2":
                advice = " (Recomendación: desconectar para prolongar vida útil)."
            elif int_pct <= 20 and status_code != "2":
                advice = " (Alerta: nivel bajo de energía, conecte el cargador pronto)."

            msg = f"Nivel de batería: {pct}%, equipo {plugged}.{advice}"
        else:
            msg = "El equipo está conectado directamente a la alimentación de CA de escritorio (sin batería)."
    except Exception as e:
        msg = f"No se pudo consultar el estado de la batería: {e}"

    if player:
        try:
            player.write_log(f"BATTERY: {msg}")
        except Exception:
            pass

    return msg
