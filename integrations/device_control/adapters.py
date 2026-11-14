from __future__ import annotations

import asyncio
import base64
import json
import shutil
import ssl
import subprocess
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

try:
    import websockets  # type: ignore

    _WS_AVAILABLE = True
except Exception:
    _WS_AVAILABLE = False

try:
    import paho.mqtt.publish as mqtt_publish  # type: ignore

    _MQTT_AVAILABLE = True
except Exception:
    _MQTT_AVAILABLE = False

from integrations.device_control.discovery import _tcp_open, send_wol
from integrations.device_control.models import NetworkDevice, StateConfidence, utc_now
from integrations.smarthome.adapters.home_assistant import ha_client


_ROKU_KEY_MAP = {
    "power_off": "PowerOff",
    "power_on": "PowerOn",
    "volume_up": "VolumeUp",
    "volume_down": "VolumeDown",
    "mute": "VolumeMute",
    "up": "Up",
    "down": "Down",
    "left": "Left",
    "right": "Right",
    "ok": "Select",
    "select": "Select",
    "back": "Back",
    "home": "Home",
    "play": "Play",
    "pause": "Play",
    "stop": "Home",
    "hdmi1": "InputHDMI1",
    "hdmi2": "InputHDMI2",
    "hdmi3": "InputHDMI3",
    "hdmi4": "InputHDMI4",
}

_SAMSUNG_KEY_MAP = {
    "power_off": "KEY_POWER",
    "volume_up": "KEY_VOLUP",
    "volume_down": "KEY_VOLDOWN",
    "mute": "KEY_MUTE",
    "up": "KEY_UP",
    "down": "KEY_DOWN",
    "left": "KEY_LEFT",
    "right": "KEY_RIGHT",
    "ok": "KEY_ENTER",
    "select": "KEY_ENTER",
    "back": "KEY_RETURN",
    "home": "KEY_HOME",
    "play": "KEY_PLAY",
    "pause": "KEY_PAUSE",
    "stop": "KEY_STOP",
    "hdmi1": "KEY_HDMI1",
    "hdmi2": "KEY_HDMI2",
    "hdmi3": "KEY_HDMI3",
    "hdmi4": "KEY_HDMI4",
}

_ANDROID_KEY_MAP = {
    "power_off": "26",
    "power_on": "224",
    "volume_up": "24",
    "volume_down": "25",
    "mute": "164",
    "up": "19",
    "down": "20",
    "left": "21",
    "right": "22",
    "ok": "23",
    "select": "23",
    "back": "4",
    "home": "3",
    "play": "126",
    "pause": "127",
    "stop": "86",
}


class BaseDeviceAdapter:
    def pair(self, device: NetworkDevice, creds: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
        return True, f"{device.name} autorizado.", {}

    def refresh_state(self, device: NetworkDevice, creds: dict[str, Any]) -> tuple[bool, dict[str, Any], str]:
        return False, device.state, StateConfidence.UNKNOWN.value

    def send_command(
        self,
        device: NetworkDevice,
        command: str,
        value: Any = None,
        creds: dict[str, Any] | None = None,
    ) -> tuple[bool, str, str]:
        return False, f"Comando '{command}' no soportado por el adaptador {device.protocol}.", StateConfidence.UNKNOWN.value


class RokuAdapter(BaseDeviceAdapter):
    def _base(self, device: NetworkDevice) -> str:
        return f"http://{device.ip}:{device.port or 8060}"

    def refresh_state(self, device: NetworkDevice, creds: dict[str, Any]) -> tuple[bool, dict[str, Any], str]:
        try:
            with urllib.request.urlopen(f"{self._base(device)}/query/device-info", timeout=2.0) as r:
                root = ET.fromstring(r.read(16384))
                pmode = (root.findtext("power-mode") or "PowerOn").strip()
                is_on = pmode.lower() == "poweron"
                return True, {**device.state, "power": is_on, "power_mode": pmode}, StateConfidence.CONFIRMED.value
        except Exception:
            return False, device.state, StateConfidence.UNKNOWN.value

    def send_command(self, device: NetworkDevice, command: str, value: Any = None, creds: dict[str, Any] | None = None):
        cmd = command.lower().strip()
        if cmd == "power_on":
            if not _tcp_open(device.ip, device.port or 8060, 0.5) and device.mac:
                ok, msg = send_wol(device.mac)
                return ok, msg, StateConfidence.ESTIMATED.value
        if cmd == "launch_app" and value:
            app_q = str(value).strip().lower()
            try:
                with urllib.request.urlopen(f"{self._base(device)}/query/apps", timeout=2.5) as r:
                    root = ET.fromstring(r.read(65536))
                    for app in root.findall("app"):
                        if app_q in (app.text or "").lower():
                            app_id = app.attrib.get("id", "")
                            req = urllib.request.Request(f"{self._base(device)}/launch/{app_id}", method="POST")
                            urllib.request.urlopen(req, timeout=2.5).read()
                            return True, f"Abriendo {app.text} en {device.name}.", StateConfidence.CONFIRMED.value
                return False, f"App '{value}' no encontrada en {device.name}.", StateConfidence.CONFIRMED.value
            except Exception as exc:
                return False, f"No se pudo abrir app en Roku: {exc}", StateConfidence.UNKNOWN.value

        ecp_key = _ROKU_KEY_MAP.get(cmd)
        if not ecp_key:
            return False, f"Comando '{cmd}' no soportado en Roku.", StateConfidence.UNKNOWN.value
        try:
            req = urllib.request.Request(f"{self._base(device)}/keypress/{ecp_key}", method="POST")
            urllib.request.urlopen(req, timeout=2.5).read()
            return True, f"Roku '{ecp_key}' ejecutado en {device.name}.", StateConfidence.CONFIRMED.value
        except Exception as exc:
            return False, f"Roku no respondió ({exc}).", StateConfidence.UNKNOWN.value


class SamsungTizenAdapter(BaseDeviceAdapter):
    def _ws_url(self, device: NetworkDevice, token: str = "") -> str:
        name_b64 = base64.b64encode(b"ViernesDeviceControl").decode("ascii")
        port = device.port or 8002
        scheme = "wss" if port == 8002 else "ws"
        tok_q = f"&token={urllib.parse.quote(token)}" if token else ""
        return f"{scheme}://{device.ip}:{port}/api/v2/channels/samsung.remote.control?name={name_b64}{tok_q}"

    def _run_ws(self, url: str, payload: dict[str, Any] | None = None, expect_token: bool = False):
        async def _inner():
            ssl_ctx = ssl._create_unverified_context() if url.startswith("wss://") else None
            async with websockets.connect(url, ssl=ssl_ctx, open_timeout=4, close_timeout=2) as ws:
                msg = json.loads(await asyncio.wait_for(ws.recv(), timeout=5))
                token = (msg.get("data") or {}).get("token", "")
                if payload is not None:
                    await ws.send(json.dumps(payload))
                return token, msg

        return asyncio.run(_inner())

    def pair(self, device: NetworkDevice, creds: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
        if not _WS_AVAILABLE:
            return False, "Falta paquete `websockets` para emparejar Samsung Tizen.", {}
        try:
            token, _ = self._run_ws(self._ws_url(device), expect_token=True)
            new_creds = {"token": token} if token else {}
            return True, f"Emparejado con {device.name} (acepta en pantalla del TV si aparece).", new_creds
        except Exception as exc:
            return False, f"Error emparejando Samsung Tizen: {exc}", {}

    def refresh_state(self, device: NetworkDevice, creds: dict[str, Any]):
        try:
            with urllib.request.urlopen(f"http://{device.ip}:8001/api/v2/", timeout=1.5) as r:
                info = json.loads(r.read(16384).decode("utf-8", errors="replace"))
                power_st = ((info.get("device") or {}).get("PowerState") or "on").lower()
                return True, {**device.state, "power": power_st == "on"}, StateConfidence.CONFIRMED.value
        except Exception:
            return False, device.state, StateConfidence.UNKNOWN.value

    def send_command(self, device: NetworkDevice, command: str, value: Any = None, creds: dict[str, Any] | None = None):
        cmd = command.lower().strip()
        if cmd == "power_on":
            if device.mac:
                ok, msg = send_wol(device.mac)
                return ok, msg, StateConfidence.ESTIMATED.value
            return False, "Samsung Tizen requiere MAC para encender vía Wake-on-LAN.", StateConfidence.UNKNOWN.value
        if not _WS_AVAILABLE:
            return False, "Paquete `websockets` no disponible.", StateConfidence.UNKNOWN.value
        key = _SAMSUNG_KEY_MAP.get(cmd)
        if not key:
            return False, f"Comando '{cmd}' no soportado en Samsung Tizen.", StateConfidence.UNKNOWN.value
        token = (creds or {}).get("token", "")
        payload = {
            "method": "ms.remote.control",
            "params": {
                "Cmd": "Click",
                "DataOfCmd": key,
                "Option": "false",
                "TypeOfRemote": "SendRemoteKey",
            },
        }
        try:
            new_tok, _ = self._run_ws(self._ws_url(device, token), payload=payload)
            if new_tok and creds is not None:
                creds["token"] = new_tok
            return True, f"Samsung '{key}' enviado a {device.name}.", StateConfidence.CONFIRMED.value
        except Exception as exc:
            return False, f"Samsung TV no respondió ({exc}).", StateConfidence.UNKNOWN.value


class LGWebOSAdapter(BaseDeviceAdapter):
    _URI_MAP = {
        "power_off": ("ssap://system/turnOff", {}),
        "volume_up": ("ssap://audio/volumeUp", {}),
        "volume_down": ("ssap://audio/volumeDown", {}),
        "mute": ("ssap://audio/setMute", {"mute": True}),
        "unmute": ("ssap://audio/setMute", {"mute": False}),
        "play": ("ssap://media.controls/play", {}),
        "pause": ("ssap://media.controls/pause", {}),
        "stop": ("ssap://media.controls/stop", {}),
        "home": ("ssap://system.launcher/launch", {"id": "com.webos.app.home"}),
    }

    def _ws_url(self, device: NetworkDevice) -> str:
        port = device.port or 3000
        scheme = "wss" if port == 3001 else "ws"
        return f"{scheme}://{device.ip}:{port}"

    def _ssap_call(self, device: NetworkDevice, client_key: str, uri: str | None = None, payload: dict[str, Any] | None = None):
        async def _inner():
            ssl_ctx = ssl._create_unverified_context() if (device.port == 3001) else None
            async with websockets.connect(self._ws_url(device), ssl=ssl_ctx, open_timeout=4) as ws:
                reg = {
                    "type": "register",
                    "id": "reg_1",
                    "payload": {
                        "pairingType": "PROMPT",
                        "client-key": client_key,
                        "manifest": {"manifestVersion": 1, "permissions": ["CONTROL_AUDIO", "CONTROL_POWER", "LAUNCH", "CONTROL_INPUT_MEDIA_PLAYBACK"]},
                    },
                }
                await ws.send(json.dumps(reg))
                resp = json.loads(await asyncio.wait_for(ws.recv(), timeout=8))
                new_key = (resp.get("payload") or {}).get("client-key") or client_key
                if uri:
                    await ws.send(json.dumps({"id": "cmd_1", "type": "request", "uri": uri, "payload": payload or {}}))
                    await asyncio.wait_for(ws.recv(), timeout=4)
                return new_key

        return asyncio.run(_inner())

    def pair(self, device: NetworkDevice, creds: dict[str, Any]):
        if not _WS_AVAILABLE:
            return False, "Falta paquete `websockets` para LG webOS.", {}
        try:
            key = self._ssap_call(device, creds.get("client_key", ""))
            return True, f"LG webOS emparejado ({device.name}).", {"client_key": key}
        except Exception as exc:
            return False, f"Error emparejando LG webOS: {exc}", {}

    def refresh_state(self, device: NetworkDevice, creds: dict[str, Any]):
        ok = _tcp_open(device.ip, device.port or 3000, 0.7)
        if ok:
            return True, {**device.state, "power": True}, StateConfidence.ESTIMATED.value
        return False, device.state, StateConfidence.UNKNOWN.value

    def send_command(self, device: NetworkDevice, command: str, value: Any = None, creds: dict[str, Any] | None = None):
        cmd = command.lower().strip()
        if cmd == "power_on":
            if device.mac:
                ok, msg = send_wol(device.mac)
                return ok, msg, StateConfidence.ESTIMATED.value
            return False, "LG webOS requiere MAC (Wake-on-LAN) para encendido.", StateConfidence.UNKNOWN.value
        if not _WS_AVAILABLE:
            return False, "Paquete `websockets` no disponible.", StateConfidence.UNKNOWN.value
        client_key = (creds or {}).get("client_key", "")
        if cmd == "launch_app" and value:
            uri, payload = "ssap://system.launcher/launch", {"id": str(value)}
        elif cmd in self._URI_MAP:
            uri, payload = self._URI_MAP[cmd]
        else:
            return False, f"Comando '{cmd}' no soportado en LG webOS.", StateConfidence.UNKNOWN.value
        try:
            self._ssap_call(device, client_key, uri=uri, payload=payload)
            return True, f"LG webOS ejecutó '{cmd}' en {device.name}.", StateConfidence.CONFIRMED.value
        except Exception as exc:
            return False, f"LG webOS no respondió ({exc}).", StateConfidence.UNKNOWN.value


class AndroidTVAdapter(BaseDeviceAdapter):
    def refresh_state(self, device: NetworkDevice, creds: dict[str, Any]):
        ok = _tcp_open(device.ip, device.port or 6466, 0.7) or _tcp_open(device.ip, 8008, 0.5)
        if ok:
            return True, {**device.state, "power": True}, StateConfidence.ESTIMATED.value
        return False, device.state, StateConfidence.UNKNOWN.value

    def send_command(self, device: NetworkDevice, command: str, value: Any = None, creds: dict[str, Any] | None = None):
        cmd = command.lower().strip()
        if cmd == "power_on" and device.mac and not _tcp_open(device.ip, 5555, 0.4):
            ok, msg = send_wol(device.mac)
            return ok, msg, StateConfidence.ESTIMATED.value
        adb_bin = shutil.which("adb")
        keycode = _ANDROID_KEY_MAP.get(cmd)
        if adb_bin and keycode:
            try:
                subprocess.run([adb_bin, "connect", f"{device.ip}:5555"], capture_output=True, timeout=3)
                proc = subprocess.run(
                    [adb_bin, "-s", f"{device.ip}:5555", "shell", "input", "keyevent", keycode],
                    capture_output=True,
                    text=True,
                    timeout=4,
                )
                if proc.returncode == 0:
                    return True, f"Android TV ejecutó '{cmd}' en {device.name}.", StateConfidence.CONFIRMED.value
            except Exception:
                pass
        return False, f"Android TV requiere ADB emparejado (puerto 5555) o puente Home Assistant para '{cmd}'.", StateConfidence.UNKNOWN.value


class ChromecastAdapter(BaseDeviceAdapter):
    def refresh_state(self, device: NetworkDevice, creds: dict[str, Any]):
        try:
            with urllib.request.urlopen(f"http://{device.ip}:8008/setup/eureka_info", timeout=1.5) as r:
                info = json.loads(r.read(16384).decode("utf-8", errors="replace"))
                return True, {**device.state, "power": True, "cast_name": info.get("name")}, StateConfidence.CONFIRMED.value
        except Exception:
            return False, device.state, StateConfidence.UNKNOWN.value


class AppleTVAdapter(BaseDeviceAdapter):
    def refresh_state(self, device: NetworkDevice, creds: dict[str, Any]):
        ok = _tcp_open(device.ip, device.port or 7000, 0.7)
        if ok:
            return True, {**device.state, "power": True}, StateConfidence.ESTIMATED.value
        return False, device.state, StateConfidence.UNKNOWN.value


class MQTTAdapter(BaseDeviceAdapter):
    def send_command(self, device: NetworkDevice, command: str, value: Any = None, creds: dict[str, Any] | None = None):
        if not _MQTT_AVAILABLE:
            return False, "Paquete `paho-mqtt` no disponible.", StateConfidence.UNKNOWN.value
        broker = (creds or {}).get("broker_host") or device.ip
        port = int((creds or {}).get("broker_port") or device.port or 1883)
        topic = (creds or {}).get("command_topic") or f"viernes/devices/{device.id}/set"
        payload = json.dumps({"command": command, "value": value})
        try:
            mqtt_publish.single(topic, payload=payload, hostname=broker, port=port)
            return True, f"MQTT enviado a {topic} ({command}).", StateConfidence.ESTIMATED.value
        except Exception as exc:
            return False, f"Error MQTT: {exc}", StateConfidence.UNKNOWN.value


class HomeAssistantBridgeAdapter(BaseDeviceAdapter):
    def refresh_state(self, device: NetworkDevice, creds: dict[str, Any]):
        if not ha_client.is_connected():
            return False, device.state, StateConfidence.UNKNOWN.value
        eid = device.id.removeprefix("ha_")
        st = ha_client.get_state(eid)
        if not st:
            return False, device.state, StateConfidence.UNKNOWN.value
        raw_state = str(st.get("state", "")).lower()
        if raw_state in ("unavailable", "unknown"):
            return False, device.state, StateConfidence.UNKNOWN.value
        return True, {**device.state, "power": raw_state in ("on", "playing", "idle"), "ha_state": raw_state}, StateConfidence.CONFIRMED.value

    def send_command(self, device: NetworkDevice, command: str, value: Any = None, creds: dict[str, Any] | None = None):
        if not ha_client.is_connected():
            return False, "Home Assistant no está conectado.", StateConfidence.UNKNOWN.value
        eid = device.id.removeprefix("ha_")
        domain = eid.split(".")[0]
        cmd = command.lower().strip()
        if cmd in ("power_on", "turn_on"):
            ok, msg = ha_client.call_service(domain, "turn_on", entity_id=eid)
        elif cmd in ("power_off", "turn_off"):
            ok, msg = ha_client.call_service(domain, "turn_off", entity_id=eid)
        elif cmd == "volume_up":
            ok, msg = ha_client.call_service("media_player", "volume_up", entity_id=eid)
        elif cmd == "volume_down":
            ok, msg = ha_client.call_service("media_player", "volume_down", entity_id=eid)
        elif cmd in ("mute", "unmute"):
            ok, msg = ha_client.call_service("media_player", "volume_mute", entity_id=eid, service_data={"is_volume_muted": cmd == "mute"})
        elif cmd == "play":
            ok, msg = ha_client.call_service("media_player", "media_play", entity_id=eid)
        elif cmd == "pause":
            ok, msg = ha_client.call_service("media_player", "media_pause", entity_id=eid)
        elif cmd == "stop":
            ok, msg = ha_client.call_service("media_player", "media_stop", entity_id=eid)
        else:
            return False, f"Comando '{cmd}' no mapeado en Home Assistant para {eid}.", StateConfidence.UNKNOWN.value
        return ok, msg, StateConfidence.CONFIRMED.value if ok else StateConfidence.UNKNOWN.value


_ADAPTERS: dict[str, BaseDeviceAdapter] = {
    "roku": RokuAdapter(),
    "samsung_tizen": SamsungTizenAdapter(),
    "lg_webos": LGWebOSAdapter(),
    "android_tv": AndroidTVAdapter(),
    "chromecast": ChromecastAdapter(),
    "apple_tv": AppleTVAdapter(),
    "mqtt": MQTTAdapter(),
    "home_assistant": HomeAssistantBridgeAdapter(),
}
_DEFAULT_ADAPTER = BaseDeviceAdapter()


def get_adapter(protocol: str) -> BaseDeviceAdapter:
    return _ADAPTERS.get((protocol or "").lower(), _DEFAULT_ADAPTER)
