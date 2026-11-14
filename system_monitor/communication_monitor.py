"""
Inbound Communication Monitor for VIERNES
==========================================
Monitors real-time incoming communications:
1. WhatsApp Desktop (Windows App):
   - Intercepts incoming messages, senders, and unread badges via Windows Notification DB (wpndatabase.db).
   - Zero-dependency, read-only SQLite reader.
2. Google Gmail (IMAP):
   - Periodically checks for new incoming unread emails.
   - Extracts sender, subject, and snippet without duplicate notifications.
3. Proactive Dispatcher:
   - Dispatches visual UI notifications (core.notifications).
   - Generates speech prompts for natural voice alerts.
   - Caches last message & email for immediate recall.
"""
from __future__ import annotations

import os
import sqlite3
import threading
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from core.notifications import notify, LEVEL_INFO
from integrations.crypto import decrypt_secret
from integrations.gmail.gmail_client import gmail
from security.audit_logger import record_audit


class CommunicationMonitor:
    """Central watcher for WhatsApp and Gmail incoming messages."""

    def __init__(self):
        self._lock = threading.Lock()
        self._running = False
        self._thread: Optional[threading.Thread] = None

        # WhatsApp state
        self._wpn_db_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Notifications\wpndatabase.db")
        self._last_wpn_order: int = 0
        self._last_whatsapp_badge: int = 0
        self._last_whatsapp_msg: Optional[Dict[str, Any]] = None
        self._wpn_initialized = False

        # Gmail state
        self._seen_email_ids: set[str] = set()
        self._last_gmail_check: float = 0.0
        self._gmail_check_interval: float = 30.0  # seconds
        self._last_email_msg: Optional[Dict[str, Any]] = None
        self._gmail_initialized = False

        # Pending alerts queue for voice / UI consumption
        self._pending_alerts: List[Dict[str, Any]] = []
        self._alert_listeners: List[Callable[[Dict[str, Any]], None]] = []

        self._init_baselines()

    def _init_baselines(self):
        """Record initial baselines so we don't spam notifications for old messages."""
        # 1. WhatsApp baseline
        if os.path.exists(self._wpn_db_path):
            try:
                conn = sqlite3.connect(f"file:{self._wpn_db_path}?mode=ro", uri=True, timeout=3.0)
                c = conn.cursor()
                # Find maximum Order for WhatsApp notifications
                query = """
                SELECT MAX(n.[Order])
                FROM Notification n
                JOIN NotificationHandler h ON n.HandlerId = h.RecordId
                WHERE h.PrimaryId LIKE '%WhatsApp%'
                """
                c.execute(query)
                max_order = c.fetchone()[0]
                if max_order is not None:
                    self._last_wpn_order = int(max_order)

                # Find current badge value
                c.execute("""
                SELECT n.Payload
                FROM Notification n
                JOIN NotificationHandler h ON n.HandlerId = h.RecordId
                WHERE h.PrimaryId LIKE '%WhatsApp%' AND n.Type = 'badge'
                ORDER BY n.[Order] DESC LIMIT 1
                """)
                row = c.fetchone()
                if row and row[0]:
                    xml_str = row[0].decode("utf-8", errors="replace") if isinstance(row[0], bytes) else str(row[0])
                    root = ET.fromstring(xml_str)
                    val = root.attrib.get("value", "0")
                    if val.isdigit():
                        self._last_whatsapp_badge = int(val)

                conn.close()
                self._wpn_initialized = True
            except Exception as e:
                print(f"[CommMonitor] Error initializing WhatsApp baseline: {e}")

        # 2. Gmail baseline
        if gmail.is_connected():
            try:
                recents = gmail.list_recent_emails(max_results=10, unread_only=True)
                for m in recents:
                    if m.get("id"):
                        self._seen_email_ids.add(m["id"])
                self._gmail_initialized = True
            except Exception as e:
                print(f"[CommMonitor] Error initializing Gmail baseline: {e}")

    def register_alert_listener(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register a callback that fires whenever a new WhatsApp or Gmail alert arrives."""
        with self._lock:
            if callback not in self._alert_listeners:
                self._alert_listeners.append(callback)

    def unregister_alert_listener(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        with self._lock:
            if callback in self._alert_listeners:
                self._alert_listeners.remove(callback)

    def _dispatch_alert(self, alert: Dict[str, Any]):
        with self._lock:
            self._pending_alerts.append(alert)
            listeners = list(self._alert_listeners)

        for listener in listeners:
            try:
                listener(alert)
            except Exception as e:
                print(f"[CommMonitor] Listener error: {e}")

    def check_whatsapp(self) -> List[Dict[str, Any]]:
        """Poll wpndatabase.db for new WhatsApp notifications."""
        if not os.path.exists(self._wpn_db_path):
            return []

        alerts = []
        try:
            conn = sqlite3.connect(f"file:{self._wpn_db_path}?mode=ro", uri=True, timeout=3.0)
            c = conn.cursor()

            query = """
            SELECT n.[Order], n.Id, n.Type, n.Payload, n.ArrivalTime
            FROM Notification n
            JOIN NotificationHandler h ON n.HandlerId = h.RecordId
            WHERE h.PrimaryId LIKE '%WhatsApp%' AND n.[Order] > ?
            ORDER BY n.[Order] ASC
            """
            c.execute(query, (self._last_wpn_order,))
            rows = c.fetchall()

            for r in rows:
                order, nid, ntype, payload, arr_time = r
                if order > self._last_wpn_order:
                    self._last_wpn_order = order

                xml_str = payload.decode("utf-8", errors="replace") if isinstance(payload, bytes) else str(payload)
                try:
                    root = ET.fromstring(xml_str)
                except Exception:
                    continue

                if ntype == "toast":
                    texts = [elem.text.strip() for elem in root.iter("text") if elem.text and elem.text.strip()]
                    sender = texts[0] if len(texts) > 0 else "WhatsApp"
                    message_text = texts[1] if len(texts) > 1 else ""
                    if len(texts) > 2 and not message_text:
                        message_text = texts[2]

                    if sender or message_text:
                        alert = {
                            "type": "whatsapp",
                            "source": "WhatsApp",
                            "sender": sender,
                            "message": message_text,
                            "timestamp": time.time(),
                            "spoken_text": (
                                f"Señor, tiene un nuevo mensaje de WhatsApp de {sender}: '{message_text}'"
                                if message_text else
                                f"Señor, tiene un nuevo mensaje de WhatsApp de {sender}."
                            ),
                        }
                        self._last_whatsapp_msg = alert
                        alerts.append(alert)

                        # System notifications & audit
                        notify(f"WhatsApp — {sender}", message_text or "Nuevo mensaje", LEVEL_INFO, "WHATSAPP")
                        record_audit("WHATSAPP_NOTIFICATION", target=sender, result="SUCCESS")

                elif ntype == "badge":
                    val_str = root.attrib.get("value", "")
                    if val_str.isdigit():
                        badge_val = int(val_str)
                        if badge_val > self._last_whatsapp_badge:
                            diff = badge_val - self._last_whatsapp_badge
                            self._last_whatsapp_badge = badge_val
                            # Only alert if no toast was already produced
                            if not alerts:
                                alert = {
                                    "type": "whatsapp_badge",
                                    "source": "WhatsApp",
                                    "sender": "WhatsApp",
                                    "count": badge_val,
                                    "message": f"{badge_val} mensajes no leídos",
                                    "timestamp": time.time(),
                                    "spoken_text": f"Señor, tiene {badge_val} mensajes nuevos sin leer en WhatsApp.",
                                }
                                alerts.append(alert)
                                notify("WhatsApp", f"Tienes {badge_val} mensajes nuevos sin leer", LEVEL_INFO, "WHATSAPP")
                        else:
                            self._last_whatsapp_badge = badge_val

            conn.close()
        except Exception as e:
            # Database might be momentarily locked by Windows WPN service; ignore and retry next cycle
            pass

        for a in alerts:
            self._dispatch_alert(a)

        return alerts

    def check_gmail(self) -> List[Dict[str, Any]]:
        """Poll Gmail IMAP for new unread emails."""
        if not gmail.is_connected():
            return []

        now = time.monotonic()
        if (now - self._last_gmail_check) < self._gmail_check_interval:
            return []
        self._last_gmail_check = now

        alerts = []
        try:
            # Query recent unread emails
            unread_emails = gmail.list_recent_emails(max_results=5, unread_only=True)
            if not self._gmail_initialized:
                for m in unread_emails:
                    if m.get("id"):
                        self._seen_email_ids.add(m["id"])
                self._gmail_initialized = True
                return []

            for m in unread_emails:
                mid = m.get("id")
                if not mid or mid in self._seen_email_ids:
                    continue

                self._seen_email_ids.add(mid)
                raw_sender = m.get("sender", "Desconocido")
                sender_clean = raw_sender.split("<")[0].strip('\" ')
                subject = m.get("subject", "(Sin Asunto)")
                snippet = m.get("snippet", "")

                alert = {
                    "type": "gmail",
                    "source": "Gmail",
                    "sender": sender_clean,
                    "subject": subject,
                    "snippet": snippet,
                    "email_id": mid,
                    "timestamp": time.time(),
                    "spoken_text": f"Señor, le ha llegado un nuevo correo de {sender_clean} con el asunto: '{subject}'.",
                }
                self._last_email_msg = alert
                alerts.append(alert)

                notify(f"Gmail — {sender_clean}", subject, LEVEL_INFO, "GMAIL")
                record_audit("GMAIL_NOTIFICATION", target=sender_clean, result="SUCCESS")

        except Exception as e:
            print(f"[CommMonitor] Gmail check error: {e}")

        for a in alerts:
            self._dispatch_alert(a)

        return alerts

    def poll_once(self) -> List[Dict[str, Any]]:
        """Run one check cycle across WhatsApp and Gmail."""
        alerts = []
        alerts.extend(self.check_whatsapp())
        alerts.extend(self.check_gmail())
        return alerts

    def get_pending_alerts(self) -> List[Dict[str, Any]]:
        """Retrieve and clear pending alerts."""
        with self._lock:
            alerts = list(self._pending_alerts)
            self._pending_alerts.clear()
            return alerts

    def get_last_whatsapp(self) -> Optional[Dict[str, Any]]:
        return self._last_whatsapp_msg

    def get_last_email(self) -> Optional[Dict[str, Any]]:
        return self._last_email_msg

    def get_status(self) -> Dict[str, Any]:
        return {
            "whatsapp_installed": os.path.exists(self._wpn_db_path),
            "whatsapp_last_order": self._last_wpn_order,
            "whatsapp_last_badge": self._last_whatsapp_badge,
            "gmail_connected": gmail.is_connected(),
            "gmail_seen_count": len(self._seen_email_ids),
            "has_recent_whatsapp": bool(self._last_whatsapp_msg),
            "has_recent_email": bool(self._last_email_msg),
        }


# Global singleton instance
comm_monitor = CommunicationMonitor()
