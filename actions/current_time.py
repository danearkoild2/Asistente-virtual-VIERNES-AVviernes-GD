"""
Current Time & Date Action
==========================
Returns the exact real-time local date, time, and day of the week instantly (0ms).
"""

from datetime import datetime


def time_action(parameters: dict = None, player=None, session_memory=None) -> str:
    now = datetime.now()
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]
    dia_sem = dias[now.weekday()]
    mes_nom = meses[now.month - 1]

    hora_12 = now.strftime("%I:%M %p").lstrip("0")
    hora_24 = now.strftime("%H:%M")
    fecha_full = f"{dia_sem}, {now.day} de {mes_nom} de {now.year}"

    msg = f"Son las {hora_12} ({hora_24}). Hoy es {fecha_full}."
    return msg


TOOL = {
    "name": "get_current_time",
    "description": (
        "Returns the exact real-time local current time, 12h/24h format, date, and day of the week. "
        "Use whenever the user asks for the time, hour, date, day, or current moment."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {},
    },
    "handler": time_action,
}
