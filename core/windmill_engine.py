from __future__ import annotations

import importlib.util
import io
import json
import os
import sqlite3
import subprocess
import threading
import uuid
from contextlib import contextmanager, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

try:
    from wmill import Windmill as RemoteWindmill  # type: ignore
except Exception:
    RemoteWindmill = None  # type: ignore


_BASE_DIR = Path("memory") / "windmill"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class WindmillEngine:
    """Native Windmill (windmill-labs/windmill) runner for Viernes.
    Supports remote Windmill servers via `wmill.Windmill` (WINDMILL_BASE_URL / WINDMILL_TOKEN)
    and a native local Windmill-compatible script/flow/variable/job engine on Windows.
    """

    def __init__(self, base_dir: Path | str = _BASE_DIR) -> None:
        self.base_dir = Path(base_dir).resolve()
        self.scripts_dir = self.base_dir / "scripts"
        self.flows_dir = self.base_dir / "flows"
        self.db_path = self.base_dir / "windmill.db"
        self.scripts_dir.mkdir(parents=True, exist_ok=True)
        self.flows_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._remote = self._init_remote()
        self._init_db()

    def _init_remote(self) -> Any | None:
        if RemoteWindmill is None:
            return None
        base_url = os.environ.get("WINDMILL_BASE_URL", "").strip()
        token = os.environ.get("WINDMILL_TOKEN", "").strip()
        workspace = os.environ.get("WINDMILL_WORKSPACE", "admins").strip() or "admins"
        if not base_url or not token:
            return None
        try:
            return RemoteWindmill(base_url=base_url, token=token, workspace=workspace)
        except Exception:
            return None

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS variables (
                    path TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    is_secret INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    kind TEXT NOT NULL,
                    path TEXT NOT NULL,
                    status TEXT NOT NULL,
                    args_json TEXT NOT NULL,
                    result_json TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    finished_at TEXT NOT NULL
                )
                """
            )

    def _safe_rel(self, base: Path, rel_path: str) -> Path:
        clean = rel_path.strip().lstrip("/\\")
        target = (base / clean).resolve()
        if base != target and base not in target.parents:
            raise ValueError(f"Ruta fuera del workspace Windmill: {rel_path}")
        return target

    def _record_job(
        self,
        kind: str,
        path: str,
        status: str,
        args: dict[str, Any],
        result: Any,
        started_at: str,
    ) -> str:
        job_id = str(uuid.uuid4())
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO jobs (id, kind, path, status, args_json, result_json, started_at, finished_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_id,
                    kind,
                    path,
                    status,
                    json.dumps(args, ensure_ascii=False)[:4000],
                    json.dumps(result, ensure_ascii=False, default=str)[:8000],
                    started_at,
                    _utc_now(),
                ),
            )
        return job_id

    def set_variable(self, path: str, value: str, is_secret: bool = False) -> dict[str, Any]:
        path = (path or "").strip()
        if not path:
            return {"ok": False, "error": "path es obligatorio."}
        if self._remote is not None:
            try:
                self._remote.set_variable(path, value)
                return {"ok": True, "mode": "remote", "path": path}
            except Exception:
                pass
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO variables (path, value, is_secret, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(path) DO UPDATE SET
                    value = excluded.value,
                    is_secret = excluded.is_secret,
                    updated_at = excluded.updated_at
                """,
                (path, str(value), int(bool(is_secret)), _utc_now()),
            )
        return {"ok": True, "mode": "local", "path": path}

    def get_variable(self, path: str) -> dict[str, Any]:
        path = (path or "").strip()
        if not path:
            return {"ok": False, "error": "path es obligatorio."}
        if self._remote is not None:
            try:
                val = self._remote.get_variable(path)
                return {"ok": True, "mode": "remote", "path": path, "value": val}
            except Exception:
                pass
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT value, is_secret, updated_at FROM variables WHERE path = ?",
                (path,),
            ).fetchone()
            if not row:
                return {"ok": False, "error": f"Variable '{path}' no encontrada."}
            return {
                "ok": True,
                "mode": "local",
                "path": path,
                "value": "***" if row["is_secret"] else row["value"],
            }

    def create_script(self, path: str, code: str, language: str = "python") -> dict[str, Any]:
        path = (path or "").strip()
        if not path or not (code or "").strip():
            return {"ok": False, "error": "path y code son obligatorios."}
        ext = ".ps1" if language.lower() in ("powershell", "ps1") else ".py"
        if not path.endswith((".py", ".ps1")):
            path = f"{path}{ext}"
        target = self._safe_rel(self.scripts_dir, path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(code, encoding="utf-8")
        return {"ok": True, "path": str(target.relative_to(self.scripts_dir)).replace("\\", "/")}

    def run_script(self, path: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
        path = (path or "").strip()
        args = args or {}
        if not path:
            return {"ok": False, "error": "path es obligatorio."}

        if self._remote is not None:
            try:
                res = self._remote.run_script_by_path(path, args=args)
                return {"ok": True, "mode": "remote", "path": path, "result": res}
            except Exception as exc:
                return {"ok": False, "mode": "remote", "error": str(exc)}

        started_at = _utc_now()
        candidates = [path] if path.endswith((".py", ".ps1")) else [f"{path}.py", f"{path}.ps1"]
        target: Path | None = None
        for cand in candidates:
            p = self._safe_rel(self.scripts_dir, cand)
            if p.is_file():
                target = p
                break
        if target is None:
            return {"ok": False, "error": f"Script no encontrado: {path}"}

        try:
            if target.suffix == ".ps1":
                proc = subprocess.run(
                    ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(target)],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=60,
                )
                result: Any = {
                    "returncode": proc.returncode,
                    "stdout": proc.stdout[:3000],
                    "stderr": proc.stderr[:1500],
                }
                status = "success" if proc.returncode == 0 else "failure"
            else:
                spec = importlib.util.spec_from_file_location("wmill_local_script", str(target))
                if spec is None or spec.loader is None:
                    raise RuntimeError("No se pudo cargar el script Python.")
                mod = importlib.util.module_from_spec(spec)
                buf = io.StringIO()
                with redirect_stdout(buf):
                    spec.loader.exec_module(mod)
                    main_fn = getattr(mod, "main", None)
                    ret = main_fn(**args) if callable(main_fn) else None
                result = {"return": ret, "stdout": buf.getvalue()[:3000]}
                status = "success"
        except Exception as exc:
            job_id = self._record_job("script", path, "failure", args, {"error": str(exc)}, started_at)
            return {"ok": False, "job_id": job_id, "error": str(exc)}

        job_id = self._record_job("script", path, status, args, result, started_at)
        return {"ok": status == "success", "mode": "local", "job_id": job_id, "path": path, "result": result}

    def create_flow(self, path: str, steps: list[dict[str, Any]]) -> dict[str, Any]:
        path = (path or "").strip()
        if not path or not steps:
            return {"ok": False, "error": "path y steps son obligatorios."}
        if not path.endswith(".flow.json"):
            path = f"{path}.flow.json"
        target = self._safe_rel(self.flows_dir, path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps({"steps": steps}, ensure_ascii=False, indent=2), encoding="utf-8")
        return {"ok": True, "path": str(target.relative_to(self.flows_dir)).replace("\\", "/"), "steps": len(steps)}

    def run_flow(self, path: str, args: dict[str, Any] | None = None) -> dict[str, Any]:
        path = (path or "").strip()
        args = args or {}
        if not path:
            return {"ok": False, "error": "path es obligatorio."}
        if self._remote is not None:
            try:
                res = self._remote.run_flow_by_path(path, args=args)
                return {"ok": True, "mode": "remote", "path": path, "result": res}
            except Exception as exc:
                return {"ok": False, "mode": "remote", "error": str(exc)}

        started_at = _utc_now()
        flow_name = path if path.endswith(".flow.json") else f"{path}.flow.json"
        target = self._safe_rel(self.flows_dir, flow_name)
        if not target.is_file():
            return {"ok": False, "error": f"Flow no encontrado: {path}"}

        flow_def = json.loads(target.read_text(encoding="utf-8"))
        steps = flow_def.get("steps", [])
        results: dict[str, Any] = {"flow_input": args}

        for idx, step in enumerate(steps, start=1):
            step_id = str(step.get("id") or f"step_{idx}")
            script_path = str(step.get("script_path", "")).strip()
            step_args = dict(step.get("args") or {})
            for k, v in list(step_args.items()):
                if isinstance(v, str) and v.startswith("results."):
                    ref_id = v.split(".", 1)[1]
                    step_args[k] = results.get(ref_id)
            out = self.run_script(script_path, step_args)
            results[step_id] = out.get("result")
            if not out.get("ok"):
                job_id = self._record_job("flow", path, "failure", args, results, started_at)
                return {"ok": False, "job_id": job_id, "failed_step": step_id, "error": out.get("error")}

        job_id = self._record_job("flow", path, "success", args, results, started_at)
        return {"ok": True, "mode": "local", "job_id": job_id, "path": path, "results": results}

    def list_assets(self) -> dict[str, Any]:
        scripts = [
            str(p.relative_to(self.scripts_dir)).replace("\\", "/")
            for p in self.scripts_dir.rglob("*")
            if p.is_file()
        ]
        flows = [
            str(p.relative_to(self.flows_dir)).replace("\\", "/")
            for p in self.flows_dir.rglob("*.flow.json")
            if p.is_file()
        ]
        return {"ok": True, "scripts": sorted(scripts), "flows": sorted(flows)}

    def get_job(self, job_id: str) -> dict[str, Any]:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
            if not row:
                return {"ok": False, "error": f"Job '{job_id}' no encontrado."}
            data = dict(row)
            data["result"] = json.loads(data.pop("result_json", "{}"))
            data["args"] = json.loads(data.pop("args_json", "{}"))
            return {"ok": True, "job": data}

    def status(self) -> dict[str, Any]:
        assets = self.list_assets()
        with self._lock, self._connect() as conn:
            jobs_count = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
            vars_count = conn.execute("SELECT COUNT(*) FROM variables").fetchone()[0]
        return {
            "ok": True,
            "sdk_installed": RemoteWindmill is not None,
            "remote_connected": self._remote is not None,
            "workspace_dir": str(self.base_dir),
            "scripts_count": len(assets["scripts"]),
            "flows_count": len(assets["flows"]),
            "variables_count": vars_count,
            "jobs_count": jobs_count,
        }


_ENGINE: WindmillEngine | None = None
_ENGINE_LOCK = threading.Lock()


def get_windmill_engine() -> WindmillEngine:
    global _ENGINE
    if _ENGINE is None:
        with _ENGINE_LOCK:
            if _ENGINE is None:
                _ENGINE = WindmillEngine()
    return _ENGINE
