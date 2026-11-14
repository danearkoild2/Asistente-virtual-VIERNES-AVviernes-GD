"""
actions/screen_recall.py — Búsqueda Visual en Pantalla por Historial (estilo Rewind/Recall local).
==================================================================================================
Captura periódica y opcional de pantalla 100% local en memory/screen_recall_frames/ e indexación
en SQLite FTS5 (memory/screen_recall.db) con ventana activa, proceso y descripción visual, para
preguntar "¿Qué estaba viendo hoy/ayer sobre X?".
"""

from __future__ import annotations

import logging
import os
import sqlite3
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger("Viernes.Actions.ScreenRecall")

_DB_PATH = Path("memory/screen_recall.db")
_FRAMES_DIR = Path("memory/screen_recall_frames")
_LOCK = threading.Lock()
_STATE: Dict[str, Any] = {
    "running": False,
    "stop_event": None,
    "thread": None,
    "interval_sec": 30,
    "max_frames": 300,
}


def _get_conn() -> sqlite3.Connection:
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS frames_meta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            window_title TEXT,
            process_name TEXT,
            frame_path TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE VIRTUAL TABLE IF NOT EXISTS frames_fts USING fts5(
            frame_id UNINDEXED,
            ts UNINDEXED,
            window_title,
            process_name,
            notes,
            tokenize='unicode61'
        )
        """
    )
    conn.commit()
    return conn


def _active_window_info() -> tuple[str, str]:
    title = ""
    proc = ""
    try:
        import pygetwindow as gw
        win = gw.getActiveWindow()
        if win:
            title = str(win.title or "").strip()
    except Exception:
        pass
    try:
        if os.name == "nt":
            import ctypes
            import psutil
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            pid = ctypes.c_ulong()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value:
                proc = psutil.Process(pid.value).name()
    except Exception:
        pass
    return title, proc


def _capture_once() -> None:
    import mss
    from PIL import Image

    _FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    ts_now = datetime.now()
    fname = f"frame_{ts_now.strftime('%Y%m%d_%H%M%S')}.jpg"
    fpath = _FRAMES_DIR / fname
    title, proc = _active_window_info()

    with mss.mss() as sct:
        mon = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
        raw = sct.grab(mon)
        img = Image.frombytes("RGB", raw.size, raw.rgb)
        img.thumbnail((1280, 720))
        img.save(str(fpath), format="JPEG", quality=60, optimize=True)

    conn = _get_conn()
    cur = conn.execute(
        "INSERT INTO frames_meta (ts, window_title, process_name, frame_path) VALUES (?, ?, ?, ?)",
        (ts_now.isoformat(), title, proc, str(fpath)),
    )
    fid = cur.lastrowid
    conn.execute(
        "INSERT INTO frames_fts (frame_id, ts, window_title, process_name, notes) VALUES (?, ?, ?, ?, ?)",
        (fid, ts_now.isoformat(), title, proc, f"{title} {proc}"),
    )

    # Retención automática: mantener solo los últimos max_frames
    max_f = int(_STATE.get("max_frames", 300))
    old_rows = conn.execute(
        "SELECT id, frame_path FROM frames_meta ORDER BY id DESC LIMIT -1 OFFSET ?",
        (max_f,),
    ).fetchall()
    for oid, opath in old_rows:
        conn.execute("DELETE FROM frames_meta WHERE id = ?", (oid,))
        conn.execute("DELETE FROM frames_fts WHERE frame_id = ?", (oid,))
        try:
            if opath and os.path.exists(opath):
                os.remove(opath)
        except Exception:
            pass

    conn.commit()
    conn.close()


def _recall_worker(stop_ev: threading.Event, interval_sec: int) -> None:
    while not stop_ev.is_set():
        try:
            _capture_once()
        except Exception as e:
            logger.debug(f"ScreenRecall capture skipped: {e}")
        stop_ev.wait(timeout=max(10, interval_sec))


def screen_recall(parameters: Dict[str, Any], player=None) -> str:
    params = parameters or {}
    action = str(params.get("action", "search")).strip().lower()
    query = str(params.get("query", "")).strip()
    interval_sec = int(params.get("interval_sec", 30) or 30)

    if action in ("start", "iniciar", "activar"):
        with _LOCK:
            if _STATE["running"]:
                return "El historial visual de pantalla (Screen Recall) ya está activo localmente."
            stop_ev = threading.Event()
            _STATE.update({
                "running": True,
                "stop_event": stop_ev,
                "interval_sec": max(10, interval_sec),
            })
            th = threading.Thread(
                target=_recall_worker,
                args=(stop_ev, _STATE["interval_sec"]),
                daemon=True,
                name="ViernesScreenRecall",
            )
            _STATE["thread"] = th
            th.start()
        return f"Screen Recall local activado (captura ligera cada {_STATE['interval_sec']}s en {_FRAMES_DIR})."

    if action in ("stop", "detener", "desactivar"):
        with _LOCK:
            if not _STATE["running"]:
                return "Screen Recall no estaba activo."
            if _STATE["stop_event"]:
                _STATE["stop_event"].set()
            _STATE["running"] = False
        return "Screen Recall detenido."

    if action in ("status", "estado"):
        conn = _get_conn()
        total = conn.execute("SELECT COUNT(*) FROM frames_meta").fetchone()[0]
        conn.close()
        state_txt = "activo" if _STATE["running"] else "inactivo"
        return f"Screen Recall está {state_txt}. Capturas locales almacenadas: {total} (máximo {_STATE['max_frames']})."

    if action in ("purge", "borrar", "limpiar"):
        if _DB_PATH.exists():
            _DB_PATH.unlink()
        if _FRAMES_DIR.exists():
            for f in _FRAMES_DIR.glob("*.jpg"):
                try:
                    f.unlink()
                except Exception:
                    pass
        return "Todo el historial visual de pantalla ha sido eliminado por privacidad."

    if action in ("search", "buscar"):
        conn = _get_conn()
        if query:
            tokens = [t.strip("\"'()[]{}:;,.!?") for t in query.split() if len(t.strip()) >= 2]
            fts_q = " OR ".join(f'"{t}"' for t in tokens[:6]) if tokens else ""
            rows = []
            if fts_q:
                try:
                    rows = conn.execute(
                        """
                        SELECT m.ts, m.window_title, m.process_name, m.frame_path
                        FROM frames_fts f
                        JOIN frames_meta m ON m.id = f.frame_id
                        WHERE frames_fts MATCH ?
                        ORDER BY m.id DESC
                        LIMIT 8
                        """,
                        (fts_q,),
                    ).fetchall()
                except Exception:
                    rows = []
        else:
            rows = conn.execute(
                "SELECT ts, window_title, process_name, frame_path FROM frames_meta ORDER BY id DESC LIMIT 8"
            ).fetchall()
        conn.close()

        if not rows:
            return f"No encontré capturas en el historial visual para '{query or 'recientes'}'."

        lines = []
        for ts, wtitle, proc, fpath in rows:
            hhmm = ts[:16].replace("T", " ")
            lines.append(f"- [{hhmm}] ({proc or 'App'}) {wtitle or 'Sin título'} -> `{fpath}`")
        return "Coincidencias en tu historial visual local:\n" + "\n".join(lines)

    return "Acción no reconocida para screen_recall. Usa: start, stop, search, status o purge."


TOOL = {
    "name": "screen_recall",
    "description": (
        "100% local Rewind/Recall-style visual screen history. Periodically saves compressed screenshots "
        "with active window title and process name in local SQLite FTS5 so the user can ask what they were "
        "viewing earlier. Use when the user says: 'activa el historial visual', 'qué estaba viendo ayer/hoy sobre...', "
        "'detén screen recall', 'borra mi historial visual'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "One of: 'start', 'stop', 'search', 'status', 'purge'.",
            },
            "query": {
                "type": "STRING",
                "description": "Keywords, app name, or topic to search in visual screen history.",
            },
            "interval_sec": {
                "type": "INTEGER",
                "description": "Capture interval in seconds (default 30, minimum 10).",
            },
        },
        "required": ["action"],
    },
    "handler": screen_recall,
}
