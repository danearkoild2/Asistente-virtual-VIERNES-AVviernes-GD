"""
Repeat Last Said Action
=======================
Instantly retrieves and returns the last thing Viernes said to the user.
"""

# Global reference updated by main.py
LAST_SPOKEN_TEXT: str = ""


def set_last_spoken(text: str) -> None:
    global LAST_SPOKEN_TEXT
    if text and text.strip():
        LAST_SPOKEN_TEXT = text.strip()


def get_last_spoken() -> str:
    return LAST_SPOKEN_TEXT


def repeat_action(parameters: dict = None, player=None, session_memory=None, last_said: str = None) -> str:
    msg = (last_said or "").strip() or LAST_SPOKEN_TEXT or (session_memory.get_last_response() if session_memory else "")
    if not msg:
        return "No he dicho nada todavía que pueda repetir."
    return f"Lo último que dije fue: {msg}"


TOOL = {
    "name": "repeat_last_said",
    "description": (
        "Repeats the exact last sentence or response that the assistant spoke. "
        "Use whenever the user asks 'qué dijiste?', 'repite lo que dijiste', 'puedes repetir?', 'repeat that', etc."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {},
    },
    "handler": repeat_action,
}
