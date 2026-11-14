from __future__ import annotations

import json


def openhands_action(
    parameters: dict,
    response=None,
    player=None,
    session_memory=None,
    speak=None,
) -> str:
    from core.openhands_runner import run_openhands_task

    params = parameters or {}
    task = str(params.get("task", "")).strip()
    workspace_dir = params.get("workspace_dir")
    max_steps = int(params.get("max_steps", 4))
    allow_commands = bool(params.get("allow_commands", True))

    res = run_openhands_task(
        task=task,
        workspace_dir=workspace_dir,
        max_steps=max_steps,
        allow_commands=allow_commands,
    )
    return json.dumps(res, ensure_ascii=False)


TOOL = {
    "name": "openhands_agent",
    "description": (
        "Agente de ingeniería autónomo estilo OpenHands (CodeAct: leer, editar, escribir, ejecutar y verificar) "
        "o remoto vía OPENHANDS_BASE_URL."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "task": {
                "type": "STRING",
                "description": "Objetivo de programación o ingeniería a resolver en el workspace.",
            },
            "workspace_dir": {
                "type": "STRING",
                "description": "Ruta del workspace (opcional, usa el actual por defecto).",
            },
            "max_steps": {
                "type": "INTEGER",
                "description": "Máximo de iteraciones CodeAct (default 4, máx 8).",
            },
            "allow_commands": {
                "type": "BOOLEAN",
                "description": "Permitir comandos de terminal dentro del workspace (default true).",
            },
        },
        "required": ["task"],
    },
    "handler": openhands_action,
}
