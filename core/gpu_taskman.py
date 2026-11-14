"""
Native GPU Task Manager (gputaskman) for VIERNES.

Inspired by shanselman/gputaskman:
- Per-process GPU memory categorization (Dedicated VRAM, Shared System RAM,
  Total Committed) and hardware engine utilization (3D, Compute, Copy,
  VideoDecode, VideoEncode) via Windows WDDM Performance Counters.
- Optional NVIDIA NVML / nvidia-smi enrichment (temperature, power draw, clocks).
- Local AI & LLM workload inspector (Ollama /api/ps, LM Studio, llama.cpp,
  ONNX Runtime, PyTorch/Whisper/Diffusion processes).
- Safe process termination guard and JSON snapshot export.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional
from urllib.request import Request, urlopen

import psutil

BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = BASE_DIR / "memory"

_PID_RE = re.compile(r"pid_(\d+)_luid_[^_]+_[^_]+_phys_(\d+)(?:_eng_(\d+)_engtype_([a-zA-Z0-9]+))?", re.I)

_AI_KEYWORDS = (
    "ollama",
    "llama",
    "lm studio",
    "lmstudio",
    "vllm",
    "kobold",
    "text-generation",
    "comfyui",
    "stable-diffusion",
    "whisper",
    "faster_whisper",
    "onnxruntime",
    "torch",
    "transformers",
    "ggml",
)

_PROTECTED_PROCESSES = {
    "system",
    "system idle process",
    "csrss.exe",
    "wininit.exe",
    "winlogon.exe",
    "services.exe",
    "lsass.exe",
    "smss.exe",
    "dwm.exe",
    "explorer.exe",
    "svchost.exe",
}


def _fmt_bytes(num_bytes: float) -> str:
    val = float(max(0.0, num_bytes))
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if val < 1024.0 or unit == "TB":
            return f"{val:.1f} {unit}" if unit != "B" else f"{int(val)} B"
        val /= 1024.0
    return f"{val:.1f} TB"


@dataclass
class GpuProcessInfo:
    pid: int
    name: str
    dedicated_bytes: int = 0
    shared_bytes: int = 0
    committed_bytes: int = 0
    engine_pct: dict[str, float] = field(default_factory=dict)
    total_engine_pct: float = 0.0
    cpu_pct: float = 0.0
    ram_bytes: int = 0
    cmdline: str = ""
    is_ai_workload: bool = False
    ai_runtime: str = ""

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["dedicated_human"] = _fmt_bytes(self.dedicated_bytes)
        d["shared_human"] = _fmt_bytes(self.shared_bytes)
        d["committed_human"] = _fmt_bytes(self.committed_bytes)
        d["ram_human"] = _fmt_bytes(self.ram_bytes)
        return d


@dataclass
class GpuAdapterInfo:
    name: str
    driver_version: str = ""
    video_processor: str = ""
    adapter_ram_bytes: int = 0
    dedicated_used_bytes: int = 0
    shared_used_bytes: int = 0
    total_committed_bytes: int = 0
    engine_utilization: dict[str, float] = field(default_factory=dict)
    temperature_c: Optional[float] = None
    power_w: Optional[float] = None
    nvidia_util_pct: Optional[float] = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["adapter_ram_human"] = _fmt_bytes(self.adapter_ram_bytes)
        d["dedicated_used_human"] = _fmt_bytes(self.dedicated_used_bytes)
        d["shared_used_human"] = _fmt_bytes(self.shared_used_bytes)
        d["total_committed_human"] = _fmt_bytes(self.total_committed_bytes)
        return d


def _run_ps_json(script: str, timeout: float = 10.0) -> Any:
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="ignore",
        )
        out = (proc.stdout or "").strip()
        if not out:
            return None
        return json.loads(out)
    except Exception:
        return None


def _query_wddm_counters() -> dict[str, list[dict[str, Any]]]:
    """Query Windows WDDM GPU Adapter, Process Memory, and Engine counters in one call."""
    ps_script = r"""
$ErrorActionPreference = 'SilentlyContinue'
$res = [ordered]@{}
$paths = @{
    'adapter_ded' = '\GPU Adapter Memory(*)\Dedicated Usage'
    'adapter_shr' = '\GPU Adapter Memory(*)\Shared Usage'
    'adapter_com' = '\GPU Adapter Memory(*)\Total Committed'
    'proc_ded'    = '\GPU Process Memory(*)\Dedicated Usage'
    'proc_shr'    = '\GPU Process Memory(*)\Shared Usage'
    'proc_com'    = '\GPU Process Memory(*)\Total Committed'
    'engine_util' = '\GPU Engine(*)\Utilization Percentage'
}
foreach ($k in $paths.Keys) {
    $c = Get-Counter $paths[$k]
    if ($c -and $c.CounterSamples) {
        $res[$k] = @($c.CounterSamples | ForEach-Object {
            @{ inst = $_.InstanceName; val = [double]$_.CookedValue }
        })
    } else {
        $res[$k] = @()
    }
}
$res['controllers'] = @(Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion, VideoProcessor)
$res | ConvertTo-Json -Depth 4 -Compress
"""
    data = _run_ps_json(ps_script, timeout=12.0)
    return data if isinstance(data, dict) else {}


def _query_nvidia_smi() -> list[dict[str, Any]]:
    """Optional NVIDIA telemetry if nvidia-smi is installed."""
    if not shutil.which("nvidia-smi"):
        return []
    try:
        proc = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.total,memory.used,utilization.gpu,temperature.gpu,power.draw",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            timeout=4.0,
        )
        if proc.returncode != 0:
            return []
        rows = []
        for line in (proc.stdout or "").splitlines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 6:
                rows.append({
                    "name": parts[0],
                    "mem_total_mb": float(parts[1] or 0),
                    "mem_used_mb": float(parts[2] or 0),
                    "util_pct": float(parts[3] or 0),
                    "temp_c": float(parts[4] or 0),
                    "power_w": float(parts[5] or 0),
                })
        return rows
    except Exception:
        return []


def inspect_local_ai_servers() -> dict[str, Any]:
    """Query local Ollama and LM Studio servers for live loaded models & VRAM/KV stats."""
    info: dict[str, Any] = {"ollama": None, "lm_studio": None}

    # Ollama /api/ps
    try:
        req = Request("http://127.0.0.1:11434/api/ps", headers={"Accept": "application/json"})
        with urlopen(req, timeout=1.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        models = []
        for m in data.get("models", []):
            details = m.get("details") or {}
            models.append({
                "name": m.get("name") or m.get("model", ""),
                "size_bytes": int(m.get("size", 0)),
                "size_vram_bytes": int(m.get("size_vram", 0)),
                "size_vram_human": _fmt_bytes(m.get("size_vram", 0)),
                "parameter_size": details.get("parameter_size", ""),
                "quantization": details.get("quantization_level", ""),
                "family": details.get("family", ""),
                "context_length": m.get("context_length"),
                "expires_at": m.get("expires_at", ""),
            })
        info["ollama"] = {"running": True, "models": models}
    except Exception:
        info["ollama"] = {"running": False, "models": []}

    # LM Studio /v1/models
    try:
        req = Request("http://127.0.0.1:1234/v1/models", headers={"Accept": "application/json"})
        with urlopen(req, timeout=1.5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        info["lm_studio"] = {
            "running": True,
            "models": [m.get("id", "") for m in data.get("data", [])],
        }
    except Exception:
        info["lm_studio"] = {"running": False, "models": []}

    return info


def collect_gpu_snapshot() -> dict[str, Any]:
    """Collect a full gputaskman-style GPU snapshot (adapters, processes, AI workloads)."""
    raw = _query_wddm_counters()
    nv_rows = _query_nvidia_smi()

    # 1. Process map from WDDM counters
    proc_map: dict[int, GpuProcessInfo] = {}
    engine_totals: dict[str, float] = {}

    def _get_proc(pid: int) -> GpuProcessInfo:
        if pid not in proc_map:
            name = f"pid:{pid}"
            ram = 0
            cpu = 0.0
            cmdline = ""
            try:
                p = psutil.Process(pid)
                name = p.name()
                ram = int(p.memory_info().rss)
                cpu = float(p.cpu_percent(interval=None))
                cmd_list = p.cmdline()
                cmdline = " ".join(cmd_list)[:220] if cmd_list else ""
            except Exception:
                pass
            low_sig = f"{name} {cmdline}".lower()
            ai_rt = next((kw for kw in _AI_KEYWORDS if kw in low_sig), "")
            proc_map[pid] = GpuProcessInfo(
                pid=pid,
                name=name,
                ram_bytes=ram,
                cpu_pct=cpu,
                cmdline=cmdline,
                is_ai_workload=bool(ai_rt),
                ai_runtime=ai_rt,
            )
        return proc_map[pid]

    for key, attr in (
        ("proc_ded", "dedicated_bytes"),
        ("proc_shr", "shared_bytes"),
        ("proc_com", "committed_bytes"),
    ):
        samples = raw.get(key) or []
        if isinstance(samples, dict):
            samples = [samples]
        for s in samples:
            m = _PID_RE.search(str(s.get("inst", "")))
            if not m:
                continue
            pid = int(m.group(1))
            val = int(max(0.0, float(s.get("val", 0.0))))
            pinfo = _get_proc(pid)
            setattr(pinfo, attr, getattr(pinfo, attr) + val)

    eng_samples = raw.get("engine_util") or []
    if isinstance(eng_samples, dict):
        eng_samples = [eng_samples]
    for s in eng_samples:
        val = float(max(0.0, float(s.get("val", 0.0))))
        m = _PID_RE.search(str(s.get("inst", "")))
        if not m:
            continue
        pid = int(m.group(1))
        eng_type = (m.group(4) or "Other").strip()
        if val > 0.01:
            pinfo = _get_proc(pid)
            pinfo.engine_pct[eng_type] = round(pinfo.engine_pct.get(eng_type, 0.0) + val, 2)
            pinfo.total_engine_pct = round(pinfo.total_engine_pct + val, 2)
            engine_totals[eng_type] = round(engine_totals.get(eng_type, 0.0) + val, 2)

    # 2. Adapter summary
    def _sum_samples(key: str) -> int:
        items = raw.get(key) or []
        if isinstance(items, dict):
            items = [items]
        return int(sum(max(0.0, float(x.get("val", 0.0))) for x in items))

    ded_total = _sum_samples("adapter_ded")
    shr_total = _sum_samples("adapter_shr")
    com_total = _sum_samples("adapter_com")

    controllers = raw.get("controllers") or []
    if isinstance(controllers, dict):
        controllers = [controllers]

    adapters: list[GpuAdapterInfo] = []
    for idx, ctrl in enumerate(controllers):
        cname = str(ctrl.get("Name") or f"GPU {idx}")
        nv = nv_rows[idx] if idx < len(nv_rows) else None
        adapters.append(
            GpuAdapterInfo(
                name=cname,
                driver_version=str(ctrl.get("DriverVersion") or ""),
                video_processor=str(ctrl.get("VideoProcessor") or ""),
                adapter_ram_bytes=int(ctrl.get("AdapterRAM") or 0),
                dedicated_used_bytes=ded_total if idx == 0 else 0,
                shared_used_bytes=shr_total if idx == 0 else 0,
                total_committed_bytes=com_total if idx == 0 else 0,
                engine_utilization=engine_totals if idx == 0 else {},
                temperature_c=nv["temp_c"] if nv else None,
                power_w=nv["power_w"] if nv else None,
                nvidia_util_pct=nv["util_pct"] if nv else None,
            )
        )

    processes = sorted(
        proc_map.values(),
        key=lambda p: (p.dedicated_bytes, p.total_engine_pct, p.shared_bytes),
        reverse=True,
    )

    ai_servers = inspect_local_ai_servers()
    ai_processes = [p.to_dict() for p in processes if p.is_ai_workload]

    return {
        "timestamp": time.time(),
        "adapters": [a.to_dict() for a in adapters],
        "processes": [p.to_dict() for p in processes],
        "ai_workloads": {
            "servers": ai_servers,
            "processes": ai_processes,
        },
    }


def kill_gpu_process(pid: int) -> dict[str, Any]:
    """Safely terminate a GPU-consuming process (blocking critical OS & self PIDs)."""
    if pid <= 4 or pid == os.getpid():
        return {"ok": False, "reason": f"PID {pid} está protegido."}
    try:
        proc = psutil.Process(pid)
        pname = proc.name()
        if pname.lower() in _PROTECTED_PROCESSES:
            return {"ok": False, "reason": f"'{pname}' es un proceso crítico de Windows y está protegido."}
        proc.terminate()
        try:
            proc.wait(timeout=3.0)
        except psutil.TimeoutExpired:
            proc.kill()
        return {"ok": True, "pid": pid, "name": pname}
    except psutil.NoSuchProcess:
        return {"ok": False, "reason": f"El proceso PID {pid} ya no existe."}
    except Exception as exc:
        return {"ok": False, "reason": str(exc)}


def export_snapshot_json(snapshot: Optional[dict[str, Any]] = None) -> Path:
    """Write a gputaskman JSON snapshot to memory/ and return its path."""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    snap = snapshot or collect_gpu_snapshot()
    ts = time.strftime("%Y%m%d_%H%M%S")
    out_path = MEMORY_DIR / f"gpu_snapshot_{ts}.json"
    out_path.write_text(json.dumps(snap, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path
