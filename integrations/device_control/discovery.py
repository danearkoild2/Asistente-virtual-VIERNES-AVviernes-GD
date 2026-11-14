from __future__ import annotations

import ipaddress
import re
import socket
import subprocess
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

try:
    from zeroconf import ServiceBrowser, ServiceListener, Zeroconf  # type: ignore

    _ZEROCONF_AVAILABLE = True
except Exception:
    _ZEROCONF_AVAILABLE = False

from integrations.device_control.models import DeviceCategory, NetworkDevice, StateConfidence, utc_now


_SSDP_ADDR = ("239.255.255.250", 1900)
_MDNS_SERVICES = [
    "_googlecast._tcp.local.",
    "_androidtvremote2._tcp.local.",
    "_airplay._tcp.local.",
    "_companion-link._tcp.local.",
    "_matter._tcp.local.",
    "_matterc._tcp.local.",
    "_hap._tcp.local.",
    "_roku-ecp._tcp.local.",
]


def get_local_ipv4() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("192.0.2.1", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def default_authorized_cidrs() -> list[str]:
    ip = get_local_ipv4()
    try:
        addr = ipaddress.ip_address(ip)
        if addr.is_private and not addr.is_loopback:
            net = ipaddress.ip_network(f"{ip}/24", strict=False)
            return [str(net)]
    except ValueError:
        pass
    return ["192.168.0.0/16", "10.0.0.0/8", "172.16.0.0/12"]


class AuthorizedNetworkPolicy:
    """Enforces that discovery and control only target authorized private LAN subnets."""

    def __init__(self, allowed_cidrs: list[str] | None = None) -> None:
        self.allowed_cidrs = allowed_cidrs or default_authorized_cidrs()
        self._networks: list[ipaddress.IPv4Network] = []
        for cidr in self.allowed_cidrs:
            try:
                net = ipaddress.ip_network(cidr.strip(), strict=False)
                if isinstance(net, ipaddress.IPv4Network) and net.is_private:
                    self._networks.append(net)
            except ValueError:
                continue

    def is_ip_authorized(self, ip_str: str) -> bool:
        try:
            addr = ipaddress.ip_address(ip_str.strip())
        except ValueError:
            return False
        if not isinstance(addr, ipaddress.IPv4Address):
            return False
        if not addr.is_private or addr.is_multicast:
            return False
        return any(addr in net for net in self._networks)


def get_arp_table() -> dict[str, str]:
    """Read local ARP cache on Windows/POSIX to map IPv4 -> MAC."""
    mapping: dict[str, str] = {}
    try:
        proc = subprocess.run(
            ["arp", "-a"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=4,
        )
        for line in (proc.stdout or "").splitlines():
            m = re.search(
                r"(\d{1,3}(?:\.\d{1,3}){3})\s+([0-9a-fA-F]{2}(?:[:-][0-9a-fA-F]{2}){5})",
                line,
            )
            if m:
                ip, mac = m.group(1), m.group(2).replace("-", ":").upper()
                mapping[ip] = mac
    except Exception:
        pass
    return mapping


def send_wol(mac: str, broadcast_ip: str = "255.255.255.255", port: int = 9) -> tuple[bool, str]:
    """Send a Wake-on-LAN magic packet to the given MAC address."""
    clean = re.sub(r"[^0-9a-fA-F]", "", mac or "")
    if len(clean) != 12:
        return False, f"MAC inválida para Wake-on-LAN: '{mac}'"
    try:
        payload = b"\xff" * 6 + bytes.fromhex(clean) * 16
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(payload, (broadcast_ip, port))
        return True, f"Paquete Wake-on-LAN enviado a {mac}"
    except Exception as exc:
        return False, f"Error enviando Wake-on-LAN: {exc}"


def _classify_from_metadata(
    name: str, manufacturer: str, model: str, server: str = "", service_type: str = ""
) -> tuple[str, str, list[str], list[str], str]:
    blob = f"{name} {manufacturer} {model} {server} {service_type}".lower()
    if "roku" in blob:
        return (
            DeviceCategory.TV.value,
            "roku",
            ["power", "volume", "mute", "dpad", "apps", "media", "hdmi"],
            ["api", "network_standby", "wol"],
            "Roku TV permite encendido en red si 'Fast TV Start' está activo; sticks USB dependen del HDMI/TV.",
        )
    if "samsung" in blob or "tizen" in blob:
        return (
            DeviceCategory.TV.value,
            "samsung_tizen",
            ["power", "volume", "mute", "dpad", "apps", "media", "hdmi"],
            ["wol", "api", "network_standby"],
            "Samsung Tizen suele apagar el Wi-Fi al suspender; encendido remoto requiere Wake-on-LAN (LAN/WoWLAN).",
        )
    if "lg" in blob or "webos" in blob:
        return (
            DeviceCategory.TV.value,
            "lg_webos",
            ["power", "volume", "mute", "dpad", "apps", "media", "hdmi"],
            ["wol", "api", "network_standby"],
            "LG webOS requiere 'Encender con móvil (Wi-Fi/Bluetooth)' o Wake-on-LAN para encender desde reposo.",
        )
    if "androidtv" in blob or "google tv" in blob or "bravia" in blob or "shield" in blob:
        return (
            DeviceCategory.TV.value,
            "android_tv",
            ["power", "volume", "mute", "dpad", "apps", "media"],
            ["network_standby", "wol", "api"],
            "Android TV / Google TV puede requerir ADB/Remote v2 emparejado o HDMI-CEC para encendido completo.",
        )
    if "googlecast" in blob or "chromecast" in blob:
        return (
            DeviceCategory.MEDIA.value,
            "chromecast",
            ["volume", "mute", "media", "apps"],
            ["network_standby"],
            "Chromecast permanece en espera por red; no controla encendido físico del TV sin HDMI-CEC.",
        )
    if "apple" in blob or "airplay" in blob or "appletv" in blob:
        return (
            DeviceCategory.MEDIA.value,
            "apple_tv",
            ["media", "volume", "dpad"],
            ["network_standby"],
            "Apple TV requiere emparejamiento Companion/AirPlay para control completo.",
        )
    if "matter" in blob:
        return (
            DeviceCategory.OTHER.value,
            "matter",
            ["power", "status"],
            ["api"],
            "Dispositivo Matter detectado; requiere comisionamiento en fabric local o Home Assistant.",
        )
    return (
        DeviceCategory.MEDIA.value if "media" in blob or "renderer" in blob else DeviceCategory.OTHER.value,
        "upnp",
        ["status"],
        ["none"],
        "Dispositivo UPnP/genérico: capacidades limitadas al perfil anunciado.",
    )


def _fetch_upnp_xml(location: str, policy: AuthorizedNetworkPolicy) -> dict[str, str]:
    parsed = urllib.parse.urlparse(location)
    if not parsed.hostname or not policy.is_ip_authorized(parsed.hostname):
        return {}
    try:
        req = urllib.request.Request(location, headers={"User-Agent": "ViernesDeviceControl/1.0"})
        with urllib.request.urlopen(req, timeout=2.0) as resp:
            raw = resp.read(65536).decode("utf-8", errors="replace")
        root = ET.fromstring(raw)
        ns = {"upnp": "urn:schemas-upnp-org:device-1-0"}
        dev = root.find(".//upnp:device", ns) or root.find(".//device")
        if dev is None:
            return {}

        def _txt(tag: str) -> str:
            el = dev.find(f"upnp:{tag}", ns)
            if el is None:
                el = dev.find(tag)
            return (el.text or "").strip() if el is not None and el.text else ""

        return {
            "friendlyName": _txt("friendlyName"),
            "manufacturer": _txt("manufacturer"),
            "modelName": _txt("modelName"),
            "deviceType": _txt("deviceType"),
            "UDN": _txt("UDN"),
        }
    except Exception:
        return {}


def ssdp_discover(policy: AuthorizedNetworkPolicy, timeout: float = 2.2) -> list[NetworkDevice]:
    """Discover UPnP/SSDP devices on authorized LAN."""
    msg = (
        "M-SEARCH * HTTP/1.1\r\n"
        f"HOST: {_SSDP_ADDR[0]}:{_SSDP_ADDR[1]}\r\n"
        'MAN: "ssdp:discover"\r\n'
        "MX: 2\r\n"
        "ST: ssdp:all\r\n\r\n"
    ).encode("ascii")

    seen_ips: dict[str, dict[str, str]] = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(0.5)
        sock.sendto(msg, _SSDP_ADDR)
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                data, (ip, _) = sock.recvfrom(4096)
            except socket.timeout:
                continue
            if not policy.is_ip_authorized(ip):
                continue
            headers: dict[str, str] = {}
            for line in data.decode("utf-8", errors="replace").splitlines()[1:]:
                if ":" in line:
                    k, v = line.split(":", 1)
                    headers[k.strip().lower()] = v.strip()
            if ip not in seen_ips or ("location" in headers and "location" not in seen_ips[ip]):
                seen_ips[ip] = headers
    finally:
        sock.close()

    arp = get_arp_table()
    devices: list[NetworkDevice] = []
    for ip, hdr in seen_ips.items():
        loc = hdr.get("location", "")
        meta = _fetch_upnp_xml(loc, policy) if loc else {}
        name = meta.get("friendlyName") or f"Dispositivo {ip}"
        mfg = meta.get("manufacturer") or "Desconocido"
        model = meta.get("modelName") or "UPnP"
        cat, proto, caps, p_strats, p_lim = _classify_from_metadata(
            name, mfg, model, hdr.get("server", ""), hdr.get("st", "")
        )
        port = 8060 if proto == "roku" else (8001 if proto == "samsung_tizen" else (3000 if proto == "lg_webos" else 0))
        dev_id = f"lan_{proto}_{ip.replace('.', '_')}"
        devices.append(
            NetworkDevice(
                id=dev_id,
                name=name,
                ip=ip,
                mac=arp.get(ip, ""),
                manufacturer=mfg,
                model=model,
                category=cat,
                protocol=proto,
                port=port,
                services=[s for s in [hdr.get("st", ""), hdr.get("server", "")] if s][:4],
                capabilities=caps,
                power_strategies=p_strats,
                power_limitations=p_lim,
                online=True,
                state={"power": True},
                state_confidence=StateConfidence.CONFIRMED.value,
                source="ssdp",
                last_seen=utc_now(),
            )
        )
    return devices


def mdns_discover(policy: AuthorizedNetworkPolicy, timeout: float = 2.0) -> list[NetworkDevice]:
    """Discover Cast, AirPlay, Android TV, Matter, HomeKit devices via mDNS."""
    if not _ZEROCONF_AVAILABLE:
        return []

    found: dict[str, dict[str, Any]] = {}

    class _Listener(ServiceListener):
        def add_service(self, zc: Zeroconf, stype: str, name: str) -> None:
            info = zc.get_service_info(stype, name, timeout=800)
            if not info:
                return
            addrs = info.parsed_addresses()
            ip = next((a for a in addrs if policy.is_ip_authorized(a)), "")
            if not ip:
                return
            props = {
                (k.decode("utf-8", errors="ignore") if isinstance(k, bytes) else str(k)): (
                    v.decode("utf-8", errors="ignore") if isinstance(v, bytes) else str(v)
                )
                for k, v in (info.properties or {}).items()
            }
            found[f"{ip}:{stype}"] = {
                "ip": ip,
                "port": info.port or 0,
                "stype": stype,
                "name": props.get("fn") or name.split(".")[0],
                "model": props.get("md") or props.get("model") or stype,
                "props": props,
            }

        def update_service(self, zc: Zeroconf, stype: str, name: str) -> None:
            pass

        def remove_service(self, zc: Zeroconf, stype: str, name: str) -> None:
            pass

    zc = Zeroconf()
    try:
        listener = _Listener()
        for st in _MDNS_SERVICES:
            ServiceBrowser(zc, st, listener)
        time.sleep(timeout)
    finally:
        zc.close()

    arp = get_arp_table()
    devices: list[NetworkDevice] = []
    for item in found.values():
        ip = item["ip"]
        stype = item["stype"]
        name = item["name"]
        model = item["model"]
        cat, proto, caps, p_strats, p_lim = _classify_from_metadata(name, "", model, stype, stype)
        devices.append(
            NetworkDevice(
                id=f"lan_{proto}_{ip.replace('.', '_')}",
                name=name,
                ip=ip,
                mac=arp.get(ip, ""),
                manufacturer="Google" if proto == "chromecast" else ("Apple" if proto == "apple_tv" else "mDNS"),
                model=model,
                category=cat,
                protocol=proto,
                port=int(item["port"]),
                services=[stype],
                capabilities=caps,
                power_strategies=p_strats,
                power_limitations=p_lim,
                online=True,
                state={"power": True},
                state_confidence=StateConfidence.CONFIRMED.value,
                source="mdns",
                last_seen=utc_now(),
            )
        )
    return devices


def _tcp_open(ip: str, port: int, timeout: float = 0.6) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False


def probe_manual_ip(ip: str, policy: AuthorizedNetworkPolicy, custom_name: str = "") -> tuple[bool, NetworkDevice | str]:
    """Probe an authorized LAN IP for supported TV/Media/IoT protocols."""
    ip = ip.strip()
    if not policy.is_ip_authorized(ip):
        return False, f"IP no autorizada o fuera de la red local permitida: {ip}"

    arp = get_arp_table()
    mac = arp.get(ip, "")

    # 1. Roku ECP :8060
    if _tcp_open(ip, 8060):
        name, mfg, model = custom_name or f"Roku {ip}", "Roku", "Roku TV/Player"
        try:
            with urllib.request.urlopen(f"http://{ip}:8060/query/device-info", timeout=1.5) as r:
                root = ET.fromstring(r.read(16384))
                name = custom_name or (root.findtext("friendly-device-name") or root.findtext("user-device-name") or name)
                mfg = root.findtext("vendor-name") or mfg
                model = root.findtext("model-name") or model
                if not mac:
                    mac = (root.findtext("wifi-mac") or root.findtext("ethernet-mac") or "").upper()
        except Exception:
            pass
        cat, proto, caps, p_strats, p_lim = _classify_from_metadata(name, mfg, model, "roku")
        return True, NetworkDevice(
            id=f"lan_roku_{ip.replace('.', '_')}",
            name=name,
            ip=ip,
            mac=mac,
            manufacturer=mfg,
            model=model,
            category=cat,
            protocol=proto,
            port=8060,
            services=["roku-ecp"],
            capabilities=caps,
            power_strategies=p_strats,
            power_limitations=p_lim,
            online=True,
            state={"power": True},
            state_confidence=StateConfidence.CONFIRMED.value,
            source="manual",
        )

    # 2. Samsung Tizen :8001 / :8002
    if _tcp_open(ip, 8001) or _tcp_open(ip, 8002):
        name, model = custom_name or f"Samsung TV {ip}", "Samsung Tizen"
        try:
            import json as _json

            with urllib.request.urlopen(f"http://{ip}:8001/api/v2/", timeout=1.5) as r:
                info = _json.loads(r.read(16384).decode("utf-8", errors="replace"))
                dev = info.get("device") or {}
                name = custom_name or dev.get("name") or name
                model = dev.get("modelName") or model
                if not mac and dev.get("wifiMac"):
                    mac = str(dev["wifiMac"]).upper()
        except Exception:
            pass
        cat, proto, caps, p_strats, p_lim = _classify_from_metadata(name, "Samsung", model, "tizen")
        return True, NetworkDevice(
            id=f"lan_samsung_tizen_{ip.replace('.', '_')}",
            name=name,
            ip=ip,
            mac=mac,
            manufacturer="Samsung",
            model=model,
            category=cat,
            protocol=proto,
            port=8002 if _tcp_open(ip, 8002, 0.3) else 8001,
            services=["samsung-tizen-ws"],
            capabilities=caps,
            power_strategies=p_strats,
            power_limitations=p_lim,
            online=True,
            state={"power": True},
            state_confidence=StateConfidence.CONFIRMED.value,
            source="manual",
        )

    # 3. LG webOS :3000 / :3001
    if _tcp_open(ip, 3000) or _tcp_open(ip, 3001):
        cat, proto, caps, p_strats, p_lim = _classify_from_metadata(custom_name or "LG webOS", "LG", "webOS TV", "webos")
        return True, NetworkDevice(
            id=f"lan_lg_webos_{ip.replace('.', '_')}",
            name=custom_name or f"LG TV {ip}",
            ip=ip,
            mac=mac,
            manufacturer="LG",
            model="webOS Smart TV",
            category=cat,
            protocol=proto,
            port=3000 if _tcp_open(ip, 3000, 0.3) else 3001,
            services=["lg-webos-ssap"],
            capabilities=caps,
            power_strategies=p_strats,
            power_limitations=p_lim,
            online=True,
            state={"power": True},
            state_confidence=StateConfidence.CONFIRMED.value,
            source="manual",
        )

    # 4. Chromecast / Google TV :8008 / :8009 / :6466 / :5555
    if _tcp_open(ip, 8008) or _tcp_open(ip, 8009) or _tcp_open(ip, 6466) or _tcp_open(ip, 5555):
        is_atv = _tcp_open(ip, 6466, 0.3) or _tcp_open(ip, 5555, 0.3)
        proto = "android_tv" if is_atv else "chromecast"
        cat = DeviceCategory.TV.value if is_atv else DeviceCategory.MEDIA.value
        return True, NetworkDevice(
            id=f"lan_{proto}_{ip.replace('.', '_')}",
            name=custom_name or (f"Android/Google TV {ip}" if is_atv else f"Chromecast {ip}"),
            ip=ip,
            mac=mac,
            manufacturer="Google / Android TV",
            model="Android TV" if is_atv else "Google Cast",
            category=cat,
            protocol=proto,
            port=6466 if is_atv else 8008,
            services=["androidtv-remote" if is_atv else "googlecast"],
            capabilities=["power", "volume", "mute", "dpad", "apps", "media"] if is_atv else ["volume", "mute", "media", "apps"],
            power_strategies=["network_standby", "wol"],
            power_limitations="Android TV/Cast depende de HDMI-CEC o red en espera para encendido.",
            online=True,
            state={"power": True},
            state_confidence=StateConfidence.CONFIRMED.value,
            source="manual",
        )

    # 5. Apple TV / AirPlay :7000
    if _tcp_open(ip, 7000):
        return True, NetworkDevice(
            id=f"lan_apple_tv_{ip.replace('.', '_')}",
            name=custom_name or f"Apple TV {ip}",
            ip=ip,
            mac=mac,
            manufacturer="Apple",
            model="Apple TV / AirPlay",
            category=DeviceCategory.MEDIA.value,
            protocol="apple_tv",
            port=7000,
            services=["airplay"],
            capabilities=["media", "volume", "dpad"],
            power_strategies=["network_standby"],
            power_limitations="Apple TV requiere emparejamiento Companion/AirPlay.",
            online=True,
            state={"power": True},
            state_confidence=StateConfidence.CONFIRMED.value,
            source="manual",
        )

    return False, f"No se detectaron puertos de TV/Media compatibles activos en {ip} (verifica que el dispositivo esté encendido y en la misma red)."
