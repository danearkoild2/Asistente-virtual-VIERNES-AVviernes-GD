from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


_RUNNER_PATH = Path(__file__).resolve().parent / "midscene_node" / "runner.mjs"


def run_midscene_task(
    url: str,
    mode: str = "action",
    instruction: str = "",
    target: str = "",
    value: str = "",
    headless: bool = True,
    timeout_s: int = 90,
) -> dict[str, Any]:
    node_bin = shutil.which("node")
    if not node_bin:
        return {"ok": False, "error": "Node.js no está disponible en PATH."}
    if not _RUNNER_PATH.exists():
        return {"ok": False, "error": f"No se encontró {_RUNNER_PATH}."}

    payload = json.dumps(
        {
            "url": url,
            "mode": mode,
            "instruction": instruction,
            "target": target,
            "value": value,
            "headless": headless,
        },
        ensure_ascii=False,
    )

    try:
        proc = subprocess.run(
            [node_bin, str(_RUNNER_PATH)],
            input=payload,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout_s,
            cwd=str(_RUNNER_PATH.parent),
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Midscene excedió timeout de {timeout_s}s."}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}

    stdout = (proc.stdout or "").strip()
    if not stdout:
        err = (proc.stderr or "").strip() or f"Código de salida {proc.returncode}"
        return {"ok": False, "error": err}

    last_line = stdout.splitlines()[-1]
    try:
        return json.loads(last_line)
    except json.JSONDecodeError:
        return {"ok": proc.returncode == 0, "raw": last_line[:1500]}
