"""
Official Google SMTP & IMAP Client Integration for VIERNES
===========================================================
Replaces fragile OAuth 2.0 with official, secure Google App Passwords (SMTP / IMAP).
- SMTP (smtp.gmail.com:587): Enviar correos y respuestas.
- IMAP (imap.gmail.com:993): Leer correos, contar no leídos, listar recientes y buscar.
- Almacenamiento seguro cifrado mediante integrations.crypto (Fernet / AES).
"""

from __future__ import annotations

import email
import imaplib
import json
import logging
import os
import re
import smtplib
import webbrowser
from datetime import datetime
from email.header import decode_header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from integrations.crypto import decrypt_secret, encrypt_secret
from security.audit_logger import record_audit
from core.context_memory import task_context
from core.notifications import notify, LEVEL_INFO, LEVEL_SUCCESS, LEVEL_WARNING

logger = logging.getLogger("Viernes.Integrations.Gmail")

_CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "config"
_CREDENTIALS_FILE = _CONFIG_DIR / "gmail_smtp_credentials.enc"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993


def _decode_mime_words(raw_header: Optional[str]) -> str:
    """Decodifica encabezados MIME con codificaciones utf-8, latin1, base64, etc."""
    if not raw_header:
        return ""
    try:
        fragments = decode_header(raw_header)
        out = []
        for frag, enc in fragments:
            if isinstance(frag, bytes):
                out.append(frag.decode(enc or "utf-8", errors="replace"))
            else:
                out.append(str(frag))
        return "".join(out).strip()
    except Exception:
        return str(raw_header)


def _extract_body_from_message(msg: email.message.Message) -> str:
    """Extrae el cuerpo de texto plano de un mensaje MIME."""
    text_content = ""
    try:
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdisp = str(part.get("Content-Disposition") or "")
                if ctype == "text/plain" and "attachment" not in cdisp:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or "utf-8"
                        text_content += payload.decode(charset, errors="replace") + "\n"
            if not text_content:
                # Fallback to HTML if plain text missing
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        payload = part.get_payload(decode=True)
                        if payload:
                            charset = part.get_content_charset() or "utf-8"
                            raw_html = payload.decode(charset, errors="replace")
                            text_content = re.sub(r"<[^>]+>", " ", raw_html)
                            break
        else:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "utf-8"
                text_content = payload.decode(charset, errors="replace")
    except Exception as e:
        logger.warning(f"Error extracting email body: {e}")

    clean = " ".join(text_content.split())
    return clean


class GmailManager:
    """Gestor oficial de Google SMTP e IMAP para Viernes."""

    def __init__(self):
        self._account_email = ""
        self._app_password = ""
        self._is_connected = False
        self._load_credentials()

    def _load_credentials(self) -> bool:
        if not _CREDENTIALS_FILE.exists():
            return False
        try:
            enc_data = _CREDENTIALS_FILE.read_text(encoding="utf-8")
            raw_json = decrypt_secret(enc_data)
            if raw_json:
                data = json.loads(raw_json)
                self._account_email = (data.get("email") or "").strip()
                self._app_password = (data.get("password") or "").strip().replace(" ", "")
                if self._account_email and self._app_password:
                    self._is_connected = True
                    return True
        except Exception as e:
            logger.error(f"[Gmail] Error loading encrypted credentials: {e}")
        self._is_connected = False
        return False

    def save_credentials(self, email_address: str, app_password: str) -> Tuple[bool, str]:
        """Verifica y guarda las credenciales SMTP/IMAP de Google cifradas."""
        clean_email = email_address.strip()
        clean_pass = app_password.strip().replace(" ", "")

        if not clean_email or "@" not in clean_email:
            return False, "Por favor ingresa un correo de Google/Gmail válido."
        if not clean_pass or len(clean_pass) < 8:
            return False, "La contraseña de aplicación de Google debe tener al menos 16 letras."

        # Probar conexión real con los servidores de Google antes de guardar
        ok, msg = self.test_connection(clean_email, clean_pass)
        if not ok:
            return False, msg

        try:
            payload = json.dumps({"email": clean_email, "password": clean_pass})
            enc = encrypt_secret(payload)
            _CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
            _CREDENTIALS_FILE.write_text(enc, encoding="utf-8")

            self._account_email = clean_email
            self._app_password = clean_pass
            self._is_connected = True

            record_audit("GMAIL_CONNECT", target=clean_email, result="SUCCESS")
            notify("Gmail Conectado", f"Cuenta Google vinculada exitosamente vía SMTP/IMAP: {clean_email}", LEVEL_SUCCESS, "GMAIL")
            return True, f"¡Conexión exitosa! Cuenta configurada: {clean_email}"
        except Exception as e:
            logger.error(f"[Gmail] Error saving credentials: {e}")
            return False, f"Error al guardar credenciales: {e}"

    def test_connection(self, email_address: str, app_password: str) -> Tuple[bool, str]:
        """Prueba de autenticación en vivo con IMAP y SMTP de Google."""
        clean_email = email_address.strip()
        clean_pass = app_password.strip().replace(" ", "")

        # 1. Probar IMAP (Lectura y recepción)
        try:
            imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, timeout=12)
            imap.login(clean_email, clean_pass)
            imap.logout()
        except imaplib.IMAP4.error as e:
            err_str = str(e)
            if "Application-specific password required" in err_str or "Invalid credentials" in err_str:
                return False, (
                    "Google rechazó las credenciales. Asegúrate de usar una 'Contraseña de aplicación' "
                    "(App Password) de 16 caracteres generada en myaccount.google.com/apppasswords "
                    "y que la verificación en dos pasos esté activa en tu cuenta."
                )
            return False, f"Fallo al conectar con Google IMAP (imap.gmail.com): {e}"
        except Exception as e:
            return False, f"Error de red al conectar con Google IMAP: {e}"

        # 2. Probar SMTP (Envío)
        try:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=12)
            server.starttls()
            server.login(clean_email, clean_pass)
            server.quit()
        except Exception as e:
            return False, f"Fallo al autenticar en Google SMTP (smtp.gmail.com): {e}"

        return True, "Credenciales verificadas exitosamente en Google SMTP e IMAP."

    def is_connected(self) -> bool:
        return self._is_connected and bool(self._account_email) and bool(self._app_password)

    def get_status(self) -> Dict[str, Any]:
        return {
            "connected": self.is_connected(),
            "account": self._account_email,
            "provider": "Google SMTP & IMAP (SSL/TLS)",
            "smtp_host": f"{SMTP_HOST}:{SMTP_PORT}",
            "imap_host": f"{IMAP_HOST}:{IMAP_PORT}",
            "has_credentials": _CREDENTIALS_FILE.exists(),
        }

    def disconnect(self) -> bool:
        """Elimina las credenciales guardadas."""
        try:
            if _CREDENTIALS_FILE.exists():
                _CREDENTIALS_FILE.unlink()
            self._account_email = ""
            self._app_password = ""
            self._is_connected = False
            record_audit("GMAIL_DISCONNECT", result="SUCCESS")
            notify("Gmail Desconectado", "Se desvincularon las credenciales de correo.", LEVEL_INFO, "GMAIL")
            return True
        except Exception as e:
            logger.error(f"[Gmail] Disconnect error: {e}")
            return False

    @property
    def account(self) -> str:
        return self._account_email

    def set_credentials(self, email_address: str, app_password: str) -> Tuple[bool, str]:
        """Alias para save_credentials."""
        return self.save_credentials(email_address, app_password)

    def send_email(
        self,
        to_address: Optional[str] = None,
        subject: str = "",
        body: str = "",
        cc_address: Optional[str] = None,
        to: Optional[str] = None,
        cc: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """Envía un correo electrónico mediante Google SMTP."""
        dest = (to or to_address or "").strip()
        copy = (cc or cc_address or "").strip()

        if not self.is_connected():
            return False, "Gmail no está configurado. Por favor configura tu correo y contraseña de aplicación en Integraciones (F8)."

        if not dest or "@" not in dest:
            return False, f"Dirección de destinatario inválida: '{dest}'."

        try:
            msg = MIMEMultipart()
            msg["From"] = f"Viernes <{self._account_email}>"
            msg["To"] = dest
            msg["Subject"] = subject
            msg["Date"] = email.utils.formatdate(localtime=True)

            recipients = [dest]
            if copy and "@" in copy:
                msg["Cc"] = copy
                recipients.append(copy)
                recipients.append(cc_address.strip())

            # Adjuntar cuerpo en texto plano
            msg.attach(MIMEText(body, "plain", "utf-8"))

            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15)
            server.starttls()
            server.login(self._account_email, self._app_password)
            server.sendmail(self._account_email, recipients, msg.as_string())
            server.quit()

            record_audit("GMAIL_SEND", target=to_clean, result="SUCCESS", metadata={"subject": subject})
            notify("Correo Enviado", f"Correo enviado a {to_clean}: '{subject}'", LEVEL_SUCCESS, "GMAIL")
            return True, f"Correo enviado exitosamente a {to_clean}."
        except Exception as e:
            logger.error(f"[Gmail] Error sending email via SMTP: {e}")
            record_audit("GMAIL_SEND", target=to_clean, result="FAILED", reason=str(e))
            return False, f"Error al enviar correo por SMTP: {e}"

    def get_unread_count(self) -> int:
        """Obtiene la cantidad de correos no leídos en la bandeja de entrada vía IMAP."""
        if not self.is_connected():
            return 0
        try:
            imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, timeout=10)
            imap.login(self._account_email, self._app_password)
            imap.select("INBOX", readonly=True)
            status, response = imap.search(None, "UNSEEN")
            count = len(response[0].split()) if status == "OK" and response[0] else 0
            imap.logout()
            return count
        except Exception as e:
            logger.warning(f"[Gmail] Error getting unread count: {e}")
            return 0

    def list_recent_emails(
        self,
        max_results: int = 5,
        query: Optional[str] = None,
        unread_only: bool = False,
    ) -> List[Dict[str, Any]]:
        """Lista los correos más recientes de la bandeja de entrada mediante IMAP."""
        if not self.is_connected():
            return []

        results = []
        try:
            imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, timeout=14)
            imap.login(self._account_email, self._app_password)
            imap.select("INBOX", readonly=True)

            criteria = "UNSEEN" if unread_only else "ALL"
            if query:
                criteria = f'(SUBJECT "{query}")'

            status, response = imap.search(None, criteria)
            if status != "OK" or not response[0]:
                imap.logout()
                return []

            msg_ids = response[0].split()
            # Tomar los últimos max_results (los más recientes)
            recent_ids = msg_ids[-max_results:]
            recent_ids.reverse()

            for mid in recent_ids:
                res_fetch, data = imap.fetch(mid, "(RFC822.HEADER BODY.PEEK[TEXT])")
                if res_fetch != "OK":
                    continue

                raw_email = None
                for part in data:
                    if isinstance(part, tuple) and part[1]:
                        raw_email = part[1]
                        break

                if not raw_email:
                    continue

                msg = email.message_from_bytes(raw_email)
                sender = _decode_mime_words(msg.get("From"))
                subject = _decode_mime_words(msg.get("Subject")) or "(Sin Asunto)"
                date_str = msg.get("Date") or ""
                snippet = _extract_body_from_message(msg)[:220]

                str_id = mid.decode("utf-8") if isinstance(mid, bytes) else str(mid)

                results.append({
                    "id": str_id,
                    "thread_id": str_id,
                    "sender": sender,
                    "subject": subject,
                    "date": date_str,
                    "unread": unread_only,
                    "snippet": snippet,
                    "web_url": "https://mail.google.com/mail/u/0/#inbox",
                })

            imap.logout()
            task_context.set_entity("last_emails", results)
            record_audit("GMAIL_LIST", target="INBOX", result="SUCCESS", metadata={"count": len(results)})
            return results

        except Exception as e:
            logger.error(f"[Gmail] Error listing emails: {e}")
            return []

    def read_email(self, message_id: str) -> Dict[str, Any]:
        """Obtiene el contenido completo de un correo específico por su ID."""
        if not self.is_connected():
            return {"error": "Gmail no está configurado."}

        try:
            imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, timeout=12)
            imap.login(self._account_email, self._app_password)
            imap.select("INBOX", readonly=True)

            res_fetch, data = imap.fetch(message_id.encode("utf-8"), "(RFC822)")
            imap.logout()

            if res_fetch != "OK" or not data:
                return {"error": f"No se encontró el correo con ID '{message_id}'."}

            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            sender = _decode_mime_words(msg.get("From"))
            to = _decode_mime_words(msg.get("To"))
            subject = _decode_mime_words(msg.get("Subject"))
            date_val = msg.get("Date") or ""
            body = _extract_body_from_message(msg)

            record_audit("GMAIL_READ", target=f"ID {message_id} ({sender})", result="SUCCESS")
            return {
                "id": message_id,
                "sender": sender,
                "to": to,
                "subject": subject,
                "date": date_val,
                "snippet": body[:180],
                "body": body[:3500],
                "web_url": "https://mail.google.com/mail/u/0/#inbox",
            }
        except Exception as e:
            logger.error(f"[Gmail] Error reading email: {e}")
            return {"error": f"Error al leer correo: {e}"}

    def summarize_email(self, message_id: str) -> str:
        """Genera un resumen conciso del correo especificado."""
        data = self.read_email(message_id)
        if "error" in data:
            return data["error"]
        body = data.get("body") or data.get("snippet") or "Sin contenido."
        sender = data.get("sender", "Desconocido")
        subj = data.get("subject", "Sin Asunto")
        return f"Resumen del correo de {sender} ('{subj}'):\n{body[:350]}..."

    def open_in_gmail(self) -> None:
        """Abre Gmail en el navegador web predeterminado."""
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")


# Instancia global única
gmail = GmailManager()
