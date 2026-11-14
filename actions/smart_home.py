"""
Smart Home Action Handler for VIERNES
======================================
Auto-discovered by core/action_loader.py.
Handles natural commands:
- "Enciende la luz de la sala"
- "Apaga todas las luces"
- "¿Qué dispositivos están encendidos?"
- "Apaga el televisor"
- "Ejecuta la escena noche"
- "Abre la cerradura principal" (con confirmación de seguridad)
"""
from __future__ import annotations

from typing import Any, Dict
from integrations.smarthome.smarthome_manager import smarthome
from security.voice_id import voice_id_engine

TOOL = {
    "name": "smart_home",
    "description": (
        "Controla dispositivos del hogar inteligente (luces, enchufes, televisor, termostato, cerraduras, "
        "y escenas como Noche o Modo Cine). Permite consultar qué dispositivos están encendidos, cambiar "
        "estados, ajustar brillo o temperatura y activar escenas. Las cerraduras requieren confirmación explícita."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "operation": {
                "type": "STRING",
                "enum": ["turn_on", "turn_off", "toggle", "list_devices", "execute_scene", "set_lock", "set_temperature"],
                "description": "Acción a realizar en el hogar inteligente.",
            },
            "target": {
                "type": "STRING",
                "description": "Nombre del dispositivo, tipo ('luces', 'televisor'), habitación ('sala', 'cocina') o escena ('noche', 'cine').",
            },
            "room": {
                "type": "STRING",
                "description": "Habitación opcional para limitar la acción (ej: 'sala', 'cocina').",
            },
            "value": {
                "type": "NUMBER",
                "description": "Valor numérico para temperatura o brillo (ej: 21.5 para grados o 50 para brillo).",
            },
            "confirmed": {
                "type": "BOOLEAN",
                "description": "Indica si el usuario confirmó explícitamente una acción sensible como abrir una cerradura.",
            },
        },
        "required": ["operation"],
    },
    "handler": None,
}


def smarthome_action(parameters: Dict[str, Any] = None, player=None, session_memory=None) -> str:
    params = parameters or {}
    op = (params.get("operation") or "list_devices").lower()
    target = (params.get("target") or "").strip()
    room = (params.get("room") or "").strip()
    val = params.get("value")
    confirmed = bool(params.get("confirmed", False))

    # 1. Voice ID & RBAC Permission Gate
    req_perm = "smarthome.locks" if (op == "set_lock" or "cerradura" in target.lower()) else "smarthome.control"
    auth_ok, auth_msg = voice_id_engine.verify_action_authorized(req_perm, target=f"SmartHome {op} {target}")
    if not auth_ok:
        if player and hasattr(player, "write_log"):
            player.write_log(f"SEC: {auth_msg}")
        return auth_msg

    # 2. List Devices / Status Check
    if op == "list_devices":
        only_on = ("encendido" in target.lower() or "prendido" in target.lower() or "activo" in target.lower())
        devs = smarthome.list_devices(room=room or None, only_on=only_on)
        if not devs:
            return "No hay dispositivos encendidos en este momento." if only_on else "No encontré dispositivos registrados con ese filtro."

        lines = []
        for d in devs:
            state_str = "Encendido" if d["is_on"] else "Apagado"
            if d["type"] == "lock":
                state_str = "Bloqueada" if d["state"].get("locked") else "Abierta"
            elif d["type"] == "thermostat":
                state_str = f"{d['state'].get('temperature', 22)}°C (Objetivo: {d['state'].get('target', 21)}°C)"
            lines.append(f"- {d['name']} [{d['room']}]: {state_str}")

        prefix = "Dispositivos encendidos:" if only_on else "Estado de dispositivos del hogar:"
        return f"{prefix}\n" + "\n".join(lines)

    # 3. Execute Scene
    if op == "execute_scene":
        scene_name = target or "noche"
        ok, msg = smarthome.execute_scene(scene_name)
        return msg

    # 4. Mass Control (e.g. "apaga todas las luces")
    if any(k in target.lower() for k in ("luces", "todas las luces", "luz")):
        if "todas" in target.lower() or not room:
            # Check if room mentioned in target string (e.g. "luz de la sala")
            for r in ["sala", "cocina", "dormitorio", "oficina", "entrada"]:
                if r in target.lower():
                    room = r
                    break
        power = (op == "turn_on")
        return smarthome.control_by_type("light", power=power, room=room or None)

    # 5. Lock Control
    if op == "set_lock" or "cerradura" in target.lower():
        dev = smarthome.get_device("lock_entrada") or smarthome.get_device(target)
        if not dev:
            return "No encontré la cerradura especificada."
        locked = False if ("abrir" in target.lower() or "desbloquear" in target.lower() or op == "turn_on") else True
        ok, msg = smarthome.set_device_state(dev.id, {"locked": locked}, confirmed=confirmed)
        return msg

    # 6. Specific Device Control
    dev = smarthome.get_device(target)
    if not dev:
        # Try finding in specific room
        devs_in_room = smarthome.list_devices(room=target)
        if devs_in_room:
            # Toggle or power first device in room
            dev = smarthome.get_device(devs_in_room[0]["id"])

    if not dev:
        return f"No encontré ningún dispositivo llamado o ubicado en '{target}'."

    new_state = {}
    if op == "turn_on":
        new_state["power"] = True
        if val is not None and "brightness" in dev.capabilities:
            new_state["brightness"] = int(val)
    elif op == "turn_off":
        new_state["power"] = False
    elif op == "toggle":
        new_state["power"] = not dev.is_on()
    elif op == "set_temperature" and "temperature" in dev.capabilities:
        if val is not None:
            new_state["target"] = float(val)

    ok, msg = smarthome.set_device_state(dev.id, new_state, confirmed=confirmed)
    return msg


TOOL["handler"] = smarthome_action
