"""
WhatsApp automation driver and message composer for VIERNES.
Supports:
1. Windows WhatsApp Desktop app automation via Win32 / PyAutoGUI / URI protocol.
2. WhatsApp Web fallback via default browser.
3. Intelligent draft composition, clipboard synchronization, and HUD preview.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Optional, Tuple

try:
    import pyautogui
    pyautogui.FAILSAFE = True
    _PYAUTOGUI = True
except ImportError:
    _PYAUTOGUI = False

try:
    import pyperclip
    _PYPERCLIP = True
except ImportError:
    _PYPERCLIP = False


class WhatsAppTransport:
    """Robust WhatsApp transport driver for Windows desktop and web."""

    def __init__(self):
        self.os_name = "windows"

    def compose_and_copy(self, receiver: str, message: str) -> str:
        """Copies drafted message to clipboard and formats preview."""
        if _PYPERCLIP:
            pyperclip.copy(message)
        return message

    def open_whatsapp_uri(self, text: str, phone: Optional[str] = None) -> bool:
        """Opens WhatsApp with pre-filled message text via Windows protocol handler."""
        try:
            encoded_text = urllib.parse.quote(text)
            if phone:
                clean_phone = "".join(ch for ch in phone if ch.isdigit() or ch == "+")
                uri = f"whatsapp://send?phone={clean_phone}&text={encoded_text}"
            else:
                uri = f"whatsapp://send?text={encoded_text}"
            
            # Try Windows protocol handler first (launches official WhatsApp Desktop app)
            if sys.platform == "win32":
                os.startfile(uri)
                return True
            else:
                subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", uri])
                return True
        except Exception as e:
            print(f"[WhatsApp] Protocol launch error ({e}), falling back to web...")
            return False

    def open_whatsapp_web(self, text: str, phone: Optional[str] = None) -> bool:
        """Opens WhatsApp Web in default browser with pre-filled text."""
        import webbrowser
        try:
            encoded_text = urllib.parse.quote(text)
            if phone:
                clean_phone = "".join(ch for ch in phone if ch.isdigit() or ch == "+")
                url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={encoded_text}"
            else:
                url = f"https://web.whatsapp.com/send?text={encoded_text}"
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"[WhatsApp] Web open error: {e}")
            return False

    def send_message_to(self, receiver: str, message: str, draft_only: bool = False) -> Tuple[bool, str]:
        """
        Sends or drafts a message to receiver on WhatsApp.
        Copies text to clipboard, prepares desktop app / web, and delivers.
        """
        if not message.strip():
            return False, "El contenido del mensaje está vacío."

        # 1. Always copy the polished message to clipboard so user has it immediately
        self.compose_and_copy(receiver, message)

        # 2. Check if receiver looks like a phone number
        is_phone = any(ch.isdigit() for ch in receiver) and len([c for c in receiver if c.isdigit()]) >= 7
        phone_num = receiver if is_phone else None

        # 3. If draft_only, open WhatsApp with text ready without automatically submitting
        if draft_only:
            opened = self.open_whatsapp_uri(message, phone_num)
            if not opened:
                self.open_whatsapp_web(message, phone_num)
            return True, f"Borrador preparado para {receiver} y copiado al portapapeles."

        # 4. Attempt desktop app automation if PyAutoGUI is present
        if _PYAUTOGUI:
            try:
                # Open or focus WhatsApp
                opened_uri = self.open_whatsapp_uri(message, phone_num)
                time.sleep(1.8)

                if not is_phone:
                    # Search contact in WhatsApp
                    pyautogui.hotkey("ctrl", "f")
                    time.sleep(0.5)
                    pyautogui.hotkey("ctrl", "a")
                    pyautogui.press("backspace")
                    time.sleep(0.1)
                    if _PYPERCLIP:
                        pyperclip.copy(receiver)
                        time.sleep(0.1)
                        pyautogui.hotkey("ctrl", "v")
                    else:
                        pyautogui.write(receiver, interval=0.03)
                    time.sleep(1.0)
                    pyautogui.press("enter")
                    time.sleep(0.8)

                    # Paste the message into the message box
                    if _PYPERCLIP:
                        pyperclip.copy(message)
                        time.sleep(0.1)
                        pyautogui.hotkey("ctrl", "v")
                    else:
                        pyautogui.write(message, interval=0.02)
                    time.sleep(0.3)

                # Send
                pyautogui.press("enter")
                time.sleep(0.4)
                return True, f"Mensaje enviado con éxito a {receiver} vía WhatsApp."
            except Exception as e:
                print(f"[WhatsApp] Desktop automation error: {e}")

        # Fallback to URI / Web
        if self.open_whatsapp_uri(message, phone_num) or self.open_whatsapp_web(message, phone_num):
            return True, f"WhatsApp abierto con el mensaje listo para {receiver} (copiado al portapapeles)."

        return False, "No se pudo abrir WhatsApp en el sistema."


_instance: Optional[WhatsAppTransport] = None


def get() -> Tuple[Optional[WhatsAppTransport], str]:
    """Returns singleton WhatsApp transport."""
    global _instance
    try:
        if _instance is None:
            _instance = WhatsAppTransport()
        return _instance, "WhatsApp driver ready."
    except Exception as e:
        return None, f"Error initializing WhatsApp transport: {e}"
