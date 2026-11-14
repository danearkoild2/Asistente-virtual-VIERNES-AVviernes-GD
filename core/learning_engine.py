"""
Autonomous Cognitive Learning & Memory Consolidation Engine for VIERNES
=======================================================================
1. Background Memory Consolidation: Extracts structured facts, preferences,
   project updates, and episodic takeaways from recent conversations silently.
2. Behavioral Habit Learning: Tracks tool/workflow patterns by time-of-day
   in memory/user_habits.json so VIERNES anticipates routines proactively.
"""
from __future__ import annotations

import json
import re
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from memory.memory_manager import (
    get_base_dir,
    record_episode,
    update_memory,
)

HABITS_PATH = get_base_dir() / "memory" / "user_habits.json"
_HABITS_LOCK = threading.Lock()
_CONSOLIDATE_LOCK = threading.Lock()


def _time_bucket(hour: int | None = None) -> str:
    h = hour if hour is not None else datetime.now().hour
    if 5 <= h < 12:
        return "morning"
    if 12 <= h < 18:
        return "afternoon"
    if 18 <= h < 23:
        return "evening"
    return "night"


class LearningEngine:
    def __init__(self):
        self._last_consolidated_idx: int = 0
        self._last_consolidate_ts: float = 0.0
        self._consolidating: bool = False
        self._habits: Dict[str, Any] = self._load_habits()

    def _load_habits(self) -> Dict[str, Any]:
        if HABITS_PATH.exists():
            try:
                data = json.loads(HABITS_PATH.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    return data
            except Exception:
                pass
        return {"tool_counts": {}, "by_time": {"morning": {}, "afternoon": {}, "evening": {}, "night": {}}}

    def _save_habits(self) -> None:
        try:
            HABITS_PATH.parent.mkdir(parents=True, exist_ok=True)
            with _HABITS_LOCK:
                HABITS_PATH.write_text(
                    json.dumps(self._habits, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
        except Exception:
            pass

    def record_tool_habit(self, tool_name: str) -> None:
        """Record tool usage by time-of-day to learn recurring user workflows."""
        if not tool_name or tool_name in ("recall_memory", "save_memory", "system_status"):
            return
        bucket = _time_bucket()
        tc = self._habits.setdefault("tool_counts", {})
        tc[tool_name] = int(tc.get(tool_name, 0)) + 1

        bt = self._habits.setdefault("by_time", {})
        tb = bt.setdefault(bucket, {})
        tb[tool_name] = int(tb.get(tool_name, 0)) + 1

        # Save asynchronously / cheaply every 3rd event to avoid disk churn
        total = sum(tc.values())
        if total % 3 == 0:
            threading.Thread(target=self._save_habits, daemon=True).start()

    def get_learned_habits_prompt(self) -> str:
        """Compact summary of learned user routines for the current time of day."""
        bucket = _time_bucket()
        tb = self._habits.get("by_time", {}).get(bucket, {})
        tc = self._habits.get("tool_counts", {})
        if not tc:
            return ""

        top_now = sorted(tb.items(), key=lambda x: x[1], reverse=True)[:3]
        top_all = sorted(tc.items(), key=lambda x: x[1], reverse=True)[:4]
        lines = []
        if top_all:
            lines.append("Most used tools overall: " + ", ".join(f"{k}({v})" for k, v in top_all))
        if top_now:
            lines.append(f"Common in {bucket}: " + ", ".join(f"{k}({v})" for k, v in top_now))
        if not lines:
            return ""
        return "[LEARNED BEHAVIORAL PATTERNS]\n" + "\n".join(f"- {l}" for l in lines) + "\n"

    def maybe_consolidate(self, session_log: List[str], force: bool = False) -> None:
        """
        Trigger background cognitive consolidation if enough new turns accrued
        (>= 8 lines since last run) or `force=True` on sleep/shutdown.
        """
        if self._consolidating or not session_log:
            return
        new_lines = len(session_log) - self._last_consolidated_idx
        if not force:
            if new_lines < 8:
                return
            if (time.monotonic() - self._last_consolidate_ts) < 90.0:
                return

        slice_lines = list(session_log[max(0, self._last_consolidated_idx - 2):])
        if len(slice_lines) < 3:
            return

        self._last_consolidated_idx = len(session_log)
        self._last_consolidate_ts = time.monotonic()
        self._consolidating = True

        threading.Thread(
            target=self._run_consolidation,
            args=(slice_lines,),
            daemon=True,
            name="ViernesLearningConsolidator",
        ).start()

    def _run_consolidation(self, lines: List[str]) -> None:
        try:
            from core import gemini
            convo = "\n".join(lines[-24:])
            prompt = (
                "Analyze this assistant-user conversation excerpt and extract ONLY durable, "
                "high-value facts worth remembering long-term (preferences, active projects, "
                "relationships, goals, recurring habits, or important decisions). "
                "Ignore small talk, greetings, or transient requests.\n"
                "Return STRICT JSON only (no markdown fences) with this exact schema:\n"
                '{"facts": [{"category": "preferences|projects|relationships|wishes|notes|identity", '
                '"key": "short_snake_case_key", "value": "concise fact in Spanish", "importance": 1-5}], '
                '"episode": {"topic": "2-4 word topic", "summary": "1 concise sentence in Spanish"}}\n\n'
                f"CONVERSATION:\n{convo}"
            )
            raw = gemini.text(prompt, model=gemini.FAST, timeout_ms=20_000)
            if not raw:
                return
            # Strip optional markdown code fences
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.IGNORECASE).strip()
            data = json.loads(cleaned)
            if not isinstance(data, dict):
                return

            facts = data.get("facts", [])
            if isinstance(facts, list) and facts:
                updates: Dict[str, Any] = {}
                valid_cats = {"identity", "preferences", "projects", "relationships", "wishes", "notes"}
                for item in facts[:6]:
                    if not isinstance(item, dict):
                        continue
                    cat = str(item.get("category", "notes")).lower().strip()
                    if cat not in valid_cats:
                        cat = "notes"
                    key = re.sub(r"[^a-z0-9_]", "_", str(item.get("key", "")).lower()).strip("_")[:48]
                    val = str(item.get("value", "")).strip()
                    imp = int(item.get("importance", 3)) if str(item.get("importance", "3")).isdigit() else 3
                    if key and val and len(val) >= 4:
                        updates.setdefault(cat, {})[key] = {"value": val, "importance": max(1, min(5, imp))}
                if updates:
                    with _CONSOLIDATE_LOCK:
                        update_memory(updates)

            ep = data.get("episode")
            if isinstance(ep, dict) and ep.get("summary"):
                with _CONSOLIDATE_LOCK:
                    record_episode(
                        topic=str(ep.get("topic", "conversación")),
                        summary=str(ep.get("summary", "")),
                    )
        except Exception as e:
            print(f"[LearningEngine] Consolidation skipped: {e}")
        finally:
            self._consolidating = False


_learning_engine: Optional[LearningEngine] = None


def get_learning_engine() -> LearningEngine:
    global _learning_engine
    if _learning_engine is None:
        _learning_engine = LearningEngine()
    return _learning_engine
