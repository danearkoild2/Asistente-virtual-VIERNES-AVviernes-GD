"""
Gmail Action Handler for VIERNES
=================================
Auto-discovered by core/action_loader.py.
Handles natural queries like:
- "¿tengo correos nuevos?"
- "¿quién me escribió?"
- "Lee el correo de Juan"
- "Resúmeme el correo de Juan"
- "Abre mi Gmail" / "Muéstrame el correo de Juan en Gmail"
"""
from __future__ import annotations

from typing import Any, Dict
from integrations.gmail.gmail_client import gmail
from security.voice_id import voice_id_engine
from core.context_memory import task_context

TOOL = {
    "name": "gmail_manager",
    "description": (
        "Gestiona y consulta la cuenta de correo Gmail del usuario (revisar correos nuevos, listar "
        "recientes, leer contenido bajo solicitud, resumir correos o abrir un correo en el navegador). "
        "Utiliza esta herramienta cuando el usuario pregunte por sus correos, pida un resumen de un email "
        "o solicite abrir Gmail."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "operation": {
                "type": "STRING",
                "enum": ["check_unread", "list_recent", "read_email", "summarize_email", "open_in_browser", "search", "send_email"],
                "description": "Acción a realizar en Gmail.",
            },
            "to": {
                "type": "STRING",
                "description": "Destinatario del correo electrónico al enviar un mensaje.",
            },
            "subject": {
                "type": "STRING",
                "description": "Asunto del correo electrónico.",
            },
            "body": {
                "type": "STRING",
                "description": "Cuerpo o texto del correo a enviar.",
            },
            "reference": {
                "type": "STRING",
                "description": "Nombre del remitente, palabra clave, número ('el primero') o ID del correo al que se hace referencia.",
            },
            "query": {
                "type": "STRING",
                "description": "Filtro opcional de búsqueda en Gmail (ej: 'from:Google', 'reunión').",
            },
            "unread_only": {
                "type": "BOOLEAN",
                "description": "Si es True, sólo busca correos no leídos.",
            },
        },
        "required": ["operation"],
    },
    "handler": None,  # assigned below
}


def gmail_action(parameters: Dict[str, Any] = None, player=None, session_memory=None) -> str:
    params = parameters or {}
    op = (params.get("operation") or "list_recent").lower()
    ref = (params.get("reference") or "").strip()
    query = (params.get("query") or "").strip()
    unread_only = bool(params.get("unread_only", False))

    # 1. Voice ID & RBAC Permission Gate
    auth_ok, auth_msg = voice_id_engine.verify_action_authorized("gmail.read", target=f"Gmail {op}")
    if not auth_ok:
        if player and hasattr(player, "write_log"):
            player.write_log(f"SEC: {auth_msg}")
        return auth_msg

    # 2. Check Unread Count
    if op == "check_unread":
        unread_count = gmail.get_unread_count()
        if not gmail.is_connected():
            unread_count = len([m for m in gmail.list_recent_emails() if m.get("unread")])
        if unread_count == 0:
            return "No tienes correos nuevos sin leer en la bandeja de entrada."
        elif unread_count == 1:
            return "Tienes 1 correo nuevo sin leer."
        else:
            return f"Tienes {unread_count} correos nuevos sin leer."

    # 3. List Recent Emails
    if op in ("list_recent", "search"):
        emails = gmail.list_recent_emails(max_results=5, query=query or None, unread_only=unread_only)
        if not emails:
            return "No encontré correos recientes con ese criterio."

        senders = [m["sender"].split("<")[0].strip().strip('"') for m in emails]
        lines = []
        for i, m in enumerate(emails, 1):
            s_name = m["sender"].split("<")[0].strip().strip('"')
            u_tag = " [NUEVO]" if m.get("unread") else ""
            lines.append(f"{i}. {s_name}: '{m['subject']}'{u_tag}")

        summary = f"Tienes {len(emails)} correos recientes de {', '.join(senders[:3])}.\n" + "\n".join(lines)
        if player and hasattr(player, "write_log"):
            player.write_log(f"GMAIL: Listados {len(emails)} correos.")
        return summary

    # 4. Read Email on demand
    if op == "read_email":
        target_email = None
        if ref:
            target_email = task_context.find_email_by_reference(ref)
        if not target_email:
            recent = task_context.get_entity("last_emails") or gmail.list_recent_emails(max_results=1)
            target_email = recent[0] if recent else None

        if not target_email:
            return "No encontré a qué correo te refieres. Por favor especifica de quién es."

        msg_id = target_email.get("id")
        detail = gmail.read_email(msg_id)
        sender = detail.get("sender", "").split("<")[0].strip().strip('"')
        body = detail.get("body") or detail.get("snippet") or "Sin contenido."
        return f"Correo de {sender} sobre '{detail.get('subject')}':\n{body}"

    # 5. Summarize Email
    if op == "summarize_email":
        target_email = None
        if ref:
            target_email = task_context.find_email_by_reference(ref)
        if not target_email:
            recent = task_context.get_entity("last_emails") or gmail.list_recent_emails(max_results=1)
            target_email = recent[0] if recent else None

        if not target_email:
            return "No encontré a qué correo te refieres para resumir."

        msg_id = target_email.get("id")
        return gmail.summarize_email(msg_id)

    # 6. Open Email / Inbox in Web Browser
    if op == "open_in_browser":
        msg_id = None
        if ref:
            target_email = task_context.find_email_by_reference(ref)
            if target_email:
                msg_id = target_email.get("id")
        return gmail.open_in_gmail(msg_id)

    # 7. Send Email via Google SMTP
    if op == "send_email":
        to_addr = (params.get("to") or ref).strip()
        subject_txt = (params.get("subject") or "Mensaje de VIERNES").strip()
        body_txt = (params.get("body") or "").strip()

        if not to_addr:
            return "Debes indicar a quién deseas enviar el correo."
        if not body_txt:
            return "El correo necesita un cuerpo o mensaje para ser enviado."

        auth_ok, auth_msg = voice_id_engine.verify_action_authorized("gmail.send", target=f"Gmail send to {to_addr}")
        if not auth_ok:
            return auth_msg

        ok, msg = gmail.send_email(to=to_addr, subject=subject_txt, body=body_txt)
        if ok:
            return f"Correo enviado exitosamente a {to_addr} con el asunto '{subject_txt}'."
        return f"No se pudo enviar el correo: {msg}"

    return f"Operación de Gmail '{op}' no reconocida."


TOOL["handler"] = gmail_action
