from __future__ import annotations

import json


def windmill_action(
    parameters: dict,
    response=None,
    player=None,
    session_memory=None,
    speak=None,
) -> str:
    from core.windmill_engine import get_windmill_engine

    params = parameters or {}
    action = str(params.get("action", "status")).strip().lower()
    engine = get_windmill_engine()

    if action == "create_script":
        res = engine.create_script(
            str(params.get("path", "")),
            str(params.get("code", "")),
            str(params.get("language", "python")),
        )
    elif action == "run_script":
        res = engine.run_script(
            str(params.get("path", "")),
            params.get("args") if isinstance(params.get("args"), dict) else {},
        )
    elif action == "create_flow":
        steps = params.get("steps") if isinstance(params.get("steps"), list) else []
        res = engine.create_flow(str(params.get("path", "")), steps)
    elif action == "run_flow":
        res = engine.run_flow(
            str(params.get("path", "")),
            params.get("args") if isinstance(params.get("args"), dict) else {},
        )
    elif action == "set_variable":
        res = engine.set_variable(
            str(params.get("path", "")),
            str(params.get("value", "")),
            bool(params.get("is_secret", False)),
        )
    elif action == "get_variable":
        res = engine.get_variable(str(params.get("path", "")))
    elif action == "list":
        res = engine.list_assets()
    elif action == "get_job":
        res = engine.get_job(str(params.get("job_id", "")))
    elif action == "status":
        res = engine.status()
    else:
        res = {
            "ok": False,
            "error": (
                "Acción inválida. Usa: create_script, run_script, create_flow, "
                "run_flow, set_variable, get_variable, list, get_job, status."
            ),
        }

    return json.dumps(res, ensure_ascii=False, default=str)


TOOL = {
    "name": "windmill_workflow",
    "description": (
        "Motor nativo de Windmill (windmill-labs/windmill): crea y ejecuta scripts Python/PowerShell "
        "(con `def main(**args)`), flows multi-paso, variables y jobs locales o remotos (WINDMILL_BASE_URL)."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": (
                    "create_script | run_script | create_flow | run_flow | "
                    "set_variable | get_variable | list | get_job | status"
                ),
            },
            "path": {
                "type": "STRING",
                "description": "Ruta lógica del script, flow o variable (ej. f/viernes/hola).",
            },
            "code": {
                "type": "STRING",
                "description": "Código del script (para create_script).",
            },
            "language": {
                "type": "STRING",
                "description": "Lenguaje: python | powershell (default python).",
            },
            "args": {
                "type": "OBJECT",
                "description": "Argumentos JSON para run_script o run_flow.",
            },
            "steps": {
                "type": "ARRAY",
                "items": {"type": "OBJECT"},
                "description": "Lista de pasos [{id, script_path, args}] para create_flow.",
            },
            "value": {
                "type": "STRING",
                "description": "Valor para set_variable.",
            },
            "is_secret": {
                "type": "BOOLEAN",
                "description": "Marcar variable como secreta (default false).",
            },
            "job_id": {
                "type": "STRING",
                "description": "ID del job a consultar (para get_job).",
            },
        },
        "required": ["action"],
    },
    "handler": windmill_action,
}
