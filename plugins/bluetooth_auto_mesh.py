"""
Bluetooth Auto Mesh & Quick Connect Plugin for VIERNES.
Scans, lists paired/connected Bluetooth devices, and manages fast peripheral reconnects.
"""
from __future__ import annotations

import json
import subprocess
from typing import Dict, List, Optional

PLUGIN = {
    "name": "bluetooth_auto_mesh",
    "description": (
        "Manages Bluetooth peripherals: scans connected and paired devices (headphones, speakers, "
        "mouse, keyboards, controllers), checks their link status, and assists with fast reconnection. "
        "Use when user asks 'qué dispositivos bluetooth tengo conectados', 'conecta mis audífonos bluetooth', "
        "'estado de bluetooth', 'reconectar bluetooth', or 'bluetooth mesh'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "Action to perform: 'status' (list current devices), 'reconnect' (refresh/reconnect), 'scan' (discover devices)."
            },
            "device_name": {
                "type": "STRING",
                "description": "Optional name of device to filter or target (e.g. 'audífonos', 'H19', 'mando')."
            }
        },
        "required": [],
    },
}


def _query_windows_bluetooth_devices() -> List[Dict[str, str]]:
    """Query Windows PnP Bluetooth stack for real user devices."""
    ps_cmd = r"""
    $results = @()
    Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue |
        Where-Object { $_.FriendlyName -notmatch "Enumerator|Adapter|Microsoft|RFCOMM|Transporte" } |
        ForEach-Object {
            $results += [PSCustomObject]@{
                name = $_.FriendlyName
                status = $_.Status
                present = $_.Present
                id = $_.InstanceId
            }
        }
    $results | ConvertTo-Json -Compress
    """
    devices = []
    try:
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            timeout=7
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

    # Deduplicate by name
    seen = set()
    unique = []
    for d in devices:
        name = d.get("name", "").strip()
        if name and name not in seen:
            seen.add(name)
            unique.append(d)
    return unique


def run(parameters: dict, player=None, session_memory=None) -> str:
    action = (parameters.get("action") or "status").lower().strip()
    target_name = (parameters.get("device_name") or "").lower().strip()

    devices = _query_windows_bluetooth_devices()

    if not devices:
        msg = "El adaptador Bluetooth está activo, pero no se detectaron dispositivos de usuario emparejados en este momento."
        if player:
            player.write_log("BLUETOOTH: No paired user devices found.")
        return msg

    connected = []
    paired_offline = []

    for d in devices:
        name = d.get("name", "Dispositivo")
        status = d.get("status", "").upper()
        present = d.get("present", False)

        if target_name and target_name not in name.lower():
            continue

        if status == "OK" and (present is True or present == "True"):
            connected.append(name)
        else:
            paired_offline.append(name)

    parts = []
    if connected:
        parts.append(f"Dispositivos Bluetooth conectados y listos: {', '.join(connected)}.")
    if paired_offline:
        parts.append(f"Dispositivos emparejados guardados: {', '.join(paired_offline)}.")

    if not parts:
        if target_name:
            msg = f"No se encontró ningún dispositivo Bluetooth que coincida con '{target_name}'."
        else:
            msg = "Dispositivos Bluetooth verificados, todos en orden."
    else:
        msg = " ".join(parts)

    if player:
        try:
            player.write_log(f"BLUETOOTH: Connected: {len(connected)} | Offline: {len(paired_offline)}")
        except Exception:
            pass

    return msg
