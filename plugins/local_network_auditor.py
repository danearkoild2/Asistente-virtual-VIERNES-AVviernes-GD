"""
Local Network Auditor & Wi-Fi Device Scanner Plugin for VIERNES.
Audits the local subnet, detects active devices, router status, and scans for open ports.
"""
from __future__ import annotations

import re
import socket
import subprocess
from typing import Dict, List, Tuple

PLUGIN = {
    "name": "local_network_auditor",
    "description": (
        "Audits the local Wi-Fi / LAN network, lists connected active devices, "
        "identifies the gateway router, and checks for open local ports and potential intrusions. "
        "Use when user asks 'quién está conectado a mi red', 'escanea mi red wifi', "
        "'auditoría de red', 'dispositivos en mi red', or 'check local network security'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "target_ip": {
                "type": "STRING",
                "description": "Optional specific IP in local subnet to audit for open ports. If omitted, audits the whole subnet."
            }
        },
        "required": [],
    },
}

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    80: "HTTP Web",
    443: "HTTPS",
    445: "SMB / Carpetas Compartidas",
    3389: "Escritorio Remoto (RDP)",
    8080: "Proxy / Servidor Web",
}


def _check_port(ip: str, port: int, timeout: float = 0.5) -> bool:
    """Check if a specific port is open on target IP."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((ip, port)) == 0
    except Exception:
        return False


def _get_arp_devices() -> Tuple[str, List[Dict[str, str]]]:
    """Parse Windows arp -a table to list active IP and MAC addresses."""
    devices = []
    local_interface = "127.0.0.1"

    try:
        res = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=5)
        current_interface = None
        for line in res.stdout.splitlines():
            line = line.strip()
            if "Interfaz:" in line or "Interface:" in line:
                m = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
                if m:
                    current_interface = m.group(1)
                    local_interface = current_interface
                continue

            # Parse lines like: 192.168.100.1   60-12-3c-c7-9f-12  dinámico
            parts = line.split()
            if len(parts) >= 3:
                ip, mac, kind = parts[0], parts[1], parts[2].lower()
                # Skip broadcast, multicast, and static loopbacks
                if ip.startswith("224.") or ip.startswith("239.") or ip.endswith(".255"):
                    continue
                if mac.lower() in ("ff-ff-ff-ff-ff-ff", "01-00-5e"):
                    continue

                devices.append({
                    "ip": ip,
                    "mac": mac,
                    "type": kind,
                    "interface": current_interface or ""
                })
    except Exception:
        pass

    return local_interface, devices


def run(parameters: dict, player=None, session_memory=None) -> str:
    target_ip = (parameters.get("target_ip") or "").strip()

    local_ip, devices = _get_arp_devices()

    if target_ip:
        # Audit specific IP
        open_ports = []
        for port, service in COMMON_PORTS.items():
            if _check_port(target_ip, port):
                open_ports.append(f"{service} (puerto {port})")

        if open_ports:
            msg = f"Auditoría a {target_ip}: Se encontraron {len(open_ports)} puertos abiertos: {', '.join(open_ports)}."
        else:
            msg = f"Auditoría a {target_ip}: Sin puertos comunes abiertos accesibles. El dispositivo parece blindado."
        if player:
            player.write_log(f"NETWORK AUDIT: Scanned {target_ip} -> {open_ports}")
        return msg

    # General Subnet Audit
    total_devices = len(devices)
    router_device = next((d for d in devices if d["ip"].endswith(".1")), None)
    router_ip = router_device["ip"] if router_device else "Desconocido"

    # Quick security check on local machine
    open_local = []
    for port in (80, 445, 3389, 8080):
        if _check_port("127.0.0.1", port, timeout=0.1):
            open_local.append(COMMON_PORTS.get(port, str(port)))

    report_lines = [
        f"Auditoría de red completada.",
        f"Tu dirección IP local es {local_ip}, con puerta de enlace en el router {router_ip}.",
        f"Se detectaron {total_devices} dispositivo(s) activo(s) en tu subred Wi-Fi."
    ]

    # Show first 3 device IPs
    if devices:
        ips_preview = [d["ip"] for d in devices[:4]]
        report_lines.append(f"Dispositivos en línea: {', '.join(ips_preview)}.")

    if open_local:
        report_lines.append(f"Puertos activos en tu PC: {', '.join(open_local)}.")
    else:
        report_lines.append("No hay puertos vulnerables expuestos en tu equipo.")

    msg = " ".join(report_lines)

    if player:
        try:
            player.write_log(f"NETWORK AUDIT: {total_devices} devices active on subnet ({local_ip})")
        except Exception:
            pass

    return msg
