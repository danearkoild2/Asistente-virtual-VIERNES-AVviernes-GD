from __future__ import annotations

import json
from typing import Any


def device_control_action(
    parameters: dict[str, Any] | None = None,
    response=None,
    player=None,
    session_memory=None,
    speak=None,
) -> str:
    from integrations.device_control.manager import device_control

    params = parameters or {}
    action = str(params.get("action") or "list").strip().lower()
    target = str(params.get("target") or "").strip()
    category = str(params.get("category") or "").strip().lower()
    command = str(params.get("command") or "").strip().lower()
    value = params.get("value")
    confirmed = bool(params.get("confirmed", False))
    apply_all = bool(params.get("all", False))

    if action == "discover":
        found = device_control.discover_devices()
        return json.dumps(
            {
                "ok": True,
                "discovered_count": len(found),
                "devices": [
                    {
                        "id": d.id,
                        "name": d.name,
                        "ip": d.ip,
                        "mac": d.mac,
                        "manufacturer": d.manufacturer,
                        "model": d.model,
                        "protocol": d.protocol,
                        "category": d.category,
                        "paired": d.paired,
                    }
                    for d in found
                ],
            },
            ensure_ascii=False,
        )

    if action == "connect_ip":
        ip = str(params.get("ip") or target).strip()
        ok, res = device_control.connect_manual_ip(
            ip,
            name=str(params.get("name") or ""),
            room=str(params.get("room") or "General"),
        )
        if not ok:
            return json.dumps({"ok": False, "error": res}, ensure_ascii=False)
        return json.dumps({"ok": True, "device": res.to_dict()}, ensure_ascii=False)  # type: ignore[union-attr]

    if action == "pair":
        dev_id = str(params.get("device_id") or target).strip()
        ok, msg = device_control.authorize_and_pair(
            dev_id,
            custom_name=str(params.get("name") or ""),
            room=str(params.get("room") or ""),
        )
        return json.dumps({"ok": ok, "message": msg}, ensure_ascii=False)

    if action in ("list", "status"):
        if action == "status" and target:
            matches, _ = device_control.resolve_target(target, category=category)
            for m in matches:
                device_control.refresh_device(m.id)
        else:
            matches = device_control.list_devices(category=category, include_discovered=False)
        return json.dumps(
            {
                "ok": True,
                "count": len(matches),
                "devices": [
                    {
                        "id": d.id,
                        "name": d.name,
                        "room": d.room,
                        "ip": d.ip,
                        "category": d.category,
                        "protocol": d.protocol,
                        "online": d.online,
                        "state": d.state,
                        "state_confidence": d.state_confidence,
                        "power_strategies": d.power_strategies,
                        "power_limitations": d.power_limitations,
                    }
                    for d in matches
                ],
            },
            ensure_ascii=False,
        )

    if action == "scene":
        scene_id = str(params.get("scene") or target).strip()
        ok, msg = device_control.execute_scene(scene_id, confirmed=confirmed)
        return json.dumps({"ok": ok, "message": msg}, ensure_ascii=False)

    if action == "history":
        events = [e.to_dict() for e in device_control.get_history(limit=20)]
        return json.dumps({"ok": True, "events": events}, ensure_ascii=False)

    if action == "control":
        if not command:
            return json.dumps({"ok": False, "error": "command es obligatorio para action='control'."}, ensure_ascii=False)
        matches, match_type = device_control.resolve_target(target, category=category)
        if not matches:
            return json.dumps(
                {"ok": False, "error": f"No encontré dispositivos emparejados para '{target or category}'."},
                ensure_ascii=False,
            )
        if len(matches) > 1 and not apply_all and match_type != "exact":
            return json.dumps(
                {
                    "ok": False,
                    "ambiguous": True,
                    "message": "Múltiples dispositivos coinciden; pregunta al usuario cuál controlar o usa all=true.",
                    "candidates": [{"id": d.id, "name": d.name, "room": d.room, "ip": d.ip} for d in matches],
                },
                ensure_ascii=False,
            )
        results = []
        all_ok = True
        for d in matches:
            ok, msg = device_control.control_device(d.id, command, value=value, confirmed=confirmed)
            all_ok = all_ok and ok
            results.append({"id": d.id, "name": d.name, "ok": ok, "message": msg, "state_confidence": d.state_confidence})
        return json.dumps({"ok": all_ok, "results": results}, ensure_ascii=False)

    return json.dumps(
        {
            "ok": False,
            "error": "Acción inválida. Usa: discover, connect_ip, pair, list, status, control, scene, history.",
        },
        ensure_ascii=False,
    )


TOOL = {
    "name": "device_control",
    "description": (
        "Viernes Device Control: descubrimiento LAN (SSDP/UPnP/mDNS), conexión por IP, emparejamiento y "
        "control universal de TVs (Samsung Tizen, LG webOS, Android/Google TV, Roku, Apple TV, Chromecast), "
        "multimedia, luces, clima, sensores, Wake-on-LAN, MQTT, Home Assistant y escenas domóticas."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "enum": ["discover", "connect_ip", "pair", "list", "status", "control", "scene", "history"],
                "description": "Operación del centro de dispositivos.",
            },
            "target": {
                "type": "STRING",
                "description": "Nombre, habitación, ID o IP del dispositivo (ej. 'televisor de la sala', 'luces').",
            },
            "category": {
                "type": "STRING",
                "description": "Filtro opcional: tv, media, light, climate, plug, fan, sensor, lock.",
            },
            "command": {
                "type": "STRING",
                "description": (
                    "Para control: power_on, power_off, volume_up, volume_down, mute, unmute, "
                    "up, down, left, right, ok, back, home, play, pause, stop, hdmi1..hdmi4, launch_app, wol."
                ),
            },
            "value": {
                "type": "STRING",
                "description": "Valor opcional (ej. nombre de app para launch_app como 'Netflix', o brillo).",
            },
            "ip": {
                "type": "STRING",
                "description": "IP local autorizada para connect_ip.",
            },
            "device_id": {
                "type": "STRING",
                "description": "ID del dispositivo para pair.",
            },
            "name": {
                "type": "STRING",
                "description": "Nombre personalizado opcional.",
            },
            "room": {
                "type": "STRING",
                "description": "Habitación opcional.",
            },
            "scene": {
                "type": "STRING",
                "description": "Escena: modo_cine, modo_dormir, modo_ausente, modo_musica, apagado_general.",
            },
            "all": {
                "type": "BOOLEAN",
                "description": "Aplicar comando a todos los dispositivos coincidentes (ej. todas las luces).",
            },
            "confirmed": {
                "type": "BOOLEAN",
                "description": "Confirmación explícita para acciones sensibles.",
            },
        },
        "required": ["action"],
    },
    "handler": device_control_action,
}
