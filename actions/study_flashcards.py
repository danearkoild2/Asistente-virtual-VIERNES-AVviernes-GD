"""
actions/study_flashcards.py — Modo Estudio y Flashcards por Voz (estilo Anki).
===============================================================================
Crea mazos de tarjetas de estudio desde un tema, texto, PDF/DOCX/TXT o libros
aprendidos, y realiza sesiones interactivas por voz con repaso espaciado local
guardado en memory/flashcards.json.
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger("Viernes.Actions.StudyFlashcards")

_CARDS_PATH = Path("memory/flashcards.json")


def _load_decks() -> Dict[str, Any]:
    if not _CARDS_PATH.exists():
        return {"decks": {}}
    try:
        return json.loads(_CARDS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"decks": {}}


def _save_decks(data: Dict[str, Any]) -> None:
    _CARDS_PATH.parent.mkdir(parents=True, exist_ok=True)
    _CARDS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _extract_source_text(source: str) -> str:
    p = Path(source).expanduser()
    if p.exists() and p.is_file():
        ext = p.suffix.lower()
        if ext in (".txt", ".md"):
            return p.read_text(encoding="utf-8", errors="ignore")[:18000]
        if ext == ".pdf":
            try:
                from pypdf import PdfReader
                reader = PdfReader(str(p))
                return "\n".join((pg.extract_text() or "") for pg in reader.pages[:15])[:18000]
            except Exception:
                return ""
        if ext == ".docx":
            try:
                import docx
                doc = docx.Document(str(p))
                return "\n".join(par.text for par in doc.paragraphs)[:18000]
            except Exception:
                return ""
    return source


def _generate_cards_ai(topic_or_text: str, count: int = 8) -> List[Dict[str, str]]:
    from google import genai
    from memory.config_manager import get_gemini_key

    api_key = get_gemini_key()
    if not api_key:
        raise RuntimeError("Se requiere la API Key de Gemini para generar flashcards.")

    client = genai.Client(api_key=api_key)
    prompt = (
        f"Genera exactamente {count} flashcards de estudio estilo Anki en español sobre el siguiente material o tema.\n"
        "Responde ÚNICAMENTE con un JSON válido (lista de objetos) donde cada objeto tenga:\n"
        '  "question": pregunta clara y directa para hacer por voz,\n'
        '  "answer": respuesta concisa y precisa,\n'
        '  "hint": pista breve.\n\n'
        f"Material / Tema:\n{topic_or_text[:15000]}"
    )
    resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    raw = (resp.text or "").strip()
    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    cards = json.loads(raw)
    out: List[Dict[str, str]] = []
    for c in cards:
        if isinstance(c, dict) and c.get("question") and c.get("answer"):
            out.append({
                "question": str(c["question"]).strip(),
                "answer": str(c["answer"]).strip(),
                "hint": str(c.get("hint", "")).strip(),
            })
    return out


def study_flashcards(parameters: Dict[str, Any], player=None) -> str:
    params = parameters or {}
    action = str(params.get("action", "quiz_next")).strip().lower()
    deck_name = str(params.get("deck_name", "general")).strip() or "general"
    source = str(params.get("source", "")).strip()
    user_answer = str(params.get("user_answer", "")).strip()
    count = int(params.get("count", 8) or 8)

    data = _load_decks()
    decks = data.setdefault("decks", {})

    if action in ("create", "create_from_source", "crear"):
        material = _extract_source_text(source or deck_name)
        if not material:
            return "Indica un tema, texto o ruta de archivo (PDF/TXT/MD/DOCX) para generar las flashcards."
        try:
            cards = _generate_cards_ai(material, count=max(3, min(count, 20)))
        except Exception as e:
            return f"No se pudieron generar las flashcards: {e}"

        now_iso = datetime.now().isoformat()
        deck = decks.setdefault(deck_name, {"cards": [], "last_index": -1})
        for c in cards:
            deck["cards"].append({
                **c,
                "interval_days": 0,
                "ease": 2.5,
                "hits": 0,
                "misses": 0,
                "next_review": now_iso,
            })
        _save_decks(data)
        return (
            f"Listo: agregué {len(cards)} flashcards al mazo '{deck_name}'. "
            "Di 'hazme una pregunta de estudio' para empezar el repaso por voz."
        )

    if action in ("quiz_next", "preguntar", "estudiar"):
        if not decks:
            return "Aún no tienes mazos de estudio. Pídeme: 'crea flashcards sobre Python' o pasa un PDF."
        deck = decks.get(deck_name)
        if not deck:
            deck_name = next(iter(decks))
            deck = decks[deck_name]
        cards = deck.get("cards", [])
        if not cards:
            return f"El mazo '{deck_name}' está vacío."

        now = datetime.now()
        due_indices = [
            i for i, c in enumerate(cards)
            if datetime.fromisoformat(c.get("next_review", now.isoformat())) <= now
        ]
        idx = due_indices[0] if due_indices else ((deck.get("last_index", -1) + 1) % len(cards))
        deck["last_index"] = idx
        _save_decks(data)
        card = cards[idx]
        hint_txt = f" (Pista disponible si la pides)" if card.get("hint") else ""
        return f"Mazo '{deck_name}' — Pregunta {idx + 1}/{len(cards)}:{hint_txt} {card['question']}"

    if action in ("check_answer", "responder", "evaluar"):
        deck = decks.get(deck_name)
        if not deck or not deck.get("cards"):
            return f"No encontré el mazo '{deck_name}' activo."
        idx = deck.get("last_index", 0)
        if idx < 0 or idx >= len(deck["cards"]):
            idx = 0
        card = deck["cards"][idx]
        expected = card["answer"]
        correct = False

        if user_answer:
            # Evaluación semántica rápida con Gemini o coincidencia básica
            try:
                from google import genai
                from memory.config_manager import get_gemini_key
                api_key = get_gemini_key()
                if api_key:
                    client = genai.Client(api_key=api_key)
                    ev = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=(
                            f"Pregunta: {card['question']}\nRespuesta esperada: {expected}\n"
                            f"Respuesta del estudiante: {user_answer}\n"
                            "Responde SOLO con 'CORRECTO' o 'INCORRECTO' seguido de una explicación breve de 1 frase en español."
                        ),
                    )
                    verdict = (ev.text or "").strip()
                    correct = verdict.upper().startswith("CORRECTO")
                    feedback = verdict
                else:
                    correct = user_answer.lower() in expected.lower()
                    feedback = f"Respuesta esperada: {expected}"
            except Exception:
                correct = user_answer.lower() in expected.lower()
                feedback = f"Respuesta esperada: {expected}"
        else:
            feedback = f"La respuesta es: {expected}"

        if correct:
            card["hits"] = card.get("hits", 0) + 1
            interval = max(1, int((card.get("interval_days", 0) or 1) * card.get("ease", 2.5)))
            card["interval_days"] = interval
            card["next_review"] = (datetime.now() + timedelta(days=interval)).isoformat()
        else:
            card["misses"] = card.get("misses", 0) + 1
            card["interval_days"] = 0
            card["next_review"] = (datetime.now() + timedelta(minutes=10)).isoformat()

        _save_decks(data)
        return feedback

    if action in ("list_decks", "stats", "listar"):
        if not decks:
            return "No tienes mazos de estudio creados todavía."
        lines = []
        for name, d in decks.items():
            cards = d.get("cards", [])
            hits = sum(c.get("hits", 0) for c in cards)
            misses = sum(c.get("misses", 0) for c in cards)
            lines.append(f"- {name}: {len(cards)} tarjetas (aciertos: {hits}, fallos: {misses})")
        return "Mazos de estudio:\n" + "\n".join(lines)

    return "Acción no reconocida para study_flashcards. Usa: create_from_source, quiz_next, check_answer o list_decks."


TOOL = {
    "name": "study_flashcards",
    "description": (
        "Voice-interactive Anki-style study and spaced-repetition flashcard mode. Generates decks from topics, "
        "text, or PDF/DOCX/MD files, quizzes the user aloud, and evaluates spoken answers. "
        "Use when the user says: 'crea flashcards de...', 'modo estudio', 'hazme preguntas de repaso', "
        "'evalúa mi respuesta', 'mis mazos de estudio'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "One of: 'create_from_source', 'quiz_next', 'check_answer', 'list_decks'.",
            },
            "deck_name": {
                "type": "STRING",
                "description": "Name of the flashcard deck.",
            },
            "source": {
                "type": "STRING",
                "description": "Topic, raw text, or file path (PDF/DOCX/MD/TXT) to generate cards from.",
            },
            "user_answer": {
                "type": "STRING",
                "description": "The user's spoken answer to evaluate (used with action='check_answer').",
            },
            "count": {
                "type": "INTEGER",
                "description": "Number of flashcards to generate (default 8).",
            },
        },
        "required": ["action"],
    },
    "handler": study_flashcards,
}
