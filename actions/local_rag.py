"""
actions/local_rag.py — Segundo Cerebro / RAG Local de Carpetas y Proyectos.
===========================================================================
Indexa archivos de texto, código, Markdown, PDFs y DOCX en SQLite FTS5 local
(memory/local_rag.db) con ruta exacta y rango de líneas, permitiendo búsquedas
instantáneas sin subir carpetas enteras a la nube.
"""

from __future__ import annotations

import logging
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Tuple

logger = logging.getLogger("Viernes.Actions.LocalRAG")

_DB_PATH = Path("memory/local_rag.db")
_SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv", "env",
    "build", "dist", ".idea", ".vscode", "outputs", "logs",
}
_TEXT_EXTS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".md", ".txt",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".sql", ".sh", ".bat", ".ps1",
}


def _get_conn() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks USING fts5(
            file_path,
            start_line UNINDEXED,
            end_line UNINDEXED,
            content,
            tokenize='unicode61'
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS indexed_files (
            file_path TEXT PRIMARY KEY,
            mtime REAL NOT NULL,
            chunk_count INTEGER NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def _extract_lines(path: Path) -> List[str]:
    ext = path.suffix.lower()
    if ext in _TEXT_EXTS:
        return path.read_text(encoding="utf-8", errors="ignore").splitlines()
    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            lines: List[str] = []
            for i, page in enumerate(reader.pages, 1):
                txt = page.extract_text() or ""
                for ln in txt.splitlines():
                    lines.append(f"[p.{i}] {ln}")
            return lines
        except Exception:
            return []
    if ext == ".docx":
        try:
            import docx
            doc = docx.Document(str(path))
            return [p.text for p in doc.paragraphs if p.text.strip()]
        except Exception:
            return []
    return []


def _chunk_lines(lines: List[str], chunk_size: int = 45, overlap: int = 8) -> List[Tuple[int, int, str]]:
    chunks: List[Tuple[int, int, str]] = []
    if not lines:
        return chunks
    step = max(1, chunk_size - overlap)
    for idx in range(0, len(lines), step):
        part = lines[idx: idx + chunk_size]
        text = "\n".join(part).strip()
        if text:
            chunks.append((idx + 1, idx + len(part), text))
        if idx + chunk_size >= len(lines):
            break
    return chunks


def _index_path(target: Path) -> Tuple[int, int]:
    conn = _get_conn()
    files_indexed = 0
    chunks_added = 0

    candidates: List[Path] = []
    if target.is_file():
        candidates.append(target)
    elif target.is_dir():
        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d not in _SKIP_DIRS]
            for fn in files:
                fp = Path(root) / fn
                if fp.suffix.lower() in _TEXT_EXTS or fp.suffix.lower() in (".pdf", ".docx"):
                    if fp.stat().st_size <= 5_000_000:
                        candidates.append(fp)

    for fp in candidates:
        fp_str = str(fp.resolve())
        mtime = fp.stat().st_mtime
        row = conn.execute("SELECT mtime FROM indexed_files WHERE file_path = ?", (fp_str,)).fetchone()
        if row and abs(row[0] - mtime) < 0.01:
            continue

        lines = _extract_lines(fp)
        chunks = _chunk_lines(lines)
        conn.execute("DELETE FROM chunks WHERE file_path = ?", (fp_str,))
        for s_line, e_line, content in chunks:
            conn.execute(
                "INSERT INTO chunks (file_path, start_line, end_line, content) VALUES (?, ?, ?, ?)",
                (fp_str, s_line, e_line, content),
            )
        conn.execute(
            "INSERT OR REPLACE INTO indexed_files (file_path, mtime, chunk_count) VALUES (?, ?, ?)",
            (fp_str, mtime, len(chunks)),
        )
        files_indexed += 1
        chunks_added += len(chunks)

    conn.commit()
    conn.close()
    return files_indexed, chunks_added


def _search_fts(query: str, limit: int = 6) -> List[Tuple[str, int, int, str]]:
    conn = _get_conn()
    tokens = [t.strip("\"'()[]{}:;,.!?") for t in query.split() if len(t.strip()) >= 2]
    if not tokens:
        conn.close()
        return []
    fts_query = " OR ".join(f'"{t}"' for t in tokens[:8])
    try:
        rows = conn.execute(
            """
            SELECT file_path, start_line, end_line, content
            FROM chunks
            WHERE chunks MATCH ?
            ORDER BY bm25(chunks)
            LIMIT ?
            """,
            (fts_query, limit),
        ).fetchall()
    except Exception:
        rows = []
    conn.close()
    return rows


def local_rag(parameters: Dict[str, Any], player=None) -> str:
    params = parameters or {}
    action = str(params.get("action", "query")).strip().lower()
    path_arg = str(params.get("path", ".")).strip() or "."
    query = str(params.get("query", "")).strip()

    if action in ("index", "indexar"):
        target = Path(path_arg).expanduser()
        if not target.exists():
            return f"No encontré la ruta '{path_arg}' para indexar."
        files_n, chunks_n = _index_path(target)
        return (
            f"Segundo Cerebro actualizado para `{target}`: "
            f"{files_n} archivo(s) nuevo(s)/modificado(s) y {chunks_n} fragmentos indexados localmente."
        )

    if action in ("stats", "estado"):
        conn = _get_conn()
        f_count = conn.execute("SELECT COUNT(*) FROM indexed_files").fetchone()[0]
        c_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        conn.close()
        return f"Índice RAG local: {f_count} archivo(s) y {c_count} fragmentos almacenados en `{_DB_PATH}`."

    if action in ("clear", "limpiar"):
        if _DB_PATH.exists():
            _DB_PATH.unlink()
        return "Índice local del Segundo Cerebro eliminado."

    if action in ("query", "buscar", "preguntar"):
        if not query:
            return "Indica qué pregunta o término deseas buscar en tu Segundo Cerebro local."
        hits = _search_fts(query, limit=6)
        if not hits:
            return (
                f"No encontré fragmentos relevantes para '{query}' en el índice local. "
                "Si aún no indexaste la carpeta, pídeme 'indexa la carpeta ...'."
            )

        context_blocks = []
        sources = []
        for fp, s_l, e_l, txt in hits:
            rel = os.path.relpath(fp, start=".") if os.path.exists(fp) else fp
            sources.append(f"- `{rel}:L{s_l}-L{e_l}`")
            context_blocks.append(f"[{rel} L{s_l}-L{e_l}]\n{txt[:900]}")

        try:
            from google import genai
            from memory.config_manager import get_gemini_key

            api_key = get_gemini_key()
            if api_key:
                client = genai.Client(api_key=api_key)
                prompt = (
                    f"Responde en español de forma precisa usando SOLO estos fragmentos locales indexados. "
                    f"Cita siempre el archivo y rango de líneas.\n\nPregunta: {query}\n\n"
                    + "\n\n---\n\n".join(context_blocks)
                )
                resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                answer = (resp.text or "").strip()
                if answer:
                    return f"{answer}\n\n**Fuentes locales:**\n" + "\n".join(sources)
        except Exception as e:
            logger.warning(f"Síntesis Gemini RAG falló, devolviendo fragmentos directos: {e}")

        return "**Coincidencias locales encontradas:**\n" + "\n".join(sources) + "\n\n" + context_blocks[0][:600]

    return "Acción no reconocida para local_rag. Usa: index, query, stats o clear."


TOOL = {
    "name": "local_rag",
    "description": (
        "Local Second Brain / RAG engine that indexes folders, code repositories, Markdown, TXT, PDF, and DOCX "
        "into a local SQLite FTS5 database with exact file paths and line numbers. "
        "Use when the user says: 'indexa esta carpeta', 'busca en mi segundo cerebro', 'pregunta sobre mis archivos', "
        "'en qué archivo está...', 'estado del índice local'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "One of: 'index', 'query', 'stats', 'clear'.",
            },
            "path": {
                "type": "STRING",
                "description": "Folder or file path to index (used with action='index'). Defaults to '.'.",
            },
            "query": {
                "type": "STRING",
                "description": "Question or search terms (used with action='query').",
            },
        },
        "required": ["action"],
    },
    "handler": local_rag,
}
