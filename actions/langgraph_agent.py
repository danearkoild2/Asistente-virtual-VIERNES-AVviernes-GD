"""
actions/langgraph_agent.py — Acción nativa de orquestación LangGraph para VIERNES.
"""
from __future__ import annotations


def langgraph_action(
    parameters: dict,
    response=None,
    player=None,
    session_memory=None,
    speak=None,
) -> str:
    from core.langgraph_orchestrator import run_langgraph_task

    p = parameters or {}
    goal = (p.get("goal") or "").strip()
    if not goal:
        return "Indica el objetivo para ejecutar el flujo LangGraph."
    url = (p.get("url") or "").strip()
    thread_id = (p.get("thread_id") or "viernes-default").strip()
    max_steps = int(p.get("max_steps", 3))

    res = run_langgraph_task(goal=goal, url=url, thread_id=thread_id, max_steps=max_steps)
    return f"[LangGraph · {res['steps']} pasos]\n\nPlan:\n{res['plan']}\n\nResultado:\n{res['answer']}"


TOOL = {
    "name": "langgraph_workflow",
    "description": "Ejecuta un flujo agéntico estructurado con LangGraph (planificación -> ejecución con Crawl4AI opcional -> verificación con estado persistente).",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "goal": {
                "type": "STRING",
                "description": "Objetivo o tarea compleja a resolver paso a paso"
            },
            "url": {
                "type": "STRING",
                "description": "URL opcional a investigar automáticamente dentro del grafo"
            },
            "thread_id": {
                "type": "STRING",
                "description": "Identificador de hilo persistente de LangGraph"
            },
            "max_steps": {
                "type": "INTEGER",
                "description": "Máximo de pasos en el grafo (default: 3)"
            }
        },
        "required": ["goal"]
    },
    "handler": langgraph_action,
}
