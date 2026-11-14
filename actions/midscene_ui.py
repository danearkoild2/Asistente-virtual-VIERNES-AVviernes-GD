from __future__ import annotations

import json
from core.midscene_bridge import run_midscene_task


def midscene_ui_action(
    parameters: dict,
    response=None,
    player=None,
    session_memory=None,
    speak=None,
) -> str:
    params = parameters or {}
    url = str(params.get("url", "")).strip()
    mode = str(params.get("mode", "action")).strip().lower()
    instruction = str(params.get("instruction", "")).strip()
    target = str(params.get("target", "")).strip()
    value = str(params.get("value", "")).strip()
    headless = bool(params.get("headless", True))

    if not url:
        return json.dumps({"ok": False, "error": "url es obligatoria."}, ensure_ascii=False)

    res = run_midscene_task(
        url=url,
        mode=mode,
        instruction=instruction,
        target=target,
        value=value,
        headless=headless,
    )
    return json.dumps(res, ensure_ascii=False)


TOOL = {
    "name": "midscene_ui",
    "description": (
        "Automatización web visual con Midscene.js (@midscene/web + Playwright). "
        "Modos: action (aiAction), query (aiQuery), assert (aiAssert), tap (aiTap), input (aiInput)."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "url": {
                "type": "STRING",
                "description": "URL de destino a abrir y automatizar.",
            },
            "mode": {
                "type": "STRING",
                "description": "Modo: action | query | assert | tap | input (default action).",
            },
            "instruction": {
                "type": "STRING",
                "description": "Instrucción en lenguaje natural para aiAction/aiQuery/aiAssert.",
            },
            "target": {
                "type": "STRING",
                "description": "Elemento objetivo para tap o input.",
            },
            "value": {
                "type": "STRING",
                "description": "Texto a escribir (solo modo input).",
            },
            "headless": {
                "type": "BOOLEAN",
                "description": "Ejecutar navegador oculto (default true).",
            },
        },
        "required": ["url", "instruction"],
    },
    "handler": midscene_ui_action,
}
