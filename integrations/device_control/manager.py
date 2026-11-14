from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from typing import Any, Callable

from integrations.crypto import decrypt_secret, encrypt_secret
from integrations.device_control.adapters import get_adapter
from integrations.device_control.discovery import (
    AuthorizedNetworkPolicy,
    default_authorized_cidrs,
    mdns_discover,
    probe_manual_ip,
    send_wol,
    ssdp_discover,
)
from integrations.device_control.models import (
    ActivityEvent,
    DeviceAutomation,
    DeviceScene,
    NetworkDevice,
    StateConfidence,
    utc_now,
)
from integrations.smarthome.adapters.home_assistant import ha_client
from integrations.smarthome.smarthome_manager import smarthome
from security.audit_logger import record_audit
from security.voice_id import voice_id_engine


_STATE_FILE = Path(__file__).resolve().parent.parent.parent / "config" / "device_control_state.json"
_CREDS_FILE = Path(__file__).resolve().parent.parent.parent / "config" / "device_control_creds.enc"


class DeviceControlManager:
    """Enterprise Device Control Hub for Viernes."""

    def __init__(
        self,
        state_file: Path | str = _STATE_FILE,
        creds_file: Path | str = _CREDS_FILE,
    ) -> None:
        self._state_file = Path(state_file)
        self._creds_file = Path(creds_file)
        self._lock = threading.RLock()
        self._listeners: list[Callable[[ActivityEvent], None]] = []

        self._devices: dict[str, NetworkDevice] = {}
        self._discovered: dict[str, NetworkDevice] = {}
        self._scenes: dict[str, DeviceScene] = {}
        self._automations: dict[str, DeviceAutomation] = {}
        self._history: list[ActivityEvent] = []
        self._creds: dict[str, dict[str, Any]] = {}
        self._allowed_cidrs: list[str] = default_authorized_cidrs()
        self._mqtt_config: dict[str, Any] = {"host": "", "port": 1883, "topic_prefix": "viernes/devices"}

        self._init_default_scenes()
        self._load_creds()
        self._load_state()
        self.sync_existing_smarthome()

    def _init_default_scenes(self) -> None:
        defaults = [
            DeviceScene(
                id="modo_cine",
                name="Modo Cine",
                description="Atenúa luces al 15%, enciende el TV principal y prepara multimedia.",
                actions=[
                    {"target": "luz", "command": "turn_on", "value": 15},
                    {"target": "televisor", "command": "power_on"},
                ],
            ),
            DeviceScene(
                id="modo_dormir",
                name="Modo Dormir",
                description="Apaga televisores, multimedia y luces activas.",
                actions=[
                    {"target": "televisor", "command": "power_off"},
                    {"target": "luces", "command": "turn_off"},
                ],
            ),
            DeviceScene(
                id="modo_ausente",
                name="Modo Ausente",
                description="Apaga dispositivos no esenciales y asegura cerraduras.",
                actions=[
                    {"target": "luces", "command": "turn_off"},
                    {"target": "multimedia", "command": "power_off"},
                ],
            ),
            DeviceScene(
                id="modo_musica",
                name="Modo Música",
                description="Activa equipos de sonido y multimedia con iluminación ambiental.",
                actions=[
                    {"target": "media", "command": "play"},
                    {"target": "luz", "command": "turn_on", "value": 45},
                ],
            ),
            DeviceScene(
                id="apagado_general",
                name="Apagado General",
                description="Apaga todos los televisores, luces, enchufes y equipos multimedia.",
                actions=[
                    {"target": "all_tv", "command": "power_off"},
                    {"target": "all_media", "command": "power_off"},
                    {"target": "luces", "command": "turn_off"},
                ],
            ),
        ]
        for s in defaults:
            self._scenes[s.id] = s

    def _load_creds(self) -> None:
        if not self._creds_file.exists():
            return
        try:
            raw = decrypt_secret(self._creds_file.read_text(encoding="utf-8"))
            if raw:
                self._creds = json.loads(raw)
        except Exception:
            self._creds = {}

    def _save_creds(self) -> None:
        self._creds_file.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self._creds, ensure_ascii=False)
        self._creds_file.write_text(encrypt_secret(payload), encoding="utf-8")

    def _load_state(self) -> None:
        if not self._state_file.exists():
            return
        try:
            data = json.loads(self._state_file.read_text(encoding="utf-8"))
            if data.get("allowed_cidrs"):
                self._allowed_cidrs = list(data["allowed_cidrs"])
            if data.get("mqtt_config"):
                self._mqtt_config.update(data["mqtt_config"])
            for d_id, d_raw in (data.get("devices") or {}).items():
                self._devices[d_id] = NetworkDevice.from_dict(d_raw)
            for s_id, s_raw in (data.get("scenes") or {}).items():
                self._scenes[s_id] = DeviceScene.from_dict(s_raw)
            for a_id, a_raw in (data.get("automations") or {}).items():
                self._automations[a_id] = DeviceAutomation.from_dict(a_raw)
            for ev in (data.get("history") or [])[-120:]:
                self._history.append(ActivityEvent(**ev))
        except Exception as exc:
            print(f"[DeviceControl] Error loading state: {exc}")

    def _save_state(self) -> None:
        with self._lock:
            self._state_file.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "allowed_cidrs": self._allowed_cidrs,
                "mqtt_config": self._mqtt_config,
                "devices": {k: v.to_dict() for k, v in self._devices.items()},
                "scenes": {k: v.to_dict() for k, v in self._scenes.items()},
                "automations": {k: v.to_dict() for k, v in self._automations.items()},
                "history": [e.to_dict() for e in self._history[-120:]],
            }
            self._state_file.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    def _emit_event(self, actor: str, device_id: str, action: str, status: str, detail: str) -> ActivityEvent:
        ev = ActivityEvent(
            timestamp=utc_now(),
            actor=actor,
            device_id=device_id,
            action=action,
            status=status,
            detail=detail,
        )
        with self._lock:
            self._history.append(ev)
            self._history = self._history[-120:]
        try:
            record_audit(f"device_control.{action}", target=device_id, status=status, detail=detail)
        except Exception:
            pass
        for cb in list(self._listeners):
            try:
                cb(ev)
            except Exception:
                pass
        self._save_state()
        return ev

    def subscribe(self, callback: Callable[[ActivityEvent], None]) -> None:
        if callback not in self._listeners:
            self._listeners.append(callback)

    def get_policy(self) -> AuthorizedNetworkPolicy:
        return AuthorizedNetworkPolicy(self._allowed_cidrs)

    def set_allowed_cidrs(self, cidrs: list[str]) -> tuple[bool, str]:
        cleaned = [c.strip() for c in cidrs if c.strip()]
        policy = AuthorizedNetworkPolicy(cleaned)
        if not policy._networks:
            return False, "Debes indicar al menos una subred privada válida (RFC1918, ej. 192.168.1.0/24)."
        with self._lock:
            self._allowed_cidrs = cleaned
        self._emit_event("user", "network_policy", "update_cidrs", "ok", f"Subredes: {cleaned}")
        return True, f"Redes autorizadas actualizadas: {', '.join(cleaned)}"

    def set_mqtt_config(self, host: str, port: int = 1883, topic_prefix: str = "viernes/devices") -> None:
        with self._lock:
            self._mqtt_config = {"host": host.strip(), "port": int(port), "topic_prefix": topic_prefix.strip()}
        self._emit_event("user", "mqtt_broker", "configure_mqtt", "ok", f"{host}:{port}")

    def sync_existing_smarthome(self) -> int:
        """Merge devices from existing SmartHomeManager / Home Assistant into Device Control."""
        count = 0
        try:
            for d in smarthome.list_devices():
                d_id = str(d["id"])
                prov = str(d.get("provider", "mock_iot"))
                proto = "home_assistant" if prov == "home_assistant" else "smarthome_local"
                cat = d.get("type", "other")
                if cat == "thermostat":
                    cat = "climate"
                if d_id not in self._devices:
                    self._devices[d_id] = NetworkDevice(
                        id=d_id,
                        name=d["name"],
                        room=d.get("room", "General"),
                        manufacturer="Home Assistant" if proto == "home_assistant" else "Viernes SmartHome",
                        model=d.get("type", "IoT"),
                        category=cat,
                        protocol=proto,
                        capabilities=list(d.get("capabilities") or ["power"]),
                        power_strategies=["api"],
                        paired=True,
                        authorized=True,
                        online=bool(d.get("is_online", True)),
                        state=dict(d.get("state") or {}),
                        state_confidence=StateConfidence.CONFIRMED.value if proto == "home_assistant" else StateConfidence.ESTIMATED.value,
                        source=proto,
                    )
                    count += 1
        except Exception:
            pass
        return count

    def discover_devices(self, timeout: float = 2.2) -> list[NetworkDevice]:
        """Run authorized LAN discovery via SSDP/UPnP and mDNS/Zeroconf."""
        policy = self.get_policy()
        found: dict[str, NetworkDevice] = {}

        for dev in ssdp_discover(policy, timeout=timeout):
            found[dev.id] = dev
        for dev in mdns_discover(policy, timeout=timeout):
            if dev.id in found:
                existing = found[dev.id]
                if not existing.mac and dev.mac:
                    existing.mac = dev.mac
                existing.services = list(dict.fromkeys(existing.services + dev.services))
            else:
                found[dev.id] = dev

        with self._lock:
            for d_id, dev in found.items():
                self._discovered[d_id] = dev
                if d_id in self._devices:
                    saved = self._devices[d_id]
                    saved.ip = dev.ip or saved.ip
                    saved.mac = dev.mac or saved.mac
                    saved.online = True
                    saved.last_seen = utc_now()
                    saved.state_confidence = StateConfidence.CONFIRMED.value
        self._emit_event("system", "lan", "discover", "ok", f"Detectados {len(found)} dispositivos en LAN autorizada.")
        return list(found.values())

    def connect_manual_ip(self, ip: str, name: str = "", room: str = "General") -> tuple[bool, NetworkDevice | str]:
        policy = self.get_policy()
        ok, res = probe_manual_ip(ip, policy, custom_name=name)
        if not ok or not isinstance(res, NetworkDevice):
            self._emit_event("user", ip, "connect_ip", "error", str(res))
            return False, str(res)
        res.room = room or "General"
        with self._lock:
            self._discovered[res.id] = res
        self._emit_event("user", res.id, "connect_ip", "ok", f"Detectado {res.name} ({res.protocol}) en {ip}")
        return True, res

    def authorize_and_pair(self, device_id: str, custom_name: str = "", room: str = "") -> tuple[bool, str]:
        dev = self._discovered.get(device_id) or self._devices.get(device_id)
        if not dev:
            return False, f"Dispositivo '{device_id}' no encontrado."
        adapter = get_adapter(dev.protocol)
        creds = dict(self._creds.get(device_id) or {})
        ok, msg, new_creds = adapter.pair(dev, creds)
        if not ok:
            self._emit_event("user", device_id, "pair", "error", msg)
            return False, msg
        with self._lock:
            if new_creds:
                self._creds[device_id] = {**creds, **new_creds}
                self._save_creds()
            if custom_name.strip():
                dev.name = custom_name.strip()
            if room.strip():
                dev.room = room.strip()
            dev.paired = True
            dev.authorized = True
            self._devices[dev.id] = dev
        self._emit_event("user", dev.id, "pair", "ok", msg)
        return True, msg

    def refresh_device(self, device_id: str) -> tuple[bool, NetworkDevice | None]:
        dev = self._devices.get(device_id) or self._discovered.get(device_id)
        if not dev:
            return False, None
        adapter = get_adapter(dev.protocol)
        creds = self._creds.get(device_id) or {}
        ok, new_state, conf = adapter.refresh_state(dev, creds)
        with self._lock:
            if ok:
                dev.online = True
                dev.state = new_state
                dev.state_confidence = conf
                dev.last_seen = utc_now()
            else:
                # Never mark power=False just because a device stopped responding
                dev.online = False
                dev.state_confidence = StateConfidence.UNKNOWN.value
        self._save_state()
        return ok, dev

    def list_devices(self, category: str = "", include_discovered: bool = False) -> list[NetworkDevice]:
        with self._lock:
            items = list(self._devices.values())
            if include_discovered:
                known_ids = {d.id for d in items}
                items.extend(d for d_id, d in self._discovered.items() if d_id not in known_ids)
        if category:
            cat = category.lower().strip()
            items = [d for d in items if d.category.lower() == cat]
        return items

    def list_discovered(self) -> list[NetworkDevice]:
        with self._lock:
            return list(self._discovered.values())

    def resolve_target(self, query: str, category: str = "") -> tuple[list[NetworkDevice], str]:
        q = (query or "").strip().lower()
        devs = self.list_devices(category=category, include_discovered=False)
        if not q:
            return devs, "empty"
        exact = [d for d in devs if d.id.lower() == q or d.name.lower() == q]
        if exact:
            return exact, "exact"
        partial = [d for d in devs if q in d.name.lower() or q in d.room.lower() or q in d.category.lower() or q in d.ip]
        return partial, "partial"

    def control_device(
        self,
        device_id: str,
        command: str,
        value: Any = None,
        confirmed: bool = False,
        actor: str = "viernes",
    ) -> tuple[bool, str]:
        dev = self._devices.get(device_id)
        if not dev:
            return False, f"Dispositivo '{device_id}' no está emparejado en Mis dispositivos."
        if not dev.authorized or not dev.paired:
            return False, f"'{dev.name}' requiere autorización y emparejamiento previo."

        perm = "smarthome.locks" if dev.category == "lock" else "smarthome.control"
        auth_ok, auth_msg = voice_id_engine.verify_action_authorized(perm, target=f"DeviceControl {command} {dev.name}")
        if not auth_ok:
            self._emit_event(actor, dev.id, command, "denied", auth_msg)
            return False, auth_msg

        if dev.category == "lock" and not confirmed:
            self._emit_event(actor, dev.id, command, "confirmed_required", "Requiere confirmación explícita.")
            return False, f"Acción sensible en '{dev.name}'. Confirma explícitamente para continuar."

        if dev.protocol == "smarthome_local":
            if command in ("power_on", "turn_on"):
                if value is not None:
                    ok, msg = smarthome.set_device_state(dev.id, {"power": True, "brightness": int(value)}, confirmed=confirmed)
                else:
                    ok, msg = smarthome.set_device_state(dev.id, {"power": True}, confirmed=confirmed)
            elif command in ("power_off", "turn_off"):
                ok, msg = smarthome.set_device_state(dev.id, {"power": False}, confirmed=confirmed)
            else:
                ok, msg = False, f"Comando '{command}' no disponible en dispositivo local '{dev.name}'."
            if ok:
                updated = smarthome.get_device(dev.id)
                if updated:
                    dev.state = dict(updated.state)
                dev.state_confidence = StateConfidence.ESTIMATED.value
            self._emit_event(actor, dev.id, command, "ok" if ok else "error", msg)
            return ok, msg

        if command == "wol":
            if not dev.mac:
                return False, f"'{dev.name}' no tiene dirección MAC registrada para Wake-on-LAN."
            ok, msg = send_wol(dev.mac)
            if ok:
                dev.state_confidence = StateConfidence.ESTIMATED.value
            self._emit_event(actor, dev.id, "wol", "ok" if ok else "error", msg)
            return ok, msg

        adapter = get_adapter(dev.protocol)
        creds = dict(self._creds.get(dev.id) or {})
        if dev.protocol == "mqtt":
            creds.setdefault("broker_host", self._mqtt_config.get("host", ""))
            creds.setdefault("broker_port", self._mqtt_config.get("port", 1883))

        ok, msg, conf = adapter.send_command(dev, command, value=value, creds=creds)
        with self._lock:
            if creds and creds != self._creds.get(dev.id):
                self._creds[dev.id] = creds
                self._save_creds()
            if ok:
                dev.online = True
                dev.last_seen = utc_now()
                dev.state_confidence = conf
                if command in ("power_on", "turn_on"):
                    dev.state["power"] = True
                elif command in ("power_off", "turn_off"):
                    dev.state["power"] = False
            else:
                dev.state_confidence = StateConfidence.UNKNOWN.value
        self._emit_event(actor, dev.id, command, "ok" if ok else "error", msg)
        return ok, msg

    def execute_scene(self, scene_id: str, confirmed: bool = False, actor: str = "viernes") -> tuple[bool, str]:
        sc = self._scenes.get(scene_id) or next(
            (s for s in self._scenes.values() if s.name.lower() == scene_id.lower()), None
        )
        if not sc:
            return False, f"Escena '{scene_id}' no encontrada."
        if sc.id == "apagado_general" and not confirmed:
            return False, "Apagado General afecta múltiples dispositivos. Confirma explícitamente para ejecutar."

        results: list[str] = []
        for step in sc.actions:
            target = str(step.get("target", ""))
            cmd = str(step.get("command", "power_off"))
            val = step.get("value")
            if target == "all_tv":
                devs = self.list_devices(category="tv")
            elif target == "all_media":
                devs = self.list_devices(category="media")
            elif target in ("luces", "luz"):
                devs = self.list_devices(category="light")
            else:
                devs, _ = self.resolve_target(target)
            for d in devs:
                _, m = self.control_device(d.id, cmd, value=val, confirmed=confirmed, actor=f"scene:{sc.id}")
                results.append(f"{d.name}: {m}")
        summary = f"Escena '{sc.name}' ejecutada ({len(results)} acciones)."
        self._emit_event(actor, sc.id, "execute_scene", "ok", summary)
        return True, summary

    def add_automation(
        self,
        auto_id: str,
        name: str,
        trigger_type: str,
        trigger_config: dict[str, Any],
        scene_id: str = "",
        actions: list[dict[str, Any]] | None = None,
    ) -> DeviceAutomation:
        auto = DeviceAutomation(
            id=auto_id,
            name=name,
            trigger_type=trigger_type,
            trigger_config=trigger_config,
            scene_id=scene_id,
            actions=actions or [],
            enabled=True,
        )
        with self._lock:
            self._automations[auto.id] = auto
        self._emit_event("user", auto.id, "add_automation", "ok", f"Automatización '{name}' ({trigger_type})")
        return auto

    def get_history(self, limit: int = 40) -> list[ActivityEvent]:
        with self._lock:
            return list(reversed(self._history[-limit:]))


_MANAGER: DeviceControlManager | None = None
_MGR_LOCK = threading.Lock()


def get_device_control_manager() -> DeviceControlManager:
    global _MANAGER
    if _MANAGER is None:
        with _MGR_LOCK:
            if _MANAGER is None:
                _MANAGER = DeviceControlManager()
    return _MANAGER


device_control = get_device_control_manager()
