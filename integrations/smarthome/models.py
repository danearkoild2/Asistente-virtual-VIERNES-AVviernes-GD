"""
Smart Home Data Models for VIERNES
===================================
Defines Devices, Rooms, Scenes, and Automations.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Device:
    id: str
    name: str
    room: str
    type: str  # "light" | "switch" | "tv" | "thermostat" | "lock" | "camera" | "sensor" | "speaker"
    state: Dict[str, Any] = field(default_factory=dict)
    provider: str = "mock_iot"
    capabilities: List[str] = field(default_factory=list)
    is_online: bool = True
    is_critical: bool = False  # e.g. Smart Locks, Alarm Systems require confirmation

    def is_on(self) -> bool:
        return bool(self.state.get("power", False) or self.state.get("on", False))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "room": self.room,
            "type": self.type,
            "state": self.state,
            "provider": self.provider,
            "capabilities": self.capabilities,
            "is_online": self.is_online,
            "is_critical": self.is_critical,
            "is_on": self.is_on(),
        }


@dataclass
class Room:
    name: str
    device_ids: List[str] = field(default_factory=list)


@dataclass
class Scene:
    id: str
    name: str
    description: str = ""
    actions: List[Dict[str, Any]] = field(default_factory=list)  # list of {"device_id": ..., "state": ...}


@dataclass
class Automation:
    id: str
    name: str
    trigger: Dict[str, Any] = field(default_factory=dict)
    actions: List[Dict[str, Any]] = field(default_factory=list)
    enabled: bool = True
