"""
Inbound Communications Action for VIERNES
==========================================
Auto-discovered by core/action_loader.py.
Handles natural commands like:
- "¿Me llegó algún mensaje de WhatsApp?"
- "¿Quién me escribió por WhatsApp?"
- "Léeme el último mensaje de WhatsApp"
- "Abre WhatsApp"
- "¿Tengo notificaciones o correos pendientes?"
"""
from __future__ import annotations

import os
import subprocess
import time
from typing import Any, Dict

TOOL = {
    "name": "inbound_communications",
    "description": (
        "Consulta y gestiona las notificaciones y mensajes entrantes de WhatsApp Desktop y Gmail. "
        "Permite verificar si hay mensajes de WhatsApp nuevos, quién escribió, leer el contenido "
        "del último mensaje o abrir la aplicación de WhatsApp instalada en Windows."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "operation": {
                "type": "STRING",
                "enum": ["check_whatsapp", "read_last_whatsapp", "open_whatsapp", "check_all_inbox"],
                "description": "Acción a realizar sobre WhatsApp o comunicaciones entrantes.",
            },
        },
        "required": ["operation"],
    },
    "handler": None,
}


def inbound_action(parameters: Dict[str, Any] = None, player=None, session_memory=None) -> str:
    from system_monitor.communication_monitor import comm_monitor
    from integrations.gmail.gmail_client import gmail
    from security.voice_id import voice_id_engine

    params = parameters or {}
    op = (params.get("operation") or "check_whatsapp").lower()

    # 1. Voice ID Gate
    auth_ok, auth_msg = voice_id_engine.verify_action_authorized("social.read", target=f"Inbound {op}")
    if not auth_ok:
        if player and hasattr(player, "write_log"):
            player.write_log(f"SEC: {auth_msg}")
        return auth_msg

    # Poll fresh
    comm_monitor.poll_once()

    # 2. Check WhatsApp messages
    if op == "check_whatsapp":
        last_wa = comm_monitor.get_last_whatsapp()
        status = comm_monitor.get_status()
        badge = status.get("whatsapp_last_badge", 0)

        if last_wa:
            elapsed_mins = int((time.time() - last_wa.get("timestamp", time.time())) / 60)
            time_txt = f"hace {elapsed_mins} minutos" if elapsed_mins > 0 else "hace un momento"
            sender = last_wa.get("sender", "un contacto")
            msg = last_wa.get("message", "")
            return f"El último mensaje de WhatsApp recibido fue de {sender} ({time_txt}): \"{msg}\"."
        elif badge > 0:
            return f"Tienes {badge} mensajes sin leer en WhatsApp. Puedes decir 'Abre WhatsApp' para revisarlos."
        else:
            return "No tienes mensajes nuevos de WhatsApp en este momento."

    # 3. Read last WhatsApp message
    if op == "read_last_whatsapp":
        last_wa = comm_monitor.get_last_whatsapp()
        if not last_wa:
            return "No tengo registrado ningún mensaje reciente de WhatsApp en el historial de notificaciones."
        sender = last_wa.get("sender", "Remitente desconocido")
        text = last_wa.get("message", "(Sin texto)")
        return f"Mensaje de {sender} en WhatsApp:\n\"{text}\""

    # 4. Open WhatsApp Desktop App
    if op == "open_whatsapp":
        try:
            # WhatsApp Store App execution on Windows
            subprocess.Popen(["explorer.exe", "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"])
            if player and hasattr(player, "write_log"):
                player.write_log("APP: Abriendo WhatsApp Desktop...")
            return "Abriendo la aplicación de WhatsApp en pantalla, señor."
        except Exception as e:
            return f"No se pudo abrir WhatsApp: {e}"

    # 5. Check all inbox (WhatsApp + Gmail)
    if op == "check_all_inbox":
        lines = []
        # WhatsApp check
        last_wa = comm_monitor.get_last_whatsapp()
        badge = comm_monitor.get_status().get("whatsapp_last_badge", 0)
        if last_wa:
            lines.append(f"• WhatsApp: Mensaje de {last_wa.get('sender')}: \"{last_wa.get('message')}\"")
        elif badge > 0:
            lines.append(f"• WhatsApp: {badge} mensajes sin leer.")
        else:
            lines.append("• WhatsApp: Sin mensajes pendientes.")

        # Gmail check
        if gmail.is_connected():
            unread = gmail.get_unread_count()
            if unread > 0:
                lines.append(f"• Gmail: {unread} correos nuevos sin leer.")
            else:
                lines.append("• Gmail: Bandeja al día, sin correos nuevos.")
        else:
            lines.append("• Gmail: Cuenta no vinculada (puedes configurarla con F8).")

        return "Resumen de comunicaciones entrantes:\n" + "\n".join(lines)

    return f"Operación '{op}' no reconocida."


TOOL["handler"] = inbound_action
