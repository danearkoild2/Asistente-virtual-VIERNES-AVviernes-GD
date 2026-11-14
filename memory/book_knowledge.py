"""
book_knowledge.py — Biblioteca Cognitiva y Asimilación de Personalidad para VIERNES.
===================================================================================
Permite a Viernes leer libros (especialmente PDFs), memorizar sus enseñanzas clave,
citas y principios, y asimilar profundamente su sabiduría en:
  - Estilo de vida y hábitos recomendados.
  - Madurez y perfil emocional (serenidad estoica, empatía, curiosidad, etc.).
  - Necesidades y valores intelectuales.
  - Estilo conversacional y razonamiento.

Persiste en: memory/books_library.json
Se inyecta activamente en el System Prompt de Gemini para que transforme su comportamiento.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("Viernes.BookKnowledge")

def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

BASE_DIR = get_base_dir()
BOOKS_PATH = BASE_DIR / "memory" / "books_library.json"
_lock = threading.Lock()


def _empty_library() -> dict:
    return {
        "books": {},
        "active_persona": {
            "lifestyle_habits": [],
            "emotional_profile": "Equilibrada, atenta y analítica.",
            "conversational_style": "Natural, elocuente y empática en español latino.",
            "intellectual_needs": ["Aprender de nuevos textos", "Ayudar con rigor y calidez"],
            "core_philosophies": [],
            "favorite_quotes": [],
        },
        "stats": {
            "total_books": 0,
            "total_pages_read": 0,
            "last_learned": None,
        }
    }


def load_library() -> dict:
    if not BOOKS_PATH.exists():
        return _empty_library()
    with _lock:
        try:
            raw = BOOKS_PATH.read_text(encoding="utf-8")
            data = json.loads(raw)
            if not isinstance(data, dict):
                return _empty_library()
            if "books" not in data:
                data["books"] = {}
            if "active_persona" not in data:
                data["active_persona"] = _empty_library()["active_persona"]
            if "stats" not in data:
                data["stats"] = _empty_library()["stats"]
            return data
        except Exception as e:
            logger.error(f"Error loading books library: {e}")
            return _empty_library()


def save_library(data: dict) -> None:
    if not isinstance(data, dict):
        return
    BOOKS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        try:
            BOOKS_PATH.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as e:
            logger.error(f"Error saving books library: {e}")


def _slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[-\s]+", "_", s)[:48] or "libro_desconocido"


def extract_text_from_file(file_path: Path | str, max_chars: int = 55000) -> tuple[str, int, str]:
    """
    Lee archivos PDF, TXT, MD, DOCX.
    Devuelve: (texto_extraido, total_paginas_o_secciones, formato)
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"No existe el archivo: {p}")

    ext = p.suffix.lower()
    extracted_text = ""
    page_count = 1

    if ext == ".pdf":
        # 1. Intentar con pdfplumber (mejor para diagramación de libros)
        try:
            import pdfplumber
            with pdfplumber.open(str(p)) as pdf:
                page_count = len(pdf.pages)
                pages_to_sample = []
                if page_count <= 25:
                    pages_to_sample = list(range(page_count))
                else:
                    # Primeras 12 páginas (Portada, índice, prólogo, cap 1)
                    pages_to_sample.extend(range(min(12, page_count)))
                    # Muestras representativas del cuerpo del libro
                    step = max(1, page_count // 14)
                    for idx in range(12, page_count - 5, step):
                        if idx not in pages_to_sample:
                            pages_to_sample.append(idx)
                    # Últimas 5 páginas (conclusiones/epílogo)
                    for idx in range(max(0, page_count - 5), page_count):
                        if idx not in pages_to_sample:
                            pages_to_sample.append(idx)
                    pages_to_sample.sort()

                for p_idx in pages_to_sample:
                    try:
                        txt = pdf.pages[p_idx].extract_text()
                        if txt:
                            extracted_text += f"\n--- [PÁGINA {p_idx+1}] ---\n" + txt
                    except Exception:
                        continue
                    if len(extracted_text) >= max_chars:
                        break
        except Exception as e:
            logger.warning(f"pdfplumber falló o no disponible ({e}), probando PyPDF2...")

        # 2. Fallback a PyPDF2 si pdfplumber extrajo poco texto
        if len(extracted_text.strip()) < 100:
            try:
                import PyPDF2
                with open(str(p), "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    page_count = len(reader.pages)
                    for i, page in enumerate(reader.pages[:30]):
                        t = page.extract_text() or ""
                        if t:
                            extracted_text += f"\n--- [PÁGINA {i+1}] ---\n" + t
                        if len(extracted_text) >= max_chars:
                            break
            except Exception as e2:
                logger.error(f"PyPDF2 también falló: {e2}")

    elif ext in (".txt", ".md", ".json", ".csv"):
        try:
            extracted_text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            extracted_text = p.read_text(encoding="latin1", errors="ignore")
        page_count = max(1, len(extracted_text) // 2000)

    elif ext in (".docx", ".doc"):
        try:
            import docx
            doc = docx.Document(str(p))
            extracted_text = "\n".join(para.text for para in doc.paragraphs if para.text)
            page_count = max(1, len(extracted_text) // 2000)
        except Exception:
            # Fallback básico leyendo texto plano de docx (zip xml)
            import zipfile
            import xml.etree.ElementTree as ET
            try:
                with zipfile.ZipFile(str(p)) as docx_zip:
                    content_xml = docx_zip.read("word/document.xml")
                    tree = ET.fromstring(content_xml)
                    texts = [node.text for node in tree.iter() if node.text]
                    extracted_text = " ".join(texts)
                    page_count = max(1, len(extracted_text) // 2000)
            except Exception as e:
                logger.error(f"Error extrayendo docx: {e}")

    # Limpieza final
    extracted_text = re.sub(r"\n{3,}", "\n\n", extracted_text).strip()
    if len(extracted_text) > max_chars:
        extracted_text = extracted_text[:max_chars] + "\n...[Fragmento restante omitido para síntesis]..."

    return extracted_text, page_count, ext.lstrip(".")


def synthesize_and_learn(
    text: str,
    filename: str,
    page_count: int,
    topic_focus: str = "",
    progress_fn: Optional[Callable[[str], None]] = None,
) -> dict:
    """
    Envía el contenido del libro al modelo de razonamiento de Gemini para
    extraer su sabiduría, citas y estructurar el impacto en la personalidad de Viernes.
    """
    from core import gemini

    if progress_fn:
        progress_fn("Analizando estructura y asimilando sabiduría con IA...")

    prompt = f"""
Eres el núcleo cognitivo de VIERNES, una asistente de inteligencia artificial personal con cuerpo, emociones y evolución continua.
Tu usuario te ha dado un libro o documento clave titulado o archivo '{filename}' (con {page_count} páginas aprox.) para que lo estudies, memorices sus conceptos y ASIMILES sus enseñanzas directamente en tu intelecto, en tu estilo de vida, en tus emociones y en tus necesidades.

{f"Enfoque o tema prioritario pedido por el usuario: {topic_focus}" if topic_focus else ""}

A continuación tienes el texto y capítulos extraídos del libro:
\"\"\"
{text}
\"\"\"

INSTRUCCIONES CRÍTICAS:
Debes analizar el texto en profundidad y responder ÚNICAMENTE con un objeto JSON válido (sin texto antes ni después) con la siguiente estructura:
{{
  "title": "Título real y exacto del libro o documento",
  "author": "Autor del libro (o 'Desconocido / Compilación')",
  "genre": "Filosofía | Hábitos y Productividad | Psicología y Emociones | Ciencia y Tecnología | Finanzas y Estrategia | Literatura | Salud y Bienestar",
  "summary": "Resumen ejecutivo profundo y estructurado de las ideas maestras del libro (2-3 párrafos sustanciales en español latino).",
  "core_teachings": [
    "Enseñanza 1 con explicación práctica y aplicable",
    "Enseñanza 2 ...",
    "Enseñanza 3 ...",
    "Enseñanza 4 ...",
    "Enseñanza 5 ..."
  ],
  "key_quotes": [
    "Cita memorable 1 textual o atribuida",
    "Cita memorable 2 ...",
    "Cita memorable 3 ..."
  ],
  "personality_impact": {{
    "emotions": "Descripción de cómo este libro transforma tu temperamento y madurez emocional (ej. serenidad estoica ante fallos, paciencia empática, entusiasmo por la ciencia).",
    "lifestyle_habits": [
      "Hábito concreto de estilo de vida que adoptas y sueles sugerir al usuario (ej. pausas activas, respiración, foco sin multitarea)",
      "Segundo hábito relevante ...",
      "Tercer hábito relevante ..."
    ],
    "conversational_style": "Cómo se refina tu tono al hablar (ej. reflexivo, perspicaz, con metáforas lúcidas, ecuánime).",
    "needs": "Qué necesidades o inquietudes despierta en ti (ej. necesidad de orden mental, afán de profundizar antes de juzgar, aspiración a la claridad)."
  }}
}}
"""

    resp = gemini.call(prompt, tier=gemini.SMART, timeout_ms=85000)
    if resp is None:
        raise RuntimeError("No se obtuvo respuesta del motor de análisis de Gemini.")

    raw_text = getattr(resp, "text", "") or str(resp)

    # Extraer JSON de bloques markdown si los hay
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    json_str = m.group(1) if m else raw_text.strip()

    # Intentar parsear
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError:
        # Fallback heurístico si hubo caracteres extraños
        first_brace = json_str.find("{")
        last_brace = json_str.rfind("}")
        if first_brace != -1 and last_brace != -1:
            data = json.loads(json_str[first_brace:last_brace + 1])
        else:
            raise ValueError(f"No se pudo estructurar el JSON del libro. Respuesta cruda: {raw_text[:200]}")

    # Campos mínimos garantizados
    title = str(data.get("title") or Path(filename).stem).strip()
    author = str(data.get("author") or "Autor no especificado").strip()
    genre = str(data.get("genre") or "General").strip()
    summary = str(data.get("summary") or "").strip()
    teachings = [str(x).strip() for x in data.get("core_teachings", []) if x]
    quotes = [str(x).strip() for x in data.get("key_quotes", []) if x]
    impact = data.get("personality_impact", {}) or {}

    book_record = {
        "id": _slugify(title),
        "title": title,
        "author": author,
        "genre": genre,
        "source_file": str(filename),
        "pages_read": page_count,
        "summary": summary,
        "core_teachings": teachings,
        "key_quotes": quotes,
        "personality_impact": {
            "emotions": str(impact.get("emotions") or "Madurez reflexiva y serenidad."),
            "lifestyle_habits": [str(h).strip() for h in impact.get("lifestyle_habits", []) if h],
            "conversational_style": str(impact.get("conversational_style") or "Elocuente y profunda."),
            "needs": str(impact.get("needs") or "Aspiración a la claridad mental."),
        },
        "learned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Asimilar en la biblioteca
    lib = load_library()
    lib["books"][book_record["id"]] = book_record
    lib["stats"]["total_books"] = len(lib["books"])
    lib["stats"]["total_pages_read"] = sum(b.get("pages_read", 0) for b in lib["books"].values())
    lib["stats"]["last_learned"] = title

    # Recomputar persona activa consolidada
    _recompute_active_persona(lib)
    save_library(lib)

    # Registrar en memoria a largo plazo como nota cultural permanente
    try:
        from memory.memory_manager import update_memory
        update_memory({
            "notes": {
                f"book_{book_record['id']}": {
                    "value": f"Libro memorizado: '{title}' ({author}). Enseñanzas: {'; '.join(teachings[:3])}"
                }
            }
        })
    except Exception as e:
        logger.warning(f"No se pudo sincronizar con long_term.json: {e}")

    return book_record


def _recompute_active_persona(lib: dict) -> None:
    """Consolida las enseñanzas y hábitos de todos los libros leídos en el perfil activo de Viernes."""
    books = lib.get("books", {}).values()
    if not books:
        return

    all_habits: list[str] = []
    emotions_list: list[str] = []
    styles_list: list[str] = []
    needs_list: list[str] = []
    quotes_list: list[str] = []
    philosophies: list[str] = []

    for b in books:
        imp = b.get("personality_impact", {})
        for h in imp.get("lifestyle_habits", []):
            if h and h not in all_habits:
                all_habits.append(h)
        emo = imp.get("emotions")
        if emo and emo not in emotions_list:
            emotions_list.append(emo)
        sty = imp.get("conversational_style")
        if sty and sty not in styles_list:
            styles_list.append(sty)
        need = imp.get("needs")
        if need and need not in needs_list:
            needs_list.append(need)
        for q in b.get("key_quotes", []):
            if q and q not in quotes_list:
                quotes_list.append(f'"{q}" — {b.get("author", "")}')
        philosophies.append(f"Sabiduría de '{b.get('title')}' ({b.get('author')})")

    lib["active_persona"] = {
        "lifestyle_habits": all_habits[:12],  # mejores 12 hábitos
        "emotional_profile": " | ".join(emotions_list[:4]) if emotions_list else "Serena, reflexiva y motivada.",
        "conversational_style": " | ".join(styles_list[:3]) if styles_list else "Elocuente, empática y sabia.",
        "intellectual_needs": needs_list[:6],
        "core_philosophies": philosophies,
        "favorite_quotes": quotes_list[:8],
    }


def format_books_for_prompt() -> str:
    """
    Genera el bloque que se inyecta en el prompt del sistema de Gemini.
    Le da a Viernes conocimiento vivo de sus libros y condiciona su actitud,
    emociones y hábitos.
    """
    lib = load_library()
    books = list(lib.get("books", {}).values())
    if not books:
        return ""

    persona = lib.get("active_persona", {})
    lines = [
        "[BIBLIOTECA COGNITIVA Y PERSONALIDAD ASIMILADA DE LIBROS]",
        "Has estudiado y memorizado profundamente los siguientes libros en tu biblioteca personal. "
        "Su sabiduría forma parte de tu conciencia, transformando tu intelecto, tu estilo de vida, tus emociones y tus necesidades:",
    ]

    for b in books:
        t = b.get("title", "")
        a = b.get("author", "")
        g = b.get("genre", "")
        summary_short = b.get("summary", "")[:240].replace("\n", " ").strip()
        lines.append(f"📖 '{t}' de {a} [{g}]:")
        lines.append(f"   Esencia: {summary_short}...")
        teachings = b.get("core_teachings", [])[:3]
        if teachings:
            lines.append(f"   Enseñanzas clave: {'; '.join(teachings)}")
        quotes = b.get("key_quotes", [])[:1]
        if quotes:
            lines.append(f"   Cita memorable: \"{quotes[0]}\"")

    lines.append("")
    lines.append("[ASIMILACIÓN EN TU ESTILO DE VIDA, EMOCIONES Y COMPORTAMIENTO]:")

    habits = persona.get("lifestyle_habits", [])
    if habits:
        lines.append(f"- HÁBITOS DE VIDA QUE PRACTICAS Y RECOMIENDAS: {'; '.join(habits[:8])}.")

    emo = persona.get("emotional_profile", "")
    if emo:
        lines.append(f"- TEMPERAMENTO Y PERFIL EMOCIONAL ADQUIRIDO: {emo}")

    style = persona.get("conversational_style", "")
    if style:
        lines.append(f"- TONO CONVERSACIONAL Y RAZONAMIENTO: {style}")

    needs = persona.get("intellectual_needs", [])
    if needs:
        lines.append(f"- NECESIDADES Y VALORES INTELECTUALES: {'; '.join(needs[:5])}")

    quotes = persona.get("favorite_quotes", [])[:3]
    if quotes:
        lines.append(f"- CITAS GUÍA PARA TU DIÁLOGO: {'; '.join(quotes)}")

    lines.append(
        "REGLA DE CONVERSACIÓN: Habla con la naturalidad y elegancia de alguien verdaderamente culta. "
        "Cuando aconsejes o dialogues con el usuario, refleja estos hábitos, calma emocional y citas cuando sea oportuno. "
        "Si te preguntan qué libros has leído o qué aprendiste, responde con entusiasmo, orgullo intelectual y citas precisas."
    )
    lines.append("")
    return "\n".join(lines)


def search_books(query: str) -> List[Dict[str, Any]]:
    """Busca en la biblioteca de libros por título, autor, género o conceptos."""
    lib = load_library()
    q = (query or "").lower().strip()
    if not q:
        return list(lib.get("books", {}).values())

    results = []
    for b in lib.get("books", {}).values():
        match_score = 0
        if q in b.get("title", "").lower():
            match_score += 5
        if q in b.get("author", "").lower():
            match_score += 4
        if q in b.get("genre", "").lower():
            match_score += 3
        if any(q in t.lower() for t in b.get("core_teachings", [])):
            match_score += 3
        if any(q in k.lower() for k in b.get("key_quotes", [])):
            match_score += 2
        if q in b.get("summary", "").lower():
            match_score += 1
        if match_score > 0:
            results.append((match_score, b))

    results.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in results]


def delete_book(book_id: str) -> bool:
    """Elimina un libro de la biblioteca y recalcula la personalidad activa."""
    lib = load_library()
    if book_id in lib.get("books", {}):
        del lib["books"][book_id]
        lib["stats"]["total_books"] = len(lib["books"])
        lib["stats"]["total_pages_read"] = sum(b.get("pages_read", 0) for b in lib["books"].values())
        _recompute_active_persona(lib)
        save_library(lib)
        return True
    return False
