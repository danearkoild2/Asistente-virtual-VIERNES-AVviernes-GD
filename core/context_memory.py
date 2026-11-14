"""
Operational Task & Conversational Context Memory
=================================================
Remembers active entities (recent emails, queried devices, financial periods, etc.)
so conversational references ("¿Y el de Juan?", "Ábrelo", "Apágala") resolve naturally.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional


class ContextMemory:
    def __init__(self, ttl_seconds: float = 900.0):
        self._ttl = ttl_seconds
        self._store: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}
        self._recent_tools: List[str] = []
        self._active_topic: str = ""
        self._active_speaker: str = "Jesús"

    def set_entity(self, key: str, value: Any) -> None:
        """Store an operational entity (e.g. 'last_emails', 'last_device', 'last_finance')."""
        self._store[key] = value
        self._timestamps[key] = time.time()

    def get_entity(self, key: str, default: Any = None) -> Any:
        """Retrieve an operational entity if still within TTL."""
        if key not in self._store:
            return default
        if time.time() - self._timestamps.get(key, 0) > self._ttl:
            self._store.pop(key, None)
            return default
        return self._store[key]

    def set_speaker(self, user_name: str) -> None:
        if user_name:
            self._active_speaker = user_name

    def set_topic(self, topic: str) -> None:
        if topic:
            self._active_topic = topic.strip()[:120]

    def record_tool_use(self, tool_name: str, summary: str = "") -> None:
        entry = f"{tool_name}({summary[:40]})" if summary else tool_name
        self._recent_tools.append(entry)
        if len(self._recent_tools) > 8:
            self._recent_tools = self._recent_tools[-8:]

    def get_working_memory_summary(self) -> str:
        """Compact operational context block for prompt/reasoning."""
        lines = [f"Active speaker: {self._active_speaker}"]
        if self._active_topic:
            lines.append(f"Current topic: {self._active_topic}")
        if self._recent_tools:
            lines.append("Recent actions: " + " -> ".join(self._recent_tools[-4:]))
        last_file = self.get_entity("last_file")
        if last_file:
            lines.append(f"Last referenced file: {last_file}")
        last_query = self.get_entity("last_search")
        if last_query:
            lines.append(f"Last search: {last_query}")
        return "\n".join(lines)

    def find_email_by_reference(self, reference: str) -> Optional[Dict[str, Any]]:
        """
        Resolve natural conversational follow-up like 'el de Juan' or 'el de Google'
        from recently queried emails.
        """
        emails: List[Dict[str, Any]] = self.get_entity("last_emails", [])
        if not emails:
            return None

        ref = reference.lower().strip()
        # Direct index or order ("el primero", "el último", "el segundo")
        if any(w in ref for w in ("primero", "reciente", "ultimo", "último", "1")):
            return emails[0]
        if "segundo" in ref or "2" in ref:
            return emails[1] if len(emails) > 1 else emails[0]
        if "tercero" in ref or "3" in ref:
            return emails[2] if len(emails) > 2 else emails[0]

        # Match by sender name, email, or subject snippet
        for email in emails:
            sender = email.get("sender", "").lower()
            subject = email.get("subject", "").lower()
            if ref in sender or ref in subject:
                return email

        return None


# Global context memory singleton
task_context = ContextMemory()
