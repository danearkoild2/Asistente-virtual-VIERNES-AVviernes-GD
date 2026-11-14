import json
import sys
from pathlib import Path

def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

BASE_DIR    = get_base_dir()
CONFIG_DIR  = BASE_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "api_keys.json"

def ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def config_exists() -> bool:
    return CONFIG_FILE.exists()

def save_api_keys(gemini_api_key: str) -> None:
    ensure_config_dir()

    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}

    data["gemini_api_key"] = gemini_api_key.strip()

    CONFIG_FILE.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )

def load_api_keys() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Failed to load api_keys.json: {e}")
        return {}

def get_gemini_key() -> str | None:
    return load_api_keys().get("gemini_api_key")

def is_configured() -> bool:
    key = get_gemini_key()
    return bool(key and len(key) > 15)


def get_serpapi_key() -> str:
    """Return the configured SerpApi key, from config or SERPAPI_API_KEY environment variable."""
    import os
    env_key = os.environ.get("SERPAPI_API_KEY", "").strip()
    if env_key:
        return env_key
    return load_api_keys().get("serpapi_api_key", "").strip()


def save_serpapi_key(key: str) -> None:
    """Persist SerpApi API key safely to config."""
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data["serpapi_api_key"] = key.strip()
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def get_assistant_name() -> str:
    """Return the configured assistant name, or 'Viernes' if not set."""
    return load_api_keys().get("assistant_name", "Viernes") or "Viernes"


def get_user_name() -> str:
    """Return the configured user name for addressing."""
    return load_api_keys().get("user_name", "")


def save_assistant_config(assistant_name: str, user_name: str) -> None:
    """Persist assistant name and user name to config."""
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data["assistant_name"] = assistant_name.strip() or "Viernes"
    data["user_name"] = user_name.strip()
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


# ── Assistant voice ──────────────────────────────────────────────────────────
# Gemini Live prebuilt native voices (Colección oficial completa de 30 voces).
# Names are proper nouns — identical in every language and API endpoint.
AVAILABLE_VOICES: list[str] = [
    # Top populares / insignia
    "Aoede",
    "Kore",
    "Puck",
    "Charon",
    "Fenrir",
    "Leda",
    "Zephyr",
    "Orus",
    # Colección completa de voces nativas Gemini Live
    "Achernar",
    "Achird",
    "Algieba",
    "Algenib",
    "Alnilam",
    "Autonoe",
    "Callirrhoe",
    "Despina",
    "Enceladus",
    "Erinome",
    "Gacrux",
    "Iapetus",
    "Laomedeia",
    "Pulcherrima",
    "Rasalgethi",
    "Sadachbia",
    "Sadaltager",
    "Schedar",
    "Sulafat",
    "Umbriel",
    "Vindemiatrix",
    "Zubenelgenubi",
]

DEFAULT_VOICE = "Aoede"

# Metadatos descriptivos de cada voz: (Género, Tono/Personalidad)
VOICE_METADATA: dict[str, tuple[str, str]] = {
    "Aoede": ("Femenina", "Fresca, relajada y natural (Breezy)"),
    "Kore": ("Femenina", "Firme, segura y elegante"),
    "Puck": ("Masculina", "Vivaz, alegre y confiada (Upbeat)"),
    "Charon": ("Masculina", "Informativa, profunda y profesional"),
    "Fenrir": ("Masculina", "Enérgica, apasionada y entusiasta"),
    "Leda": ("Femenina", "Juvenil, brillante y dinámica"),
    "Zephyr": ("Femenina", "Brillante, ligera y aireada"),
    "Orus": ("Masculina", "Serena, sobria y calmada"),
    "Achernar": ("Femenina", "Suave, cálida y envolvente"),
    "Achird": ("Masculina", "Equilibrada, amistosa y neutral"),
    "Algieba": ("Masculina", "Fluida, melódica y suave"),
    "Algenib": ("Masculina", "Grave, texturizada y madura"),
    "Alnilam": ("Masculina", "Firme, imponente y segura"),
    "Autonoe": ("Femenina", "Alegre, optimista y radiante"),
    "Callirrhoe": ("Femenina", "Amigable, cercana y relajada"),
    "Despina": ("Femenina", "Delicada, tersa y dulce"),
    "Enceladus": ("Masculina", "Susurrada, suave y tranquila"),
    "Erinome": ("Femenina", "Clara, elocuente y articulada"),
    "Gacrux": ("Masculina", "Madura, profunda y constante"),
    "Iapetus": ("Masculina", "Nítida, limpia y académica"),
    "Laomedeia": ("Femenina", "Positiva, risueña y animada"),
    "Pulcherrima": ("Femenina", "Rica, armónica y sofisticada"),
    "Rasalgethi": ("Masculina", "Narrador clásico, sobria y sólida"),
    "Sadachbia": ("Femenina", "Conversacional, fluida y dulce"),
    "Sadaltager": ("Masculina", "Directa, asertiva y ejecutiva"),
    "Schedar": ("Masculina", "Estable, neutra y balanceada"),
    "Sulafat": ("Femenina", "Clara, brillante y expresiva"),
    "Umbriel": ("Masculina", "Distendida, cómoda y amena"),
    "Vindemiatrix": ("Femenina", "Expresiva, teatral y versátil"),
    "Zubenelgenubi": ("Masculina", "Resonante, solemne y profunda"),
}


def get_voice() -> str:
    """Return the configured Live voice, falling back to the default if unset
    or if the stored value is not a voice we recognise."""
    raw = (load_api_keys().get("voice_name") or "").strip()
    if not raw:
        return DEFAULT_VOICE
    # Case-insensitive match check
    for v in AVAILABLE_VOICES:
        if v.lower() == raw.lower():
            return v
    return DEFAULT_VOICE


def save_voice(voice_name: str) -> None:
    """Persist the chosen Live voice. Unknown names collapse to the default so a
    bad value can never reach the API and break the session."""
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    target = DEFAULT_VOICE
    raw = (voice_name or "").strip()
    for v in AVAILABLE_VOICES:
        if v.lower() == raw.lower():
            target = v
            break
    data["voice_name"] = target
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


# ── ElevenLabs Premade & Multilingual Voices (Instant Flash v2.5 compatible) ──
ELEVENLABS_PRESET_VOICES: dict[str, tuple[str, str, str]] = {
    "21m00Tcm4TlvDq8ikWAM": ("Rachel", "Femenina", "Ejecutiva, clara, serena y profesional"),
    "EXAVITQu4vr4xnSDxMaL": ("Sarah", "Femenina", "Suave, cálida, expresiva y muy natural"),
    "FGY2WhTYpPnrIDTdsKH5": ("Laura", "Femenina", "Animada, entusiasta y cercana"),
    "9BWtsMINqrJLrRacOk9x": ("Aria", "Femenina", "Expresiva, moderna y conversacional"),
    "cgSgspJ2msm6clMCkdW9": ("Jessica", "Femenina", "Joven, brillante, dinámica y fluida"),
    "XrExE9yKIg1WjnnlVkGX": ("Matilda", "Femenina", "Sofisticada, amable y articulada"),
    "XB0fDUnXU5powFXDhCwa": ("Charlotte", "Femenina", "Elegante, cinematográfica y envolvente"),
    "Xb7hH8MSUJpSbSDYk0k2": ("Alice", "Femenina", "Firme, segura e informativa"),
    "pFZP5JQG7iQjIQuC4Bku": ("Lily", "Femenina", "Aterciopelada, calmada y dulce"),
    "AZnzlk1XvdvUeBnXmlld": ("Domi", "Femenina", "Energética, directa y con carácter"),
    "pNInz6obpgDQGcFmaJgB": ("Adam", "Masculina", "Profunda, resonante y cinematográfica"),
    "ErXwobaYiN019PkySvjV": ("Antoni", "Masculina", "Ejecutiva, equilibrada y natural"),
    "TxGEqnHWrfWFTfGW9XjX": ("Josh", "Masculina", "Joven, profunda y conversacional"),
    "nPczCjzI2devNBz1zQrb": ("Brian", "Masculina", "Grave, serena y autoritativa"),
    "onwK4e9ZLuTAKqWW03F9": ("Daniel", "Masculina", "Clásica tipo JARVIS, formal y precisa"),
    "cjVigY5qzO86Huf0OWal": ("Eric", "Masculina", "Amigable, fluida y natural"),
}

# ── Microsoft Edge Neural Voices (100% Free, Ultra-Fast Streaming, Distinct Accents) ──
EDGE_SPANISH_VOICES: dict[str, tuple[str, str, str]] = {
    "es-MX-DaliaNeural":    ("Dalia (México)", "Femenina", "Cálida, natural y ejecutiva mexicana"),
    "es-MX-BeatrizNeural":  ("Beatriz (México)", "Femenina", "Joven, suave y conversacional"),
    "es-MX-CandelaNeural":  ("Candela (México)", "Femenina", "Brillante, expresiva y dinámica"),
    "es-MX-CarlotaNeural":  ("Carlota (México)", "Femenina", "Serena, clara y profesional"),
    "es-MX-MarinaNeural":   ("Marina (México)", "Femenina", "Fresca, amable y ligera"),
    "es-CO-SalomeNeural":   ("Salomé (Colombia)", "Femenina", "Acento colombiano melodioso y muy natural"),
    "es-AR-ElenaNeural":    ("Elena (Argentina)", "Femenina", "Acento argentino fluido y carismático"),
    "es-ES-ElviraNeural":   ("Elvira (España)", "Femenina", "Acento español peninsular nítido y elegante"),
    "es-ES-AbrilNeural":    ("Abril (España)", "Femenina", "Joven, moderna y expresiva (España)"),
    "es-CL-CatalinaNeural": ("Catalina (Chile)", "Femenina", "Clara, ágil y ejecutiva"),
    "es-PE-CamilaNeural":   ("Camila (Perú)", "Femenina", "Neutra latinoamericana, dulce y pausada"),
    "es-VE-PaolaNeural":    ("Paola (Venezuela)", "Femenina", "Cálida, alegre y cercana"),
    "es-US-PalomaNeural":   ("Paloma (Latino Neutro)", "Femenina", "Estándar internacional de asistente IA"),
    "es-MX-JorgeNeural":    ("Jorge (México)", "Masculina", "Voz masculina mexicana clara y firme"),
    "es-CO-GonzaloNeural":  ("Gonzalo (Colombia)", "Masculina", "Voz masculina colombiana cálida y ejecutiva"),
    "es-AR-TomasNeural":    ("Tomás (Argentina)", "Masculina", "Voz masculina argentina natural"),
    "es-ES-AlvaroNeural":   ("Álvaro (España)", "Masculina", "Voz masculina española profunda estilo estudio"),
}

# ── Gemini Live Acoustic Voice Styles (Modulates timbre/cadence via native audio prompt) ──
GEMINI_VOICE_STYLES: dict[str, tuple[str, str]] = {
    "default":     ("Estándar Natural", ""),
    "ejecutiva":   ("Ejecutiva VIERNES (Rápida y Precisa)", "MODULACIÓN ACÚSTICA DE VOZ: Habla con una cadencia ágil, ejecutiva, segura, nítida y ligeramente rápida, al estilo de una inteligencia artificial avanzada de alto nivel."),
    "calida":      ("Cálida, Dulce y Cercana", "MODULACIÓN ACÚSTICA DE VOZ: Habla con un timbre especialmente cálido, suave, empático, melodioso y muy cercano, con inflexiones humanas naturales."),
    "juvenil":     ("Juvenil y Dinámica", "MODULACIÓN ACÚSTICA DE VOZ: Habla con un tono juvenil, brillante, energético, fresco y expresivo."),
    "cinematica":  ("Profunda y Cinematográfica", "MODULACIÓN ACÚSTICA DE VOZ: Habla con una voz pausada, profunda, serena, con aplomo y resonancia cinematográfica."),
    "susurro":     ("Íntima / Suave (Nocturna)", "MODULACIÓN ACÚSTICA DE VOZ: Habla en un tono muy suave, relajado, calmado y ligeramente susurrado, ideal para ambientes silenciosos."),
}


def get_tts_engine() -> str:
    """Return tts_engine ('gemini', 'elevenlabs', 'edgetts', or 'coqui_xtts'). Defaults to 'gemini'."""
    val = load_api_keys().get("tts_engine", "gemini").lower().strip()
    if val in ("elevenlabs", "edgetts", "coqui_xtts", "gemini"):
        return val
    return "gemini"


def save_tts_engine(engine: str) -> None:
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    eng = (engine or "gemini").lower().strip()
    data["tts_engine"] = eng if eng in ("elevenlabs", "edgetts", "coqui_xtts", "gemini") else "gemini"
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


COQUI_XTTS_SPEAKERS: list[str] = [
    "Ana Florence",
    "Claribel Dervla",
    "Daisy Studious",
    "Sofia Hellen",
    "Tammy Grit",
    "Andrew Chipper",
    "Dionisio Schuyler",
    "Damien Black",
    "Gilberto Mathias",
    "Abrahan Mack",
]


def get_coqui_config() -> dict:
    cfg = load_api_keys()
    return {
        "speaker": (cfg.get("coqui_speaker") or "Ana Florence").strip(),
        "speaker_wav": (cfg.get("coqui_speaker_wav") or "").strip(),
        "language": (cfg.get("coqui_language") or "es").strip() or "es",
    }


def save_coqui_config(speaker: str, speaker_wav: str = "", language: str = "es") -> None:
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data["coqui_speaker"] = (speaker or "Ana Florence").strip()
    data["coqui_speaker_wav"] = (speaker_wav or "").strip()
    data["coqui_language"] = (language or "es").strip() or "es"
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def get_elevenlabs_config() -> dict:
    cfg = load_api_keys()
    return {
        "api_key": cfg.get("elevenlabs_api_key", ""),
        "voice_id": cfg.get("elevenlabs_voice_id", "21m00Tcm4TlvDq8ikWAM"),
    }


def save_elevenlabs_config(api_key: str, voice_id: str) -> None:
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data["elevenlabs_api_key"] = api_key.strip()
    data["elevenlabs_voice_id"] = voice_id.strip() or "21m00Tcm4TlvDq8ikWAM"
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def get_edge_voice() -> str:
    cfg = load_api_keys()
    v = (cfg.get("edge_voice") or "es-MX-DaliaNeural").strip()
    return v if v in EDGE_SPANISH_VOICES else "es-MX-DaliaNeural"


def save_edge_voice(voice: str) -> None:
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data["edge_voice"] = (voice or "es-MX-DaliaNeural").strip()
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def get_voice_style() -> str:
    cfg = load_api_keys()
    st = (cfg.get("voice_style") or "default").strip()
    return st if st in GEMINI_VOICE_STYLES else "default"


def save_voice_style(style: str) -> None:
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data["voice_style"] = (style or "default").strip()
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def get_wake_word_enabled() -> bool:
    """Whether local wake-word gating is on (assistant sleeps until 'Hey Viernes')."""
    return load_api_keys().get("wake_word_enabled", False)


def save_wake_word_enabled(enabled: bool) -> None:
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data["wake_word_enabled"] = bool(enabled)
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def get_push_to_talk_enabled() -> bool:
    """Hold-a-key-to-speak. When on, the mic is closed unless the chord is held."""
    return load_api_keys().get("push_to_talk_enabled", False)


def save_push_to_talk_enabled(enabled: bool) -> None:
    _save_flag("push_to_talk_enabled", enabled)


HUD_STYLES = ("vrm_3d", "edith_live2d", "face", "core")


def get_hud_style() -> str:
    """Which centrepiece the HUD draws:
    - 'edith_live2d': Edith Live2D Cubism Real-Time Pro Avatar (ultra-realistic physics, gaze tracking, lip-sync)
    - 'face': Viernes 2D frame-animated avatar (Avatar 1)
    - 'core': Holographic reactor core / mesh face (Avatar 2)
    """
    raw = load_api_keys()
    if "hud_style" not in raw:
        return "edith_live2d"
    v = str(raw.get("hud_style", "edith_live2d")).strip().lower()
    return v if v in HUD_STYLES else "edith_live2d"


def save_hud_style(style: str) -> None:
    s = str(style or "").strip().lower()
    _save_flag("hud_style", s if s in HUD_STYLES else "edith_live2d")

def get_vrm_model() -> str:
    """Nombre del archivo VRM activo en core/vrm/models (por defecto edithof.vrm)."""
    return str(load_api_keys().get("vrm_model", "edithof.vrm")).strip()


def save_vrm_model(model_name: str) -> None:
    _save_flag("vrm_model", str(model_name or "edithof.vrm").strip())



def get_edith_autonomy_enabled() -> bool:
    """Whether Edith's real-time autonomous behaviors, glance wandering, and idle actions are active."""
    return bool(load_api_keys().get("edith_autonomy_enabled", True))


def save_edith_autonomy_enabled(enabled: bool) -> None:
    _save_flag("edith_autonomy_enabled", bool(enabled))


def get_auto_animations_enabled() -> bool:
    """Whether periodic autonomous expressive avatar animations are enabled."""
    return bool(load_api_keys().get("auto_animations_enabled", True))


def save_auto_animations_enabled(enabled: bool) -> None:
    _save_flag("auto_animations_enabled", bool(enabled))


def get_edith_spontaneity_level() -> float:
    """Frequency multiplier for Edith's spontaneous actions (0.0 to 2.0, default 1.0)."""
    try:
        return float(load_api_keys().get("edith_spontaneity_level", 1.0))
    except Exception:
        return 1.0


def save_edith_spontaneity_level(level: float) -> None:
    _save_flag("edith_spontaneity_level", max(0.0, min(2.0, float(level))))


def get_edith_mood() -> str:
    """Edith's personality mood: 'cheerful', 'calm', 'playful', 'thoughtful', 'tired'."""
    raw = str(load_api_keys().get("edith_mood", "cheerful")).strip().lower()
    return raw if raw in ("cheerful", "calm", "playful", "thoughtful", "tired") else "cheerful"


def save_edith_mood(mood: str) -> None:
    m = str(mood or "cheerful").strip().lower()
    if m not in ("cheerful", "calm", "playful", "thoughtful", "tired"):
        m = "cheerful"
    _save_flag("edith_mood", m)


def get_live2d_skin() -> str:
    """Return selected Live2D skin/model name, defaulting to 'Edith'."""
    return str(load_api_keys().get("live2d_skin", "Edith")).strip()


def save_live2d_skin(skin_name: str) -> None:
    """Persist chosen Live2D skin name."""
    _save_flag("live2d_skin", str(skin_name or "Edith").strip())


# ── Live-session tuning ──────────────────────────────────────────────────────
# Everything here is optional and has a working default, so an untouched
# config behaves exactly like a configured one. Each value is also a way out:
# if a future model dislikes one of these, set it back and nothing else changes.

def get_thinking_enabled() -> bool:
    """Whether the Live model may spend tokens thinking before it answers.

    Off by default. A voice assistant is judged on how fast it starts talking,
    and the reasoning that actually needs deliberation in this app is delegated
    to the planning tools, which run on a separate non-Live model.
    """
    return bool(load_api_keys().get("thinking_enabled", False))


def save_thinking_enabled(enabled: bool) -> None:
    _save_flag("thinking_enabled", enabled)


def get_turn_tuning() -> dict:
    """How eagerly the server decides you have stopped speaking.

    OFF by default, and that default was earned. Cutting turns shorter looks
    like a free speed win and is not: proactive audio has to judge whether an
    utterance was even addressed to the assistant, and a turn clipped early
    gives it less to judge, so it stays quiet — and the reply to your first
    sentence only arrives once your second one has given it enough context.
    That reads as the assistant being a turn behind, which is far worse than
    the fraction of a second the tuning saves.

    Turn it on with "turn_tuning": {"enabled": true} if your own microphone and
    speaking pace suit it. `silence_ms` is the one that is felt: the pause the
    server sits through before accepting your turn is over.
    """
    cfg = load_api_keys().get("turn_tuning")
    cfg = cfg if isinstance(cfg, dict) else {}

    def _int(key, default, lo, hi):
        try:
            return max(lo, min(hi, int(cfg.get(key, default))))
        except (TypeError, ValueError):
            return default

    return {
        "enabled":    bool(cfg.get("enabled", False)),
        "silence_ms": _int("silence_ms", 550, 200, 3000),
        "prefix_ms":  _int("prefix_ms", 150, 0, 1000),
        # "high" = quicker to decide speech has ended.
        "end_sensitivity":   str(cfg.get("end_sensitivity", "high")).lower(),
        "start_sensitivity": str(cfg.get("start_sensitivity", "default")).lower(),
    }


def save_turn_tuning(values: dict) -> None:
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    cur = data.get("turn_tuning")
    cur = dict(cur) if isinstance(cur, dict) else {}
    cur.update(values or {})
    data["turn_tuning"] = cur
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def get_proactive_audio_enabled() -> bool:
    """Whether the model gets to decide an utterance was not aimed at it and
    stay quiet.

    On by default — it is what stops the assistant answering the room. But it
    is also the first thing to switch off if replies ever seem to arrive a turn
    late: what looks like lag is usually the model having judged your previous
    sentence as not addressed to it, and only changing its mind once the next
    one arrives.
    """
    return bool(load_api_keys().get("proactive_audio", True))


def save_proactive_audio_enabled(enabled: bool) -> None:
    _save_flag("proactive_audio", enabled)


MEDIA_RESOLUTIONS = ("default", "low", "medium", "high")


def get_media_resolution() -> str:
    """How finely the model tokenises the screenshots and camera frames it is
    sent. 'medium' keeps on-screen text readable at a fraction of the tokens a
    full-resolution frame costs; 'low' is cheaper still but starts losing small
    text, which is most of what screen captures are for."""
    v = str(load_api_keys().get("media_resolution", "medium")).strip().lower()
    return v if v in MEDIA_RESOLUTIONS else "medium"


def save_media_resolution(value: str) -> None:
    v = str(value or "").strip().lower()
    _save_flag("media_resolution", v if v in MEDIA_RESOLUTIONS else "medium")


def _save_flag(key: str, value) -> None:
    """Read-modify-write one key without disturbing the rest of the config."""
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data[key] = bool(value) if isinstance(value, bool) else value
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def get_brief_enabled() -> bool:
    return load_api_keys().get("morning_brief_enabled", True)


def save_brief_enabled(enabled: bool) -> None:
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data["morning_brief_enabled"] = enabled
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


# ── Audio devices ────────────────────────────────────────────────────────────
# Stored as device NAMES, not sounddevice indices. Indices shift every time a
# USB device is plugged in or removed, so a saved index silently starts pointing
# at a different microphone. The empty string means "system default", which is
# both the factory setting and what an unresolvable saved device falls back to —
# so unplugging a headset degrades to the built-in speakers instead of crashing.

def _patch_config(**fields) -> None:
    """Read-modify-write one or more keys in api_keys.json.

    Every setter in this file open-coded this. Collapsing it here means a new
    setting is one line, and there is one place where a corrupt config file is
    handled instead of nine."""
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    data.update(fields)
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def get_input_device() -> str:
    """Microphone device name, or '' for the system default."""
    return (load_api_keys().get("input_device", "") or "").strip()


def save_input_device(name: str) -> None:
    _patch_config(input_device=(name or "").strip())


def get_output_device() -> str:
    """Speaker device name, or '' for the system default."""
    return (load_api_keys().get("output_device", "") or "").strip()


def save_output_device(name: str) -> None:
    _patch_config(output_device=(name or "").strip())


def get_plugin_enabled(plugin_name: str) -> bool:
    """Plugins are enabled by default the moment they're discovered (opt-out model)."""
    return load_api_keys().get("plugins_enabled", {}).get(plugin_name, True)


# ── Per-plugin settings ("tokens" / connection details) ───────────────────────
# Generic store so a plugin can declare its own config fields (PLUGIN_SETTINGS)
# and the settings UI renders + persists them WITHOUT any core edit — keeping the
# drop-in model intact. Values live under plugin_config[<namespace>][<key>].
# A namespace defaults to the plugin name, but a suite of plugins (e.g. the
# several printer plugins) can share ONE namespace.
def get_plugin_config(namespace: str) -> dict:
    """All stored values for a namespace (empty dict if none set yet)."""
    cfg = load_api_keys().get("plugin_config")
    val = cfg.get(namespace) if isinstance(cfg, dict) else None
    return dict(val) if isinstance(val, dict) else {}


def get_plugin_setting(namespace: str, key: str, default=None):
    """A single value from a namespace, or `default` if unset."""
    return get_plugin_config(namespace).get(key, default)


def save_plugin_config(namespace: str, values: dict) -> None:
    """Merge `values` into a namespace's stored config (read-modify-write, like
    every other helper here). Only the provided keys are touched."""
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    pc = data.get("plugin_config")
    if not isinstance(pc, dict):
        pc = {}
    cur = pc.get(namespace)
    if not isinstance(cur, dict):
        cur = {}
    cur.update(values)
    pc[namespace] = cur
    data["plugin_config"] = pc
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def save_plugin_enabled(plugin_name: str, enabled: bool) -> None:
    ensure_config_dir()
    data: dict = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    plugins_cfg = data.get("plugins_enabled")
    if not isinstance(plugins_cfg, dict):
        plugins_cfg = {}
    plugins_cfg[plugin_name] = enabled
    data["plugins_enabled"] = plugins_cfg
    CONFIG_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")


def get_virustotal_key() -> str:
    """Return stored VirusTotal API key."""
    return (load_api_keys().get("virustotal_api_key", "") or "").strip()


def save_virustotal_key(key: str) -> None:
    """Persist VirusTotal API key."""
    _patch_config(virustotal_api_key=key.strip())


def get_weather_key() -> str:
    """Return stored WeatherAPI key."""
    return (load_api_keys().get("weather_api_key", "") or "").strip()


def save_weather_key(key: str) -> None:
    """Persist WeatherAPI key."""
    _patch_config(weather_api_key=key.strip())


def get_spotify_config() -> dict:
    """Return Spotify client ID and client secret."""
    cfg = load_api_keys()
    return {
        "client_id": (cfg.get("spotify_client_id", "") or "").strip(),
        "client_secret": (cfg.get("spotify_client_secret", "") or "").strip()
    }


def save_spotify_config(client_id: str, client_secret: str) -> None:
    """Persist Spotify client credentials."""
    _patch_config(
        spotify_client_id=client_id.strip(),
        spotify_client_secret=client_secret.strip()
    )


def save_all_api_keys(keys_dict: dict) -> None:
    """Batch save multiple API keys and credentials."""
    _patch_config(**keys_dict)
