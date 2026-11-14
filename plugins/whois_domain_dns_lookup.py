"""
WHOIS & DNS Domain Lookup Plugin for VIERNES.
Fetches domain registration dates, expiration date, registrar, nameservers, and IP addresses via RDAP & DNS.
"""
from __future__ import annotations

import json
import socket
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, List, Optional

PLUGIN = {
    "name": "whois_domain_dns_lookup",
    "description": (
        "Inspects any web domain (e.g. google.com, openai.com): checks WHOIS registration, "
        "expiration date, registrar, nameservers, and resolved IP addresses, or verifies if domain is available. "
        "Use when user asks 'quién es dueño de este dominio', 'cuándo vence el dominio', "
        "'información whois de', 'dns de', or 'whois domain'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "domain": {
                "type": "STRING",
                "description": "Domain name to lookup (e.g. 'github.com', 'tesla.com', 'miweb.org')."
            }
        },
        "required": ["domain"],
    },
}


def _clean_domain(domain: str) -> str:
    """Normalize input into bare domain name."""
    d = domain.strip().lower()
    if d.startswith("http://"):
        d = d[7:]
    elif d.startswith("https://"):
        d = d[8:]
    d = d.split("/")[0].split(":")[0]
    return d


def _lookup_dns_ips(domain: str) -> List[str]:
    """Resolve A / IPv4 addresses for the domain."""
    try:
        _, _, ips = socket.gethostbyname_ex(domain)
        return ips
    except Exception:
        return []


def _lookup_rdap_whois(domain: str) -> dict:
    """Query standard ICANN RDAP service for authoritative domain information."""
    url = f"https://rdap.org/domain/{urllib.parse.quote(domain)}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Viernes-RDAP-Client/1.0", "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            events = {e.get("eventAction"): e.get("eventDate", "")[:10] for e in data.get("events", [])}

            # Extract registrar entity
            registrar = "Desconocido"
            for entity in data.get("entities", []):
                roles = entity.get("roles", [])
                if "registrar" in roles:
                    vcard = entity.get("vcardArray", [])
                    if len(vcard) > 1 and isinstance(vcard[1], list):
                        for field in vcard[1]:
                            if field[0] == "fn" and len(field) > 3:
                                registrar = str(field[3])
                                break

            # Nameservers
            nameservers = []
            for ns in data.get("nameservers", []):
                ldh = ns.get("ldhName")
                if ldh:
                    nameservers.append(ldh.lower())

            return {
                "status": "registered",
                "created": events.get("registration", "Desconocida"),
                "expires": events.get("expiration", "Desconocida"),
                "updated": events.get("last changed", ""),
                "registrar": registrar,
                "nameservers": nameservers
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"status": "available", "message": f"El dominio {domain} no está registrado y parece disponible."}
        return {"status": "error", "message": f"Error del servidor RDAP ({e.code})"}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}


def run(parameters: dict, player=None, session_memory=None) -> str:
    raw_domain = parameters.get("domain", "")
    domain = _clean_domain(raw_domain)

    if not domain or "." not in domain:
        return "Por favor proporciona un nombre de dominio válido (ejemplo: 'github.com' o 'openai.com')."

    # 1. DNS Resolution
    ips = _lookup_dns_ips(domain)

    # 2. WHOIS / RDAP lookup
    whois_info = _lookup_rdap_whois(domain)

    if whois_info.get("status") == "available":
        msg = f"Dominio {domain}: ¡Disponible! No se encontró registro activo en ICANN, por lo que puedes comprarlo o registrarlo."
    elif whois_info.get("status") == "registered":
        created = whois_info.get("created")
        expires = whois_info.get("expires")
        reg = whois_info.get("registrar")
        ns_list = whois_info.get("nameservers", [])[:2]

        parts = [f"Información de {domain}: Registrado con {reg}"]
        if created and created != "Desconocida":
            parts.append(f"creado en {created}")
        if expires and expires != "Desconocida":
            parts.append(f"vence el {expires}")
        if ips:
            parts.append(f"apunta a la IP {ips[0]}")
        if ns_list:
            parts.append(f"servidores DNS: {', '.join(ns_list)}")

        msg = ". ".join(parts) + "."
    else:
        # Fallback to DNS only
        if ips:
            msg = f"Dominio {domain}: Activo en internet apuntando a las IP: {', '.join(ips[:3])}."
        else:
            err = whois_info.get("message", "Servidores WHOIS no disponibles")
            msg = f"No se pudo consultar el dominio {domain}: {err}."

    if player:
        try:
            player.write_log(f"WHOIS: {domain} -> {whois_info.get('status')} [IP: {', '.join(ips[:2])}]")
        except Exception:
            pass

    return msg
