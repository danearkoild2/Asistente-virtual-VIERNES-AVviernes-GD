"""
Personal Voice Journal & Mood Log Plugin for MARK LV / Viernes.
Records dated thoughts, reflections and gratitude logs in markdown.
"""
from __future__ import annotations
from datetime import datetime
from pathlib import Path

PLUGIN = {
    "name": "voice_journal",
    "description": (
        "Records an entry into the user's personal voice journal with timestamp. "
        "Use when user says 'anota en mi diario', 'entrada de diario', 'diario personal', "
        "or 'querido diario'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "entry_text": {
                "type": "STRING",
                "description": "The thought, story or note to record into the journal.",
            },
            "mood": {
                "type": "STRING",
                "description": "Optional mood assessment (e.g. 'motivado', 'cansado', 'feliz', 'productivo').",
            }
        },
        "required": ["entry_text"],
    },
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    entry = parameters.get("entry_text", "").strip()
    mood = parameters.get("mood", "neutral").strip()

    if not entry:
        return "No me dijiste qué registrar en tu diario."

    now = datetime.now()
    journal_dir = Path.home() / "Documents" / "Viernes_Journal"
    journal_dir.mkdir(parents=True, exist_ok=True)

    filename = journal_dir / f"Diario_{now.strftime('%Y_%m')}.md"
    date_header = now.strftime("%A, %d de %B de %Y - %H:%M")

    content = f"\n### 📝 {date_header}\n- **Estado de ánimo:** {mood}\n- **Entrada:** {entry}\n\n---\n"

    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content)
        msg = f"Entrada registrada en tu diario personal con fecha de hoy. Que descanses y sigas adelante."
    except Exception as e:
        msg = f"No se pudo guardar la entrada del diario: {e}"

    if player:
        try:
            player.write_log(f"SYS: {msg}")
        except Exception:
            pass

    return msg
