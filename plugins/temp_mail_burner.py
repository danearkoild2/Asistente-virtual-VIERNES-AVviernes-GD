"""
Temp Mail Burner Plugin for MARK LV / Viernes.
Creates disposable temporary mailboxes and reads verification codes/messages to avoid spam.
"""
from __future__ import annotations
import json
import secrets
import urllib.request
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "temp_mail_burner",
    "description": (
        "Generates a disposable 10-minute temporary email address and checks for incoming verification codes or emails. "
        "Use when user asks 'crea un correo temporal', 'correo desechable', 'dame un email temporal', "
        "or 'revisa si llegó el código a mi correo temporal'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "'generate' to create a new inbox, or 'check' to look for incoming emails/codes.",
            },
            "login": {
                "type": "STRING",
                "description": "The login username of an already generated email (if checking).",
            },
            "domain": {
                "type": "STRING",
                "description": "Domain of the email (e.g. 1secmail.com).",
            }
        },
        "required": ["action"],
    },
}

PLUGIN_SETTINGS = {
    "title": "Correos Temporales Desechables",
    "fields": [
        {
            "key": "default_domain",
            "label": "Dominio Predeterminado",
            "type": "choice",
            "options": ["1secmail.com", "1secmail.org", "1secmail.net"],
            "default": "1secmail.com",
        },
        {
            "key": "copy_to_clipboard",
            "label": "Copiar Correo al Portapapeles",
            "type": "toggle",
            "default": True,
        }
    ],
}

_LAST_INBOX: dict = {}

def run(parameters: dict, player=None, session_memory=None) -> str:
    global _LAST_INBOX
    action = parameters.get("action", "generate").lower().strip()

    if action in ("generate", "new", "create"):
        domain = get_plugin_setting("temp_mail_burner", "default_domain", "1secmail.com")
        rand_user = f"user_{secrets.token_hex(4)}"
        email_addr = f"{rand_user}@{domain}"
        _LAST_INBOX = {"login": rand_user, "domain": domain, "email": email_addr}

        # Copy to clipboard if enabled
        if get_plugin_setting("temp_mail_burner", "copy_to_clipboard", True):
            try:
                import subprocess
                subprocess.run(["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value '{email_addr}'"],
                               check=False, capture_output=True, timeout=2.0)
            except Exception:
                pass

        if player:
            try:
                player.write_log(f"📧 CORREO TEMPORAL CREADO: {email_addr} (copiado al portapapeles)")
            except Exception:
                pass

        return f"He creado tu correo temporal desechable: {email_addr}. Ha sido copiado a tu portapapeles. Avísame cuando quieras que revise si llegó algún mensaje."

    else: # check / read
        login = parameters.get("login") or _LAST_INBOX.get("login")
        domain = parameters.get("domain") or _LAST_INBOX.get("domain")
        if not login or not domain:
            return "Sir, no tengo un correo temporal activo registrado. Pídeme 'crea un correo temporal' primero."

        try:
            url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                msgs = json.loads(resp.read().decode("utf-8"))

            if not msgs:
                return f"La bandeja de entrada para {login}@{domain} aún está vacía. No ha llegado ningún mensaje todavía."

            # Fetch details of latest message
            latest = msgs[0]
            msg_id = latest.get("id")
            detail_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}"
            req_d = urllib.request.Request(detail_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req_d, timeout=5.0) as resp_d:
                detail = json.loads(resp_d.read().decode("utf-8"))

            subject = detail.get("subject", "Sin asunto")
            sender = detail.get("from", "Desconocido")
            body = detail.get("textBody", "") or detail.get("body", "")

            # Look for 4-8 digit verification code
            import re
            code_match = re.search(r"\b\d{4,8}\b", body)
            code_str = f" Posible código de verificación: {code_match.group(0)}." if code_match else ""

            if player:
                try:
                    player.write_log(f"📧 CORREO RECIBIDO de {sender}: '{subject}'.{code_str}")
                except Exception:
                    pass

            return f"Ha llegado un correo de {sender} con asunto '{subject}'.{code_str}"

        except Exception as e:
            return f"Hubo un problema al consultar la bandeja temporal: {e}"
