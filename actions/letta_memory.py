from __future__ import annotations

import json


def letta_memory_action(
    parameters: dict,
    response=None,
    player=None,
    session_memory=None,
    speak=None,
) -> str:
    from core.letta_memory import get_letta_engine

    params = parameters or {}
    action = str(params.get("action", "status")).strip().lower()
    engine = get_letta_engine()

    if action == "core_read":
        res = engine.core_read(params.get("block"))
    elif action == "core_append":
        res = engine.core_append(str(params.get("block", "")), str(params.get("text", "")))
    elif action == "core_replace":
        res = engine.core_replace(
            str(params.get("block", "")),
            str(params.get("old_text", "")),
            str(params.get("text", "")),
        )
    elif action == "archival_insert":
        res = engine.archival_insert(str(params.get("text", "")), str(params.get("tags", "")))
    elif action == "archival_search":
        res = engine.archival_search(str(params.get("query", "")), int(params.get("limit", 5)))
    elif action == "status":
        res = engine.status()
    else:
        res = {
            "ok": False,
            "error": "Acción inválida. Usa: core_read, core_append, core_replace, archival_insert, archival_search, status.",
        }

    return json.dumps(res, ensure_ascii=False)


TOOL = {
    "name": "letta_memory",
    "description": (
        "Memoria persistente estilo Letta/MemGPT (bloques core_memory editables y archivo FTS5). "
        "Acciones: core_read, core_append, core_replace, archival_insert, archival_search, status."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "Operación: core_read | core_append | core_replace | archival_insert | archival_search | status",
            },
            "block": {
                "type": "STRING",
                "description": "Nombre del bloque en core_memory (ej. persona, human).",
            },
            "text": {
                "type": "STRING",
                "description": "Texto a insertar, añadir o reemplazar.",
            },
            "old_text": {
                "type": "STRING",
                "description": "Texto exacto a reemplazar (solo para core_replace).",
            },
            "query": {
                "type": "STRING",
                "description": "Consulta de búsqueda en archival_memory.",
            },
            "tags": {
                "type": "STRING",
                "description": "Etiquetas opcionales para archival_insert.",
            },
            "limit": {
                "type": "INTEGER",
                "description": "Máximo de resultados en archival_search (default 5).",
            },
        },
        "required": ["action"],
    },
    "handler": letta_memory_action,
}
