"""
actions/gpu_taskman.py — Native GPU Task Manager (shanselman/gputaskman) tool.

Gives VIERNES granular per-process VRAM (Dedicated / Shared / Committed),
hardware engine utilization (3D, Compute, Copy, VideoDecode, VideoEncode),
local AI/LLM workload inspection (Ollama, LM Studio, PyTorch, ONNX, GGML),
safe process termination, and JSON snapshot export.
"""
from __future__ import annotations

from typing import Any

from core.gpu_taskman import (
    collect_gpu_snapshot,
    export_snapshot_json,
    inspect_local_ai_servers,
    kill_gpu_process,
)


def _format_engines(eng: dict[str, float]) -> str:
    if not eng:
        return "0%"
    parts = [f"{k}:{v:.1f}%" for k, v in sorted(eng.items(), key=lambda x: x[1], reverse=True) if v > 0.05]
    return ", ".join(parts[:4]) if parts else "0%"


def gpu_taskman(parameters: dict[str, Any] = None, player=None, **_) -> str:
    params = parameters or {}
    action = str(params.get("action") or "overview").strip().lower()
    filter_name = str(params.get("filter") or "").strip().lower()
    sort_by = str(params.get("sort_by") or "vram").strip().lower()
    limit = int(params.get("limit") or 12)
    pid = params.get("pid")

    if action == "kill_process":
        if pid is None:
            return "Specify a numeric 'pid' to terminate."
        res = kill_gpu_process(int(pid))
        if res.get("ok"):
            return f"Terminated GPU process {res['name']} (PID {res['pid']})."
        return f"Could not terminate PID {pid}: {res.get('reason')}"

    if action == "ai_inspector":
        snap = collect_gpu_snapshot()
        ai = snap["ai_workloads"]
        servers = ai["servers"]
        procs = ai["processes"]
        lines = ["=== GPU AI & LLM WORKLOAD INSPECTOR ==="]
        ol = servers.get("ollama") or {}
        if ol.get("running"):
            models = ol.get("models") or []
            lines.append(f"Ollama: RUNNING ({len(models)} loaded model(s))")
            for m in models:
                lines.append(
                    f"  - {m['name']} | VRAM: {m['size_vram_human']} | "
                    f"Params: {m.get('parameter_size') or '?'} | "
                    f"Quant: {m.get('quantization') or '?'} | Ctx: {m.get('context_length') or '?'}"
                )
        else:
            lines.append("Ollama: not running")

        lms = servers.get("lm_studio") or {}
        if lms.get("running"):
            lines.append(f"LM Studio: RUNNING ({len(lms.get('models') or [])} model(s)): {', '.join(lms.get('models') or [])}")
        else:
            lines.append("LM Studio: not running")

        lines.append(f"Detected AI GPU processes: {len(procs)}")
        for p in procs[:limit]:
            lines.append(
                f"  - PID {p['pid']} {p['name']} [{p['ai_runtime']}] | "
                f"VRAM: {p['dedicated_human']} | Shared: {p['shared_human']} | "
                f"Engines: {_format_engines(p['engine_pct'])}"
            )
        return "\n".join(lines)

    snap = collect_gpu_snapshot()

    if action == "export_json":
        out_path = export_snapshot_json(snap)
        return f"GPU Task Manager snapshot exported to {out_path}"

    adapters = snap["adapters"]
    processes = snap["processes"]

    if filter_name:
        processes = [
            p for p in processes
            if filter_name in p["name"].lower() or filter_name in (p.get("cmdline") or "").lower()
        ]

    if sort_by == "shared":
        processes.sort(key=lambda p: p["shared_bytes"], reverse=True)
    elif sort_by == "commit":
        processes.sort(key=lambda p: p["committed_bytes"], reverse=True)
    elif sort_by == "engine":
        processes.sort(key=lambda p: p["total_engine_pct"], reverse=True)
    elif sort_by == "name":
        processes.sort(key=lambda p: p["name"].lower())
    else:
        processes.sort(key=lambda p: (p["dedicated_bytes"], p["total_engine_pct"]), reverse=True)

    if action == "adapters":
        lines = ["=== GPU ADAPTERS ==="]
        for a in adapters:
            extra = []
            if a.get("temperature_c") is not None:
                extra.append(f"Temp: {a['temperature_c']:.0f}°C")
            if a.get("power_w") is not None:
                extra.append(f"Power: {a['power_w']:.1f}W")
            if a.get("nvidia_util_pct") is not None:
                extra.append(f"NV Util: {a['nvidia_util_pct']:.0f}%")
            lines.append(
                f"• {a['name']} (Driver {a['driver_version']})\n"
                f"  Adapter RAM: {a['adapter_ram_human']} | Dedicated Used: {a['dedicated_used_human']} | "
                f"Shared Used: {a['shared_used_human']} | Committed: {a['total_committed_human']}\n"
                f"  Engines: {_format_engines(a['engine_utilization'])}"
                + (f" | {' | '.join(extra)}" if extra else "")
            )
        return "\n".join(lines)

    if action == "processes":
        lines = [f"=== GPU PROCESSES (top {min(limit, len(processes))} of {len(processes)}) ==="]
        for p in processes[:limit]:
            ai_tag = f" [AI:{p['ai_runtime']}]" if p["is_ai_workload"] else ""
            lines.append(
                f"PID {p['pid']:>6} | {p['name']:<24}{ai_tag} | "
                f"VRAM: {p['dedicated_human']:>8} | Shared: {p['shared_human']:>8} | "
                f"Commit: {p['committed_human']:>8} | Eng: {_format_engines(p['engine_pct'])}"
            )
        return "\n".join(lines)

    # Default: overview
    lines = ["=== GPUTASKMAN OVERVIEW ==="]
    for a in adapters:
        lines.append(
            f"GPU: {a['name']} | Dedicated: {a['dedicated_used_human']} / {a['adapter_ram_human']} | "
            f"Shared: {a['shared_used_human']} | Engines: {_format_engines(a['engine_utilization'])}"
        )
    ol = snap["ai_workloads"]["servers"].get("ollama") or {}
    if ol.get("running"):
        lines.append(f"Ollama active models: {len(ol.get('models') or [])}")
    lines.append(f"Top GPU processes ({min(limit, len(processes))} of {len(processes)}):")
    for p in processes[:limit]:
        ai_tag = f" [AI:{p['ai_runtime']}]" if p["is_ai_workload"] else ""
        lines.append(
            f"  • {p['name']} (PID {p['pid']}){ai_tag}: VRAM {p['dedicated_human']}, "
            f"Shared {p['shared_human']}, Eng {_format_engines(p['engine_pct'])}"
        )
    return "\n".join(lines)


TOOL = {
    "name": "gpu_taskman",
    "description": (
        "Native GPU Task Manager (gputaskman). Inspects real-time GPU adapters, "
        "per-process VRAM (Dedicated, Shared system RAM, Total Committed), "
        "hardware engines (3D, Compute, Copy, VideoDecode, VideoEncode), local "
        "AI/LLM GPU workloads (Ollama, LM Studio, PyTorch, ONNX, GGML), can "
        "safely terminate a runaway GPU process by PID, or export a JSON snapshot. "
        "Use whenever the user asks what is using the GPU/VRAM, GPU usage, "
        "which processes consume graphics memory, or local AI GPU usage."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": (
                    "'overview' (default): GPU summary + top processes; "
                    "'processes': detailed per-process VRAM/engine table; "
                    "'adapters': hardware adapter & engine telemetry; "
                    "'ai_inspector': inspect local AI/LLM GPU workloads; "
                    "'kill_process': terminate a process by 'pid'; "
                    "'export_json': save full JSON snapshot to memory/."
                ),
                "enum": [
                    "overview",
                    "processes",
                    "adapters",
                    "ai_inspector",
                    "kill_process",
                    "export_json",
                ],
            },
            "filter": {
                "type": "STRING",
                "description": "Optional process name or command-line substring filter.",
            },
            "sort_by": {
                "type": "STRING",
                "description": "Sort processes by 'vram' (default), 'shared', 'commit', 'engine', or 'name'.",
                "enum": ["vram", "shared", "commit", "engine", "name"],
            },
            "limit": {
                "type": "INTEGER",
                "description": "Maximum number of processes to return (default 12).",
            },
            "pid": {
                "type": "INTEGER",
                "description": "For action='kill_process': PID of the process to terminate.",
            },
        },
        "required": ["action"],
    },
    "handler": gpu_taskman,
}
