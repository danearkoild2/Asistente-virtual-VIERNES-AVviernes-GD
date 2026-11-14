from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class StateConfidence(str, Enum):
    CONFIRMED = "confirmed"
    ESTIMATED = "estimated"
    UNKNOWN = "unknown"


class DeviceCategory(str, Enum):
    TV = "tv"
    MEDIA = "media"
    LIGHT = "light"
    CLIMATE = "climate"
    PLUG = "plug"
    FAN = "fan"
    SENSOR = "sensor"
    LOCK = "lock"
    OTHER = "other"


@dataclass
class NetworkDevice:
    id: str
    name: str
    ip: str = ""
    mac: str = ""
    manufacturer: str = "Desconocido"
    model: str = "Genérico"
    category: str = DeviceCategory.OTHER.value
    protocol: str = "generic"  # roku, samsung_tizen, lg_webos, android_tv, chromecast, apple_tv, mqtt, matter, home_assistant
    port: int = 0
    room: str = "General"
    services: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    power_strategies: list[str] = field(default_factory=list)  # api, wol, network_standby, smart_plug
    power_limitations: str = ""
    paired: bool = False
    authorized: bool = False
    online: bool = False
    state: dict[str, Any] = field(default_factory=dict)
    state_confidence: str = StateConfidence.UNKNOWN.value
    source: str = "manual"  # ssdp, mdns, manual, home_assistant, mqtt, matter
    last_seen: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NetworkDevice":
        valid = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore[attr-defined]
        filtered = {k: v for k, v in data.items() if k in valid}
        return cls(**filtered)


@dataclass
class DeviceScene:
    id: str
    name: str
    description: str
    actions: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeviceScene":
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            description=str(data.get("description", "")),
            actions=list(data.get("actions") or []),
        )


@dataclass
class DeviceAutomation:
    id: str
    name: str
    trigger_type: str  # schedule, event, sensor
    trigger_config: dict[str, Any] = field(default_factory=dict)
    scene_id: str = ""
    actions: list[dict[str, Any]] = field(default_factory=list)
    enabled: bool = True
    last_triggered: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeviceAutomation":
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            trigger_type=str(data.get("trigger_type", "schedule")),
            trigger_config=dict(data.get("trigger_config") or {}),
            scene_id=str(data.get("scene_id", "")),
            actions=list(data.get("actions") or []),
            enabled=bool(data.get("enabled", True)),
            last_triggered=str(data.get("last_triggered", "")),
        )


@dataclass
class ActivityEvent:
    timestamp: str
    actor: str
    device_id: str
    action: str
    status: str  # ok, denied, error, confirmed_required
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
