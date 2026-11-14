"""
core/langgraph_orchestrator.py — Orquestador de grafos agénticos con LangGraph para VIERNES.
"""
from __future__ import annotations

from typing import Any, Literal, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph


class WorkflowState(TypedDict):
    goal: str
    url: str
    plan: str
    evidence: str
    draft: str
    step: int
    max_steps: int
    approved: bool


_CHECKPOINTER = MemorySaver()


def _node_plan(state: WorkflowState) -> dict[str, Any]:
    from core import gemini

    prompt = (
        f"Objetivo: {state['goal']}\n"
        "Genera un plan concreto en máximo 3 pasos cortos en español para resolverlo."
    )
    plan = gemini.call(prompt, tier=gemini.FAST, timeout_ms=20000) or "1. Analizar objetivo\n2. Reunir datos\n3. Sintetizar respuesta"
    return {"plan": plan.strip(), "step": state.get("step", 0) + 1}


def _node_execute(state: WorkflowState) -> dict[str, Any]:
    from core import gemini

    evidence = state.get("evidence", "")
    url = (state.get("url") or "").strip()
    if url and not evidence:
        try:
            from core.crawl4ai_engine import crawl_url
            crawled = crawl_url(url, max_chars=3500)
            if crawled.get("ok"):
                evidence = f"[Fuente {url}]\n{crawled.get('markdown', '')}"
        except Exception as exc:
            evidence = f"[Error Crawl4AI: {exc}]"

    prompt = (
        f"Objetivo: {state['goal']}\n"
        f"Plan:\n{state['plan']}\n"
        f"Evidencia:\n{evidence or 'Sin fuente externa; usa razonamiento directo.'}\n\n"
        "Redacta una respuesta estructurada, precisa y concisa en español."
    )
    draft = gemini.call(prompt, tier=gemini.SMART, timeout_ms=30000) or "No se pudo generar respuesta."
    return {"evidence": evidence, "draft": draft.strip(), "step": state.get("step", 0) + 1}


def _node_verify(state: WorkflowState) -> dict[str, Any]:
    draft = (state.get("draft") or "").strip()
    approved = bool(draft and len(draft) >= 20) or state.get("step", 0) >= state.get("max_steps", 3)
    return {"approved": approved}


def _route_after_verify(state: WorkflowState) -> Literal["execute", "end"]:
    if state.get("approved"):
        return "end"
    if state.get("step", 0) >= state.get("max_steps", 3):
        return "end"
    return "execute"


def build_workflow_graph():
    g = StateGraph(WorkflowState)
    g.add_node("plan", _node_plan)
    g.add_node("execute", _node_execute)
    g.add_node("verify", _node_verify)
    g.add_edge(START, "plan")
    g.add_edge("plan", "execute")
    g.add_edge("execute", "verify")
    g.add_conditional_edges("verify", _route_after_verify, {"execute": "execute", "end": END})
    return g.compile(checkpointer=_CHECKPOINTER)


def run_langgraph_task(goal: str, url: str = "", thread_id: str = "viernes-default", max_steps: int = 3) -> dict[str, Any]:
    app = build_workflow_graph()
    init_state: WorkflowState = {
        "goal": goal,
        "url": url,
        "plan": "",
        "evidence": "",
        "draft": "",
        "step": 0,
        "max_steps": max(1, min(int(max_steps), 6)),
        "approved": False,
    }
    res = app.invoke(init_state, config={"configurable": {"thread_id": thread_id}})
    return {
        "ok": True,
        "thread_id": thread_id,
        "plan": res.get("plan", ""),
        "answer": res.get("draft", ""),
        "steps": res.get("step", 0),
    }
