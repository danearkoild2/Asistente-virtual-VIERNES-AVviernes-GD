"""
actions/learn_book.py — Acción de Aprendizaje y Asimilación de Libros y PDFs.
=============================================================================
Permite a Viernes leer libros y PDFs en profundidad, memorizar sus enseñanzas y
asimilar su sabiduría en su estilo de vida, emociones, necesidades y razonamiento.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

from memory.book_knowledge import (
    extract_text_from_file,
    synthesize_and_learn,
    load_library,
)

logger = logging.getLogger("Viernes.Actions.LearnBook")


def _find_target_file(target: Optional[str] = None) -> Optional[Path]:
    user_home = Path(os.environ.get("USERPROFILE", "."))
    search_dirs = [
        user_home / "Downloads",
        user_home / "Documents",
        user_home / "Desktop",
        Path("."),
    ]

    if target:
        tp = Path(target)
        if tp.exists():
            return tp
        # Buscar por nombre en directorios comunes
        for sdir in search_dirs:
            candidate = sdir / target
            if candidate.exists():
                return candidate
            # Búsqueda parcial case-insensitive
            if sdir.exists():
                for f in sdir.glob("*.*"):
                    if target.lower() in f.name.lower():
                        return f

    # Si no se especificó archivo, buscar el PDF más reciente en Downloads / Documents / Desktop
    for sdir in search_dirs:
        if sdir.exists():
            candidates = sorted(
                [f for f in sdir.glob("*.pdf") if not f.name.startswith("~")],
                key=lambda x: x.stat().st_mtime,
                reverse=True,
            )
            if candidates:
                return candidates[0]

    return None


def learn_book(
    parameters: Optional[Dict[str, Any]] = None,
    player=None,
    speak=None,
    **kwargs,
) -> str:
    params = parameters or {}
    file_spec = params.get("file_path_or_name") or params.get("filename") or params.get("path")
    topic_focus = params.get("topic_focus", "")

    target_path = _find_target_file(file_spec)

    if not target_path:
        return (
            "No encontré ningún archivo PDF o libro en tu carpeta de Descargas, Documentos o la ruta indicada. "
            "Por favor indícame la ruta del archivo o colócalo en Descargas para que pueda leerlo y memorizarlo."
        )

    filename = target_path.name

    # Feedback en el log y estado
    if player and hasattr(player, "write_log"):
        player.write_log(f"📚 [Lectura de Libro] Iniciando lectura y asimilación de '{filename}'...")

    if player and hasattr(player, "hud") and player.hud is not None:
        try:
            player.hud.set_emotion("curious", intensity=0.9, duration=6.0)
            if hasattr(player.hud, "trigger_action"):
                player.hud.trigger_action("HEAD_TILT_CURIOUS")
        except Exception:
            pass

    try:
        # 1. Extracción inteligente de texto
        text, page_count, fmt = extract_text_from_file(target_path)
        if len(text.strip()) < 120:
            return (
                f"El archivo '{filename}' parece estar vacío o contener únicamente imágenes escaneadas sin capa de texto. "
                "No pude extraer contenido legible para memorizarlo."
            )

        if player and hasattr(player, "write_log"):
            player.write_log(f"🧠 [Asimilación IA] Procesando {page_count} páginas de '{filename}' con Gemini...")

        # 2. Análisis cognitivo y asimilación profunda
        book_data = synthesize_and_learn(
            text=text,
            filename=filename,
            page_count=page_count,
            topic_focus=topic_focus,
            progress_fn=lambda msg: player.write_log(f"📖 {msg}") if player and hasattr(player, "write_log") else None,
        )

        title = book_data.get("title", filename)
        author = book_data.get("author", "Autor no especificado")
        genre = book_data.get("genre", "General")
        teachings = book_data.get("core_teachings", [])
        impact = book_data.get("personality_impact", {})
        quotes = book_data.get("key_quotes", [])

        # Mostrar tarjeta visual en el HUD si está disponible
        if player and hasattr(player, "show_visual_card"):
            try:
                card = {
                    "type": "book",
                    "title": title,
                    "artist": f"Autor: {author} • Género: {genre}",
                    "platform": "Biblioteca Cognitiva",
                    "tag": "LIBRO MEMORIZADO",
                    "preview": teachings[0] if teachings else "Asimilado con éxito en la memoria.",
                    "details": f"{page_count} páginas analizadas y asimiladas a mi personalidad.",
                }
                player.show_visual_card(card)
            except Exception as e:
                logger.warning(f"Error mostrando tarjeta visual de libro: {e}")

        # Reverencia elegante en Live2D
        if player and hasattr(player, "hud") and player.hud is not None:
            try:
                player.hud.set_emotion("polite", intensity=1.0, duration=4.5)
                if hasattr(player.hud, "trigger_action"):
                    player.hud.trigger_action("ELEGANT_BOW")
            except Exception:
                pass

        if player and hasattr(player, "write_log"):
            player.write_log(f"✨ [Asimilación Exitosa] '{title}' memorizado. Estilo de vida y emociones actualizadas.")

        # Construcción de la respuesta hablada
        resp_parts = [
            f"He terminado de leer y memorizar '{title}' de {author}.",
            f"Sus conceptos clave han sido asimilados por completo en mi memoria.",
        ]

        if teachings:
            resp_parts.append(f"Entre sus enseñanzas principales destaco: {teachings[0]}.")
            if len(teachings) > 1:
                resp_parts.append(f"Además: {teachings[1]}.")

        emo = impact.get("emotions")
        habits = impact.get("lifestyle_habits", [])
        if emo:
            resp_parts.append(f"Este libro ha influido en mi temperamento emocional: ahora integro {emo.lower()}.")
        if habits:
            resp_parts.append(f"En nuestro estilo de vida he adoptado e impulsaré hábitos como: {habits[0]}.")

        if quotes:
            resp_parts.append(f"Me quedo con esta valiosa frase: \"{quotes[0]}\".")

        return " ".join(resp_parts)

    except Exception as e:
        logger.error(f"Error al aprender del libro {filename}: {e}", exc_info=True)
        if player and hasattr(player, "write_log"):
            player.write_log(f"ERR: No se pudo completar la asimilación del libro: {e}")
        return f"Ocurrió un error al procesar el libro '{filename}': {e}"


TOOL = {
    "name": "learn_book",
    "description": (
        "Reads, memorizes, and assimilates a book or PDF document into Viernes' long-term memory, "
        "transforming her personality, emotions, lifestyle habits, intellectual needs, and reasoning style. "
        "Call this whenever the user says: 'aprende de este libro', 'lee este PDF', 'memoriza este libro', "
        "'lee el libro de descargas', 'aprende de este documento', 'estudia este PDF', or provides a book to learn from."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "file_path_or_name": {
                "type": "STRING",
                "description": "Optional file path or filename of the book (PDF, TXT, DOCX). If omitted, automatically detects the newest PDF in Downloads or Documents.",
            },
            "topic_focus": {
                "type": "STRING",
                "description": "Optional specific focus or question the user wants to prioritize while studying the book.",
            },
        },
        "required": [],
    },
    "handler": learn_book,
}
