"""
Centralized Notification Center for VIERNES
============================================
Broadcasts and records alerts, state changes, and event updates across all modules.
Levels: CRITICAL 🔴, WARNING 🟠, INFORMATION 🔵, SUCCESS 🟢.
"""
from __future__ import annotations

import threading
import time
from typing import Any, Callable, Dict, List, Optional

LEVEL_CRITICAL = "CRITICAL"
LEVEL_WARNING  = "WARNING"
LEVEL_INFO     = "INFORMATION"
LEVEL_SUCCESS  = "SUCCESS"

LEVEL_ICONS = {
    LEVEL_CRITICAL: "🔴",
    LEVEL_WARNING:  "🟠",
    LEVEL_INFO:     "🔵",
    LEVEL_SUCCESS:  "🟢",
}

_LISTENERS: List[Callable[[Dict[str, Any]], None]] = []
_HISTORY: List[Dict[str, Any]] = []
_MAX_HISTORY = 100
_LOCK = threading.Lock()


def register_notification_listener(callback: Callable[[Dict[str, Any]], None]) -> None:
    """Register UI or subsystem listener to receive live notifications."""
    with _LOCK:
        if callback not in _LISTENERS:
            _LISTENERS.append(callback)


def unregister_notification_listener(callback: Callable[[Dict[str, Any]], None]) -> None:
    with _LOCK:
        if callback in _LISTENERS:
            _LISTENERS.remove(callback)


def notify(
    title: str,
    message: str,
    level: str = LEVEL_INFO,
    category: str = "SYSTEM",
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Dispatch a centralized notification to all active listeners and record history."""
    level = level.upper() if level.upper() in LEVEL_ICONS else LEVEL_INFO
    icon = LEVEL_ICONS[level]

    notif = {
        "id": f"notif_{int(time.time()*1000)}",
        "timestamp": time.strftime("%H:%M:%S"),
        "epoch": time.time(),
        "level": level,
        "icon": icon,
        "title": title,
        "message": message,
        "category": category,
        "metadata": metadata or {},
    }

    with _LOCK:
        _HISTORY.append(notif)
        if len(_HISTORY) > _MAX_HISTORY:
            _HISTORY.pop(0)
        listeners_snapshot = list(_LISTENERS)

    for cb in listeners_snapshot:
        try:
            cb(notif)
        except Exception as e:
            print(f"[NotificationCenter] Listener dispatch error: {e}")

    return notif


def get_notification_history(limit: int = 30) -> List[Dict[str, Any]]:
    """Return recent notifications ordered newest first."""
    with _LOCK:
        return list(reversed(_HISTORY[-limit:]))
