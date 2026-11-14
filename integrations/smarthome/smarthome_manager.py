"""
Smart Home Central Hub & Controller for VIERNES
================================================
Coordinates IoT devices, rooms, scenes, and automations.
Supports Home Assistant REST API and built-in local IoT simulation.
Enforces security confirmation on critical devices (locks, security alarms).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from integrations.smarthome.models import Device, Room, Scene, Automation
from integrations.smarthome.adapters.home_assistant import ha_client
from security.audit_logger import record_audit
from security.safe_mode import check_action_confirmation
from core.notifications import notify, LEVEL_INFO, LEVEL_SUCCESS, LEVEL_WARNING

_CONFIG_FILE = Path(__file__).resolve().parent.parent.parent / "config" / "smarthome_devices.json"


class SmartHomeManager:
    """Central Smart Home controller."""

    def __init__(self):
        self._devices: Dict[str, Device] = {}
        self._rooms: Dict[str, Room] = {}
        self._scenes: Dict[str, Scene] = {}
        self._automations: Dict[str, Automation] = {}
        self._init_defaults()
        self._load()
        if ha_client.is_connected():
            self.sync_home_assistant()

    def _init_defaults(self):
        # Default Rooms
        for r_name in ["Sala", "Cocina", "Dormitorio", "Oficina", "Entrada"]:
            self._rooms[r_name] = Room(name=r_name)

        # Default Devices
        default_devs = [
            Device("light_sala", "Luz de la Sala", "Sala", "light", {"power": False, "brightness": 100}, capabilities=["power", "brightness"]),
            Device("light_cocina", "Luz de la Cocina", "Cocina", "light", {"power": False, "brightness": 100}, capabilities=["power", "brightness"]),
            Device("light_dormitorio", "Luz del Dormitorio", "Dormitorio", "light", {"power": False, "brightness": 80}, capabilities=["power", "brightness"]),
            Device("plug_cafetera", "Cafetera Inteligente", "Cocina", "switch", {"power": False}, capabilities=["power"]),
            Device("tv_sala", "Televisor de la Sala", "Sala", "tv", {"power": False, "channel": 1, "volume": 15}, capabilities=["power", "volume"]),
            Device("thermostat_clima", "Termostato Central", "Sala", "thermostat", {"power": True, "temperature": 22.5, "target": 21.0}, capabilities=["temperature", "power"]),
            Device("lock_entrada", "Cerradura Principal", "Entrada", "lock", {"locked": True}, capabilities=["lock"], is_critical=True),
        ]
        for d in default_devs:
            self._devices[d.id] = d
            if d.room in self._rooms and d.id not in self._rooms[d.room].device_ids:
                self._rooms[d.room].device_ids.append(d.id)

        # Default Scenes
        self._scenes["noche"] = Scene(
            id="noche",
            name="Escena Noche",
            description="Apaga todas las luces, apaga el televisor y bloquea la cerradura principal.",
            actions=[
                {"device_id": "light_sala", "state": {"power": False}},
                {"device_id": "light_cocina", "state": {"power": False}},
                {"device_id": "light_dormitorio", "state": {"power": False}},
                {"device_id": "tv_sala", "state": {"power": False}},
                {"device_id": "lock_entrada", "state": {"locked": True}},
            ]
        )
        self._scenes["cine"] = Scene(
            id="cine",
            name="Modo Cine",
            description="Atenúa las luces de la sala al 15% y enciende el televisor.",
            actions=[
                {"device_id": "light_sala", "state": {"power": True, "brightness": 15}},
                {"device_id": "tv_sala", "state": {"power": True}},
            ]
        )
        self._scenes["despertar"] = Scene(
            id="despertar",
            name="Modo Despertar",
            description="Enciende luces gradualmente y activa la cafetera de la cocina.",
            actions=[
                {"device_id": "light_dormitorio", "state": {"power": True, "brightness": 100}},
                {"device_id": "light_cocina", "state": {"power": True, "brightness": 100}},
                {"device_id": "plug_cafetera", "state": {"power": True}},
            ]
        )

    def _load(self):
        if _CONFIG_FILE.exists():
            try:
                data = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
                for d_id, d_data in data.get("devices", {}).items():
                    if d_id in self._devices:
                        self._devices[d_id].state = d_data.get("state", self._devices[d_id].state)
                    else:
                        # Restore custom or HA device
                        dev = Device(
                            id=d_id,
                            name=d_data.get("name", d_id),
                            room=d_data.get("room", "General"),
                            type=d_data.get("type", "switch"),
                            state=d_data.get("state", {}),
                            provider=d_data.get("provider", "mock_iot"),
                            capabilities=d_data.get("capabilities", ["power"]),
                            is_online=d_data.get("is_online", True),
                            is_critical=d_data.get("is_critical", False),
                        )
                        self._devices[d_id] = dev
                        if dev.room not in self._rooms:
                            self._rooms[dev.room] = Room(name=dev.room)
                        if d_id not in self._rooms[dev.room].device_ids:
                            self._rooms[dev.room].device_ids.append(d_id)
            except Exception as e:
                print(f"[SmartHome] Error loading device states: {e}")

    def sync_home_assistant(self) -> Tuple[bool, str]:
        """Fetch entities from Home Assistant and integrate them into the device list."""
        if not ha_client.is_connected():
            return False, "Home Assistant no está configurado."

        states = ha_client.get_states()
        if not states:
            return False, "No se recibieron entidades de Home Assistant."

        added = 0
        supported_domains = {"light", "switch", "climate", "lock", "media_player"}

        for item in states:
            entity_id = item.get("entity_id", "")
            domain = entity_id.split(".")[0]
            if domain not in supported_domains:
                continue

            attrs = item.get("attributes", {})
            friendly_name = attrs.get("friendly_name") or entity_id
            state_val = item.get("state", "").lower()

            caps = ["power"]
            dev_type = "switch"
            is_critical = False
            state_dict: Dict[str, Any] = {"power": state_val == "on"}

            if domain == "light":
                dev_type = "light"
                caps = ["power", "brightness"]
                if "brightness" in attrs:
                    state_dict["brightness"] = int(attrs["brightness"] / 2.55)
            elif domain == "climate":
                dev_type = "thermostat"
                caps = ["temperature", "power"]
                state_dict["temperature"] = attrs.get("current_temperature", 21.0)
                state_dict["target"] = attrs.get("temperature", 21.0)
            elif domain == "lock":
                dev_type = "lock"
                caps = ["lock"]
                is_critical = True
                state_dict = {"locked": state_val == "locked"}
            elif domain == "media_player":
                dev_type = "tv"
                caps = ["power", "volume"]

            dev = Device(
                id=entity_id,
                name=friendly_name,
                room="Home Assistant",
                type=dev_type,
                state=state_dict,
                provider="home_assistant",
                capabilities=caps,
                is_online=state_val != "unavailable",
                is_critical=is_critical,
            )
            self._devices[entity_id] = dev
            added += 1

        self.save()
        return True, f"Sincronizados {added} dispositivos desde Home Assistant."

    def save(self):
        try:
            _CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "devices": {d_id: d.to_dict() for d_id, d in self._devices.items()}
            }
            _CONFIG_FILE.write_text(json.dumps(payload, indent=4, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"[SmartHome] Error saving devices: {e}")

    def list_devices(self, room: Optional[str] = None, only_on: bool = False) -> List[Dict[str, Any]]:
        """List all registered devices or filter by room / powered on."""
        results = []
        for d in self._devices.values():
            if room and room.lower() not in d.room.lower():
                continue
            if only_on and not d.is_on():
                continue
            results.append(d.to_dict())
        return results

    def get_device(self, query: str) -> Optional[Device]:
        """Find a device by ID or approximate natural name."""
        q = query.lower().strip()
        if q in self._devices:
            return self._devices[q]
        for d in self._devices.values():
            if q in d.name.lower() or q in d.id.lower():
                return d
        return None

    def set_device_state(self, device_id: str, new_state: Dict[str, Any], confirmed: bool = False) -> Tuple[bool, str]:
        """Update device state with security confirmation gate for critical items."""
        dev = self.get_device(device_id)
        if not dev:
            return False, f"Dispositivo '{device_id}' no encontrado."

        # Security Confirmation Gate
        if dev.is_critical and not confirmed:
            action_desc = "bloquear" if new_state.get("locked") else "desbloquear/abrir"
            warn_msg = f"Esta acción de seguridad requiere confirmación. ¿Deseas {action_desc} {dev.name}?"
            record_audit("SMARTHOME_CRITICAL_GATE", target=dev.name, result="CONFIRMATION_REQUIRED", reason=warn_msg)
            return False, warn_msg

        # Forward to Home Assistant if connected and device provider is home_assistant
        if dev.provider == "home_assistant" and ha_client.is_connected():
            domain = dev.id.split(".")[0]
            if "power" in new_state:
                srv = "turn_on" if new_state["power"] else "turn_off"
                ha_client.call_service(domain, srv, entity_id=dev.id)
            if "locked" in new_state:
                srv = "lock" if new_state["locked"] else "unlock"
                ha_client.call_service("lock", srv, entity_id=dev.id)
            if "target" in new_state:
                ha_client.call_service("climate", "set_temperature", entity_id=dev.id, service_data={"temperature": new_state["target"]})

        dev.state.update(new_state)
        self.save()

        # Audit & Notification
        status_txt = "encendido" if dev.is_on() else "apagado"
        if dev.type == "lock":
            status_txt = "bloqueada" if dev.state.get("locked") else "abierta/desbloqueada"

        record_audit("SMARTHOME_CONTROL", target=dev.name, result="SUCCESS", metadata={"state": dev.state})
        notify("Smart Home", f"{dev.name} ahora está {status_txt}.", LEVEL_INFO, "SMARTHOME")
        return True, f"{dev.name} ha sido {status_txt}."

    def execute_scene(self, scene_id_or_name: str) -> Tuple[bool, str]:
        """Execute a preset scene (e.g. 'noche', 'cine', 'despertar')."""
        s_key = scene_id_or_name.lower().replace("escena", "").replace("modo", "").strip()
        scene = self._scenes.get(s_key)
        if not scene:
            for s in self._scenes.values():
                if s_key in s.name.lower() or s_key in s.id.lower():
                    scene = s
                    break

        if not scene:
            return False, f"No encontré la escena '{scene_id_or_name}'."

        for action in scene.actions:
            dev_id = action.get("device_id")
            state = action.get("state", {})
            if dev_id in self._devices:
                self._devices[dev_id].state.update(state)

        self.save()
        record_audit("SMARTHOME_SCENE", target=scene.name, result="SUCCESS")
        notify("Escena Smart Home", f"La {scene.name} fue ejecutada correctamente.", LEVEL_SUCCESS, "SMARTHOME")
        return True, f"La {scene.name} fue ejecutada con éxito. {scene.description}"

    def control_by_type(self, device_type: str, power: bool, room: Optional[str] = None) -> str:
        """Mass control (e.g. 'apaga todas las luces' or 'apaga las luces de la sala')."""
        affected = []
        for dev in self._devices.values():
            if device_type.lower() in dev.type.lower():
                if room and room.lower() not in dev.room.lower():
                    continue
                dev.state["power"] = power
                affected.append(dev.name)

        self.save()
        action_word = "encendieron" if power else "apagaron"
        if affected:
            return f"Se {action_word} {len(affected)} dispositivos: {', '.join(affected)}."
        return f"No se encontraron dispositivos de tipo '{device_type}'{' en ' + room if room else ''}."


# Global Smart Home Singleton
smarthome = SmartHomeManager()
