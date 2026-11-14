import platform as _platform
import subprocess as _subprocess

# ── Nuclear: force CREATE_NO_WINDOW on EVERY subprocess call on Windows ───────
# This patches Popen itself, so no per-file flag is needed anywhere.
if _platform.system() == "Windows":
    _OrigPopen = _subprocess.Popen

    class _Popen(_OrigPopen):
        def __init__(self, args, **kw):
            kw["creationflags"] = kw.get("creationflags", 0) | _subprocess.CREATE_NO_WINDOW
            kw.pop("startupinfo", None)   # drop any stale/shared STARTUPINFO
            super().__init__(args, **                       kw)

    _subprocess.Popen = _Popen


# ── Console must survive non-UTF-8 code pages ────────────────────────────────
# Every status line in this file carries an emoji, and on a legacy Windows
# console the active code page is the system one — cp1254 in Turkey, cp1251 in
# Russia, cp932 in Japan. Printing an emoji there raises UnicodeEncodeError, and
# because most of these prints sit inside the receive loop it takes the session
# down on startup. Reconfiguring to UTF-8 with a replacement fallback costs
# nothing and makes the app launch the same way in every locale.
import sys as _sys

for _stream in ("stdout", "stderr"):
    try:
        _s = getattr(_sys, _stream, None)
        if _s is not None and hasattr(_s, "reconfigure"):
            _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass          # pythonw / redirected pipes / anything exotic — never fatal

# ─────────────────────────────────────────────────────────────────────────────
import os as _os
_os.environ.setdefault("QT_LOGGING_RULES", "qt.multimedia.*=false;qt.rhi.*=false;qt.webenginecontext.*=false")
_os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--use-angle=d3d11 --ignore-gpu-blocklist --enable-webgl")

try:
    import PyQt6.QtWebEngineWidgets  # noqa: F401
except ImportError:
    pass

import asyncio
import collections
import re
import threading
import time
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path

import sounddevice as sd
import numpy as np
from google import genai
from google.genai import types
from ui import ViernesUI, ViernesUI
from memory.memory_manager import (
    load_memory, update_memory, format_memory_for_prompt,
    save_session_summary, pop_last_session,
    search_memory, set_trim_notifier,
)

# The file-backed tools (open_app, web_search, browser_control, …) are no longer
# imported or declared here — they self-describe via a TOOL dict in their own
# actions/*.py file and are auto-discovered by core.action_loader at startup.
# Only tools that are tied to live-session state stay inline in this file
# (screen_process, close_camera, save_memory, manage_monitor, shutdown_viernes,
# system_status).
from actions.screen_processor  import _capture_camera, _capture_screen
from actions.system_monitor    import SystemMonitor, get_system_status
from actions.proactive         import ProactiveEngine
from actions.background_monitor import (
    add_monitor, remove_monitor, list_monitors, check_all as monitor_check_all,
)
from actions.web_search        import _news as _fetch_news_sync
from memory.config_manager     import (
    get_brief_enabled, get_media_resolution, get_proactive_audio_enabled,
    get_push_to_talk_enabled, get_thinking_enabled, get_turn_tuning, get_voice,
    get_wake_word_enabled, save_wake_word_enabled,    get_input_device, get_output_device,
    get_tts_engine, get_elevenlabs_config,
)
from core                     import gemini as _gemini
from core.plugin_loader        import discover_plugins
from core                      import undo as undo_stack
from core                      import confirm as confirm_gate
from core                      import audio_devices
from core.action_loader        import discover_actions
from core.echo                 import EchoGuard
from core.viseme               import VisemeStream
from core.wake_word            import (
    WakeWordDetector, is_ready as wake_is_ready, install_and_download as wake_install,
)

# How long the assistant stays awake with no user speech before it auto-sleeps
# again (wake-word mode only).
WAKE_SLEEP_TIMEOUT = 120.0   # seconds (2 minutes)

def get_base_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent

BASE_DIR        = get_base_dir()
API_CONFIG_PATH = BASE_DIR / "config" / "api_keys.json"
PROMPT_PATH     = BASE_DIR / "core" / "prompt.txt"
# The conversation's model. A NAME, not a decision: the ladder lives in
# core/gemini.py and this is only whichever rung is currently in use, kept here
# as a module attribute because plugins read it (chat_takeover asks main for it
# so that upgrading the assistant upgrades the plugin too).
#
# It is reassigned on every connect, so a model that runs out of quota is
# stepped over and the assistant keeps talking instead of failing to start.
LIVE_MODEL          = "models/gemini-3.1-flash-live-preview"
CHANNELS            = 1
SEND_SAMPLE_RATE    = 16000 
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE          = 1024

# RMS below which 16-bit PCM is treated as room silence; above _LEVEL_FULL it
# reads as a full-height waveform. Tuned so ordinary speech lands mid-range and
# the bars still move for a quiet talker — language- and device-independent.
_LEVEL_FLOOR = 60.0
_LEVEL_FULL  = 2600.0


def _pcm_level(samples) -> float:
    """Map a block of int16 PCM samples to a 0.0–1.0 loudness level for the HUD
    waveform. Returns 0.0 on empty/invalid input so it can never raise."""
    try:
        x = np.asarray(samples, dtype=np.float32)
        if x.size == 0:
            return 0.0
        rms = float(np.sqrt(np.mean(x * x)))
    except Exception:
        return 0.0
    if rms <= _LEVEL_FLOOR:
        return 0.0
    return min(1.0, (rms - _LEVEL_FLOOR) / (_LEVEL_FULL - _LEVEL_FLOOR))


# ── Viseme extraction ─────────────────────────────────────────────────────────
# The avatar's mouth used to be driven by one RMS value per ~200 ms write batch,
# which is five updates a second averaged over a fifth of a second — it could
# only ever flap. These read the *shape* of each 20 ms slice straight from the
# spectrum of the audio being played, so no transcript, no forced alignment and
# no language assumption: it works the same for Turkish and English.
#
# Two numbers come out. Openness tracks the first formant — F1 climbs as the jaw
# drops, so /a/ reads open and /i/ or /u/ read closed. Width tracks the second —
# F2 is high for spread vowels (/i/, /e/) and low for rounded ones (/u/, /o/).
# Extra time beyond the device's reported output latency before the microphone
# is trusted again: covers room decay and the speaker's own settling.
_TAIL_MARGIN = 0.25

_VIS_WIN = 1024        # ~43 ms analysis window at 24 kHz: enough for formants
_VIS_HOP = 480         # 20 ms between frames, i.e. 50 shapes a second

# Delay from handing the first bytes of a reply to an already-running output
# stream to hearing them: one callback period, plus whatever the DAC adds.
_FIRST_SOUND = CHUNK_SIZE / RECEIVE_SAMPLE_RATE      # ~43 ms
# How far past the device's own buffer the mouth's timeline may drift before it
# is re-anchored. The buffer is the hard limit on how much audio can be queued
# ahead, so anything beyond it plus a margin for clock error is impossible.
_CURSOR_SLACK = 0.15

# Erring early is the safe direction. A viewer tolerates a mouth that moves
# slightly before the sound far better than one that moves after it — the
# broadcast limits are about 45 ms of lag against 125 ms of lead — so where
# this is uncertain it is biased to lead.


def _pcm_visemes(samples, sr: int = 24000):
    """Slice a PCM block into (level, openness, width) frames, one per 20 ms.

    Returns [] on anything unexpected — the mouth falls back to loudness-only
    articulation rather than the caller having to handle an error.
    """
    try:
        x = np.asarray(samples, dtype=np.float32)
        if x.size < _VIS_WIN:
            return []
        win = np.hanning(_VIS_WIN).astype(np.float32)
        freqs = np.fft.rfftfreq(_VIS_WIN, 1.0 / sr)
        b_f1_lo = (freqs >= 150) & (freqs < 450)     # F1 of close vowels
        b_f1_hi = (freqs >= 450) & (freqs < 1100)    # F1 of open vowels
        b_f2_bk = (freqs >= 600) & (freqs < 1300)    # F2 of rounded vowels
        b_f2_fr = (freqs >= 1700) & (freqs < 3200)   # F2 of spread vowels
        b_hiss = (freqs >= 3800) & (freqs < 8000)    # fricatives

        # One frame per hop across the *whole* block. Stepping only while a full
        # window fits stopped 1024 - 480 samples short of the end, so a 200 ms
        # batch yielded 160 ms of schedule: the mouth ran out of frames before
        # the audio ran out of sound, and each batch no longer lined up with the
        # end of the one before it. Losing 20 % of every batch is most of why
        # the mouth did not track the words.
        out = []
        for start in range(0, x.size, _VIS_HOP):
            # The level gates closures, so it is measured over exactly this
            # 20 ms and never looks ahead. The spectrum needs a longer window
            # to resolve formants and may be short-filled at the very end.
            level = _pcm_level(x[start:start + _VIS_HOP])
            seg = x[start:start + _VIS_WIN]
            if seg.size < _VIS_WIN:
                seg = np.concatenate([seg, np.zeros(_VIS_WIN - seg.size,
                                                    dtype=np.float32)])
            if level <= 0.0:
                out.append((0.0, 0.0, 0.0))
                continue
            mag = np.abs(np.fft.rfft((seg - seg.mean()) * win))
            f1l, f1h = float(mag[b_f1_lo].sum()), float(mag[b_f1_hi].sum())
            f2b, f2f = float(mag[b_f2_bk].sum()), float(mag[b_f2_fr].sum())
            hiss = float(mag[b_hiss].sum())

            openness = f1h / (f1l + f1h + 1e-6)
            width = (f2f - f2b) / (f2f + f2b + 1e-6)
            # A wide-open jaw physically cannot purse, so openness damps width.
            # /a/ has a low enough F2 to read as "rounded" on the bands alone;
            # letting openness suppress the width term is what keeps an open
            # vowel from pursing.
            width *= (1.0 - openness) ** 0.8
            # Fricatives are formed with a nearly closed mouth.
            h = hiss / (f1l + f1h + f2b + f2f + hiss + 1e-6)
            openness *= 1.0 - 0.65 * min(1.0, h * 2.5)
            out.append((level,
                        float(min(1.0, max(0.0, openness))),
                        float(min(1.0, max(-1.0, width)))))
        return out
    except Exception:
        return []


def _describe_tools(declarations) -> str:
    """One line per capability, straight from the live tool declarations.

    Derived rather than written down: the action and plugin registries are
    discovered at startup, so whatever the user has installed is what the model
    is told it can do. Adding a plugin extends this by itself, and removing one
    stops the model from claiming an ability it no longer has.
    """
    lines = []
    for d in declarations or ():
        try:
            name = d.get("name") if isinstance(d, dict) else getattr(d, "name", None)
            desc = (d.get("description") if isinstance(d, dict)
                    else getattr(d, "description", "")) or ""
        except Exception:
            continue
        if not name:
            continue
        desc = " ".join(str(desc).split())
        lines.append(f"- {name}: {desc[:150]}" if desc else f"- {name}")
    return "\n".join(lines)


def _describe_limits(has_vision: bool, has_mic: bool) -> str:
    """The other half of self-knowledge: what is out of reach, and why.

    Derived from how the program is actually built, not from a list of refusals.
    A model that knows its boundaries stops improvising around them, and stating
    them as architecture rather than as rules keeps the answer honest in any
    language.
    """
    out = [
        "- Anything not listed above is outside your reach. Say so in one clause "
        "and offer the nearest thing you can actually do — never mime an action "
        "you cannot take, and never report a result you did not get.",
        "- You act on this machine only. You cannot reach the user's other "
        "devices, accounts or hardware except through the tools listed above.",
        "- You remember what is in the memory block and what has been said this "
        "session. Anything else you were told before is gone unless it was saved.",
    ]
    if has_vision:
        out.append(
            "- Tu visión visual en tiempo real está COMPLETAMENTE HABILITADA y ACTIVA. Puedes ver tanto la cámara "
            "de la habitación en tiempo real como la pantalla del usuario. Tienes la herramienta 'screen_process' "
            "para capturar y analizar fotogramas de la cámara o de la pantalla de forma instantánea. "
            "Si el usuario te pregunta qué ves, qué hay en la habitación, qué tiene en la mano, cómo luce o qué hay "
            "en su pantalla, debes invocar 'screen_process' de inmediato y responder con total agudeza, inteligencia y precisión.")
    else:
        out.append("- You have no sight at all in this build.")
    if has_mic:
        out.append(
            "- You hear nothing while the microphone is muted, and you cannot "
            "unmute it yourself.")
    return "\n".join(out)


def _render_prompt(template: str, values: dict) -> str:
    """Fill {tokens} in the prompt template.

    A plain replace rather than str.format: the file is meant to be edited by
    hand, and a stray brace in someone's own wording must never take the app
    down at startup.
    """
    out = template or ""
    for key, val in values.items():
        out = out.replace("{" + key + "}", str(val))
    return out


def _get_api_key() -> str:
    with open(API_CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["gemini_api_key"]


def _load_system_prompt() -> str:
    try:
        return PROMPT_PATH.read_text(encoding="utf-8")
    except Exception:
        return (
            "You are Viernes, an intelligent and friendly AI companion. "
            "Be concise, direct, and always use the provided tools to complete tasks. "
            "Never simulate or guess results — always call the appropriate tool."
        )

_CTRL_RE = re.compile(r"<ctrl\d+>", re.IGNORECASE)

# Transcript chunks shorter than this may legitimately repeat ("evet, evet"),
# so only longer ones are treated as duplicates.
_REPEAT_MIN = 12


def _is_repeat_chunk(txt: str, buf: list) -> bool:
    """True if this transcript chunk has already been seen this turn.

    Guards against the API re-sending the tail of a response across the several
    turn_completes a tool-using turn produces.
    """
    if len(txt) < _REPEAT_MIN:
        return bool(buf) and txt == buf[-1]
    joined = " ".join(buf)
    return txt in joined

# Non-Latin scripts frequently hallucinated by multilingual ASR on room noise / breath
_NON_LATIN_HALLUCINATION_RE = re.compile(
    r"[\u0400-\u052F\u0590-\u05FF\u0600-\u06FF\u0900-\u0D7F\u0E00-\u0E7F\u1100-\u11FF\u3040-\u30FF\u3130-\u318F\u4E00-\u9FFF\uAC00-\uD7AF]+"
)

def _clean_transcript(text: str) -> str:    
    text = _CTRL_RE.sub("", text)
    text = re.sub(r"[\x00-\x08\x0b-\x1f]", "", text)
    return text.strip()

def _clean_input_transcript(text: str) -> str:
    text = _clean_transcript(text)
    text = _NON_LATIN_HALLUCINATION_RE.sub("", text)
    return text.strip()


def _is_silence_command(text: str) -> bool:
    """True when the user says 'Silencio' or an explicit mute/hush command."""
    if not text:
        return False
    norm = (
        text.lower()
        .replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
    )
    clean = re.sub(r"[^\w\s]", " ", norm)
    clean = " ".join(clean.split())
    if not clean:
        return False

    words = clean.split()
    filler = {"viernes", "edith", "oye", "hey", "por", "favor", "ya", "ahora", "mismo", "un", "momento"}
    core_words = [w for w in words if w not in filler]
    if core_words in (["silencio"], ["callate"], ["calla"], ["shh"], ["mute"], ["silenciar"]):
        return True

    explicit_phrases = (
        "modo silencio",
        "haz silencio",
        "guarda silencio",
        "manten silencio",
        "en silencio",
        "apaga el microfono",
        "apagar el microfono",
        "apagar microfono",
        "silencia el microfono",
        "silenciar el microfono",
        "silenciar microfono",
        "desactiva el microfono",
        "desactivar microfono",
        "no escuches mas",
        "deja de escuchar",
        "callate y apaga el microfono",
        "silencio y apaga el microfono",
    )
    if any(p in clean for p in explicit_phrases):
        return True

    if len(words) <= 5 and (words[0] in ("silencio", "callate") or words[-1] in ("silencio", "callate")):
        return True

    return False


TOOL_DECLARATIONS = [
    # ── Inline tools ─────────────────────────────────────────────────────────
    # These stay here (rather than in an actions/*.py TOOL dict) because their
    # handling is woven into live-session state — vision capture/injection,
    # camera stream, memory writes, the monitor engine, and shutdown. All other
    # tools live in their own action file and are auto-discovered by
    # core.action_loader (see ViernesLive.__init__).
    {
        "name": "system_status",
        "description": (
            "Returns real-time system metrics: CPU usage, RAM, GPU load, CPU temperature, "
            "uptime, and process count. Use when the user asks about computer performance, "
            "temperature, memory, or resource usage."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {},
        }
    },
    {
        "name": "screen_process",
        "description": (
            "Captures the screen or webcam image and lets you analyze it. "
            "MUST be called when user asks what is on screen, what you see, "
            "look at camera, analyze my screen, etc. "
            "You have NO visual ability without this tool. "
            "After the image is captured it is sent directly to you — describe what you see and answer the user's question. "
            "When using camera: the live view stays open until user says close it or calls close_camera."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "angle": {"type": "STRING", "description": "'screen' to capture display, 'camera' for webcam. Default: 'screen'"},
                "text":  {"type": "STRING", "description": "The question or instruction about the captured image"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "close_camera",
        "description": (
            "Closes the live camera view shown on screen. "
            "Call when the user says (in ANY language): close camera, stop camera, "
            "turn off camera, that's creepy, etc."
        ),
        "parameters": {"type": "OBJECT", "properties": {}, "required": []}
    },
    {
        "name": "toggle_room_sentinel",
        "description": (
            "Activa o desactiva el modo centinela de observación continua de la habitación en tiempo real. "
            "Úsalo cuando el usuario te pida vigilar la habitación, observar en vivo, mantener los ojos en la habitación, "
            "o cuando quiera que uses la cámara continuamente."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "active": {"type": "BOOLEAN", "description": "True para activar centinela en vivo, False para desactivar"}
            },
            "required": []
        }
    },
    {
        "name": "manage_monitor",
        "description": (
            "Add, remove, or list background monitoring topics. "
            "VIERNES checks these topics once a day and alerts the user when there is a new development. "
            "Use 'add' when the user says 'monitor X', 'track X', 'follow X'. "
            "Use 'remove' when the user says 'stop monitoring X'. "
            "Use 'list' when the user asks what is being monitored. "
            "Do NOT add crypto, financial, or trading topics."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action": {
                    "type":        "STRING",
                    "description": "add | remove | list",
                },
                "topic": {
                    "type":        "STRING",
                    "description": "Topic to monitor or stop monitoring (e.g. 'space exploration', 'AI news')",
                },
            },
            "required": ["action"],
        },
    },
    {
        "name": "sleep_viernes",
        "description": (
            "Puts the assistant to sleep into resting / stand-by mode on her beanbag (dormida) without closing the app. "
            "Call this whenever the user says (in Spanish, English, or any language): "
            "'duérmete', 'duerme', 'descansa', 've a dormir', 'a dormir', 'buenas noches', "
            "'ponte en modo reposo', 'modo reposo', 'standby', 'sleep', 'rest', 'go to sleep'. "
            "IMPORTANT: This does NOT close the application; it keeps the app open and listening for "
            "the wake word or touch to awaken. "
            "NEVER call shutdown_viernes for sleeping or resting commands — ALWAYS call sleep_viernes!"
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "message": {
                    "type": "STRING",
                    "description": "Optional brief friendly sleepy phrase to say before going to sleep."
                }
            },
        }
    },
    {
        "name": "silence_viernes",
        "description": (
            "Immediately silences the assistant (stops speaking right away) and turns OFF / mutes the microphone "
            "so it stops listening and does not interrupt anymore. "
            "Call this whenever the user says 'silencio', 'cállate', 'callate', 'modo silencio', 'haz silencio', "
            "'guarda silencio', 'apaga el micrófono', 'silencia el micrófono', 'no escuches más', or 'deja de escuchar'. "
            "CRITICAL: Do NOT say anything when calling this tool — stay 100% silent immediately."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {},
        }
    },
    {
        "name": "shutdown_viernes",
        "description": (
            "Completely terminates and closes the desktop application process window. "
            "CRITICAL: Call this ONLY when the user EXPLICITLY and UNAMBIGUOUSLY orders you to close the application program itself, "
            "such as 'cierra el programa', 'cierra la app', 'cierra la ventana', 'termina el proceso', 'apaga el programa', "
            "'sal de la aplicación', 'exit application', or 'close window'. "
            "NEVER call this when the user says 'duérmete', 'descansa', 'a dormir', 'buenas noches', 'hasta mañana', "
            "or 'adiós' — for any sleeping or resting requests, you MUST call 'sleep_viernes' instead! "
            "The app must NEVER close unless explicitly instructed to close the program."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {},
        }
    },
    {
        "name": "save_memory",
        "description": (
            "Save an important personal fact about the user to long-term memory. "
            "Call this silently whenever the user reveals something worth remembering: "
            "name, age, city, job, preferences, hobbies, relationships, projects, or future plans. "
            "Do NOT call for: weather, reminders, searches, or one-time commands. "
            "Do NOT announce that you are saving — just call it silently. "
            "Values must be in English regardless of the conversation language."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "category": {
                    "type": "STRING",
                    "description": (
                        "identity — name, age, birthday, city, job, language, nationality | "
                        "preferences — favorite food/color/music/film/game/sport, hobbies | "
                        "projects — active projects, goals, things being built | "
                        "relationships — friends, family, partner, colleagues | "
                        "wishes — future plans, things to buy, travel dreams | "
                        "notes — habits, schedule, anything else worth remembering"
                    )
                },
                "key":   {"type": "STRING", "description": "Short snake_case key (e.g. name, favorite_food, sister_name)"},
                "value": {"type": "STRING", "description": "Concise value in English (e.g. Danear, pizza, older sister)"},
            },
            "required": ["category", "key", "value"]
        }
    },
    {
        "name": "recall_memory",
        "description": (
            "Look up a fact you have stored about the user but which is NOT in "
            "the memory block of your system prompt. "
            "The prompt lists the keys it did not have room for under "
            "'[ALSO REMEMBERED]' — if the user asks about anything named there, "
            "call this FIRST. "
            "Also call it before saying you do not know something personal, and "
            "when the user asks what you remember about them (leave query empty "
            "for everything). "
            "This is a local file search: it is instant and costs nothing."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "query": {
                    "type": "STRING",
                    "description": (
                        "Keyword to search for — a name, a topic, a category "
                        "(e.g. 'ayse', 'coffee', 'projects'). "
                        "Leave empty to list everything stored."
                    ),
                },
            },
            "required": [],
        },
    },
    {
        "name": "undo",
        "description": (
            "Reverse the last change YOU made to this computer — a file you "
            "moved, renamed, created or wrote, or a setting you changed such as "
            "volume, brightness, dark mode or WiFi. "
            "Call this whenever the user says undo, revert, take it back, put it "
            "back, cancel that, or tells you that you did the wrong thing, in ANY "
            "language. "
            "Use action='list' when they ask what can be undone. "
            "This only covers your own actions — it is not the Ctrl+Z of whatever "
            "application is on screen (that is computer_settings with action 'undo')."
        ),
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "action": {
                    "type": "STRING",
                    "description": "undo (default) — reverse the last change | list — show what can be undone",
                },
            },
            "required": [],
        },
    },
]

class _ReconnectSignal(Exception):
    """Raised inside the session TaskGroup to force a clean, voluntary reconnect
    (e.g. the user picked a new voice — the voice is fixed at connect time, so
    the session must be rebuilt).

    Carries `keep_context`: True for an ordinary rebuild, where the stored
    resumption handle is replayed and the conversation continues; False when the
    new session must genuinely start clean (see the voice-change note in
    _on_voice_change)."""

    def __init__(self, keep_context: bool = True):
        super().__init__()
        self.keep_context = keep_context


def _is_reconnect_signal(exc: BaseException) -> bool:
    """True if `exc` is a _ReconnectSignal, or a(n) (Base)ExceptionGroup that
    wraps one — TaskGroup bundles child exceptions into a group."""
    if isinstance(exc, _ReconnectSignal):
        return True
    if isinstance(exc, BaseExceptionGroup):
        return any(_is_reconnect_signal(sub) for sub in exc.exceptions)
    return False


def _keep_context_of(exc: BaseException) -> bool:
    """Read `keep_context` off a reconnect signal, unwrapping the group the
    TaskGroup put it in. Defaults to True: an unexpected shape must not silently
    wipe the conversation."""
    if isinstance(exc, _ReconnectSignal):
        return getattr(exc, "keep_context", True)
    if isinstance(exc, BaseExceptionGroup):
        for sub in exc.exceptions:
            if _is_reconnect_signal(sub):
                return _keep_context_of(sub)
    return True


class ViernesLive:
    def __init__(self, ui: ViernesUI):
        self.ui             = ui
        # Enlazar canal de habla unificado de VIERNES hacia la UI y paneles interactivos
        try:
            self.ui._assistant_speak = self.speak
        except Exception:
            pass
        try:
            _cfg = json.loads(open(API_CONFIG_PATH, encoding="utf-8").read())
            self._asst_name = (_cfg.get("assistant_name") or "Viernes").strip()
        except Exception:
            self._asst_name = "Viernes"
        self.session              = None
        self.audio_in_queue       = None
        self.out_queue            = None
        self._loop                     = None
        self._is_speaking         = False
        self._speaking_lock       = threading.Lock()
        self._phone_active        = False   # True while phone mic is streaming; pauses PC mic
        self._audio_route         = "pc"    # 'pc' (default), 'phone' (mobile only), 'both' (PC + mobile)
        self._sleep_pending       = False   # True while parting speech plays before sleep()
        self._first_connect_done  = False   # True after initial session connect
        self._pending_vision       = None    # (img_bytes, mime_type, question, angle) to inject after tool response
        self._vision_cam_active    = False   # True if camera was opened for vision → auto-close after response
        self._vision_close_pending = False   # True after vision injected; next turn_complete closes camera
        self._vision_last_time     = 0.0     # monotonic time of last screen_process call (cooldown guard)
        self._vision_busy          = False   # True while a vision capture/inject cycle is in flight
        self._interrupted          = False   # True while draining audio after user interrupt
        # Transcript-driven mouth shapes for the avatar. Fed from the receive
        # loop as words arrive, drained by the playback loop against the audio.
        self._visemes              = VisemeStream()
        from core.speech_animation import SpeechAnimationController
        self._speech_anim          = SpeechAnimationController(
            dispatch_fn=lambda intent, meta: self.ui.set_semantic_intent(intent, meta) if hasattr(self.ui, "set_semantic_intent") else None
        )
        self._last_out_logged      = ""      # de-dupes a re-sent transcript tail
        self._last_user_query      = ""      # tracks user queries for visual context
        self._current_uploaded_file: str | None = None  # latest uploaded file (PC or Mobile)
        # Push-to-talk
        self._ptt_enabled          = False
        self._ptt_held             = False
        self._ptt                  = None    # core.hotkey.PushToTalk
        self._out_level            = 0.0     # level of the audio being played right now
        self._echo                 = EchoGuard()
        # `stream.write()` returns when the buffer accepts the audio, not when the
        # speaker has finished with it, so sound is still in the room after the
        # speaking flag drops. Streaming the microphone during that gap is how an
        # assistant ends up answering itself. Measured from the device rather than
        # guessed; see _play_audio.
        self._out_latency          = 0.20    # seconds, replaced with the real value
        self._tail_until           = 0.0     # monotonic time the echo tail expires
        # Wall-clock time at which the audio written next will begin to sound.
        # The mouth is scheduled against this, never against "now": batches are
        # handed to the device far faster than they play, so "now" ran the lips
        # ahead of the words and cut every schedule short. 0 = nothing playing.
        self._play_cursor          = 0.0
        self.ui.on_push_to_talk   = self.set_push_to_talk
        self.ui.ptt_hold          = self._on_ptt
        self.ui.on_text_command   = self._on_text_command
        self.ui.on_remote_clicked = self._make_remote_key
        self.ui.on_interrupt      = self.interrupt
        self.ui.on_voice_change   = self._on_voice_change     # voice picker → rebuild session
        self.ui.on_audio_device_change = self._on_audio_device_change
        self.ui.speak             = self.speak
        if hasattr(self.ui, "_win") and self.ui._win:
            self.ui._win._assistant_speak = self.speak
        try:
            from core.personality_manager import get_personality_manager
            get_personality_manager().add_listener(self._on_personality_changed)
        except Exception:
            pass
        self._reconnect_event: asyncio.Event | None = None
        self._reconnect_keep = True   # False → next rebuild drops the resumption handle

        # ── Session resumption ─────────────────────────────────────────
        # The server issues a resumption handle every few seconds and reissues
        # it as the conversation moves on. Before this, session_resumption was
        # switched ON in the config and the update was never read, so the handle
        # was thrown away and EVERY reconnect — a dropped packet, a voice change,
        # switching microphone — started an empty session. "Unlimited sessions"
        # leaked through exactly this hole.
        #
        # Deliberately in RAM only, never written to disk. Persisting it would
        # make a fresh launch continue yesterday's conversation, which sounds
        # appealing but breaks the session-summary flow: _save_session_summary
        # runs at shutdown and the morning briefing pops it the next day. A
        # conversation that never ends never produces a summary, and the
        # "yesterday we talked about…" line silently disappears.
        self._resume_handle: str | None = None
        self._turn_done_event: asyncio.Event | None = None
        self._dashboard     = None
        self._briefing_sent    = False          # morning briefing fires once per process
        self._sys_monitor      = SystemMonitor()  # persistent cooldown state
        self._proactive        = ProactiveEngine()
        self._last_user_speech = time.monotonic()  # updated on every user utterance
        self._session_log: list[str] = []          # conversation turns for end-of-session summary

        self._enhanced_live = True  # proactive audio; auto-disabled if the server rejects it
        self._tuned_live    = True  # turn-taking / media / thinking knobs; same fallback

        _base_dir = Path(__file__).resolve().parent
        _inline_names = {t["name"] for t in TOOL_DECLARATIONS}

        # File-backed tools: every actions/*.py with a TOOL dict, discovered the
        # same way plugins are. Reserved names = the inline tools above, so an
        # action can never shadow one.
        self._action_registry = discover_actions(
            actions_dir=_base_dir / "actions",
            reserved_names=_inline_names,
            logger=lambda msg: print(f"[Actions] {msg}"),
        )

        # Plugins must not collide with either an inline tool or a discovered action.
        _core_names = _inline_names | self._action_registry.names()
        self._plugin_registry = discover_plugins(
            plugins_dir=_base_dir / "plugins",
            core_tool_names=_core_names,
            # Console gets the full boot transcript; the activity log gets only
            # what the user has to know about. Every plugin loading correctly is
            # the expected case and does not belong in their conversation.
            logger=lambda msg: print(f"[Plugins] {msg}"),
            notify=lambda msg: self.ui.write_log(f"SYS: {msg}"),
        )
        self.ui.get_plugins = self._plugin_registry.list_for_ui
        self.ui.get_plugin_settings = self._plugin_registry.settings_schemas  # ⚙ settings tab
        self.ui.run_plugin = self._plugin_registry.run
        self.ui.request_say = self.plugin_say   # plugins: mid-task speech channel

        # ── Wake word ────────────────────────────────────────────────────────
        # _awake gates the mic (see _listen_audio) and the background speakers.
        # It is True whenever wake word is OFF, so default behaviour is unchanged.
        self._wake_enabled     = get_wake_word_enabled()
        self._awake            = not self._wake_enabled
        self._wake_detector: WakeWordDetector | None = None
        self._wake_sleep_timeout = WAKE_SLEEP_TIMEOUT

        # Environmental Attention Window (evita interrupciones por conversaciones de terceros)
        self._attention_duration = 20.0
        self._attention_until = time.monotonic() + 25.0
        self._pre_roll_mic: collections.deque = collections.deque(maxlen=16)  # ~1.0s PCM a 16kHz
        self._current_user = "Jesús"

        from core.environmental_awareness import get_environmental_awareness
        from core.learning_engine import get_learning_engine
        self._env_awareness = get_environmental_awareness()
        self._learning = get_learning_engine()

        # Restore the saved push-to-talk preference. Doing it here rather than
        # in __init__ means the hotkey thread only exists once there is a
        # session to talk to.
        if get_push_to_talk_enabled():
            try:
                self.set_push_to_talk(True)
            except Exception as e:
                print(f"[VIERNES] ⚠ Push-to-talk unavailable: {e}")
        # UI control surface for the Wake Word settings section.
        self.ui.wake_is_ready    = wake_is_ready          # () -> bool
        self.ui.wake_get_state   = self._wake_state       # () -> dict
        self.ui.on_wake_toggle   = self._ui_wake_toggle   # (enable: bool) -> str
        self.ui.on_wake_manual   = self._ui_wake_manual   # () -> toggle awake/asleep
        self.ui.on_wake_install  = self._ui_wake_install  # () -> (ok, msg)

    # ── Wake word: state machine ─────────────────────────────────────────────

    def _wake_state(self) -> dict:
        # A loaded, running detector is definitively ready; otherwise fall back
        # to the cheap on-disk model-file check (no Model construction).
        ready = bool(self._wake_detector and self._wake_detector.ready) or wake_is_ready()
        return {"enabled": self._wake_enabled, "awake": self._awake, "ready": ready}

    def _ensure_wake_detector(self) -> bool:
        """Load the detector once (model loads on first start). Idempotent."""
        if self._wake_detector is None:
            self._wake_detector = WakeWordDetector(
                on_detect=self._on_wake_detected,
                logger=lambda m: print(f"[Wake] {m}"),
                notify=lambda m: self.ui.write_log(f"SYS: {m}"),
                wake_phrase=self._asst_name,
            )
        if not self._wake_detector.ready:
            return self._wake_detector.start()
        return True

    def renew_attention(self, duration: float = 20.0) -> None:
        """Extiende la ventana de atención activa para conversación bidireccional fluida."""
        self._attention_until = time.monotonic() + duration
        self._last_user_speech = time.monotonic()

    def is_attentive(self) -> bool:
        """Indica si VIERNES está activamente atenta a la conversación."""
        if not self._awake:
            return False
        if getattr(self, "_ptt_enabled", False) and getattr(self, "_ptt_held", False):
            return True
        return time.monotonic() < self._attention_until

    def _on_wake_detected(self) -> None:
        """Called from the detector thread when wake word is heard."""
        self.wake(reason="palabra de activación de voz")
        self.renew_attention(25.0)
        if hasattr(self, "_pre_roll_mic") and self._pre_roll_mic:
            try:
                buffered = list(self._pre_roll_mic)
                self._pre_roll_mic.clear()
                if self._loop and self.out_queue:
                    for chunk in buffered:
                        self._loop.call_soon_threadsafe(
                            self.out_queue.put_nowait,
                            {"data": chunk, "mime_type": "audio/pcm"}
                        )
            except Exception:
                pass

    def wake(self, reason: str = "wake word") -> None:
        self._sleep_pending = False
        was_awake = self._awake
        self._awake = True
        self.renew_attention(25.0)
        self._last_user_speech = time.monotonic()   # start the auto-sleep clock now
        if not self.ui.muted:
            self.ui.set_state("LISTENING")
        try:
            if hasattr(self.ui, "_win") and hasattr(self.ui._win, "_wake_btns_sig"):
                self.ui._win._wake_btns_sig.emit()
        except Exception:
            pass
        if self._dashboard:
            self._dashboard._awake_state = True
            if self._loop:
                try:
                    asyncio.run_coroutine_threadsafe(
                        self._dashboard.broadcast({"type": "status", "state": "active", "awake": True}),
                        self._loop,
                    )
                except Exception:
                    pass
        if not was_awake:
            self.ui.write_log(f"SYS: Awake — {reason}.")

    def sleep(self, reason: str = "timeout") -> None:
        self._sleep_pending = False
        if not self._awake:
            return
        self._awake = False
        self.set_speaking(False)
        self.ui.set_state("SLEEPING")
        self._ensure_wake_detector()
        try:
            if hasattr(self.ui, "_win") and hasattr(self.ui._win, "_wake_btns_sig"):
                self.ui._win._wake_btns_sig.emit()
        except Exception:
            pass
        if self._dashboard:
            self._dashboard._awake_state = False
            if self._loop:
                try:
                    asyncio.run_coroutine_threadsafe(
                        self._dashboard.broadcast({"type": "status", "state": "sleeping", "awake": False}),
                        self._loop,
                    )
                except Exception:
                    pass
        self.ui.write_log(f"SYS: Sleeping — {reason}. Di '{self._asst_name}' o usa el botón WAKE NOW.")


    async def _run_sleep_watch(self) -> None:
        """Auto-sleep after the configured silence window (wake-word mode only)."""
        while True:
            await asyncio.sleep(5)
            if not self._wake_enabled or not self._awake:
                continue
            with self._speaking_lock:
                speaking = self._is_speaking
            if speaking:
                continue
            if (time.monotonic() - self._last_user_speech) > self._wake_sleep_timeout:
                self.sleep(reason="no speech for 2 minutes")

    # ── Wake word: UI callbacks (called from the Qt thread) ──────────────────

    def _ui_wake_toggle(self, enable: bool) -> str:
        """Enable/disable wake word from the settings UI. Returns a status token:
        'enabled' | 'disabled' | 'need_download'."""
        if enable:
            if not wake_is_ready():
                return "need_download"
            self._wake_enabled = True
            save_wake_word_enabled(True)
            self._ensure_wake_detector()
            self.sleep(reason="wake word enabled")
            return "enabled"
        else:
            self._wake_enabled = False
            save_wake_word_enabled(False)
            self.wake(reason="wake word disabled")
            return "disabled"

    def _ui_wake_manual(self) -> None:
        """Manual sleep/wake button in the UI."""
        if self._awake:
            self.sleep(reason="you tapped sleep")
        else:
            self.wake(reason="you tapped wake")

    def _ui_wake_install(self) -> tuple[bool, str]:
        """Download openwakeword + the model (runs in a UI worker thread)."""
        # Triggered by the user pressing the button, so its progress is exactly
        # what they are waiting to see.
        return wake_install(logger=lambda m: print(f"[Wake] {m}"),
                            notify=lambda m: self.ui.write_log(f"SYS: {m}"))

    def plugin_say(self, instruction: str) -> None:
        """
        Thread-safe speech channel for plugins: lets a plugin ask VIERNES to
        say something short WHILE its run() is still executing (plugins block
        their executor thread, so they can't speak through the tool response
        until they finish). The instruction is injected into the Live session
        exactly like a proactive check-in; Gemini phrases it naturally in the
        user's language. Silently a no-op when no session is connected.
        """
        loop = getattr(self, "_loop", None)
        if not loop or not self.session:
            return

        async def _say():
            try:
                await self.session.send_client_content(
                    turns={"role": "user", "parts": [{"text": instruction}]},
                    turn_complete=True,
                )
            except Exception as e:
                print(f"[PluginSay] {e}")

        try:
            asyncio.run_coroutine_threadsafe(_say(), loop)
        except Exception as e:
            print(f"[PluginSay] {e}")

    def request_reconnect(self, keep_context: bool = True, reason: str = ""):
        """Thread-safe: ask the run loop to tear down and rebuild the Live
        session. Called from the Qt thread. No-op until the async loop and
        reconnect event exist.

        `keep_context=False` drops the resumption handle so the new session
        starts empty — only for changes the server cannot apply to a resumed
        session."""
        loop = getattr(self, "_loop", None)
        ev   = self._reconnect_event
        self._reconnect_keep   = keep_context
        self._reconnect_reason = reason
        if loop and ev is not None:
            loop.call_soon_threadsafe(ev.set)

    def _on_voice_change(self):
        """Voice picker applied.

        The voice is baked into the session at connect time, so a rebuild is
        required. It is rebuilt WITHOUT the resumption handle on purpose:
        resuming restores the server's own session state, and the safe reading
        is that it restores the voice with it — which would make the picker
        appear to do nothing. Losing context here is acceptable because changing
        voice is a deliberate, rare act; losing it on a dropped packet was not."""
        self.request_reconnect(keep_context=False, reason="new voice")

    def _on_audio_device_change(self):
        """Microphone or speaker changed. Both streams are opened inside the
        session TaskGroup, so they can only be re-opened by rebuilding it —
        but the conversation is kept, which is the whole reason resumption
        landed before this feature did."""
        self.request_reconnect(keep_context=True, reason="audio device")

    def _on_personality_changed(self, profile):
        """Perfil de personalidad, nacionalidad o dialecto actualizado en vivo."""
        print(f"[Personality] Perfil activo actualizado: {profile.name} ({profile.dialect_id})")
        # Guardar los últimos turnos para mantener continuidad al reconstruir la sesión con el nuevo system_instruction
        if getattr(self, "_session_log", None):
            self._personality_carryover = "\n".join(self._session_log[-6:])
        if getattr(self, "session", None) is not None:
            # keep_context=False limpia _resume_handle para que Gemini Live aplique el NUEVO system_instruction
            self._resume_handle = None
            self.request_reconnect(keep_context=False, reason=f"personalidad '{profile.name}'")

    async def _watch_reconnect(self):
        """Session-scoped task: when a voluntary reconnect is requested, raise a
        signal that unwinds the TaskGroup so the run loop rebuilds the session."""
        assert self._reconnect_event is not None
        await self._reconnect_event.wait()
        self._reconnect_event.clear()
        keep   = self._reconnect_keep
        reason = getattr(self, "_reconnect_reason", "") or "settings"
        self.ui.write_log(
            f"SYS: Applying {reason} — reconnecting"
            + ("..." if keep else " (starting a fresh conversation)...")
        )
        raise _ReconnectSignal(keep_context=keep)

    def _make_remote_key(self):
        """Called from Qt main thread when user presses Remote Control."""
        if self._dashboard is None:
            self.ui.write_log(
                "SYS: Dashboard unavailable. "
                "Run: pip install fastapi \"uvicorn[standard]\" cryptography"
            )
            return None
        key    = self._dashboard.new_key()
        url    = self._dashboard.get_url()
        manual = self._dashboard.get_manual_url()
        return url, key, f"{url}/auto-login?key={key}", manual

    def _on_text_command(self, text: str):
        if not self._loop:
            return

        raw = (text or "").strip()
        if not raw:
            return

        # Special fast-path for uploaded files (Desktop UI or Remote Control):
        # Always wake VIERNES if asleep, extract instant preview / inline image, and send to session.
        if raw.startswith("[FILE_UPLOADED]"):
            if not self._awake:
                self.wake(reason="archivo cargado")
            self._last_user_speech = time.monotonic()
            file_path = ""
            try:
                import re as _re
                m = _re.search(r"path=([^|]+)", raw)
                if m:
                    file_path = m.group(1).strip()
            except Exception:
                pass
            if file_path:
                self._current_uploaded_file = file_path
            asyncio.run_coroutine_threadsafe(
                self._handle_uploaded_file(file_path, raw),
                self._loop,
            )
            return

        if not self.session:
            # Respaldo de IA local sin conexión cuando no hay sesión de red
            try:
                from core.local_ai_service import get_local_ai_service
                local_ai = get_local_ai_service()
                self.ui.set_state("THINKING")
                def _run_local():
                    resp = local_ai.generate_response(raw)
                    self.ui.set_state("SPEAKING")
                    self.ui.write_log(f"{self._asst_name} (Local/Offline): {resp}")
                    local_ai.speak_offline(resp)
                    self.ui.set_state("LISTENING")
                import threading as _th
                _th.Thread(target=_run_local, daemon=True).start()
            except Exception as _e:
                print(f"[LocalAI] Fallback error: {_e}")
            return

        self._last_user_query = raw
        if _is_silence_command(raw):
            self.silence_and_mute(reason="comando 'Silencio'")
            return

        low = raw.lower()
        sleep_phrases = ["duermete", "duérmete", "descansa", "a dormir", "ve a dormir", "modo reposo", "buenas noches", "sleep", "standby"]
        if any(low == p or low.startswith(p + " ") for p in sleep_phrases):
            self.ui.write_log("SYS: Entering sleep mode (user command)...")
            if not self._wake_enabled:
                try:
                    from core.wake_word import is_ready
                    from memory.config_manager import save_wake_word_enabled
                    if is_ready():
                        self._wake_enabled = True
                        save_wake_word_enabled(True)
                        self._ensure_wake_detector()
                        self.ui._refresh_wake_btns()
                except Exception:
                    pass
            self.sleep(reason="user commanded sleep")
            return

        # Respect wake-word sleep: allow waking up by text or hint to wake
        if not self._awake:
            wake_phrases = ["despierta", "wake", "despertar", "hola", "hey", "arriba", "viernes", self._asst_name.lower()]
            if any(w in low for w in wake_phrases):
                self.wake(reason="user typed wake")
                return
            self.ui.write_log(f"SYS: I'm asleep — di '{self._asst_name}', escribe 'despierta' o usa WAKE NOW.")
            return

        self.renew_attention(25.0)

        # ── Ultra-fast Local Fast-Path (<5ms) for time, repeat, and weather ──
        clean_low = low.rstrip("?.!,:;¿¡ ")

        time_triggers = [
            "que hora es", "la hora", "hora actual", "dime la hora",
            "que hora tienes", "hora", "what time is it", "current time", "time"
        ]
        if clean_low in time_triggers:
            from actions.current_time import time_action
            ans = time_action()
            self.ui.write_log(f"You: {raw}")
            self.ui.write_log(f"{self._asst_name}: {ans}")
            self._last_out_logged = ans
            self.speak(f"Di al usuario de forma natural: {ans}")
            return

        repeat_triggers = [
            "repite lo que dijiste", "repite eso", "que dijiste",
            "puedes repetir", "repite por favor", "repite", "repeat that", "what did you say"
        ]
        if any(clean_low == r or clean_low.startswith(r + " ") for r in repeat_triggers):
            last = getattr(self, "_last_out_logged", "").strip()
            ans = f"Dije: {last}" if last else "No he dicho nada todavía que pueda repetir."
            self.ui.write_log(f"You: {raw}")
            self.ui.write_log(f"{self._asst_name}: {ans}")
            self.speak(f"Di exactamente: {ans}")
            return

        weather_triggers = [
            "el clima", "como esta el clima", "temperatura", "clima",
            "que clima hace", "como esta el tiempo", "el tiempo", "weather"
        ]
        if clean_low in weather_triggers:
            from actions.weather_report import weather_action
            ans = weather_action()
            self.ui.write_log(f"You: {raw}")
            self.ui.write_log(f"{self._asst_name}: {ans}")
            self._last_out_logged = ans
            self.speak(f"Di al usuario de forma natural: {ans}")
            return

        personality_triggers = [
            "modo profesional", "modo ejecutiva", "modo tica", "modo paisa",
            "modo kawaii", "modo seria", "modo bromista", "modo sarcastica",
            "modo sarcástica", "modo rioplatense", "modo argentina", "modo mexicana",
            "modo cubana", "modo chilena", "modo peninsular", "modo española",
            "personalidad habitual", "vuelve a tu personalidad habitual", "modo normal"
        ]
        if any(pt in clean_low for pt in personality_triggers):
            from actions.change_personality import change_personality_action
            ans = change_personality_action({"mode": clean_low, "temporary": True})
            self.ui.write_log(f"You: {raw}")
            self.ui.write_log(f"{self._asst_name}: {ans}")
            self._last_out_logged = ans
            self.speak(f"Di con tu tono correspondiente: {ans}")
            return

        asyncio.run_coroutine_threadsafe(
            self.session.send_client_content(
                turns={"role": "user", "parts": [{"text": raw}]},
                turn_complete=True
            ),
            self._loop
        )

    async def _handle_uploaded_file(self, file_path: str, raw_msg: str) -> None:
        """Wait for active session, extract multimodal preview (image or document text), and inject into Gemini Live."""
        for _ in range(60):
            if self.session:
                break
            await asyncio.sleep(0.1)
        if not self.session:
            # Respaldo de IA local sin conexión cuando no hay sesión de red
            try:
                from core.local_ai_service import get_local_ai_service
                local_ai = get_local_ai_service()
                self.ui.set_state("THINKING")
                def _run_local():
                    resp = local_ai.generate_response(raw)
                    self.ui.set_state("SPEAKING")
                    self.ui.write_log(f"{self._asst_name} (Local/Offline): {resp}")
                    local_ai.speak_offline(resp)
                    self.ui.set_state("LISTENING")
                import threading as _th
                _th.Thread(target=_run_local, daemon=True).start()
            except Exception as _e:
                print(f"[LocalAI] Fallback error: {_e}")
            return

        parts = []
        prompt_text = raw_msg
        if file_path and Path(file_path).is_file():
            try:
                from actions.file_processor import extract_file_preview
                info = await asyncio.to_thread(extract_file_preview, Path(file_path))
                if info.get("image_part"):
                    parts.append(info["image_part"])
                preview_txt = (info.get("preview_text") or "").strip()
                if preview_txt:
                    prompt_text = (
                        f"{raw_msg}\n\n"
                        f"[CONTENIDO EXTRAÍDO DEL ARCHIVO ({info.get('type', 'file').upper()})]:\n"
                        f"{preview_txt}\n\n"
                        f"[INSTRUCCIÓN]: Ya tienes arriba el contenido o vista previa del archivo '{Path(file_path).name}' "
                        f"(ruta: {file_path}). Confirma brevemente en español al usuario que ya recibiste y puedes ver "
                        f"el archivo '{Path(file_path).name}', menciona de qué trata en una frase corta y pregúntale qué desea hacer con él. "
                        f"Si luego te pide acciones adicionales sobre el archivo (convertir, resumir completo, redimensionar, corregir, etc.), "
                        f"usa la herramienta `file_processor` con `file_path='{file_path}'`."
                    )
            except Exception as e:
                print(f"[FileUpload] Preview extraction error: {e}")

        parts.append({"text": prompt_text})
        try:
            await self.session.send_client_content(
                turns={"role": "user", "parts": parts},
                turn_complete=True,
            )
        except Exception as e:
            print(f"[FileUpload] Error sending uploaded file turn: {e}")

    def _check_visual_context(self, user_query: str, assistant_response: str) -> None:
        """Non-blocking background visual evaluation and SerpAPI image display for Edith."""
        q = (user_query or "").strip()
        resp = (assistant_response or "").strip()
        if not q and not resp:
            return

        def _worker(query_text: str, resp_text: str):
            try:
                from core.visual_engine import VisualEngine
                ve = VisualEngine.get_instance()
                card = ve.evaluate_and_fetch(query_text, resp_text)
                if card and card.images:
                    self.ui.show_visual_card(card)
            except Exception as exc:
                print(f"[VisualContext] error: {exc}")

        threading.Thread(
            target=_worker,
            args=(q, resp),
            daemon=True,
            name="EdithVisualWorker"
        ).start()

    def _tail_active(self) -> bool:
        """True while the speakers may still be finishing our last sentence."""
        return time.monotonic() < self._tail_until

    def set_speaking(self, value: bool):
        with self._speaking_lock:
            self._is_speaking = value
        if value:
            self._tail_until = 0.0
        else:
            # Hold the guard open across the device's own output latency plus a
            # margin for the room. The microphone is NOT muted during it — the
            # guard still lets a genuine reply through, so answering instantly
            # still works. Only our own echo is dropped.
            self._tail_until = time.monotonic() + self._out_latency + _TAIL_MARGIN
            self.renew_attention(20.0)
        if not value:
            # The echo history is deliberately NOT cleared here: the tail above
            # still needs it to recognise our own voice. It is dropped when the
            # tail expires. What the guard learned about the room always stays.
            self._out_level = 0.0
        if value:
            self.ui.set_state("SPEAKING")
        elif not self.ui.muted:
            self.ui.set_state("LISTENING")

    def set_push_to_talk(self, enabled: bool) -> str:
        """Turn hold-to-talk on or off. Returns the scope actually achieved."""
        from core.hotkey import PushToTalk

        self._ptt_enabled = bool(enabled)
        self._ptt_held = False
        if not enabled:
            if self._ptt is not None:
                self._ptt.stop()
                self._ptt = None
            return "off"

        if self._ptt is None:
            self._ptt = PushToTalk(self._on_ptt)
        scope = self._ptt.start()
        # A window-scoped chord is a real limitation, not a detail — say it once
        # in the log so nobody wonders why it does nothing while another app is
        # focused. Reporting it must never be able to undo the thing it reports.
        try:
            self.ui.write_log(
                f"SYS: Push-to-talk on — hold {self._ptt.label}"
                + ("." if scope == "global"
                   else " (works while this window is focused)."))
        except Exception:
            pass
        return scope

    def _on_ptt(self, held: bool) -> None:
        """Chord pressed or released — may arrive on the hotkey thread."""
        self._ptt_held = held
        if held:
            # Holding the key is also a way to wake it, so push-to-talk works
            # without having to say the wake word first.
            if self._wake_enabled and not self._awake:
                self._awake = True
                self._last_user_speech = time.monotonic()
        try:
            self.ui.set_state("LISTENING" if held else "SLEEPING")
        except Exception:
            pass

    def interrupt(self, log_msg: bool = True) -> None:
        """Stop VIERNES mid-speech: drain queued audio and open mic immediately."""
        self._interrupted = True
        q = self.audio_in_queue
        if q:
            drained = 0
            while True:
                try:
                    q.get_nowait()
                    drained += 1
                except Exception:
                    break
            if drained:
                print(f"[VIERNES] ✋ Interrupted — {drained} audio chunks discarded")
        self.set_speaking(False)
        # The words we were about to mouth are never going to be spoken now.
        self._visemes.reset()
        if hasattr(self, "_speech_anim"):
            self._speech_anim.on_speech_end()
        if hasattr(self.ui, "interrupt_gestures"):
            self.ui.interrupt_gestures()
        self._play_cursor = 0.0     # next batch starts a fresh timeline
        if self._turn_done_event:
            self._turn_done_event.clear()
        if self._dashboard and self._loop:
            try:
                asyncio.run_coroutine_threadsafe(
                    self._dashboard.broadcast({"type": "audio_clear"}),
                    self._loop,
                )
            except Exception:
                pass
        if log_msg:
            self.ui.write_log("SYS: Interrupted — listening...")

    def silence_and_mute(self, reason: str = "comando 'Silencio'") -> None:
        """Immediately stop all speech and turn OFF the microphone so VIERNES neither listens nor interrupts."""
        print(f"[VIERNES] 🔇 Silencio activado ({reason}) — cortando voz y apagando micrófono.")
        self.interrupt(log_msg=False)
        # Drain any pending outgoing microphone audio chunks so nothing else is sent
        out_q = getattr(self, "out_queue", None)
        if out_q is not None:
            while True:
                try:
                    out_q.get_nowait()
                except Exception:
                    break
        if hasattr(self.ui, "set_muted"):
            self.ui.set_muted(True, f"Silenciado por {reason}.")
        else:
            self.ui.muted = True
        self.ui.set_state("MUTED")

    def speak(self, text: str) -> bool:
        if not self._loop or not self.session:
            return False
        self._interrupted = False
        asyncio.run_coroutine_threadsafe(
            self.session.send_client_content(
                turns={"role": "user", "parts": [{"text": text}]},
                turn_complete=True
            ),
            self._loop
        )
        return True

    def speak_error(self, tool_name: str, error: str):
        short = str(error)[:120]
        self.ui.write_log(f"ERR: {tool_name} — {short}")
        self.speak(f"Sir, {tool_name} encountered an error. {short}")

    def _build_config(self) -> types.LiveConnectConfig:
        from datetime import datetime

        # Load customization from config
        try:
            _cfg = json.loads(open(API_CONFIG_PATH, encoding="utf-8").read())
            self._asst_name = (_cfg.get("assistant_name") or "Viernes").strip()
            _user_name = (_cfg.get("user_name") or "").strip()
        except Exception:
            self._asst_name = "Viernes"
            _user_name = ""

        memory     = load_memory()
        mem_str    = format_memory_for_prompt(memory)
        sys_prompt = _load_system_prompt()

        now      = datetime.now()
        time_str = now.strftime("%A, %B %d, %Y — %I:%M %p")
        time_ctx = (
            f"[CURRENT DATE & TIME]\n"
            f"Right now it is: {time_str}\n"
            f"Use this to calculate exact times for reminders.\n\n"
        )

        # Identity injection — overrides any hardcoded name in prompt.txt
        # Address form is a property of the language being spoken, so it is
        # stated as a principle rather than a two-language lookup — the model
        # already knows the respectful register of whatever language it is in.
        _addr = (f"ADDRESS: Always call the user '{_user_name}'."
                 if _user_name
                 else 'ADDRESS: Address the user with the ordinary respectful form '
                      'for a superior in the language you are currently speaking — '
                      '"sir" in English, its everyday equivalent in any other '
                      'language. Never an archaic or aristocratic form, and never '
                      'the form from a different language than the one you are '
                      'speaking in this sentence.')
        from memory.config_manager import get_voice_style, GEMINI_VOICE_STYLES
        _vstyle_key = get_voice_style()
        _vstyle_prompt = GEMINI_VOICE_STYLES.get(_vstyle_key, ("", ""))[1]
        _vstyle_line = f"{_vstyle_prompt}\n" if _vstyle_prompt else ""

        identity_ctx = (
            f"[IDENTITY & IDIOMA PREDETERMINADO]\n"
            f"Your name is {self._asst_name}. "
            f"Always refer to yourself as {self._asst_name}.\n"
            f"MANDATORY DEFAULT LANGUAGE: Tu idioma oficial, nativo y predeterminado es ESPAÑOL LATINOAMERICANO / LATINO. "
            f"Debes hablar y responder SIEMPRE en español latino de forma predeterminada en todas las interacciones. "
            f"Nunca respondas en inglés a menos que el usuario te hable explícitamente en inglés o solicite traducción.\n"
            f"{_vstyle_line}"
            f"Creator: DanearKoild, Dueño y CEO de Groovi Dev.\n"
            f"When asked who created you, who made you, or about your creator, always reply: 'Me creó DanearKoild, Dueño y CEO de Groovi Dev, y me creó para ser tu asistente!'\n"
            f"Special Capabilities: Advanced real-time data analysis, trend prediction and forecasting, and deep context comprehension of DanearKoild's active development projects at Groovi Dev.\n"
            f"{_addr}\n\n"
        )

        # Everything the model is told about *itself* is derived here, not
        # written into prompt.txt: the name comes from config, the platform from
        # the host, the capability list from the registries that were just
        # discovered. Rename the assistant, add a plugin or move to another OS
        # and this follows without anyone editing a prompt.
        _all_decls = (TOOL_DECLARATIONS
                      + self._action_registry.get_tool_declarations()
                      + self._plugin_registry.get_tool_declarations())
        _names = {(d.get("name") if isinstance(d, dict) else getattr(d, "name", ""))
                  for d in _all_decls}
        sys_prompt = _render_prompt(sys_prompt, {
            "assistant_name": self._asst_name,
            "platform": f"{_platform.system()} {_platform.release()}".strip(),
            "capabilities": _describe_tools(_all_decls),
            "limits": _describe_limits(
                has_vision="screen_process" in _names,
                has_mic=True,
            ),
        })

        parts = [time_ctx, identity_ctx]
        if mem_str:
            parts.append(mem_str)
        try:
            from core.opencv_vision import get_vision_coordinator
            sensory_ctx = get_vision_coordinator().get_sensory_context_prompt()
            if sensory_ctx:
                parts.append(sensory_ctx)
        except Exception:
            pass
        try:
            from memory.book_knowledge import format_books_for_prompt
            books_ctx = format_books_for_prompt()
            if books_ctx:
                parts.append(books_ctx)
        except Exception:
            pass
        try:
            env_ctx = self._env_awareness.get_prompt_block()
            if env_ctx:
                parts.append(env_ctx)
            habits_ctx = self._learning.get_learned_habits_prompt()
            if habits_ctx:
                parts.append(habits_ctx)
            from core.context_memory import task_context
            wm_ctx = task_context.get_working_memory_summary()
            if wm_ctx:
                parts.append(f"[WORKING MEMORY]\n{wm_ctx}\n")
        except Exception:
            pass
        parts.append(sys_prompt)

        # La personalidad, nacionalidad y forma de hablar van AL FINAL para máxima prioridad sobre el tono base
        _profile_voice = ""
        try:
            from core.personality_manager import get_personality_manager
            _pmgr = get_personality_manager()
            _active_prof = _pmgr.get_active_profile()
            _profile_voice = (getattr(_active_prof, "voice_name", "") or "").strip()
            personality_ctx = _pmgr.compile_personality_system_prompt(
                assistant_name=self._asst_name,
                user_name=_user_name
            )
            if personality_ctx:
                parts.append(personality_ctx)
        except Exception as _e_pers:
            print(f"[Personality] Error agregando prompt de personalidad: {_e_pers}")

        carryover = getattr(self, "_personality_carryover", "")
        if carryover:
            parts.append(
                "[CONTINUIDAD DE CONVERSACIÓN — acabas de actualizar tu personalidad/estilo, continúa esta charla con naturalidad]\n"
                + carryover
            )
            self._personality_carryover = ""

        _selected_voice = _profile_voice or get_voice()

        cfg = dict(
            response_modalities=["AUDIO"],
            output_audio_transcription={},
            input_audio_transcription={},
            system_instruction="\n".join(parts),
            tools=[{"function_declarations": _all_decls}],
            # Asks the server to issue session-resumption handles. Enabled but
            # NOT yet used: no handle is captured from the resumption update and
            # none is passed back here, so a reconnect starts a fresh session
            # rather than continuing the old one. Left on because the handles
            # cost nothing and are the prerequisite for doing it properly.
            # Hand back the handle captured from the last session_resumption
            # update. `handle=None` is exactly the old behaviour (ask for
            # handles, start fresh), so the first connect of a run is unchanged.
            session_resumption=types.SessionResumptionConfig(
                handle=self._resume_handle
            ),
            # Sliding-window compression: session never dies from a full context
            # window — VIERNES can stay in one conversation for hours
            context_window_compression=types.ContextWindowCompressionConfig(
                sliding_window=types.SlidingWindow(),
            ),
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=_selected_voice
                    )
                )
            ),
        )
        if self._enhanced_live:
            # Proactive audio: VIERNES stays silent when speech isn't addressed
            # to it (background chatter, talking to someone else in the room).
            # (Affective dialog was dropped: gemini-3.1-flash-live does not
            #  support it, and it never reliably detected tone in practice.
            #  To restore it on a 2.5 native-audio model, add back:
            #  cfg["enable_affective_dialog"] = True )
            if get_proactive_audio_enabled():
                cfg["proactivity"] = types.ProactivityConfig(proactive_audio=True)

        if self._tuned_live:
            cfg.update(self._tuning_config())

        return types.LiveConnectConfig(**cfg)

    def _tuning_config(self) -> dict:
        """The optional knobs, kept apart so one bad field can be dropped wholesale.

        Every one of these is a preview-API field. If a future model release
        stops accepting any of them the connection fails at setup, so the run
        loop turns `_tuned_live` off and reconnects on the plain config rather
        than leaving the user with an assistant that will not start.
        """
        out: dict = {}

        # How long the server waits through a pause before deciding your turn is
        # over. This — not the size of the prompt — is what most of the delay
        # before a reply actually is, and the default has to suit everybody, so
        # it is necessarily cautious.
        turn = get_turn_tuning()
        if turn.get("enabled", True):
            detect = types.AutomaticActivityDetection(
                silence_duration_ms=turn["silence_ms"],
                prefix_padding_ms=turn["prefix_ms"],
            )
            if turn["end_sensitivity"] == "high":
                detect.end_of_speech_sensitivity = types.EndSensitivity.END_SENSITIVITY_HIGH
            elif turn["end_sensitivity"] == "low":
                detect.end_of_speech_sensitivity = types.EndSensitivity.END_SENSITIVITY_LOW
            if turn["start_sensitivity"] == "high":
                detect.start_of_speech_sensitivity = types.StartSensitivity.START_SENSITIVITY_HIGH
            elif turn["start_sensitivity"] == "low":
                detect.start_of_speech_sensitivity = types.StartSensitivity.START_SENSITIVITY_LOW
            out["realtime_input_config"] = types.RealtimeInputConfig(
                automatic_activity_detection=detect)

        # Screenshots and camera frames are tokenised at this resolution and then
        # stay in the session's context. 'medium' keeps on-screen text legible
        # for a fraction of a full-resolution frame.
        res = get_media_resolution()
        if res != "default":
            out["media_resolution"] = {
                "low":    types.MediaResolution.MEDIA_RESOLUTION_LOW,
                "medium": types.MediaResolution.MEDIA_RESOLUTION_MEDIUM,
                "high":   types.MediaResolution.MEDIA_RESOLUTION_HIGH,
            }[res]

        # Thinking is left at the server default deliberately. Forcing the budget
        # to zero was measured on gemini-3.1-flash-live over interleaved trials
        # and did not make the first word arrive sooner — this model does not
        # appear to deliberate on the Live path, so pinning the field only adds a
        # way for a future release to behave differently. Set "thinking_enabled"
        # in config/api_keys.json to true to let it reason instead.
        if get_thinking_enabled():
            out["thinking_config"] = types.ThinkingConfig(thinking_budget=-1)

        return out

    async def _execute_tool(self, fc) -> types.FunctionResponse:
        """Wraps tool execution with the holographic Tony-Stark screens animation."""
        name = fc.name
        _holo = name not in ("save_memory", "recall_memory", "get_current_time", "repeat_last_said", "undo")
        if _holo:
            try:
                a = dict(fc.args or {})
                detail = (a.get("query") or a.get("topic") or a.get("channel")
                          or a.get("source") or a.get("action") or "")
                self.ui.holo_start(name, str(detail)[:60])
            except Exception:
                _holo = False
        try:
            return await self._execute_tool_inner(fc)
        finally:
            if _holo:
                try:
                    self.ui.holo_stop()
                except Exception:
                    pass

    async def _execute_tool_inner(self, fc) -> types.FunctionResponse:
        name = fc.name
        args = dict(fc.args or {})

        print(f"[VIERNES] 🔧 {name}  {args}")
        self.ui.set_state("THINKING")
        if hasattr(self, "_speech_anim"):
            self._speech_anim.on_tool_start(name)
        if name in ("web_search", "web_research", "browser_control"):
            q = args.get("query") or args.get("topic") or ", ".join(args.get("items", []))
            self.ui.write_log(f"SYS: 🌐 Buscando en internet: {q}..." if q else "SYS: 🌐 Buscando en internet...")


        if name == "save_memory":
            category = args.get("category", "notes")
            key      = args.get("key", "")
            value    = args.get("value", "")
            if key and value:
                update_memory({category: {key: {"value": value}}})
                print(f"[Memory] 💾 save_memory: {category}/{key} = {value}")
            if not self.ui.muted:
                self.ui.set_state("LISTENING")
            return types.FunctionResponse(
                id=fc.id, name=name,
                response={"result": "ok", "silent": True}
            )

        loop   = asyncio.get_event_loop()
        result = "Done."

        try:
            if name == "recall_memory":
                # Local file search: no network, no second model. Kept out of
                # the executor deliberately — it is a dictionary scan over a few
                # hundred short strings, and a thread hop would cost more than
                # the work itself.
                result = search_memory(args.get("query", ""), limit=8)

            elif name == "undo":
                if str(args.get("action", "")).lower().strip() == "list":
                    items = undo_stack.history()
                    result = ("Things I can undo, most recent first:\n"
                              + "\n".join(f"{i+1}. {t}" for i, t in enumerate(items))
                              ) if items else "I have not changed anything I can undo yet."
                else:
                    result = await loop.run_in_executor(None, undo_stack.undo_last)

            elif name == "screen_process":
                import time as _t_mod
                _now = _t_mod.monotonic()
                _cooldown = 4.0  # seconds — covers echo window after speaking ends
                if self._vision_busy or (_now - self._vision_last_time) < _cooldown:
                    _wait = max(0, _cooldown - (_now - self._vision_last_time))
                    print(f"[Vision] ⏳ Cooldown active ({_wait:.1f}s remaining) — ignoring duplicate call")
                    result = "Vision is still processing the previous request. I will not call this again."
                else:
                    self._vision_busy      = True
                    self._vision_last_time = _now
                    angle     = args.get("angle", "screen").lower()
                    user_text = args.get("text", "What do you see?")
                    keep_open = args.get("keep_open", False)
                    from core.opencv_vision import get_vision_coordinator
                    coord = get_vision_coordinator()
                    if angle == "camera":
                        img_b, mime_t = await loop.run_in_executor(None, lambda: coord.capture_frame_for_query("camera"))
                        is_continuous = coord.is_active()
                        if not is_continuous:
                            self.ui.start_camera_stream()
                            self._vision_cam_active = True
                        else:
                            self._vision_cam_active = False  # Keep continuous camera stream open!
                        self._vision_keep_open = keep_open or is_continuous
                        print(f"[Vision] 📷 Camera: {len(img_b)} bytes (continuous={is_continuous})")
                        _stall = "camera"
                    else:
                        img_b, mime_t = await loop.run_in_executor(None, lambda: coord.capture_frame_for_query("screen"))
                        print(f"[Vision] 🖥️ Screen: {len(img_b)} bytes")
                        _stall = "screen"
                    self._pending_vision = (img_b, mime_t, user_text, angle)
                    # The image is attached to this same exchange, so there is
                    # nothing to stall for and nothing to announce. Asking for an
                    # acknowledgement here is what produced two spoken answers —
                    # the model filled that turn by answering the question from
                    # imagination, then answered it again once it could see.
                    result = (
                        f"[VISION_ACTIVE] {_stall.capitalize()} captured and attached to this "
                        f"same exchange. Do not acknowledge and do not answer yet — the image "
                        f"is arriving with this result. Reply once, from what you actually see "
                        f"in it."
                    )

            elif name == "close_camera":
                self._vision_keep_open = False
                self.ui.stop_camera_stream()
                try:
                    from core.opencv_vision import get_vision_coordinator
                    get_vision_coordinator().room_sentinel.stop()
                except Exception:
                    pass
                result = "Camera closed."

            elif name == "toggle_room_sentinel":
                active = args.get("active", None)
                from core.opencv_vision import get_vision_coordinator
                coord = get_vision_coordinator()
                if active is None:
                    is_now_on = coord.toggle_room_sentinel()
                elif active:
                    coord.room_sentinel.start()
                    is_now_on = True
                else:
                    coord.room_sentinel.stop()
                    is_now_on = False
                
                if is_now_on:
                    self.ui.start_camera_stream()
                    self._vision_keep_open = True
                    result = "Modo centinela de habitación ACTIVADO. Estoy observando la habitación en tiempo real."
                else:
                    self._vision_keep_open = False
                    self.ui.stop_camera_stream()
                    result = "Modo centinela DESACTIVADO. Cámara en reposo."

            elif name == "system_status":
                r = await loop.run_in_executor(None, get_system_status)
                env_rep = self._env_awareness.get_environment_report()
                result = f"{r} | Entorno: {env_rep}"

            elif name == "manage_monitor":
                action = args.get("action", "").lower().strip()
                topic  = args.get("topic", "").strip()
                if action == "add" and topic:
                    result = await asyncio.to_thread(add_monitor, topic)
                elif action == "remove" and topic:
                    result = await asyncio.to_thread(remove_monitor, topic)
                elif action == "list":
                    topics = await asyncio.to_thread(list_monitors)
                    result = ("Monitoring: " + ", ".join(topics)) if topics else "No topics are being monitored."
                else:
                    result = "Specify action (add/remove/list) and a topic."

            elif name == "sleep_viernes" or name == "sleep_assistant":
                self._sleep_pending = True
                self.ui.write_log("SYS: Sleep mode requested by user.")
                if not self._wake_enabled:
                    try:
                        from core.wake_word import is_ready
                        if is_ready():
                            self._wake_enabled = True
                            self._ensure_wake_detector()
                            self.ui._refresh_wake_btns()
                    except Exception:
                        pass

                async def _do_sleep():
                    # Allow parting speech to finish before sleeping, unless woken in the meantime
                    await asyncio.sleep(2.2)
                    if self._sleep_pending:
                        self.sleep(reason="user commanded sleep")
                asyncio.create_task(_do_sleep())
                result = "Entered sleep mode. Avatar is resting on beanbag; app stays open in wake word mode."

            elif name == "silence_viernes":
                self.silence_and_mute(reason="comando de voz 'Silencio'")
                result = "[SILENCED_AND_MUTED] Do not speak or output any audio response."

            elif name == "shutdown_viernes" or name == "shutdown_assistant":
                self.ui.write_log("SYS: Shutdown explicitly requested.")
                async def _do_shutdown():
                    await self._save_session_summary()
                    if self.session:
                        try:
                            await self.session.send_client_content(
                                turns={"role": "user", "parts": [{"text": "Say a brief natural goodbye to the user."}]},
                                turn_complete=True,
                            )
                        except Exception:
                            pass
                    await asyncio.sleep(1.5)
                    import os as _os
                    _os._exit(0)
                asyncio.create_task(_do_shutdown())

            elif self._action_registry.has(name):
                # file_processor: fall back to the currently-uploaded file when none is given or only a basename is passed
                if name == "file_processor":
                    active_f = self.ui.current_file or self._current_uploaded_file
                    given_fp = (args.get("file_path") or "").strip()
                    if not given_fp and active_f:
                        args["file_path"] = active_f
                    elif given_fp and not Path(given_fp).exists():
                        if active_f and Path(active_f).exists() and (
                            Path(active_f).name.lower() == Path(given_fp).name.lower()
                            or not Path(given_fp).parent or str(Path(given_fp).parent) == "."
                        ):
                            args["file_path"] = active_f
                        elif self._dashboard and (self._dashboard._uploads_dir / Path(given_fp).name).exists():
                            args["file_path"] = str(self._dashboard._uploads_dir / Path(given_fp).name)
                _ctx = {"player": self.ui, "speak": self.speak,
                        "response": None, "session_memory": None,
                        "last_said": getattr(self, "_last_out_logged", ""),
                        "user": getattr(self, "_current_user", "Jesús")}
                r = await loop.run_in_executor(None, lambda: self._action_registry.run(name, args, _ctx))
                result = r or "Done."
                try:
                    self._learning.record_tool_habit(name)
                    from core.context_memory import task_context
                    _q_hint = args.get("query") or args.get("file_path") or args.get("app_name") or ""
                    task_context.record_tool_use(name, str(_q_hint))
                    if name in ("web_search", "web_research") and _q_hint:
                        task_context.set_entity("last_search", str(_q_hint))
                    elif args.get("file_path"):
                        task_context.set_entity("last_file", str(args["file_path"]))
                except Exception:
                    pass
                # web_search / web_research: mirror results to the on-screen content panel and trigger visual panel
                if (name in ("web_search", "web_research") and r
                        and not str(r).startswith("No results")
                        and not str(r).startswith("Search failed")):
                    _mode  = args.get("mode", "search")
                    _query = args.get("query") or args.get("topic") or ", ".join(args.get("items", []))
                    _label = f"{_mode.upper()} — {_query[:38]}" if _query else _mode.upper()
                    self.ui.show_content(_label, str(r))
                    if _query:
                        self._check_visual_context(_query, str(r))

            else:
                if self._plugin_registry.has(name):
                    r = await loop.run_in_executor(
                        None,
                        lambda: self._plugin_registry.run(name, args, player=self.ui, session_memory=None)
                    )
                    result = r or "Done."
                    if hasattr(self.ui, "notify_task_completed"):
                        self.ui.notify_task_completed()
                    if hasattr(self, "_speech_anim"):
                        self._speech_anim.on_tool_success(name)
                else:
                    result = f"Unknown tool: {name}"

        except Exception as e:
            result = f"Tool '{name}' failed: {e}"
            traceback.print_exc()
            self.speak_error(name, e)
            if hasattr(self.ui, "notify_task_error"):
                self.ui.notify_task_error(str(e))
            if hasattr(self, "_speech_anim"):
                self._speech_anim.on_tool_error(name)

        if not self.ui.muted:
            self.ui.set_state("LISTENING")

        print(f"[VIERNES] 📤 {name} → {str(result)[:80]}")

        # A tool that declared itself NON_BLOCKING also says when its answer may
        # re-enter the conversation. Without this the model finishes whatever it
        # was saying and then reads the result out on top of it — which, for
        # something like a phone call already ringing, is exactly the noise the
        # non-blocking call was meant to avoid. Tools that declared nothing get
        # the API default and behave as they always have.
        _sched = (self._action_registry.scheduling(name)
                  or self._plugin_registry.scheduling(name))
        _extra = {"scheduling": _sched} if _sched else {}
        return types.FunctionResponse(
            id=fc.id, name=name,
            response={"result": result},
            **_extra
        )

    async def _send_realtime(self):
        while True:
            msg = await self.out_queue.get()
            # Gemini 3.x Live rejects the old realtime_input.media_chunks field
            # (what `media=...` maps to) and closes the socket with a 1007. Send
            # mic / phone PCM through the new `audio` field instead. Queue items
            # are {"data": <bytes>, "mime_type": <str>} from _listen_audio and
            # the phone relay.
            await self.session.send_realtime_input(
                audio=types.Blob(
                    data=msg["data"],
                    mime_type=msg.get("mime_type", "audio/pcm"),
                )
            )

    async def _listen_audio(self):
        print("[VIERNES] 🎤 Mic started")
        loop = asyncio.get_event_loop()
        _voice_id_buf = bytearray()
        _last_voice_check = 0.0
        _barge_buf: list[np.ndarray] = []
        _barge_silence_frames = 0
        _barge_checking = False

        def _dispatch_barge_silence_check(pcm_bytes: bytes) -> None:
            nonlocal _barge_checking
            if _barge_checking or not pcm_bytes or self.ui.muted:
                return
            _barge_checking = True

            def _worker():
                nonlocal _barge_checking
                try:
                    import speech_recognition as sr
                    rec = sr.Recognizer()
                    audio_data = sr.AudioData(pcm_bytes, SEND_SAMPLE_RATE, 2)
                    txt = rec.recognize_google(audio_data, language="es-ES")
                    if txt and _is_silence_command(txt):
                        self.ui.write_log(f"You: {txt}")
                        self.silence_and_mute(reason=f"comando de voz '{txt}'")
                except Exception:
                    pass
                finally:
                    _barge_checking = False

            threading.Thread(target=_worker, daemon=True, name="BargeSilenceCheck").start()

        def callback(indata, frames, time_info, status):
            nonlocal _voice_id_buf, _last_voice_check, _barge_buf, _barge_silence_frames
            # If the microphone is muted ("Silencio" or F4), never listen or stream anything
            if self.ui.muted:
                if _barge_buf:
                    _barge_buf.clear()
                return

            # Clasificación acústica local en tiempo real (<0.4ms, sin red)
            try:
                scene = self._env_awareness.analyze_frame(indata)
            except Exception:
                scene = "DIRECT_SPEECH"

            # ── Wake-word gate ───────────────────────────────────────────────
            # While asleep, the mic audio NEVER goes to Gemini (nothing is
            # streamed, so VIERNES can't respond to speech not addressed to it and
            # nothing leaves the machine). Frames are instead handed to the local
            # detector, which runs its model in ITS OWN thread — the cost here is
            # only a queue push, so the audio path is never slowed. When wake word
            # is off (default) or we're awake, this is a single boolean check.
            if not self._awake or self._sleep_pending:
                det = self._wake_detector
                if det is None:
                    self._ensure_wake_detector()
                    det = self._wake_detector
                if det is not None and not self._sleep_pending:
                    det.feed(indata)
                return

            # ── Environmental Attention Gate ─────────────────────────────────
            # Si pasaron más de 20s desde la última interacción y no se mantiene PTT,
            # la ventana de atención activa expira: evitamos transmitir conversaciones
            # casuales de terceros en la habitación a Gemini. Retenemos un buffer
            # rodante de pre-roll y derivamos la señal al detector local de activación.
            is_active_window = (time.monotonic() < self._attention_until) or (self._ptt_enabled and self._ptt_held)
            if not is_active_window:
                data_pcm = indata.tobytes()
                self._pre_roll_mic.append(data_pcm)
                det = self._wake_detector
                if det is None:
                    self._ensure_wake_detector()
                    det = self._wake_detector
                if det is not None:
                    det.feed(indata)
                return

            with self._speaking_lock:
                viernes_speaking = self._is_speaking

            # ── Barge-in & "Silencio" while VIERNES is speaking ──────────────
            if viernes_speaking:
                try:
                    lvl = _pcm_level(indata)
                    # 1. If EchoGuard detects genuine user voice over our speaker output,
                    # forward the frame to Gemini so input_transcription catches "Silencio" in real time
                    if self._echo.is_user_speech(indata, SEND_SAMPLE_RATE, lvl):
                        if not self._phone_active and self._audio_route != "phone":
                            loop.call_soon_threadsafe(
                                self.out_queue.put_nowait,
                                {"data": indata.tobytes(), "mime_type": "audio/pcm"}
                            )
                    # 2. Parallel local Spanish keyword spotter for "Silencio" during speech
                    frame_1d = indata[:, 0] if getattr(indata, "ndim", 1) > 1 else indata
                    rms = float(np.sqrt(np.mean(frame_1d.astype(np.float32) ** 2)))
                    if rms > 145.0:
                        _barge_buf.append(frame_1d.copy())
                        _barge_silence_frames = 0
                        if len(_barge_buf) >= 22:  # ~1.1s of continuous voice while speaking
                            pcm_b = np.concatenate(_barge_buf).tobytes()
                            _barge_buf.clear()
                            _dispatch_barge_silence_check(pcm_b)
                    elif _barge_buf:
                        _barge_silence_frames += 1
                        if _barge_silence_frames >= 4:  # ~200ms pause after word "Silencio"
                            total_samples = sum(len(x) for x in _barge_buf)
                            if total_samples >= 4000:  # >= 250ms of speech
                                pcm_b = np.concatenate(_barge_buf).tobytes()
                                _dispatch_barge_silence_check(pcm_b)
                            _barge_buf.clear()
                            _barge_silence_frames = 0
                except Exception:
                    pass
                return
            elif _barge_buf:
                _barge_buf.clear()
                _barge_silence_frames = 0

            # ── Echo tail ────────────────────────────────────────────────────
            # The speaking flag has dropped but the speakers have not finished.
            # Sending this to the model is how an assistant hears itself, decides
            # it was addressed, and answers its own last sentence. The microphone
            # stays OPEN — the guard only drops blocks that are our own voice, so
            # replying the instant it stops still works.
            if self._tail_active():
                try:
                    if not self._echo.is_user_speech(
                            indata, SEND_SAMPLE_RATE, _pcm_level(indata)):
                        return
                    self._tail_until = 0.0      # a real voice ends the tail early
                except Exception:
                    return
            elif self._echo._hist:
                self._echo.reset()

            # ── Push-to-talk ─────────────────────────────────────────────────
            # When it is on the microphone is closed by default and the chord
            # opens it, which is the whole point: nothing leaves the machine
            # unless you are holding the key.
            if self._ptt_enabled and not self._ptt_held:
                return
            
            if not self.ui.muted and not self._phone_active and self._audio_route != "phone":
                data = indata.tobytes()
                loop.call_soon_threadsafe(
                    self.out_queue.put_nowait,
                    {"data": data, "mime_type": "audio/pcm"}
                )
                try:
                    # Solo renovar la ventana si detectamos voz directa cercana (no ruido ni charlas lejanas)
                    if scene == "DIRECT_SPEECH":
                        self.renew_attention(15.0)
                except Exception:
                    pass
                # Live Voice Identification buffering
                _voice_id_buf.extend(data)
                now_t = time.time()
                if len(_voice_id_buf) >= 32000 and (now_t - _last_voice_check) > 2.5:
                    _last_voice_check = now_t
                    buf_copy = bytes(_voice_id_buf[:32000])
                    _voice_id_buf.clear()
                    try:
                        from security.voice_id import voice_id_engine
                        def _identify_and_sync(pcm_b: bytes) -> None:
                            try:
                                res = voice_id_engine.identify_speaker(pcm_b)
                                if isinstance(res, dict) and res.get("speaker"):
                                    spk = str(res["speaker"])
                                    conf = float(res.get("confidence", 0.0))
                                    self._current_user = spk
                                    self._env_awareness.update_speaker(spk, conf)
                                    from core.context_memory import task_context
                                    task_context.set_speaker(spk)
                            except Exception:
                                pass
                        threading.Thread(target=_identify_and_sync, args=(buf_copy,), daemon=True).start()
                    except Exception:
                        pass

                # Feed the live mic level to the HUD so the waveform reacts to
                # the user's actual voice while listening. Purely cosmetic — any
                # failure here must never disturb the mic.
                try:
                    self.ui.set_audio_level(_pcm_level(indata))
                except Exception:
                    pass

        try:
            def _open_mic(dev):
                return sd.InputStream(
                    samplerate=SEND_SAMPLE_RATE,
                    channels=CHANNELS,
                    dtype="int16",
                    blocksize=CHUNK_SIZE,
                    device=dev,
                    callback=callback,
                )

            # Which microphone. resolve() returns None for "system default" and
            # for a saved device that is no longer present — so a headset
            # unplugged since the last run falls back to the built-in mic
            # instead of raising on startup and taking the session with it.
            _mic_name = get_input_device()
            _mic_dev  = audio_devices.resolve(_mic_name, "input")
            if _mic_dev is not None:
                print(f"[VIERNES] 🎤 Input device: {_mic_name}")
            try:
                _mic_stream = _open_mic(_mic_dev)
            except Exception as _e:
                # A device the picker listed but the driver will not open right
                # now — exclusive mode, a webcam already in use, a virtual mic
                # whose source went away. Chosen hardware failing must never
                # mean the assistant cannot hear at all.
                if _mic_dev is None:
                    raise
                print(f"[VIERNES] ⚠️  Mic '{_mic_name}' failed: {_e} — using default")
                self.ui.write_log(
                    f"SYS: Microphone '{_mic_name}' unavailable — using system default."
                )
                _mic_stream = _open_mic(None)

            with _mic_stream:
                print("[VIERNES] 🎤 Mic stream open")
                while True:
                    await asyncio.sleep(0.1)
        except Exception as e:
            print(f"[VIERNES] ❌ Mic: {e}")
            raise

    async def _flush_pending_vision(self) -> bool:
        """Send a captured frame immediately after its tool response.

        The frame is already in hand by the time `screen_process` returns — the
        capture happened inside the tool call. The old flow still made the model
        speak a turn first and only injected the image on that turn's
        turn_complete, which cost a whole extra round trip AND produced two
        spoken answers: one improvised without the picture, then the real one.
        Sending it here means the model has the tool result and the image before
        it generates anything, so the user gets one answer, sooner.
        """
        if not (self._pending_vision and self.session):
            return False

        import base64 as _b64
        img_b, mime_t, question, angle = self._pending_vision
        self._pending_vision = None
        b64 = _b64.b64encode(img_b).decode("ascii")
        print(f"[Vision] 📤 {len(img_b):,} bytes (angle={angle}) → main session")

        # Label the source. Without it the image arrives carrying nothing but
        # the user's own sentence, and a screenshot of this app — which has a
        # face in the middle of it — got read as a photo of the user. What the
        # label *means* is explained once, in the generated [SELF] block.
        src = ("[IMAGE SOURCE: WEBCAM]" if angle == "camera"
               else "[IMAGE SOURCE: SCREEN CAPTURE]")

        v_ctx = ""
        if angle == "camera":
            try:
                from core.opencv_vision import get_vision_coordinator
                v_ctx = get_vision_coordinator().get_visual_context_prompt() + "\n\n"
            except Exception:
                pass

        await self.session.send_client_content(
            turns={"role": "user", "parts": [
                {"inline_data": {"mime_type": mime_t, "data": b64}},
                {"text": f"{src}\n\n{v_ctx}{question}"},
            ]},
            turn_complete=True,
        )

        if self._vision_cam_active:
            # Camera: stay busy until VIERNES has finished speaking the answer,
            # then close the preview.
            self._vision_cam_active    = False
            self._vision_close_pending = True
        else:
            self._vision_busy = False
        return True

    async def _receive_audio(self):
        print("[VIERNES] 👂 Recv started")
        out_buf, in_buf = [], []
        tts_clause_buf: list[str] = []
        tts_clause_q: asyncio.Queue[str] = asyncio.Queue()

        def _extract_ready_clauses(buf_list: list[str], flush_all: bool = False) -> list[str]:
            joined = " ".join(buf_list).strip()
            if not joined:
                buf_list.clear()
                return []
            if flush_all:
                buf_list.clear()
                return [joined]
            # Split on sentence or clause punctuation as soon as we have a natural phrase
            m = re.search(r"^(.{18,}?[.!?;:](?:\s+|$)|.{32,}?,(?:\s+))(.*)$", joined, re.DOTALL)
            if m:
                ready = m.group(1).strip()
                rest = m.group(2).strip()
                buf_list.clear()
                if rest:
                    buf_list.append(rest)
                return [ready] if ready else []
            return []

        async def _external_tts_worker():
            while True:
                clause = await tts_clause_q.get()
                if not clause or self._interrupted:
                    continue
                eng_mode = get_tts_engine()
                try:
                    if eng_mode == "elevenlabs":
                        el_cfg = get_elevenlabs_config()
                        if el_cfg.get("api_key"):
                            from core.tts import ElevenLabsTTSEngine
                            eng = ElevenLabsTTSEngine(
                                api_key=el_cfg["api_key"],
                                voice_id=el_cfg.get("voice_id", "21m00Tcm4TlvDq8ikWAM"),
                            )
                            def _stream_el():
                                for chunk in eng.stream_pcm_chunks(clause, 24000, 2400):
                                    if self._interrupted:
                                        break
                                    if self._turn_done_event and self._turn_done_event.is_set():
                                        self._turn_done_event.clear()
                                    self.audio_in_queue.put_nowait(chunk)
                            await asyncio.to_thread(_stream_el)
                    elif eng_mode == "edgetts":
                        from memory.config_manager import get_edge_voice
                        from core.tts import EdgeTTSEngine
                        eng = EdgeTTSEngine(voice=get_edge_voice())
                        pcm_data = await asyncio.to_thread(eng.synthesize_pcm, clause, 24000)
                        if pcm_data and not self._interrupted:
                            if self._turn_done_event and self._turn_done_event.is_set():
                                self._turn_done_event.clear()
                            _SLICE = 2400
                            for _i in range(0, len(pcm_data), _SLICE):
                                if self._interrupted:
                                    break
                                self.audio_in_queue.put_nowait(pcm_data[_i : _i + _SLICE])
                    elif eng_mode == "coqui_xtts":
                        from memory.config_manager import get_coqui_config
                        from core.tts import CoquiXTTSEngine
                        cq = get_coqui_config()
                        eng = CoquiXTTSEngine(
                            speaker=cq.get("speaker", "Ana Florence"),
                            speaker_wav=cq.get("speaker_wav", ""),
                            language=cq.get("language", "es"),
                        )
                        pcm_data = await asyncio.to_thread(eng.synthesize_pcm, clause, 24000)
                        if pcm_data and not self._interrupted:
                            if self._turn_done_event and self._turn_done_event.is_set():
                                self._turn_done_event.clear()
                            _SLICE = 2400
                            for _i in range(0, len(pcm_data), _SLICE):
                                if self._interrupted:
                                    break
                                self.audio_in_queue.put_nowait(pcm_data[_i : _i + _SLICE])
                except Exception as exc:
                    print(f"[TTS Stream] ⚠️ Error ({eng_mode}): {exc}")
                    try:
                        if self.ui and hasattr(self.ui, "write_log"):
                            self.ui.write_log(f"SYS: Error en motor {eng_mode} ({exc}) — usando Edge Neural de respaldo.")
                        from memory.config_manager import get_edge_voice
                        from core.tts import EdgeTTSEngine
                        fb_eng = EdgeTTSEngine(voice=get_edge_voice())
                        pcm_data = await asyncio.to_thread(fb_eng.synthesize_pcm, clause, 24000)
                        if pcm_data and not self._interrupted:
                            _SLICE = 2400
                            for _i in range(0, len(pcm_data), _SLICE):
                                if self._interrupted:
                                    break
                                self.audio_in_queue.put_nowait(pcm_data[_i : _i + _SLICE])
                    except Exception:
                        pass

        tts_worker_task = asyncio.create_task(_external_tts_worker())

        try:
            while True:
                async for response in self.session.receive():

                    # ── Session resumption ───────────────────────────────────
                    _sru = getattr(response, "session_resumption_update", None)
                    if _sru is not None:
                        if getattr(_sru, "resumable", False) and getattr(_sru, "new_handle", None):
                            if self._resume_handle is None:
                                print("[VIERNES] 🔗 Session resumption armed")
                            self._resume_handle = _sru.new_handle

                    if response.data:
                        if self._interrupted or self.ui.muted:
                            pass  # discard: interrupted or muted
                        else:
                            # Only enqueue Gemini native audio when tts_engine == "gemini"
                            if get_tts_engine() == "gemini":
                                if self._turn_done_event and self._turn_done_event.is_set():
                                    self._turn_done_event.clear()
                                # Split into ~50 ms chunks so interrupt() stops audio within 50 ms
                                # (24000 Hz × 2 bytes/sample × 0.05 s = 2400 bytes per slice)
                                _audio_data = response.data
                                _SLICE = 2400
                                for _i in range(0, len(_audio_data), _SLICE):
                                    self.audio_in_queue.put_nowait(_audio_data[_i : _i + _SLICE])

                    if response.server_content:
                        sc = response.server_content

                        if getattr(sc, "interrupted", False):
                            self.interrupt()

                        if sc.output_transcription and sc.output_transcription.text:
                            if not self.ui.muted and not self._interrupted:
                                txt = _clean_transcript(sc.output_transcription.text)
                                if txt and not _is_repeat_chunk(txt, out_buf):
                                    out_buf.append(txt)
                                    self._visemes.feed_text(txt)
                                    if hasattr(self, "_speech_anim"):
                                        self._speech_anim.process_text_chunk(txt)
                                    # Real-time clause streaming for ElevenLabs Flash v2.5 / Edge Neural TTS
                                    if get_tts_engine() in ("elevenlabs", "edgetts", "coqui_xtts") and not self._interrupted:
                                        tts_clause_buf.append(txt)
                                        for ready_clause in _extract_ready_clauses(tts_clause_buf, flush_all=False):
                                            tts_clause_q.put_nowait(ready_clause)

                        if sc.input_transcription and sc.input_transcription.text:
                            if self._awake and not self._sleep_pending:
                                txt = _clean_input_transcript(sc.input_transcription.text)
                                if txt:
                                    in_buf.append(txt)
                                    self._last_user_speech = time.monotonic()
                                    joined_in = " ".join(in_buf).strip()
                                    if _is_silence_command(txt) or _is_silence_command(joined_in):
                                        self.ui.write_log(f"You: {joined_in or txt}")
                                        in_buf.clear()
                                        out_buf.clear()
                                        tts_clause_buf.clear()
                                        while not tts_clause_q.empty():
                                            try:
                                                tts_clause_q.get_nowait()
                                            except Exception:
                                                break
                                        self.silence_and_mute(reason="comando de voz 'Silencio'")
                                        continue

                        if sc.turn_complete:
                            if self._turn_done_event:
                                self._turn_done_event.set()

                            # If this turn_complete ends an interrupted response, clear the
                            # flag and skip all further processing for that turn.
                            if self._interrupted:
                                self._interrupted = False
                                in_buf  = []
                                out_buf = []
                                tts_clause_buf.clear()
                                while not tts_clause_q.empty():
                                    try:
                                        tts_clause_q.get_nowait()
                                    except Exception:
                                        break
                                self._visemes.reset()
                                continue

                            if self._sleep_pending or not self._awake:
                                in_buf = []

                            full_in = " ".join(in_buf).strip()
                            if full_in:
                                self._last_out_logged = ""   # new exchange
                                self.ui.write_log(f"You: {full_in}")
                                self._session_log.append(f"User: {full_in}")
                                self._last_user_query = full_in
                                if self._dashboard:
                                    asyncio.create_task(self._dashboard.broadcast({
                                        "type": "log", "speaker": "user",
                                        "text": full_in,
                                        "ts": datetime.now().isoformat(),
                                    }))
                            in_buf = []

                            full_out = " ".join(out_buf).strip()
                            if full_out and len(full_out) >= _REPEAT_MIN and self._last_out_logged:
                                if full_out in self._last_out_logged:
                                    full_out = ""
                                    tts_clause_buf.clear()
                            if full_out:
                                self._last_out_logged = full_out
                                try:
                                    from actions.repeat_last_said import set_last_spoken
                                    set_last_spoken(full_out)
                                except Exception:
                                    pass
                                self.ui.write_log(f"{self._asst_name}: {full_out}")
                                self._session_log.append(f"{self._asst_name}: {full_out}")
                                self._learning.maybe_consolidate(self._session_log)
                                if self._dashboard:
                                    asyncio.create_task(self._dashboard.broadcast({
                                        "type": "log", "speaker": "viernes",
                                        "text": full_out,
                                        "ts": datetime.now().isoformat(),
                                    }))

                                # Trigger Edith Contextual Visual Intelligence
                                self._check_visual_context(self._last_user_query, full_out)

                                # Flush any remaining trailing words to the real-time TTS stream queue
                                if get_tts_engine() in ("elevenlabs", "edgetts", "coqui_xtts") and not self._interrupted:
                                    for tail_clause in _extract_ready_clauses(tts_clause_buf, flush_all=True):
                                        tts_clause_q.put_nowait(tail_clause)
                            else:
                                tts_clause_buf.clear()
                            out_buf = []

                            if self._vision_close_pending:
                                self._vision_close_pending = False
                                self._vision_busy = False
                                from core.opencv_vision import get_vision_coordinator
                                if not getattr(self, "_vision_keep_open", False) and not get_vision_coordinator().is_active():
                                    async def _cam_close():
                                        await asyncio.sleep(2.5)
                                        if not getattr(self, "_vision_keep_open", False) and not get_vision_coordinator().is_active():
                                            self.ui.stop_camera_stream()
                                    asyncio.create_task(_cam_close())

                    if response.tool_call:
                        fn_responses = []
                        for fc in response.tool_call.function_calls:
                            print(f"[VIERNES] 📞 {fc.name}")
                            fr = await self._execute_tool(fc)
                            fn_responses.append(fr)
                        await self.session.send_tool_response(
                            function_responses=fn_responses
                        )
                        await self._flush_pending_vision()
        except Exception as e:
            print(f"[VIERNES] ❌ Recv: {e}")
            traceback.print_exc()
            raise
        finally:
            tts_worker_task.cancel()

    async def _play_audio(self):
        print("[VIERNES] 🔊 Play started")

        _spk_name = get_output_device()
        _spk_dev  = audio_devices.resolve(_spk_name, "output")
        if _spk_dev is not None:
            print(f"[VIERNES] 🔊 Output device: {_spk_name}")

        def _open_spk(dev):
            st = sd.RawOutputStream(
                samplerate=RECEIVE_SAMPLE_RATE,
                channels=CHANNELS,
                dtype="int16",
                blocksize=CHUNK_SIZE,
                device=dev,
            )
            st.start()
            return st

        try:
            stream = _open_spk(_spk_dev)
        except Exception as _e:
            # A chosen output that the host API accepts by name but refuses to
            # open (exclusive mode, wrong sample rate, device asleep) must not
            # cost the user their voice. Fall back to the default and say so.
            if _spk_dev is None:
                raise
            print(f"[VIERNES] ⚠️  Output device '{_spk_name}' failed: {_e} — using default")
            self.ui.write_log(f"SYS: Speaker '{_spk_name}' unavailable — using system default.")
            stream = _open_spk(None)

        # Ask the device how far behind the speakers actually are, rather than
        # assuming. This is what the echo tail is sized from, so a machine with a
        # large audio buffer gets a correspondingly longer guard — and one with a
        # tiny buffer is not penalised with a delay it does not need.
        try:
            lat = float(getattr(stream, "latency", 0.0) or 0.0)
            if 0.0 < lat < 1.0:
                self._out_latency = lat
            print(f"[VIERNES] 🔊 Output latency {self._out_latency*1000:.0f} ms "
                  f"→ echo tail {(self._out_latency + _TAIL_MARGIN)*1000:.0f} ms")
        except Exception:
            pass

        try:
            while True:
                try:
                    chunk = await asyncio.wait_for(
                        self.audio_in_queue.get(),
                        timeout=0.1
                    )
                except asyncio.TimeoutError:
                    if (
                        self._turn_done_event
                        and self._turn_done_event.is_set()
                        and self.audio_in_queue.empty()
                    ):
                        self.set_speaking(False)
                        if hasattr(self, "_speech_anim"):
                            self._speech_anim.on_speech_end()
                        self._turn_done_event.clear()
                    continue

                self.set_speaking(True)
                if hasattr(self, "_speech_anim"):
                    self._speech_anim.on_speech_start()

                # Batch all immediately-available chunks into one write to reduce
                # thread-pool round-trips (was one asyncio.to_thread per 50ms slice).
                # Cap at ~200 ms so interrupt() still stops audio within ~200 ms.
                batch = bytearray(chunk)
                while len(batch) < 9600:   # 9600 bytes ≈ 200 ms at 24 kHz / 16-bit mono
                    try:
                        batch.extend(self.audio_in_queue.get_nowait())
                    except asyncio.QueueEmpty:
                        break

                # Drive the HUD waveform and the avatar's mouth from VIERNES's
                # own voice. The batch is up to 200 ms long, so we hand over a
                # *schedule* of 20 ms viseme frames instead of a single averaged
                # level and let the HUD play it out in step with the audio.
                try:
                    pcm = np.frombuffer(bytes(batch), dtype=np.int16)
                    hop = _VIS_HOP / RECEIVE_SAMPLE_RATE
                    frames = _pcm_visemes(pcm, sr=RECEIVE_SAMPLE_RATE)
                    now = time.time()
                    horizon = self._out_latency + _CURSOR_SLACK
                    if not (now <= self._play_cursor <= now + horizon):
                        self._play_cursor = now + _FIRST_SOUND
                    at = self._play_cursor
                    self._play_cursor += pcm.size / RECEIVE_SAMPLE_RATE
                    if frames:
                        frames = self._visemes.frames(frames, hop)
                        self.ui.push_visemes(frames, hop, at)
                        self._out_level = max(f[0] for f in frames)
                        self._echo.note_output(pcm, RECEIVE_SAMPLE_RATE,
                                               self._out_level)
                    else:
                        lvl = _pcm_level(pcm)
                        self.ui.set_audio_level(lvl)
                        self._out_level = lvl
                        self._echo.note_output(pcm, RECEIVE_SAMPLE_RATE, lvl)
                except Exception:
                    pass

                raw_batch = bytes(batch)
                if self._dashboard and self._audio_route in ("phone", "both"):
                    try:
                        await self._dashboard.broadcast_audio(raw_batch)
                    except Exception:
                        pass

                try:
                    if self._audio_route == "phone":
                        await asyncio.sleep(len(raw_batch) / (RECEIVE_SAMPLE_RATE * 2))
                    else:
                        await asyncio.to_thread(stream.write, raw_batch)
                except (RuntimeError, asyncio.CancelledError):
                    break   # executor shutting down — exit cleanly
        except Exception as e:
            print(f"[VIERNES] ❌ Play: {e}")
            raise
        finally:
            self.set_speaking(False)
            if hasattr(self, "_speech_anim"):
                self._speech_anim.on_speech_end()
            stream.stop()
            stream.close()

    # ── Morning briefing ────────────────────────────────────────────────────────

    async def _send_startup_briefing(self) -> None:
        """
        Two-phase briefing optimized for speed:
          Phase 1 — instant greeting (no tools) → speech starts in <1s
          Phase 2 — news pre-fetched in a background thread while Phase 1 plays,
                    delivered as ready text (no Gemini tool-call round-trip) and
                    shown on the UI content panel. Waits for turn_complete event
                    instead of a fixed sleep so there is no unnecessary gap.
        """
        memory   = load_memory()
        identity = memory.get("identity", {})

        def _val(k: str) -> str:
            e = identity.get(k, {})
            return (e.get("value", "") if isinstance(e, dict) else str(e)).strip()

        lang = _val("language")
        name = _val("name")
        time_str = datetime.now().strftime("%H:%M")

        # Start fetching news immediately — runs in parallel while phase 1 plays
        loop = asyncio.get_event_loop()
        news_future = loop.run_in_executor(None, _fetch_news_sync, "top world news today")

        await asyncio.sleep(0.3)
        if not self.session:
            # Respaldo de IA local sin conexión cuando no hay sesión de red
            try:
                from core.local_ai_service import get_local_ai_service
                local_ai = get_local_ai_service()
                self.ui.set_state("THINKING")
                def _run_local():
                    resp = local_ai.generate_response(raw)
                    self.ui.set_state("SPEAKING")
                    self.ui.write_log(f"{self._asst_name} (Local/Offline): {resp}")
                    local_ai.speak_offline(resp)
                    self.ui.set_state("LISTENING")
                import threading as _th
                _th.Thread(target=_run_local, daemon=True).start()
            except Exception as _e:
                print(f"[LocalAI] Fallback error: {_e}")
            return

        # ── Phase 1: instant greeting ─────────────────────────────────────────
        # The briefing fires before the user has said anything, so the
        # remembered language is the only signal there is. It is a starting
        # point, not a setting: the moment they reply, their language wins.
        lang_clause = (f" Speak this greeting in {lang}, then follow the "
                       f"user's own language from their first reply onward."
                       if lang else "")
        name_clause = f" Address the user as {name}." if name else ""

        # Inject last session context if available — pop removes it so it's never repeated
        last = await asyncio.to_thread(pop_last_session)
        session_clause = ""
        if last:
            try:
                _delta = (datetime.now() - datetime.strptime(last["date"], "%Y-%m-%d")).days
                _when  = "earlier today" if _delta == 0 else ("yesterday" if _delta == 1 else f"{_delta} days ago")
            except Exception:
                _when = "last time"
            session_clause = (
                f" Also briefly and naturally mention that {_when}: {last['summary']}"
            )

        p1 = (
            f"Greet the user warmly, mention it is {time_str}, and say you are fetching today's news now.{session_clause} "
            f"Keep it to 2 short sentences max. Do not call any tools.{lang_clause}{name_clause}"
        )

        # Clear the turn-done event so we can wait for Phase 1 to finish
        if self._turn_done_event:
            self._turn_done_event.clear()

        await self.session.send_client_content(
            turns={"role": "user", "parts": [{"text": p1}]},
            turn_complete=True,
        )
        print("[VIERNES] Briefing phase 1 (greeting) sent.")

        # ── Phase 2: fire as soon as Phase 1 audio is done ───────────────────
        async def _deliver_news():
            try:
                lang_str = (f" Speak in {lang} unless the user has since "
                            f"spoken another language, in which case use theirs."
                            if lang else "")

                # Wait for news fetch (already running) and Phase 1 turn-complete
                # in parallel — whichever takes longer determines the wait time
                news_done   = asyncio.wrap_future(news_future)
                turn_waited = False
                if self._turn_done_event:
                    try:
                        await asyncio.wait_for(self._turn_done_event.wait(), timeout=6.0)
                        turn_waited = True
                    except asyncio.TimeoutError:
                        pass

                # Extra buffer: turn_complete fires when Gemini finishes *generating*
                # Phase 1, but audio may still be playing.  Waiting a beat here
                # prevents Phase 2 audio from arriving while Phase 1 is mid-sentence
                # (which sounds like a "repeated first response" to the user).
                if turn_waited:
                    await asyncio.sleep(0.8)
                else:
                    await asyncio.sleep(1.0)

                try:
                    news_text = await asyncio.wait_for(news_done, timeout=8.0)
                except Exception as e:
                    self.ui.write_log(f"SYS: News fetch timed out/failed: {e!r}")
                    news_text = ""

                if not self.session:
                    return

                failed = (not news_text) or news_text.startswith(
                    ("No news found", "Search failed", "Please provide")
                )
                if not failed:
                    # Show on UI content panel immediately
                    self.ui.show_content("NEWS — top world news today", news_text)

                    p2 = (
                        f"[BRIEFING] Here are today's top news headlines:\n{news_text}\n\n"
                        "Pick ONE headline, summarise it in one sentence, then say the full list "
                        f"is displayed on screen. Do not call any tools.{lang_str}"
                    )
                else:
                    self.ui.write_log(
                        f"SYS: News unavailable — backend returned: {news_text[:120]!r}"
                    )
                    p2 = (
                        "News headlines could not be fetched right now. "
                        f"Let the user know briefly.{lang_str}"
                    )

                await self.session.send_client_content(
                    turns={"role": "user", "parts": [{"text": p2}]},
                    turn_complete=True,
                )
                print("[VIERNES] Briefing phase 2 (news) sent.")
            except Exception as e:
                print(f"[Briefing] Phase 2 error: {e}")
                print(f"[VIERNES] Briefing phase 2 failed: {e}")
                self.ui.write_log("SYS: Could not fetch the news for the briefing.")

        asyncio.create_task(_deliver_news())

    # ── Session memory ──────────────────────────────────────────────────────────

    async def _save_session_summary(self) -> None:
        """Summarise the current session in 1-2 sentences and save to long_term.json."""
        log = self._session_log
        if len(log) < 3:          # need at least one exchange to be worth saving
            return
        try:
            self._learning.maybe_consolidate(log, force=True)
        except Exception:
            pass
        self._session_log = []    # reset immediately so the next session starts clean

        memory = load_memory()
        lang_entry = memory.get("identity", {}).get("language", {})
        lang = (lang_entry.get("value", "") if isinstance(lang_entry, dict) else str(lang_entry)).strip()
        lang = lang or "English"

        convo = "\n".join(log[-40:])   # cap at last 40 turns to stay within token budget
        prompt = (
            f"Summarize this conversation in 1-2 sentences in {lang}. "
            "Focus on what the user accomplished or discussed. "
            "Output ONLY the summary text, nothing else:\n\n" + convo
        )
        try:
            from core import gemini
            summary = await asyncio.to_thread(
                gemini.text, prompt, gemini.SMART, None, 30_000,
            )
            if summary:
                save_session_summary(summary, lang)
        except Exception as e:
            print(f"[Memory] ⚠️ Session summary failed: {e}")

    # ── System monitor ──────────────────────────────────────────────────────────

    async def _run_system_monitor(self) -> None:
        """Background task: voice alerts when metrics exceed thresholds."""
        while True:
            await asyncio.sleep(10)
            alert = await asyncio.to_thread(self._sys_monitor.check)
            if not alert or not self.session or not self._awake or self.ui.muted:
                continue
            # Don't interrupt an active conversation
            with self._speaking_lock:
                speaking = self._is_speaking
            if speaking or (time.monotonic() - self._last_user_speech) < 10:
                continue
            try:
                await self.session.send_client_content(
                    turns={"role": "user", "parts": [{"text": alert}]},
                    turn_complete=True,
                )
            except Exception as e:
                print(f"[Monitor] ⚠️ Could not send alert: {e}")

    # ── Communication monitor (WhatsApp & Gmail) ──────────────────────────────

    async def _run_communication_monitor(self) -> None:
        """Background task: instant notification for WhatsApp messages and Gmail incoming emails."""
        try:
            from system_monitor.communication_monitor import comm_monitor

            # Forward alerts directly to UI cybernetic log
            def _on_comm_alert(alert):
                txt = alert.get("spoken_text", "")
                icon = "💬" if alert.get("type", "").startswith("whatsapp") else "✉️"
                if hasattr(self, "ui") and self.ui and hasattr(self.ui, "write_log") and txt:
                    self.ui.write_log(f"{icon} {txt}")

            comm_monitor.register_alert_listener(_on_comm_alert)

            while True:
                await asyncio.sleep(2.5)
                alerts = await asyncio.to_thread(comm_monitor.poll_once)
                if not alerts:
                    continue

                for alert in alerts:
                    spoken = alert.get("spoken_text", "")
                    if not spoken:
                        continue

                    # If Live voice session is connected, awake, and not muted, voice the alert
                    if self.session and self._awake and not self.ui.muted:
                        with self._speaking_lock:
                            speaking = self._is_speaking
                        recent_speech = (time.monotonic() - self._last_user_speech) < 4
                        if not speaking and not recent_speech:
                            prompt = (
                                f"[NOTIFICACIÓN ENTRANTE EN TIEMPO REAL]\n{spoken}\n"
                                f"Comunícaselo inmediatamente al usuario en español con naturalidad y brevedad ejecutiva."
                            )
                            try:
                                await self.session.send_client_content(
                                    turns={"role": "user", "parts": [{"text": prompt}]},
                                    turn_complete=True,
                                )
                                print(f"[VIERNES] Communication alert voiced: {alert.get('source')}")
                            except Exception as e:
                                print(f"[CommMonitor] ⚠️ Could not voice alert: {e}")
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"[CommMonitor] ⚠️ Background task error: {e}")

    # ── Background monitor ──────────────────────────────────────────────────────

    async def _run_background_monitor(self) -> None:
        """Check user-configured topics once per day; speak alerts when new headlines appear."""
        await asyncio.sleep(300)          # wait 5 min after startup before first check
        while True:
            if self.session and self._awake and not self.ui.muted:
                # Don't interrupt if user spoke recently or VIERNES is mid-sentence
                with self._speaking_lock:
                    speaking = self._is_speaking
                recent_speech = (time.monotonic() - self._last_user_speech) < 30
                if not speaking and not recent_speech:
                    try:
                        alerts = await asyncio.to_thread(monitor_check_all)
                        memory = load_memory()
                        lang_e = memory.get("identity", {}).get("language", {})
                        lang   = (lang_e.get("value", "") if isinstance(lang_e, dict) else str(lang_e)).strip() or "English"
                        for alert in alerts:
                            msg = (
                                f"{alert}\n\n"
                                f"Inform the user about this development naturally in {lang}. "
                                "One brief sentence only."
                            )
                            await self.session.send_client_content(
                                turns={"role": "user", "parts": [{"text": msg}]},
                                turn_complete=True,
                            )
                            print("[VIERNES] Monitor alert sent.")
                            await asyncio.sleep(6)   # gap between consecutive alerts
                    except Exception as e:
                        print(f"[Monitor] ⚠️ Background check error: {e}")
            await asyncio.sleep(1800)     # check every 30 minutes

    # ── Proactive mode ──────────────────────────────────────────────────────────

    async def _run_proactive_mode(self) -> None:
        """
        Background task: periodically checks if the user has been silent long enough,
        then hands time + memory context to Gemini so it can decide what (if anything)
        to say proactively. No hardcoded rules — Gemini makes the call.
        """
        while True:
            await asyncio.sleep(60)   # evaluate once per minute

            if not self.session or not self._awake or self.ui.muted:
                continue

            with self._speaking_lock:
                speaking = self._is_speaking
            if speaking:
                continue

            if not self._proactive.should_trigger(self._last_user_speech):
                continue

            self._proactive.mark_triggered()

            try:
                memory       = await asyncio.to_thread(load_memory)
                monitors     = await asyncio.to_thread(list_monitors)
                recent_turns = self._session_log[-8:] if self._session_log else []
                prompt = self._proactive.build_prompt(
                    memory       = memory,
                    monitors     = monitors or None,
                    recent_turns = recent_turns or None,
                )
                await self.session.send_client_content(
                    turns={"role": "user", "parts": [{"text": prompt}]},
                    turn_complete=True,
                )
                print("[VIERNES] Proactive check-in.")
            except Exception as e:
                print(f"[Proactive] ⚠️ {e}")

    # ── Phone audio relay & Remote Control callbacks ─────────────────────────────

    async def _relay_phone_audio(self) -> None:
        """Forward phone mic PCM chunks from dashboard queue into the Gemini Live session."""
        q = self._dashboard._phone_audio_queue
        while True:
            try:
                chunk = await asyncio.wait_for(q.get(), timeout=1.0)
            except asyncio.TimeoutError:
                # No audio for 1 s → phone mic inactive, give PC mic back
                self._phone_active = False
                continue
            self._phone_active = True   # phone is streaming — silence PC mic
            self._last_user_speech = time.monotonic()
            if not self._awake:
                self.wake(reason="micrófono del celular")
            with self._speaking_lock:
                speaking = self._is_speaking
            if not speaking:
                try:
                    self.out_queue.put_nowait(chunk)
                except asyncio.QueueFull:
                    pass

    def _on_phone_connected(self) -> None:
        self.ui.write_log("SYS: Dispositivo móvil conectado al Control Remoto.")
        self.ui.notify_phone_connected()

    def _on_remote_wake(self) -> None:
        """Called when the user taps 'Despertar VIERNES' on the mobile Remote Control."""
        was_awake = self._awake
        self._sleep_pending = False
        try:
            if getattr(self.ui, "muted", False) and hasattr(self.ui, "_win"):
                self.ui._win._set_muted(False)
        except Exception:
            pass
        self.wake(reason="Control Remoto")
        self.ui.set_state("LISTENING")
        if was_awake:
            self.ui.write_log("SYS: Señal de activación recibida desde Control Remoto (VIERNES en escucha).")
        if self._dashboard and self._loop:
            try:
                asyncio.run_coroutine_threadsafe(
                    self._dashboard.broadcast({
                        "type": "sys",
                        "text": "⚡ VIERNES está despierta y escuchando."
                    }),
                    self._loop,
                )
            except Exception:
                pass

    def _on_remote_sleep(self) -> None:
        """Called when the user taps 'Modo Reposo' on the mobile Remote Control."""
        if not self._wake_enabled:
            try:
                from core.wake_word import is_ready
                if is_ready():
                    self._wake_enabled = True
                    self._ensure_wake_detector()
            except Exception:
                pass
        self.sleep(reason="Control Remoto")
        if self._dashboard and self._loop:
            try:
                asyncio.run_coroutine_threadsafe(
                    self._dashboard.broadcast({
                        "type": "sys",
                        "text": "🌙 VIERNES entró en modo reposo."
                    }),
                    self._loop,
                )
            except Exception:
                pass

    def _on_audio_route_change(self, route: str, reset_default: bool = False) -> None:
        """Switch VIERNES audio output/input between 'pc' (default), 'phone' (mobile), and 'both'."""
        route = (route or "pc").strip().lower()
        if route not in ("pc", "phone", "both"):
            route = "pc"
        prev_route = self._audio_route
        self._audio_route = route

        if route == "pc":
            self._phone_active = False
            if reset_default:
                try:
                    from memory.config_manager import save_input_device, save_output_device
                    save_input_device("")
                    save_output_device("")
                    if prev_route == "pc":
                        self._on_audio_device_change()
                except Exception as e:
                    print(f"[AudioRoute] Reset default error: {e}")
            self.ui.write_log("SYS: 💻 Audio de VIERNES restaurado en la PC (Dispositivo predeterminado).")
        elif route == "phone":
            if not self._awake:
                self.wake(reason="audio móvil activado")
            self.ui.write_log("SYS: 📱 Audio de VIERNES transferido al Celular (Control Remoto).")
        elif route == "both":
            if not self._awake:
                self.wake(reason="audio compartido activado")
            self.ui.write_log("SYS: 🔊 Audio de VIERNES activo en PC + Celular simultáneamente.")

    async def _on_remote_voice_blob(self, audio_bytes: bytes, mime_type: str) -> None:
        """Handle recorded voice audio uploaded from the mobile Remote Control (works over plain HTTP too)."""
        if not audio_bytes or not self.session:
            return
        if not self._awake:
            self.wake(reason="voz desde Control Remoto")
        self._last_user_speech = time.monotonic()

        # Method 1: Decode to 16kHz mono int16 PCM via PyAV and stream into Gemini Live
        decoded_pcm = None
        try:
            import io
            import av
            container = av.open(io.BytesIO(audio_bytes))
            resampler = av.AudioResampler(format="s16", layout="mono", rate=SEND_SAMPLE_RATE)
            pcm_chunks = bytearray()
            for frame in container.decode(audio=0):
                for out_frame in resampler.resample(frame):
                    pcm_chunks.extend(bytes(out_frame.planes[0]))
            for out_frame in resampler.resample(None):
                pcm_chunks.extend(bytes(out_frame.planes[0]))
            container.close()
            if len(pcm_chunks) > 0:
                decoded_pcm = bytes(pcm_chunks)
        except Exception as e:
            print(f"[DashboardVoice] PyAV decode fallback: {e}")

        if decoded_pcm:
            # Stream PCM chunks + trailing silence so VAD triggers turn completion immediately
            step = 3200  # 100ms at 16kHz int16
            for i in range(0, len(decoded_pcm), step):
                await self.session.send_realtime_input(
                    audio=types.Blob(data=decoded_pcm[i:i + step], mime_type="audio/pcm")
                )
                await asyncio.sleep(0.015)
            # Send 600ms of silence so automatic activity detection closes the user turn
            silence = bytes(step)
            for _ in range(6):
                await self.session.send_realtime_input(
                    audio=types.Blob(data=silence, mime_type="audio/pcm")
                )
                await asyncio.sleep(0.02)
            return

        # Method 2: Direct inline_data audio turn to Gemini Live
        try:
            import base64 as _b64
            b64_audio = _b64.b64encode(audio_bytes).decode("ascii")
            clean_mime = (mime_type or "audio/webm").split(";")[0].strip()
            await self.session.send_client_content(
                turns={
                    "role": "user",
                    "parts": [
                        {"inline_data": {"mime_type": clean_mime, "data": b64_audio}},
                        {"text": "Responde en español a lo que acabo de decir en este audio."},
                    ],
                },
                turn_complete=True,
            )
        except Exception as e:
            print(f"[DashboardVoice] Error sending audio turn: {e}")

    def _on_remote_file_uploaded(self, file_path: str) -> None:
        """Called when the user uploads a file from the mobile Remote Control."""
        if not file_path or not Path(file_path).is_file():
            return
        self._current_uploaded_file = file_path
        p = Path(file_path)
        try:
            sz = p.stat().st_size
            size_str = f"{sz} B" if sz < 1024 else (f"{sz/1024:.1f} KB" if sz < 1024**2 else f"{sz/1024**2:.1f} MB")
        except Exception:
            size_str = ""
        if hasattr(self.ui, "set_uploaded_file"):
            self.ui.set_uploaded_file(file_path)
        self.ui.write_log(f"FILE: 📱 {p.name} ({size_str}) recibido desde Control Remoto")
        msg = (
            f"[FILE_UPLOADED] path={file_path} | name={p.name} | "
            f"type={p.suffix.lstrip('.')} | size={size_str} | "
            f"El usuario acaba de subir el archivo '{p.name}' ({size_str}) desde el Control Remoto móvil. "
            f"Confirma brevemente en español que recibiste el archivo '{p.name}' y pregúntale qué desea hacer con él."
        )
        self._on_text_command(msg)

    # ── dashboard command relay ─────────────────────────────────────────────

    async def _process_dashboard_commands(self) -> None:
        while True:
            try:
                text = await asyncio.wait_for(
                    self._dashboard._command_queue.get(), timeout=0.5
                )
                if not text:
                    continue
                # Wait up to 8s for session to become ready after a wake
                for _ in range(80):
                    if self.session:
                        break
                    await asyncio.sleep(0.1)
                if self.session:
                    text_clean = text.strip()
                    low = text_clean.lower()
                    self._sleep_pending = False
                    self._last_user_speech = time.monotonic()
                    self._last_user_query = text_clean

                    if _is_silence_command(text_clean):
                        self.ui.write_log(f"You: 📱 {text_clean}")
                        self.silence_and_mute(reason="comando 'Silencio' desde Control Remoto")
                        continue

                    sleep_phrases = ["duermete", "duérmete", "descansa", "a dormir", "ve a dormir", "modo reposo", "buenas noches", "sleep", "standby"]
                    if any(low == p or low.startswith(p + " ") for p in sleep_phrases):
                        self.ui.write_log(f"You: 📱 {text_clean}")
                        self._on_remote_sleep()
                        continue

                    # Always wake VIERNES if asleep when receiving a command from Remote Control
                    if not self._awake:
                        self.wake(reason="comando desde Control Remoto")

                    self.ui.write_log(f"You: 📱 {text_clean}")
                    self._session_log.append(f"User: {text_clean}")

                    wake_only = ["despierta", "wake", "despertar", "arriba"]
                    if low in wake_only:
                        await self.session.send_client_content(
                            turns={"role": "user", "parts": [{"text": "El usuario te acaba de despertar desde el Control Remoto móvil. Salúdalo brevemente en español y pregúntale en qué le puedes ayudar."}]},
                            turn_complete=True,
                        )
                        continue

                    await self.session.send_client_content(
                        turns={"role": "user", "parts": [{"text": text_clean}]},
                        turn_complete=True,
                    )
                else:
                    print(f"[Dashboard] Dropped command (no session): {text}")
            except asyncio.TimeoutError:
                pass
            except Exception as e:
                print(f"[Dashboard] Command error: {e}")
                await asyncio.sleep(0.5)

    # ── main loop ───────────────────────────────────────────────────────────

    async def run(self):
        self._loop = asyncio.get_event_loop()
        self._reconnect_event = asyncio.Event()

        # ── Wire the shared core services to the interface ───────────────────
        # The confirmation gate is useless without a way to ask, and a memory
        # trim is invisible without a way to say so. Both are bound once here
        # rather than passed down through every action signature.
        confirm_gate.bind(
            show = self.ui.show_confirm,
            hide = self.ui.hide_confirm,
            log  = self.ui.write_log,
        )
        set_trim_notifier(self.ui.write_log)

        # Tell the device picker the exact rates the streams open at, from the
        # constants that actually open them — so it can never list a device that
        # cannot be opened at them.
        audio_devices.configure(SEND_SAMPLE_RATE, RECEIVE_SAMPLE_RATE)

        # Enumerate audio devices off-thread. The settings drawer must never pay
        # for host-API enumeration on the Qt thread.
        audio_devices.prefetch()

        # Start dashboard (optional — needs: pip install fastapi "uvicorn[standard]" cryptography)
        try:
            from dashboard.server import DashboardServer
            self._dashboard = DashboardServer()
            self._dashboard.set_connect_callback(self._on_phone_connected)
            self._dashboard.set_wake_callback(self._on_remote_wake)
            self._dashboard.set_sleep_callback(self._on_remote_sleep)
            self._dashboard.set_audio_route_callback(self._on_audio_route_change)
            self._dashboard.set_voice_blob_callback(self._on_remote_voice_blob)
            self._dashboard.set_file_upload_callback(self._on_remote_file_uploaded)
            asyncio.create_task(self._dashboard.serve())
            # Runs for the whole lifetime, not just inside an active session
            asyncio.create_task(self._process_dashboard_commands())
        except Exception as e:
            print(f"[Dashboard] Disabled: {e}")
            self._dashboard = None

        while True:
            try:
                print("[VIERNES] Connecting...")
                self.ui.set_state("THINKING")
                # Pick the rung to open the conversation on. A model resting
                # off a quota limit is skipped; the name is published back to
                # LIVE_MODEL so plugins follow whatever is actually in use.
                global LIVE_MODEL
                LIVE_MODEL = _gemini.live_model()
                live_model = LIVE_MODEL
                print(f"[VIERNES] Live model: {live_model}")

                _resumed_with = self._resume_handle is not None
                config = self._build_config()

                # Fresh client on every reconnect — avoids stale HTTP session state
                # v1alpha carries proactive audio; if it gets rejected we fall
                # back to v1beta.
                client = genai.Client(
                    api_key=_get_api_key(),
                    http_options={"api_version": "v1alpha" if self._enhanced_live else "v1beta"}
                )

                async with (
                    client.aio.live.connect(model=live_model, config=config) as session,
                    asyncio.TaskGroup() as tg,
                ):
                    self.session          = session
                    self.audio_in_queue   = asyncio.Queue()
                    self.out_queue        = asyncio.Queue(maxsize=200)
                    self._turn_done_event = asyncio.Event()

                    # Reset transient state that must not carry over from a previous session
                    self._pending_vision       = None
                    self._vision_cam_active    = False
                    self._vision_close_pending = False
                    self._vision_busy          = False
                    self._vision_last_time     = 0.0
                    self._interrupted          = False

                    print("[VIERNES] Connected.")
                    if _resumed_with:
                        # Say it plainly: the difference between "it reconnected"
                        # and "it reconnected and still knows what we were doing"
                        # is the whole point, and it is invisible otherwise.
                        self.ui.write_log("SYS: Reconnected — conversation restored.")

                    # Only force SLEEPING on the very first startup connect if wake_word is enabled.
                    # On reconnects/resumptions, preserve self._awake so an active conversation
                    # or remote wake is never interrupted by a session reconnect.
                    if not self._first_connect_done:
                        self._first_connect_done = True
                        if self._wake_enabled:
                            self._ensure_wake_detector()
                            self._awake = False
                        else:
                            self._awake = True

                    if not self._awake:
                        self._ensure_wake_detector()
                        self.ui.set_state("SLEEPING")
                        self.ui.write_log(f"SYS: {self._asst_name.upper()} online — sleeping. Di '{self._asst_name}' o usa el botón WAKE NOW.")
                    else:
                        if self.ui.muted:
                            self.ui.set_state("MUTED")
                        else:
                            self.ui.set_state("LISTENING")
                        if not _resumed_with:
                            self.ui.write_log(f"SYS: {self._asst_name.upper()} online.")

                    if self._dashboard:
                        self._dashboard._awake_state = self._awake
                        await self._dashboard.broadcast({
                            "type": "status",
                            "state": "active" if self._awake else "sleeping",
                            "awake": self._awake,
                        })

                    self._reconnect_event.clear()  # ignore requests from before this session
                    tg.create_task(self._watch_reconnect())
                    tg.create_task(self._send_realtime())
                    tg.create_task(self._listen_audio())
                    tg.create_task(self._receive_audio())
                    tg.create_task(self._play_audio())
                    tg.create_task(self._run_system_monitor())
                    tg.create_task(self._run_communication_monitor())
                    tg.create_task(self._run_background_monitor())
                    tg.create_task(self._run_proactive_mode())
                    tg.create_task(self._run_sleep_watch())
                    if self._dashboard:
                        tg.create_task(self._relay_phone_audio())

                    # Morning briefing — fires once per process launch (if enabled).
                    # Skipped in wake-word mode: it comes up asleep, and a briefing
                    # would mean talking while "asleep".
                    if not self._briefing_sent and get_brief_enabled() and self._awake:
                        self._briefing_sent = True
                        tg.create_task(self._send_startup_briefing())

            except KeyboardInterrupt:
                raise
            except SystemExit:
                raise
            except BaseException as e:
                # Catches both Exception and BaseExceptionGroup (Python 3.11+
                # TaskGroup raises BaseExceptionGroup when tasks are cancelled
                # externally, which `except Exception` would miss, letting the
                # exception escape the while-loop and causing asyncio.run() to
                # start shutdown — resulting in "executor after shutdown" errors).
                # Voluntary reconnect (voice change) — not an error. Rebuild the
                # session immediately with no backoff and no scary logs.
                if _is_reconnect_signal(e):
                    print("[VIERNES] Voluntary reconnect requested.")
                    if not _keep_context_of(e):
                        # A deliberate clean slate (voice change) — drop the
                        # handle so the next connect really does start empty.
                        self._resume_handle = None
                    self._conn_backoff = 0
                    continue

                # A resumption handle the server will not accept — expired, or
                # belonging to a session it has since dropped. Without this, the
                # same dead handle would be replayed on every retry and the
                # assistant would never come back at all: the feature meant to
                # survive a reconnect would be the thing preventing one. Drop it
                # once and let the next attempt start clean.
                if _resumed_with and (
                    "resum" in str(e).lower()
                    or "handle" in str(e).lower()
                    or "INVALID_ARGUMENT" in str(e)
                    or "NOT_FOUND" in str(e)
                ):
                    print("[VIERNES] 🔗 Resumption handle rejected — starting a fresh session")
                    self.ui.write_log("SYS: Could not restore the conversation — starting fresh.")
                    self._resume_handle = None
                    self._conn_backoff = 0
                    continue

                err_str = str(e)
                print(f"[VIERNES] Error ({type(e).__name__}): {e}")
                traceback.print_exc()

                # Out of quota, or this model is not available to this key —
                # step down the ladder and reconnect straight away. This is the
                # difference between "VIERNES is quieter today" and "VIERNES does
                # not start today": one model means one daily limit, and the
                # limit always arrives mid-conversation.
                if _gemini.note_live_failure(live_model, err_str):
                    nxt = _gemini.live_model()
                    self.ui.write_log(
                        f"SYS: Switching to {nxt.split('/')[-1]} — the previous "
                        f"model is out of quota."
                        if nxt != live_model else
                        "SYS: Every live model is rate-limited — retrying.")
                    self._conn_backoff = 0 if nxt != live_model else 15
                    if nxt == live_model:
                        await asyncio.sleep(self._conn_backoff)
                    continue

                # Turn-taking / media / thinking knobs rejected by the server
                # (preview API drift) — drop them first, because they are the
                # newest fields and the cheapest to lose. Proactive audio is
                # tried again on the next pass if the error persists.
                if self._tuned_live and (
                    "INVALID_ARGUMENT" in err_str
                    or "Unknown name" in err_str
                    or "unexpected keyword" in err_str
                    or "realtime_input" in err_str.lower()
                    or "media_resolution" in err_str.lower()
                    or "thinking" in err_str.lower()
                ):
                    self._tuned_live = False
                    print("[VIERNES] Live tuning rejected — reconnecting without it.")
                    continue

                # Proactive audio rejected by the server (preview API drift) —
                # drop it and reconnect with the plain config.
                if self._enhanced_live and (
                    "INVALID_ARGUMENT" in err_str
                    or "proactiv" in err_str.lower()
                    or "Unknown name" in err_str
                    or "unexpected keyword" in err_str
                ):
                    self._enhanced_live = False
                    self.ui.write_log(
                        "SYS: Proactive audio unavailable — reconnecting without it."
                    )
                    continue

                # Invalid API key — stop hammering the API, prompt re-configuration
                if "API key not valid" in err_str or "API_KEY_INVALID" in err_str:
                    self.ui.write_log("ERR: API key invalid — please re-enter your key.")
                    self.ui.set_state("SLEEPING")
                    self.ui.prompt_reconfig()
                    while not self.ui._win._ready:
                        await asyncio.sleep(1)
                    print("[VIERNES] New API key saved — reconnecting...")
                    _conn_backoff = 3
                    continue

                # Network / timeout errors — log clearly and back off
                is_net_err = any(k in err_str for k in (
                    "TimeoutError", "timed out", "getaddrinfo", "CancelledError",
                    "ConnectionRefusedError", "OSError", "Cannot connect",
                ))
                if is_net_err:
                    _conn_backoff = min(getattr(self, "_conn_backoff", 3) * 2, 60)
                    self._conn_backoff = _conn_backoff
                    self.ui.write_log(
                        f"NET: Connection failed — retrying in {_conn_backoff}s. "
                        "(a VPN may be required)"
                    )
                else:
                    self._conn_backoff = 3
            finally:
                self.session = None
                # Only save if there was a real conversation (≥3 turns)
                if len(self._session_log) >= 3:
                    asyncio.create_task(self._save_session_summary())

            self.set_speaking(False)
            self.ui.set_state("SLEEPING")

            if self._dashboard:
                await self._dashboard.broadcast({"type": "status", "state": "sleeping"})

            delay = getattr(self, "_conn_backoff", 3)
            print(f"[VIERNES] Reconnecting in {delay}s...")
            await asyncio.sleep(delay)

ViernesLive = ViernesLive

def main():
    ui = ViernesUI("face.png")

    def runner():
        ui.wait_for_api_key()
        viernes = ViernesLive(ui)
        try:
            asyncio.run(viernes.run())
        except KeyboardInterrupt:
            print("\n🔴 Shutting down...")
        except Exception as exc:
            traceback.print_exc()
            ui.write_log(f"SYS: Error en motor principal: {exc}")

    threading.Thread(target=runner, daemon=True).start()
    ui.root.mainloop()

if __name__ == "__main__":
    main()