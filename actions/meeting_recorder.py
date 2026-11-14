"""
actions/meeting_recorder.py — Grabador y Resumidor de Reuniones (Meet / Zoom / Teams / Discord).
==================================================================================================
Graba audio en segundo plano a WAV en outputs/meetings/ y, al detener, transcribe, identifica
hablantes y genera minutas en Markdown con acuerdos y tareas pendientes usando Gemini.
"""

from __future__ import annotations

import logging
import os
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("Viernes.Actions.MeetingRecorder")

_MEETINGS_DIR = Path("outputs/meetings")
_LOCK = threading.Lock()
_STATE: Dict[str, Any] = {
    "recording": False,
    "thread": None,
    "stop_event": None,
    "wav_path": None,
    "title": "reunion",
    "started_at": 0.0,
    "sample_rate": 16000,
    "frames": [],
}


def _record_worker(stop_event: threading.Event, sample_rate: int) -> None:
    import sounddevice as sd
    import numpy as np

    chunks: List[Any] = []

    def _cb(indata, frames, time_info, status):
        if not stop_event.is_set():
            chunks.append(indata.copy())

    try:
        with sd.InputStream(samplerate=sample_rate, channels=1, dtype="float32", callback=_cb):
            while not stop_event.is_set():
                time.sleep(0.1)
    except Exception as e:
        logger.error(f"Error grabando audio de reunión: {e}")
    finally:
        with _LOCK:
            _STATE["frames"] = chunks


def _save_wav(chunks: List[Any], wav_path: Path, sample_rate: int) -> float:
    import numpy as np
    import soundfile as sf

    if not chunks:
        return 0.0
    audio = np.concatenate(chunks, axis=0)
    wav_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(wav_path), audio, sample_rate)
    return float(len(audio)) / float(sample_rate)


def _summarize_meeting_with_gemini(wav_path: Path, title: str, duration_sec: float) -> str:
    from google import genai
    from google.genai import types
    from memory.config_manager import get_gemini_key

    api_key = get_gemini_key()
    if not api_key:
        return (
            f"Audio guardado en `{wav_path}` ({duration_sec:.1f}s). "
            "No hay API Key de Gemini configurada para transcribir y resumir automáticamente."
        )

    client = genai.Client(api_key=api_key)
    audio_bytes = wav_path.read_bytes()
    prompt = (
        f"Eres un secretario ejecutivo profesional. Analiza esta grabación de la reunión titulada '{title}' "
        f"(duración aproximada: {duration_sec:.0f} segundos).\n"
        "Genera una minuta completa en español con formato Markdown que incluya:\n"
        "1. **Resumen Ejecutivo** (3-5 líneas).\n"
        "2. **Puntos Clave y Decisiones**.\n"
        "3. **Tareas Pendientes (Action Items)** en formato `- [ ] Responsable/Tema: tarea`.\n"
        "4. **Transcripción Resumida / Diálogo por Hablantes** (identificando Hablante 1, Hablante 2, etc.).\n"
    )

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
            prompt,
        ],
    )
    return (resp.text or "").strip() or "No se pudo generar contenido de la grabación."


def meeting_recorder(parameters: Dict[str, Any], player=None, speak=None) -> str:
    action = str((parameters or {}).get("action", "start")).strip().lower()
    title = str((parameters or {}).get("title", "reunion")).strip() or "reunion"
    safe_title = "".join(c if c.isalnum() or c in "-_" else "_" for c in title).strip("_") or "reunion"

    if action in ("start", "iniciar", "grabar"):
        with _LOCK:
            if _STATE["recording"]:
                elapsed = time.time() - _STATE["started_at"]
                return f"Ya hay una reunión grabándose ('{_STATE['title']}', {elapsed:.0f}s). Di 'detén la grabación de la reunión' cuando termines."

            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            wav_path = _MEETINGS_DIR / f"{safe_title}_{ts}.wav"
            stop_ev = threading.Event()
            _STATE.update({
                "recording": True,
                "stop_event": stop_ev,
                "wav_path": wav_path,
                "title": title,
                "started_at": time.time(),
                "frames": [],
            })
            th = threading.Thread(
                target=_record_worker,
                args=(stop_ev, _STATE["sample_rate"]),
                daemon=True,
                name="ViernesMeetingRecorder",
            )
            _STATE["thread"] = th
            th.start()

        if player and hasattr(player, "write_log"):
            player.write_log(f"🎙️ Grabación de reunión iniciada: {title}")
        return f"Grabación de reunión '{title}' iniciada. Cuando termines, pídeme detener y resumir la reunión."

    if action in ("stop", "detener", "resumir", "finalizar"):
        with _LOCK:
            if not _STATE["recording"]:
                return "No hay ninguna grabación de reunión activa en este momento."
            stop_ev = _STATE["stop_event"]
            th = _STATE["thread"]
            wav_path = _STATE["wav_path"]
            rec_title = _STATE["title"]
            sample_rate = _STATE["sample_rate"]
            _STATE["recording"] = False

        if stop_ev:
            stop_ev.set()
        if th and th.is_alive():
            th.join(timeout=3.0)

        with _LOCK:
            chunks = list(_STATE["frames"])
            _STATE["frames"] = []

        duration = _save_wav(chunks, wav_path, sample_rate)
        if duration <= 0.2:
            return "La grabación no capturó audio suficiente. Verifica tu micrófono."

        if player and hasattr(player, "write_log"):
            player.write_log(f"📝 Transcribiendo y resumiendo reunión ({duration:.1f}s)...")

        try:
            summary_md = _summarize_meeting_with_gemini(wav_path, rec_title, duration)
        except Exception as e:
            logger.error(f"Error resumiendo reunión: {e}")
            return f"Audio guardado en {wav_path} ({duration:.1f}s), pero falló el resumen IA: {e}"

        md_path = wav_path.with_suffix(".md")
        md_content = (
            f"# Minuta de Reunión: {rec_title}\n"
            f"- **Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"- **Duración:** {duration:.1f} s\n"
            f"- **Audio:** `{wav_path.name}`\n\n---\n\n{summary_md}\n"
        )
        md_path.write_text(md_content, encoding="utf-8")
        return f"Reunión resumida y guardada en {md_path}.\n\n{summary_md[:1200]}"

    if action in ("status", "estado"):
        with _LOCK:
            if not _STATE["recording"]:
                return "No hay ninguna grabación de reunión en curso."
            elapsed = time.time() - _STATE["started_at"]
            return f"Grabando reunión '{_STATE['title']}' desde hace {elapsed:.0f} segundos."

    if action in ("list", "listar"):
        if not _MEETINGS_DIR.exists():
            return "Aún no hay minutas de reuniones guardadas."
        mds = sorted(_MEETINGS_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)[:10]
        if not mds:
            return "Aún no hay minutas de reuniones en outputs/meetings/."
        lines = [f"- {m.name} ({datetime.fromtimestamp(m.stat().st_mtime).strftime('%Y-%m-%d %H:%M')})" for m in mds]
        return "Últimas minutas guardadas:\n" + "\n".join(lines)

    return "Acción no reconocida para meeting_recorder. Usa: start, stop, status o list."


TOOL = {
    "name": "meeting_recorder",
    "description": (
        "Records meetings (Meet, Zoom, Teams, Discord, or voice) to outputs/meetings/ and automatically "
        "transcribes, identifies speakers, and generates Markdown minutes with action items using Gemini. "
        "Use when the user says: 'graba la reunión', 'inicia minuta', 'detén y resume la reunión', "
        "'estado de la grabación', 'lista mis minutas de reunión'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "One of: 'start', 'stop', 'status', 'list'.",
            },
            "title": {
                "type": "STRING",
                "description": "Optional meeting title when starting a recording.",
            },
        },
        "required": ["action"],
    },
    "handler": meeting_recorder,
}
