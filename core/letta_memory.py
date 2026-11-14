from __future__ import annotations

import os
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

try:
    from letta_client import Letta as RemoteLettaClient  # type: ignore
except Exception:
    RemoteLettaClient = None  # type: ignore


_DB_PATH = Path("memory") / "letta_memory.db"
_DEFAULT_BLOCKS = {
    "persona": (
        "Soy Viernes, asistente técnico directo, preciso y eficiente.",
        2000,
    ),
    "human": (
        "Usuario principal en Windows. Prefiere respuestas en español, concisas y soluciones nativas.",
        2000,
    ),
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class LettaMemoryEngine:
    """Native MemGPT/Letta-style tiered memory (core blocks, archival FTS5, recall log)
    with optional remote Letta server sync when LETTA_BASE_URL / LETTA_API_KEY are set.
    """

    def __init__(self, db_path: Path | str = _DB_PATH) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._fts_enabled = True
        self._remote = self._init_remote()
        self._init_db()

    def _init_remote(self) -> Any | None:
        if RemoteLettaClient is None:
            return None
        base_url = os.environ.get("LETTA_BASE_URL", "").strip()
        api_key = os.environ.get("LETTA_API_KEY", "").strip()
        if not base_url and not api_key:
            return None
        try:
            kwargs: dict[str, Any] = {}
            if base_url:
                kwargs["base_url"] = base_url
            if api_key:
                kwargs["api_key"] = api_key
            return RemoteLettaClient(**kwargs)
        except Exception:
            return None

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS core_memory (
                    block_name TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    char_limit INTEGER NOT NULL DEFAULT 2000,
                    updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS archival_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content TEXT NOT NULL,
                    tags TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS recall_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            try:
                conn.execute(
                    """
                    CREATE VIRTUAL TABLE IF NOT EXISTS archival_memory_fts
                    USING fts5(content, tags, content='archival_memory', content_rowid='id')
                    """
                )
            except sqlite3.OperationalError:
                self._fts_enabled = False

            now = _utc_now()
            for name, (default_text, limit) in _DEFAULT_BLOCKS.items():
                conn.execute(
                    """
                    INSERT OR IGNORE INTO core_memory (block_name, content, char_limit, updated_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, default_text, limit, now),
                )
            conn.commit()

    def core_read(self, block_name: str | None = None) -> dict[str, Any]:
        with self._lock, self._connect() as conn:
            if block_name:
                row = conn.execute(
                    "SELECT block_name, content, char_limit, updated_at FROM core_memory WHERE block_name = ?",
                    (block_name,),
                ).fetchone()
                if not row:
                    return {"ok": False, "error": f"Bloque '{block_name}' no existe."}
                return {"ok": True, "blocks": {row["block_name"]: dict(row)}}
            rows = conn.execute(
                "SELECT block_name, content, char_limit, updated_at FROM core_memory ORDER BY block_name"
            ).fetchall()
            return {"ok": True, "blocks": {r["block_name"]: dict(r) for r in rows}}

    def core_append(self, block_name: str, text: str) -> dict[str, Any]:
        text = (text or "").strip()
        if not block_name or not text:
            return {"ok": False, "error": "block y text son obligatorios."}
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT content, char_limit FROM core_memory WHERE block_name = ?",
                (block_name,),
            ).fetchone()
            now = _utc_now()
            if not row:
                limit = 2000
                new_content = text[:limit]
                conn.execute(
                    "INSERT INTO core_memory (block_name, content, char_limit, updated_at) VALUES (?, ?, ?, ?)",
                    (block_name, new_content, limit, now),
                )
            else:
                existing = row["content"]
                limit = int(row["char_limit"])
                sep = "\n" if existing and not existing.endswith("\n") else ""
                candidate = f"{existing}{sep}{text}"
                if len(candidate) > limit:
                    return {
                        "ok": False,
                        "error": f"Límite excedido en '{block_name}' ({len(candidate)}/{limit} chars).",
                    }
                new_content = candidate
                conn.execute(
                    "UPDATE core_memory SET content = ?, updated_at = ? WHERE block_name = ?",
                    (new_content, now, block_name),
                )
            conn.commit()
            return {"ok": True, "block": block_name, "length": len(new_content)}

    def core_replace(self, block_name: str, old_text: str, new_text: str) -> dict[str, Any]:
        if not block_name or not old_text:
            return {"ok": False, "error": "block y old_text son obligatorios."}
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT content, char_limit FROM core_memory WHERE block_name = ?",
                (block_name,),
            ).fetchone()
            if not row:
                return {"ok": False, "error": f"Bloque '{block_name}' no existe."}
            content = row["content"]
            if old_text not in content:
                return {"ok": False, "error": f"No se encontró old_text en '{block_name}'."}
            updated = content.replace(old_text, new_text or "", 1)
            limit = int(row["char_limit"])
            if len(updated) > limit:
                return {
                    "ok": False,
                    "error": f"Límite excedido en '{block_name}' ({len(updated)}/{limit} chars).",
                }
            conn.execute(
                "UPDATE core_memory SET content = ?, updated_at = ? WHERE block_name = ?",
                (updated, _utc_now(), block_name),
            )
            conn.commit()
            return {"ok": True, "block": block_name, "length": len(updated)}

    def archival_insert(self, content: str, tags: str = "") -> dict[str, Any]:
        content = (content or "").strip()
        if not content:
            return {"ok": False, "error": "content es obligatorio."}
        with self._lock, self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO archival_memory (content, tags, created_at) VALUES (?, ?, ?)",
                (content, tags.strip(), _utc_now()),
            )
            row_id = cur.lastrowid
            if self._fts_enabled:
                conn.execute(
                    "INSERT INTO archival_memory_fts (rowid, content, tags) VALUES (?, ?, ?)",
                    (row_id, content, tags.strip()),
                )
            conn.commit()
            return {"ok": True, "id": row_id}

    def archival_search(self, query: str, limit: int = 5) -> dict[str, Any]:
        query = (query or "").strip()
        limit = max(1, min(int(limit or 5), 20))
        if not query:
            return {"ok": False, "error": "query es obligatorio."}
        with self._lock, self._connect() as conn:
            rows = []
            if self._fts_enabled:
                try:
                    safe_q = " ".join(w for w in query.replace('"', " ").split() if w)
                    rows = conn.execute(
                        """
                        SELECT a.id, a.content, a.tags, a.created_at
                        FROM archival_memory_fts f
                        JOIN archival_memory a ON a.id = f.rowid
                        WHERE archival_memory_fts MATCH ?
                        ORDER BY rank
                        LIMIT ?
                        """,
                        (safe_q, limit),
                    ).fetchall()
                except sqlite3.OperationalError:
                    rows = []
            if not rows:
                like = f"%{query}%"
                rows = conn.execute(
                    """
                    SELECT id, content, tags, created_at
                    FROM archival_memory
                    WHERE content LIKE ? OR tags LIKE ?
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (like, like, limit),
                ).fetchall()
            return {"ok": True, "results": [dict(r) for r in rows]}

    def recall_log(self, role: str, content: str) -> None:
        content = (content or "").strip()
        if not content:
            return
        with self._lock, self._connect() as conn:
            conn.execute(
                "INSERT INTO recall_memory (role, content, created_at) VALUES (?, ?, ?)",
                ((role or "user")[:32], content[:4000], _utc_now()),
            )
            conn.commit()

    def status(self) -> dict[str, Any]:
        with self._lock, self._connect() as conn:
            core_count = conn.execute("SELECT COUNT(*) FROM core_memory").fetchone()[0]
            arch_count = conn.execute("SELECT COUNT(*) FROM archival_memory").fetchone()[0]
            recall_count = conn.execute("SELECT COUNT(*) FROM recall_memory").fetchone()[0]
        return {
            "ok": True,
            "db_path": str(self.db_path),
            "fts5": self._fts_enabled,
            "remote_connected": self._remote is not None,
            "core_blocks": core_count,
            "archival_entries": arch_count,
            "recall_entries": recall_count,
        }

    def get_core_prompt_block(self) -> str:
        data = self.core_read()
        blocks = data.get("blocks", {})
        parts = [f"[{k}] {v['content']}" for k, v in blocks.items()]
        return "\n".join(parts)


_ENGINE: LettaMemoryEngine | None = None
_ENGINE_LOCK = threading.Lock()


def get_letta_engine() -> LettaMemoryEngine:
    global _ENGINE
    if _ENGINE is None:
        with _ENGINE_LOCK:
            if _ENGINE is None:
                _ENGINE = LettaMemoryEngine()
    return _ENGINE
