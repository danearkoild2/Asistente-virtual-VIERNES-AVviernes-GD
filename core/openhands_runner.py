from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from core import gemini

try:
    import openhands  # type: ignore

    _OPENHANDS_SDK_AVAILABLE = True
except Exception:
    _OPENHANDS_SDK_AVAILABLE = False


class OpenHandsRunner:
    """Native OpenHands CodeAct-style autonomous engineering runner for Viernes.
    Supports remote OpenHands server (OPENHANDS_BASE_URL) or native sandboxed CodeAct loop.
    """

    def __init__(self, workspace_dir: str | Path | None = None) -> None:
        self.workspace = Path(workspace_dir or os.getcwd()).resolve()

    def _safe_path(self, rel_path: str) -> Path:
        target = (self.workspace / rel_path).resolve()
        if self.workspace != target and self.workspace not in target.parents:
            raise ValueError(f"Ruta fuera del workspace: {rel_path}")
        return target

    def _try_remote(self, task: str) -> dict[str, Any] | None:
        base_url = os.environ.get("OPENHANDS_BASE_URL", "").strip().rstrip("/")
        if not base_url:
            return None
        api_key = os.environ.get("OPENHANDS_API_KEY", "").strip()
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        req = urllib.request.Request(
            f"{base_url}/api/conversations",
            data=json.dumps({"initial_user_msg": task}).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
                return {"ok": True, "mode": "remote_openhands", "response": data}
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            return {"ok": False, "mode": "remote_openhands", "error": str(exc)}

    def _exec_action(self, action: dict[str, Any], allow_commands: bool) -> str:
        kind = str(action.get("action", "")).strip().lower()
        if kind == "read":
            p = self._safe_path(str(action.get("path", "")))
            if not p.is_file():
                return f"ERROR: Archivo no encontrado: {p.name}"
            text = p.read_text(encoding="utf-8", errors="replace")
            return text[:2500]
        if kind == "write":
            p = self._safe_path(str(action.get("path", "")))
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(str(action.get("content", "")), encoding="utf-8")
            return f"OK: Escrito {p.relative_to(self.workspace)}"
        if kind == "edit":
            p = self._safe_path(str(action.get("path", "")))
            if not p.is_file():
                return f"ERROR: Archivo no encontrado: {p.name}"
            old = str(action.get("old", ""))
            new = str(action.get("new", ""))
            content = p.read_text(encoding="utf-8", errors="replace")
            if old not in content:
                return "ERROR: Texto objetivo no encontrado para editar."
            p.write_text(content.replace(old, new, 1), encoding="utf-8")
            return f"OK: Editado {p.relative_to(self.workspace)}"
        if kind == "list":
            rel = str(action.get("path", ".")).strip() or "."
            p = self._safe_path(rel)
            if not p.is_dir():
                return f"ERROR: Directorio inválido: {rel}"
            entries = sorted(e.name + ("/" if e.is_dir() else "") for e in p.iterdir())[:60]
            return "\n".join(entries)
        if kind == "run":
            if not allow_commands:
                return "ERROR: Ejecución de comandos deshabilitada."
            cmd = str(action.get("command", "")).strip()
            if not cmd:
                return "ERROR: Comando vacío."
            proc = subprocess.run(
                cmd,
                shell=True,
                cwd=str(self.workspace),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
            out = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
            return f"exit={proc.returncode}\n{out[:1800]}"
        return f"ERROR: Acción desconocida '{kind}'."

    def run(
        self,
        task: str,
        max_steps: int = 4,
        allow_commands: bool = True,
    ) -> dict[str, Any]:
        task = (task or "").strip()
        if not task:
            return {"ok": False, "error": "task es obligatoria."}

        remote = self._try_remote(task)
        if remote is not None:
            return remote

        max_steps = max(1, min(int(max_steps or 4), 8))
        history: list[str] = []

        for step in range(1, max_steps + 1):
            prompt = (
                "Eres un agente CodeAct estilo OpenHands ejecutando tareas de ingeniería en Windows.\n"
                f"Workspace: {self.workspace}\n"
                f"Tarea: {task}\n"
                "Historial reciente:\n"
                + ("\n".join(history[-6:]) if history else "(sin pasos previos)")
                + "\n\nResponde SOLO con un JSON válido usando una de estas acciones:\n"
                '{"action":"list","path":"."}\n'
                '{"action":"read","path":"archivo.py"}\n'
                '{"action":"write","path":"archivo.py","content":"..."}\n'
                '{"action":"edit","path":"archivo.py","old":"...","new":"..."}\n'
                '{"action":"run","command":"..."}\n'
                '{"action":"finish","summary":"resumen breve en español"}\n'
            )
            raw = gemini.call(prompt, tier=gemini.SMART, timeout_ms=25000) or ""
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                lines = cleaned.splitlines()
                cleaned = "\n".join(lines[1:-1] if lines[-1].startswith("```") else lines[1:]).strip()
            try:
                act = json.loads(cleaned)
            except json.JSONDecodeError:
                history.append(f"Paso {step}: respuesta no JSON -> {cleaned[:200]}")
                continue

            if str(act.get("action", "")).lower() == "finish":
                return {
                    "ok": True,
                    "mode": "native_codeact",
                    "sdk_installed": _OPENHANDS_SDK_AVAILABLE,
                    "steps": step,
                    "summary": str(act.get("summary", "Tarea completada.")),
                }

            try:
                obs = self._exec_action(act, allow_commands=allow_commands)
            except Exception as exc:
                obs = f"ERROR: {exc}"
            history.append(f"Paso {step} ({act.get('action')}): {obs[:500]}")

        return {
            "ok": True,
            "mode": "native_codeact",
            "sdk_installed": _OPENHANDS_SDK_AVAILABLE,
            "steps": max_steps,
            "summary": "Límite de pasos alcanzado.",
            "last_observations": history[-3:],
        }


def run_openhands_task(
    task: str,
    workspace_dir: str | None = None,
    max_steps: int = 4,
    allow_commands: bool = True,
) -> dict[str, Any]:
    return OpenHandsRunner(workspace_dir=workspace_dir).run(
        task=task,
        max_steps=max_steps,
        allow_commands=allow_commands,
    )
