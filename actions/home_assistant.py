from __future__ import annotations

import json


def home_assistant_action(
    parameters: dict,
    response=None,
    player=None,
    session_memory=None,
    speak=None,
) -> str:
    from integrations.smarthome.adapters.home_assistant import HomeAssistantAPIClient, ha_client
    from integrations.smarthome.smarthome_manager import smarthome

    params = parameters or {}
    action = str(params.get("action", "status")).strip().lower()

    if action == "status":
        ok, msg = (
            ha_client.test_connection()
            if ha_client.is_connected()
            else (False, "Home Assistant sin configurar (usa action='configure' o Ajustes → Integraciones).")
        )
        res = {
            "ok": ok,
            "connected": ha_client.is_connected(),
            "base_url": ha_client.base_url,
            "ha_api_sdk": HomeAssistantAPIClient is not None,
            "message": msg,
        }
    elif action == "configure":
        base_url = str(params.get("base_url", "")).strip()
        token = str(params.get("token", "")).strip()
        if not base_url or not token:
            res = {"ok": False, "error": "base_url y token son obligatorios."}
        else:
            ok, msg = ha_client.test_connection(base_url, token)
            if ok:
                ha_client.save_credentials(base_url, token)
                sync_ok, sync_msg = smarthome.sync_home_assistant()
                res = {"ok": True, "message": msg, "sync": {"ok": sync_ok, "message": sync_msg}}
            else:
                res = {"ok": False, "error": msg}
    elif action == "sync":
        ok, msg = smarthome.sync_home_assistant()
        res = {"ok": ok, "message": msg}
    elif action == "list_entities":
        domain_filter = str(params.get("domain", "")).strip().lower()
        states = ha_client.get_states()
        entities = []
        for s in states:
            eid = s.get("entity_id", "")
            if domain_filter and not eid.startswith(f"{domain_filter}."):
                continue
            entities.append(
                {
                    "entity_id": eid,
                    "state": s.get("state"),
                    "name": (s.get("attributes") or {}).get("friendly_name", eid),
                }
            )
        res = {"ok": ha_client.is_connected(), "count": len(entities), "entities": entities[:50]}
    elif action == "get_state":
        eid = str(params.get("entity_id", "")).strip()
        st = ha_client.get_state(eid)
        res = {"ok": st is not None, "state": st}
    elif action == "call_service":
        domain = str(params.get("domain", "")).strip()
        service = str(params.get("service", "")).strip()
        entity_id = params.get("entity_id")
        service_data = params.get("service_data") if isinstance(params.get("service_data"), dict) else None
        ok, msg = ha_client.call_service(domain, service, entity_id=entity_id, service_data=service_data)
        res = {"ok": ok, "message": msg}
    elif action == "fire_event":
        event_type = str(params.get("event_type", "")).strip()
        event_data = params.get("event_data") if isinstance(params.get("event_data"), dict) else None
        ok, msg = ha_client.fire_event(event_type, event_data=event_data)
        res = {"ok": ok, "message": msg}
    elif action == "render_template":
        tpl = str(params.get("template", "")).strip()
        ok, out = ha_client.render_template(tpl)
        res = {"ok": ok, "output": out}
    else:
        res = {
            "ok": False,
            "error": (
                "Acción inválida. Usa: status, configure, sync, list_entities, "
                "get_state, call_service, fire_event, render_template."
            ),
        }

    return json.dumps(res, ensure_ascii=False, default=str)


TOOL = {
    "name": "home_assistant",
    "description": (
        "Control y consulta directa de Home Assistant Core (API REST + homeassistant-api): "
        "status, configure, sync, list_entities, get_state, call_service, fire_event, render_template."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": (
                    "status | configure | sync | list_entities | get_state | "
                    "call_service | fire_event | render_template"
                ),
            },
            "base_url": {
                "type": "STRING",
                "description": "URL de Home Assistant (ej. http://homeassistant.local:8123) para configure.",
            },
            "token": {
                "type": "STRING",
                "description": "Long-Lived Access Token de Home Assistant para configure.",
            },
            "domain": {
                "type": "STRING",
                "description": "Dominio (light, switch, climate, automation, script, sensor).",
            },
            "service": {
                "type": "STRING",
                "description": "Servicio a llamar (turn_on, turn_off, toggle, trigger, etc.).",
            },
            "entity_id": {
                "type": "STRING",
                "description": "ID de entidad (ej. light.sala).",
            },
            "service_data": {
                "type": "OBJECT",
                "description": "Datos extra para call_service.",
            },
            "event_type": {
                "type": "STRING",
                "description": "Nombre del evento para fire_event.",
            },
            "event_data": {
                "type": "OBJECT",
                "description": "Datos JSON para fire_event.",
            },
            "template": {
                "type": "STRING",
                "description": "Plantilla Jinja2 para render_template.",
            },
        },
        "required": ["action"],
    },
    "handler": home_assistant_action,
}
