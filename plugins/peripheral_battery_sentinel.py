"""
Peripheral Battery Sentinel Plugin for VIERNES.
Monitors battery levels of connected Bluetooth peripherals (headphones, mouse,
keyboard, controllers) and alerts if any device is running low on power.
"""
from __future__ import annotations

import json
import subprocess
from typing import Any, Dict, List, Optional
import psutil

PLUGIN = {
    "name": "peripheral_battery_sentinel",
    "description": (
        "Monitors and reports battery levels of connected Bluetooth peripherals "
        "(headphones, mouse, keyboard, gamepad controllers, earbuds) and system battery. "
        "Use when user asks 'cuánta batería le queda a mis audífonos/mouse', 'batería de periféricos', "
        "'estado de batería bluetooth', or 'revisa mis dispositivos bluetooth'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "device_name": {
                "type": "STRING",
                "description": "Optional name of a specific peripheral to check (e.g. 'audífonos', 'mouse', 'mando')."
            }
        },
        "required": [],
    },
}


def _get_bluetooth_battery_powershell() -> List[Dict[str, Any]]:
    """Query Bluetooth LE and PnP battery properties via Windows PowerShell."""
    devices = []
    ps_cmd = r"""
    $results = @()
    # 1. Query PnP Bluetooth devices with battery property key
    Get-PnpDevice -Class Bluetooth -Status OK -ErrorAction SilentlyContinue | ForEach-Object {
        try {
            $prop = Get-PnpDeviceProperty -InstanceId $_.InstanceId -KeyName '{104EA319-6EE2-4701-BD47-8DDBF425BBE5} 2' -ErrorAction SilentlyContinue
            if ($prop -and $prop.Data -ne $null) {
                $results += [PSCustomObject]@{
                    name = $_.FriendlyName
                    battery = [int]$prop.Data
                    type = "Bluetooth"
                }
            }
        } catch {}
    }
    # 2. Query Bluetooth Battery Services in registry if any
    $bthKeys = Get-ChildItem -Path "HKLM:\SYSTEM\CurrentControlSet\Services\BthLEEnum\Parameters" -ErrorAction SilentlyContinue
    if ($bthKeys) {
        # Check subkeys for battery cache
    }
    $results | ConvertTo-Json -Compress
    """
    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            timeout=8
        )
        out = (res.stdout or "").strip()
        if out:
            data = json.loads(out)
            if isinstance(data, dict):
                devices.append(data)
            elif isinstance(data, list):
                devices.extend(data)
    except Exception:
        pass
    return devices


def _get_connected_bluetooth_devices() -> List[str]:
    """Get list of connected Bluetooth audio / input devices as fallback context."""
    ps_cmd = r"""
    Get-PnpDevice -Class Bluetooth -Status OK -ErrorAction SilentlyContinue |
        Where-Object { $_.FriendlyName -notmatch "Enumerator|Adapter|Microsoft|Transporte|Protocol|RFCOMM" } |
        Select-Object -ExpandProperty FriendlyName -Unique
    """
    names = []
    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            timeout=5
        )
        for line in (res.stdout or "").splitlines():
            clean = line.strip()
            if clean and clean not in names:
                names.append(clean)
    except Exception:
        pass
    return names


def run(parameters: dict, player=None, session_memory=None) -> str:
    target = (parameters.get("device_name") or "").lower().strip()

    # 1. Check system battery
    sys_batt = None
    try:
        sb = psutil.sensors_battery()
        if sb:
            sys_batt = {
                "percent": int(sb.percent),
                "power_plugged": sb.power_plugged,
                "secsleft": sb.secsleft
            }
    except Exception:
        pass

    # 2. Check Bluetooth peripheral batteries
    bt_devices = _get_bluetooth_battery_powershell()
    connected_names = _get_connected_bluetooth_devices()

    low_battery_warnings = []
    reports = []

    # Filter if target requested
    matched_devices = []
    for d in bt_devices:
        name = d.get("name", "Dispositivo Bluetooth")
        pct = d.get("battery", 0)
        if target and target not in name.lower():
            continue
        matched_devices.append(f"{name}: {pct}%")
        if pct <= 20:
            low_battery_warnings.append(f"{name} ({pct}%)")

    # Build response message
    if matched_devices:
        reports.append("Periféricos detectados: " + ", ".join(matched_devices))
    elif connected_names:
        # Connected without explicit battery report from driver
        filt_conn = [n for n in connected_names if not target or target in n.lower()]
        if filt_conn:
            reports.append(f"Dispositivos Bluetooth conectados activos: {', '.join(filt_conn[:4])}. (El controlador no reporta porcentaje exacto de batería)")

    if sys_batt:
        plug = "conectada a la corriente" if sys_batt["power_plugged"] else "usando batería"
        reports.append(f"Batería del equipo principal al {sys_batt['percent']}% ({plug})")

    if not reports:
        msg = "No se detectaron dispositivos Bluetooth con reporte de batería activo en este momento."
    else:
        msg = ". ".join(reports) + "."
        if low_battery_warnings:
            msg += f" ⚠️ ¡Atención! Batería baja en: {', '.join(low_battery_warnings)}. Te recomiendo recargarlos pronto."

    if player:
        try:
            player.write_log(f"SENTINEL: {msg}")
        except Exception:
            pass

    return msg
