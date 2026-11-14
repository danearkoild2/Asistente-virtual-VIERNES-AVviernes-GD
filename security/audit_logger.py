"""
Audit Logging Subsystem for VIERNES
====================================
Maintains an immutable, structured record of every critical action executed,
denied, or held for user confirmation.
"""
from __future__ import annotations

import json
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

_LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
_AUDIT_LOG_FILE = _LOGS_DIR / "audit_trail.log"
_AUDIT_JSONL_FILE = _LOGS_DIR / "audit_trail.jsonl"
_LOCK = threading.Lock()


def record_audit(
    action: str,
    user: str = "Jesús",
    role: str = "CREATOR",
    target: str = "-",
    result: str = "SUCCESS",  # "SUCCESS" | "DENIED" | "CONFIRMATION_REQUIRED" | "PENDING"
    reason: str = "",
    metadata: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """
    Record an event in the audit trail.
    Thread-safe and persists immediately.
    """
    now = datetime.now()
    ts_str = now.strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": ts_str,
        "epoch": time.time(),
        "user": user,
        "role": role,
        "action": action,
        "target": target,
        "result": result,
        "reason": reason,
        "metadata": metadata or {},
    }

    # Human-readable format matching spec
    hr_line = f"[{now.strftime('%H:%M:%S')}] USER: {user} ({role}) | ACTION: {action} | TARGET: {target} | RESULT: {result}"
    if reason:
        hr_line += f" | REASON: {reason}"
    hr_line += "\n"

    json_line = json.dumps(entry, ensure_ascii=False) + "\n"

    try:
        with _LOCK:
            _LOGS_DIR.mkdir(parents=True, exist_ok=True)
            with open(_AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(hr_line)
            with open(_AUDIT_JSONL_FILE, "a", encoding="utf-8") as f:
                f.write(json_line)
    except Exception as e:
        print(f"[AuditLogger] Failed to write audit record: {e}")

    return entry


def get_recent_audit_logs(
    limit: int = 50,
    filter_user: Optional[str] = None,
    filter_action: Optional[str] = None,
    filter_result: Optional[str] = None,
) -> list[dict[str, Any]]:
    """Retrieve recent audit events for UI dashboard and security reviews."""
    if not _AUDIT_JSONL_FILE.exists():
        return []

    results = []
    try:
        with _LOCK:
            with open(_AUDIT_JSONL_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()

        for line in reversed(lines):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if filter_user and filter_user.lower() not in record.get("user", "").lower():
                    continue
                if filter_action and filter_action.lower() not in record.get("action", "").lower():
                    continue
                if filter_result and filter_result.upper() != record.get("result", "").upper():
                    continue
                results.append(record)
                if len(results) >= limit:
                    break
            except Exception:
                continue
    except Exception as e:
        print(f"[AuditLogger] Error reading audit records: {e}")

    return results
