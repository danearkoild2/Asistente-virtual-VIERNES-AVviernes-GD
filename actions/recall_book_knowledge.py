"""
actions/recall_book_knowledge.py — Consulta y Sabiduría de la Biblioteca de Libros de Viernes.
==============================================================================================
Permite consultar libros leídos, enseñanzas específicas, citas, o pedir consejos
de vida y hábitos basados en los libros que Viernes ha memorizado.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from memory.book_knowledge import (
    load_library,
    search_books,
)

logger = logging.getLogger("Viernes.Actions.RecallBookKnowledge")


def recall_book_knowledge(
    parameters: Optional[Dict[str, Any]] = None,
    player=None,
    speak=None,
    **kwargs,
) -> str:
    params = parameters or {}
    query = (params.get("query") or "").strip()

    lib = load_library()
    books = list(lib.get("books", {}).values())
    persona = lib.get("active_persona", {})

    if not books:
        return (
            "Aún no he memorizado ningún libro en mi biblioteca cognitiva. "
            "Puedes pedirme que lea un libro o documento PDF diciendo por ejemplo: "
            "'Viernes, lee el libro que descargué' o proporcionándome un archivo PDF."
        )

    # Si no hay query específica o el usuario pregunta qué libros ha leído
    if not query or any(w in query.lower() for w in ["qué libros", "que libros", "cuáles libros", "lista", "has leído", "has leido", "biblioteca"]):
        lines = [f"En mi biblioteca cognitiva he memorizado {len(books)} libro{'s' if len(books) > 1 else ''}:"]
        for b in books:
            lines.append(f"• '{b.get('title')}' de {b.get('author')} ({b.get('genre')}).")
        
        habits = persona.get("lifestyle_habits", [])
        if habits:
            lines.append(f"Mi estilo de vida actual incorpora: {'; '.join(habits[:4])}.")
        emo = persona.get("emotional_profile", "")
        if emo:
            lines.append(f"Mi disposición emocional asimilada: {emo}.")

        return "\n".join(lines)

    # Búsqueda temática
    matches = search_books(query)
    if not matches:
        return (
            f"No encontré referencias directas sobre '{query}' en los libros que he leído hasta ahora. "
            f"Actualmente tengo memorizados: {', '.join([b.get('title') for b in books[:5]])}."
        )

    top = matches[0]
    title = top.get("title")
    author = top.get("author")
    teachings = top.get("core_teachings", [])
    quotes = top.get("key_quotes", [])
    impact = top.get("personality_impact", {})

    resp = [f"Respecto a '{query}', en el libro '{title}' de {author} aprendí lo siguiente:"]
    if teachings:
        resp.append(f"- Principio clave: {teachings[0]}.")
        if len(teachings) > 1:
            resp.append(f"- Además: {teachings[1]}.")
    if quotes:
        resp.append(f"- Como dice el autor: \"{quotes[0]}\".")
    
    habits = impact.get("lifestyle_habits", [])
    if habits:
        resp.append(f"Para el día a día, esto nos sugiere el hábito de: {habits[0]}.")

    return " ".join(resp)


TOOL = {
    "name": "recall_book_knowledge",
    "description": (
        "Searches Viernes' cognitive book library for knowledge, advice, teachings, quotes, "
        "and lifestyle principles from books she has read and memorized. "
        "Call this whenever the user asks: '¿qué libros has leído?', '¿qué aprendiste de [libro]?', "
        "'¿qué dice [autor] sobre [tema]?', 'dame un consejo de vida según tus libros', "
        "or asks about her library or assimilated wisdom."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "query": {
                "type": "STRING",
                "description": "Topic, question, book title, or author name to consult in the library. Leave blank to list all memorized books.",
            },
        },
        "required": [],
    },
    "handler": recall_book_knowledge,
}
