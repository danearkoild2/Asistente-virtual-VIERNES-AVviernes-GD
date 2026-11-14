import json
import subprocess
import sys
import time
from pathlib import Path

try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE    = 0.06
    _PYAUTOGUI = True
except ImportError:
    _PYAUTOGUI = False

try:
    import pyperclip
    _PYPERCLIP = True
except ImportError:
    _PYPERCLIP = False

def _base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

def _get_os() -> str:
    try:
        cfg = json.loads(
            (_base_dir() / "config" / "api_keys.json").read_text(encoding="utf-8")
        )
        return cfg.get("os_system", "windows").lower()
    except Exception:
        return "windows"


def _require_pyautogui():
    if not _PYAUTOGUI:
        raise RuntimeError("PyAutoGUI not installed. Run: pip install pyautogui")


def _paste_text(text: str) -> None:
    _require_pyautogui()

    os_name = _get_os()
    paste_hotkey = ("command", "v") if os_name == "mac" else ("ctrl", "v")

    if _PYPERCLIP:
        pyperclip.copy(text)
        time.sleep(0.15)
        pyautogui.hotkey(*paste_hotkey)
        time.sleep(0.1)
    else:
        pyautogui.write(text, interval=0.03)


def _clear_and_paste(text: str) -> None:
    _require_pyautogui()
    os_name = _get_os()
    select_all = ("command", "a") if os_name == "mac" else ("ctrl", "a")
    pyautogui.hotkey(*select_all)
    time.sleep(0.1)
    pyautogui.press("delete")
    time.sleep(0.1)
    _paste_text(text)

def _open_app(app_name: str) -> bool:
    _require_pyautogui()
    os_name = _get_os()

    try:
        if os_name == "windows":
            if "whatsapp" in app_name.lower():
                try:
                    subprocess.Popen(["explorer.exe", "shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"])
                    time.sleep(2.0)
                    return True
                except Exception:
                    pass
            pyautogui.press("win")
            time.sleep(0.5)
            _paste_text(app_name)
            time.sleep(0.6)
            pyautogui.press("enter")
            time.sleep(2.5)
            return True

        elif os_name == "mac":
            result = subprocess.run(
                ["open", "-a", app_name],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode != 0:
                result = subprocess.run(
                    ["open", "-a", f"{app_name}.app"],
                    capture_output=True, text=True, timeout=10,
                )
            time.sleep(2.5)
            return result.returncode == 0

        else: 
            launched = False
            for launcher in [
                ["gtk-launch", app_name.lower()],
                [app_name.lower()],
            ]:
                try:
                    subprocess.Popen(
                        launcher,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    launched = True
                    break
                except FileNotFoundError:
                    continue
            time.sleep(2.5)
            return launched

    except Exception as e:
        print(f"[SendMessage] ⚠️ Could not open {app_name}: {e}")
        return False


def _open_browser_url(url: str) -> bool:
    import webbrowser
    try:
        webbrowser.open(url)
        time.sleep(4.0) 
        return True
    except Exception as e:
        print(f"[SendMessage] ⚠️ Could not open browser: {e}")
        return False

def _search_in_app(query: str) -> None:
    _require_pyautogui()
    os_name = _get_os()
    search_hotkey = ("command", "f") if os_name == "mac" else ("ctrl", "f")

    pyautogui.hotkey(*search_hotkey)
    time.sleep(0.5)
    _clear_and_paste(query)
    time.sleep(1.0)

def _desktop_send(app_name: str, receiver: str, message: str) -> str:
    if not _open_app(app_name):
        return f"Could not open {app_name}."

    time.sleep(1.0)
    _search_in_app(receiver)
    pyautogui.press("enter")
    time.sleep(0.8)

    _paste_text(message)
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(0.3)
    return f"Message sent to {receiver} via {app_name}."

def _send_whatsapp(receiver: str, message: str) -> str:
    """WhatsApp goes through the verified driver when there is one.

    _desktop_send below is a sequence of keystrokes with sleeps between them:
    it presses Win, types the app name, presses Ctrl+F, types the contact,
    presses Enter twice and reports success — without ever reading back which
    window received any of that. When the machine is a second slower than the
    sleeps assume, the whole sequence lands somewhere else and the user is
    still told the message was sent.

    plugins/_whatsapp_core.py already drives WhatsApp properly for the calling
    plugins: it finds the real window, opens the conversation, checks the
    conversation is the right person's, types, and confirms the box emptied
    before it says "sent". Using it here costs nothing and removes the one
    failure that matters — a message reported as delivered that never left.

    The blind path stays as the fallback for a machine where the driver cannot
    run at all (the plugin file removed, a missing dependency, no WhatsApp).
    But once the driver HAS run, its answer stands: falling back after it
    refused to send is how a message ends up typed into the wrong
    conversation, which is worse than not sending it.
    """
    try:
        from plugins import _whatsapp_core as wa
    except Exception as e:
        print(f"[SendMessage] WhatsApp driver unavailable ({e}) — typing blind.")
        return _desktop_send("WhatsApp", receiver, message)

    try:
        transport, why = wa.get()
    except Exception as e:
        print(f"[SendMessage] WhatsApp driver failed to start ({e}) — typing blind.")
        return _desktop_send("WhatsApp", receiver, message)

    if transport is None:
        print(f"[SendMessage] {why} — typing blind.")
        return _desktop_send("WhatsApp", receiver, message)

    sent, failure = transport.send_message_to(receiver, message)
    if sent:
        return f"Message sent to {receiver} via WhatsApp."
    return (f"The message to {receiver} was NOT sent on WhatsApp: {failure}. "
            f"Tell the user plainly that it was not sent, and why - do not "
            f"say it was sent.")

def _send_telegram(receiver: str, message: str) -> str:
    return _desktop_send("Telegram", receiver, message)

def _send_signal(receiver: str, message: str) -> str:
    return _desktop_send("Signal", receiver, message)


def _send_discord(receiver: str, message: str) -> str:
    return _desktop_send("Discord", receiver, message)


def _send_instagram(receiver: str, message: str) -> str:
    _require_pyautogui()

    if not _open_browser_url("https://www.instagram.com/direct/new/"):
        return "Could not open Instagram in browser."

    _paste_text(receiver)
    time.sleep(1.5)

    pyautogui.press("down")
    time.sleep(0.3)
    pyautogui.press("enter")   
    time.sleep(0.4)

    for _ in range(4):
        pyautogui.press("tab")
        time.sleep(0.15)
    pyautogui.press("enter")
    time.sleep(2.0)

    _paste_text(message)
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(0.3)

    return f"Message sent to {receiver} via Instagram."


def _send_messenger(receiver: str, message: str) -> str:
    _require_pyautogui()

    if not _open_browser_url("https://www.messenger.com/"):
        return "Could not open Messenger in browser."


    _search_in_app(receiver)
    time.sleep(0.5)
    pyautogui.press("down")
    time.sleep(0.3)
    pyautogui.press("enter")
    time.sleep(1.0)

    _paste_text(message)
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(0.3)

    return f"Message sent to {receiver} via Messenger."

_PLATFORM_MAP = [
    ({"whatsapp", "wp", "wapp"},              _send_whatsapp),
    ({"telegram", "tg"},                      _send_telegram),
    ({"instagram", "ig", "insta"},            _send_instagram),
    ({"signal"},                               _send_signal),
    ({"discord"},                              _send_discord),
    ({"messenger", "facebook", "fb"},         _send_messenger),
]


def _resolve_platform(platform_str: str):
    key = platform_str.lower().strip()
    for keywords, handler in _PLATFORM_MAP:
        if any(k in key for k in keywords):
            return handler
    return lambda r, m: _desktop_send(platform_str.strip().title(), r, m)


def send_message(
    parameters: dict,
    response=None,
    player=None,
    session_memory=None,
) -> str:
    params       = parameters or {}
    receiver     = params.get("receiver", "").strip()
    message_text = params.get("message_text", "").strip()
    platform     = params.get("platform", "whatsapp").strip()
    action_type  = params.get("action_type", "send").strip().lower()  # "send" | "draft"

    if not receiver:
        return "Por favor especifica un destinatario (ej. 'Sami')."
    if not message_text:
        return "Por favor indica el contenido o idea del mensaje a redactar/enviar."

    # Copy to clipboard immediately for convenient access
    if _PYPERCLIP:
        try:
            pyperclip.copy(message_text)
        except Exception:
            pass

    # Show drafted message card in the UI HUD panel
    if player and hasattr(player, "show_content"):
        try:
            preview_card = (
                f"📱 WhatsApp para: {receiver}\n"
                f"────────────────────────────\n"
                f"{message_text}\n\n"
                f"📋 Estado: Copiado al portapapeles | {'Borrador listo' if action_type == 'draft' else 'Enviando...'}"
            )
            player.show_content(f"WhatsApp: {receiver}", preview_card)
        except Exception:
            pass

    preview = message_text[:50] + ("..." if len(message_text) > 50 else "")
    try:
        print(f"[SendMessage] [MSG] {platform} ({action_type}) -> {receiver}: {preview}")
    except Exception:
        pass
    if player and hasattr(player, "write_log"):
        player.write_log(f"MSG: {platform} -> {receiver} ({action_type})")

    # If user explicitly asked only to draft / compose:
    if action_type in ("draft", "redactar", "compose"):
        try:
            from plugins import _whatsapp_core as wa
            transport, _ = wa.get()
            if transport:
                transport.send_message_to(receiver, message_text, draft_only=True)
        except Exception:
            pass
        return (
            f"Mensaje para {receiver} redactado y copiado al portapapeles con éxito: "
            f"\"{message_text}\". Está listo en WhatsApp para que lo revises y envíes."
        )

    try:
        handler = _resolve_platform(platform)
        result  = handler(receiver, message_text)
    except Exception as e:
        result = f"No se pudo enviar el mensaje: {e}"

    lowered = result.lower()
    ok = "sent" in lowered and "not sent" not in lowered
    try:
        print(f"[SendMessage] {'[OK]' if ok else '[FAIL]'} {result}")
    except Exception:
        pass
    if player and hasattr(player, "write_log"):
        player.write_log(f"MSG: {result}")

    return result


# ── Tool declaration (auto-discovered by core/action_loader.py) ──────────────
TOOL = {
    "name": "send_message",
    "description": (
        "Redacta y envía mensajes de texto por WhatsApp, Telegram u otra plataforma. "
        "Cuando el usuario pida enviar o redactar un mensaje (ejemplo: 'envíale un mensaje a Sami "
        "diciendo que no podré ir hoy, redáctalo bien'), redacta un mensaje completo, amable, "
        "natural y educado en 'message_text' en el idioma del usuario (con saludo cordial, explicación "
        "clara y despedida afectuosa), y especifica 'receiver' y 'platform' ('whatsapp'). "
        "Usa 'action_type'='draft' si el usuario pide redactarlo o prepararlo, o 'send' para enviarlo."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "receiver": {
                "type": "STRING",
                "description": "Nombre del contacto o destinatario (ej. 'Sami', 'Mamá', 'Carlos')."
            },
            "message_text": {
                "type": "STRING",
                "description": "El texto del mensaje redactado de forma profesional, clara y cordial."
            },
            "platform": {
                "type": "STRING",
                "description": "Plataforma: 'whatsapp' (por defecto), 'telegram', etc."
            },
            "action_type": {
                "type": "STRING",
                "enum": ["send", "draft"],
                "description": "'send' para enviar directamente, o 'draft' para redactar, copiar al portapapeles y previsualizar."
            }
        },
        "required": [
            "receiver",
            "message_text",
            "platform"
        ]
    },
    "handler": send_message,
}
