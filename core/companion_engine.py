"""
Native OpenAmika Companion Engine (inspired by zeekk0/OpenAmika) for VIERNES.

Provides:
- Persistent Affinity & Relationship Progression (levels, tiers, interaction
  streaks, milestones) stored in memory/openamika_state.json.
- Dynamic Emotional State Machine (mood, energy, valence, arousal) with
  natural time decay and Live2D/VRM expression + gesture mapping.
- Interactive Companion Reactions (headpat, poke, compliment, cheer, sleep, wake).
- Flexible Secondary Brain Bridge: local Ollama (/api/chat) and OpenRouter
  (/v1/chat/completions) with companion mood/affinity context.
"""
from __future__ import annotations

import json
import threading
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional
from urllib.request import Request, urlopen

BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = BASE_DIR / "memory"
CONFIG_DIR = BASE_DIR / "config"
STATE_FILE = MEMORY_DIR / "openamika_state.json"
API_KEYS_FILE = CONFIG_DIR / "api_keys.json"

AFFINITY_TIERS = [
    (0, "Desconocido"),
    (50, "Conocido"),
    (150, "Amigo"),
    (350, "Buen Amigo"),
    (650, "Compañero Cercano"),
    (900, "Vínculo Inseparable"),
]

MOOD_TO_AVATAR: dict[str, tuple[str, str]] = {
    "neutral": ("neutral", "IDLE"),
    "happy": ("happy", "HAPPY_JUMP"),
    "playful": ("playful", "WINK"),
    "affectionate": ("happy", "HEAD_TILT"),
    "curious": ("curious", "THINKING"),
    "focused": ("focused", "NOD"),
    "sleepy": ("tired", "YAWN"),
    "concerned": ("concerned", "SHY"),
    "excited": ("excited", "CHEER"),
    "tsundere": ("proud", "HEAD_SHAKE"),
}

INTERACTION_EFFECTS: dict[str, dict[str, Any]] = {
    "headpat": {"affinity": 8, "energy": 3, "mood": "affectionate", "emotion": "happy", "gesture": "HEAD_TILT"},
    "poke": {"affinity": 4, "energy": 5, "mood": "playful", "emotion": "surprised", "gesture": "WINK"},
    "compliment": {"affinity": 10, "energy": 6, "mood": "happy", "emotion": "proud", "gesture": "CHEER"},
    "cheer": {"affinity": 7, "energy": 10, "mood": "excited", "emotion": "excited", "gesture": "HAPPY_JUMP"},
    "chat": {"affinity": 3, "energy": -1, "mood": "curious", "emotion": "curious", "gesture": "NOD"},
    "sleep": {"affinity": 2, "energy": 20, "mood": "sleepy", "emotion": "tired", "gesture": "YAWN"},
    "wake": {"affinity": 3, "energy": 10, "mood": "happy", "emotion": "happy", "gesture": "WAVE"},
}


@dataclass
class CompanionState:
    affinity_points: int = 120
    mood: str = "happy"
    energy: int = 85
    total_interactions: int = 0
    headpats: int = 0
    compliments: int = 0
    streak_days: int = 1
    last_interaction_day: str = ""
    last_updated: float = field(default_factory=time.time)
    preferred_brain: str = "ollama"
    recent_events: list[str] = field(default_factory=list)

    @property
    def tier(self) -> str:
        label = AFFINITY_TIERS[0][1]
        for threshold, name in AFFINITY_TIERS:
            if self.affinity_points >= threshold:
                label = name
        return label

    @property
    def level(self) -> int:
        return max(1, (self.affinity_points // 50) + 1)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["tier"] = self.tier
        d["level"] = self.level
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CompanionState:
        return cls(
            affinity_points=int(data.get("affinity_points", 120)),
            mood=str(data.get("mood", "happy")),
            energy=max(0, min(100, int(data.get("energy", 85)))),
            total_interactions=int(data.get("total_interactions", 0)),
            headpats=int(data.get("headpats", 0)),
            compliments=int(data.get("compliments", 0)),
            streak_days=int(data.get("streak_days", 1)),
            last_interaction_day=str(data.get("last_interaction_day", "")),
            last_updated=float(data.get("last_updated", time.time())),
            preferred_brain=str(data.get("preferred_brain", "ollama")),
            recent_events=list(data.get("recent_events", []))[-20:],
        )


class CompanionEngine:
    """Singleton OpenAmika-inspired companion state, mood & multi-brain manager."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._state = self._load_state()

    def _load_state(self) -> CompanionState:
        try:
            if STATE_FILE.exists():
                raw = json.loads(STATE_FILE.read_text(encoding="utf-8"))
                if isinstance(raw, dict):
                    return CompanionState.from_dict(raw)
        except Exception:
            pass
        return CompanionState()

    def _save_state(self) -> None:
        try:
            MEMORY_DIR.mkdir(parents=True, exist_ok=True)
            STATE_FILE.write_text(
                json.dumps(self._state.to_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception:
            pass

    def _apply_decay_locked(self) -> None:
        elapsed_hrs = max(0.0, (time.time() - self._state.last_updated) / 3600.0)
        if elapsed_hrs >= 2.0:
            self._state.energy = min(100, self._state.energy + int(elapsed_hrs * 5))
            if elapsed_hrs >= 6.0 and self._state.mood not in ("neutral", "sleepy"):
                self._state.mood = "neutral"
            self._state.last_updated = time.time()

    def get_status(self) -> dict[str, Any]:
        with self._lock:
            self._apply_decay_locked()
            return self._state.to_dict()

    def set_mood(self, mood: str, player=None) -> dict[str, Any]:
        m = (mood or "neutral").strip().lower()
        if m not in MOOD_TO_AVATAR:
            m = "neutral"
        with self._lock:
            self._state.mood = m
            self._state.last_updated = time.time()
            self._save_state()
            emo, gest = MOOD_TO_AVATAR[m]
            self._apply_to_avatar(player, emo, gest)
            return self._state.to_dict()

    def interact(self, interaction: str, note: str = "", player=None) -> dict[str, Any]:
        kind = (interaction or "chat").strip().lower()
        fx = INTERACTION_EFFECTS.get(kind, INTERACTION_EFFECTS["chat"])
        today = time.strftime("%Y-%m-%d")

        with self._lock:
            self._apply_decay_locked()
            prev_tier = self._state.tier
            if self._state.last_interaction_day and self._state.last_interaction_day != today:
                self._state.streak_days += 1
            self._state.last_interaction_day = today
            self._state.total_interactions += 1
            if kind == "headpat":
                self._state.headpats += 1
            elif kind == "compliment":
                self._state.compliments += 1

            self._state.affinity_points = max(0, min(1000, self._state.affinity_points + fx["affinity"]))
            self._state.energy = max(5, min(100, self._state.energy + fx["energy"]))
            self._state.mood = fx["mood"]
            self._state.last_updated = time.time()
            ev = f"{time.strftime('%H:%M')} {kind}" + (f": {note[:60]}" if note else "")
            self._state.recent_events = (self._state.recent_events + [ev])[-20:]
            self._save_state()

            self._apply_to_avatar(player, fx["emotion"], fx["gesture"])
            new_tier = self._state.tier
            return {
                "interaction": kind,
                "tier_up": new_tier != prev_tier,
                "emotion": fx["emotion"],
                "gesture": fx["gesture"],
                "state": self._state.to_dict(),
            }

    @staticmethod
    def _apply_to_avatar(player, emotion: str, gesture: str) -> None:
        if player is None:
            return
        try:
            if hasattr(player, "set_emotion") and emotion:
                player.set_emotion(emotion, 0.9, 3.8)
            if hasattr(player, "trigger_gesture") and gesture and gesture != "IDLE":
                player.trigger_gesture(gesture, 3.2, 1.0)
        except Exception:
            pass

    def reset_state(self) -> dict[str, Any]:
        with self._lock:
            self._state = CompanionState()
            self._save_state()
            return self._state.to_dict()

    # ── OpenAmika Multi-Brain (Ollama / OpenRouter) ──────────────────────────
    def brain_status(self) -> dict[str, Any]:
        ollama_models: list[str] = []
        ollama_up = False
        try:
            req = Request("http://127.0.0.1:11434/api/tags", headers={"Accept": "application/json"})
            with urlopen(req, timeout=1.5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            ollama_up = True
            ollama_models = [m.get("name", "") for m in data.get("models", []) if m.get("name")]
        except Exception:
            pass

        openrouter_key = ""
        try:
            if API_KEYS_FILE.exists():
                keys = json.loads(API_KEYS_FILE.read_text(encoding="utf-8"))
                openrouter_key = str(keys.get("openrouter_api_key") or keys.get("OPENROUTER_API_KEY") or "")
        except Exception:
            pass

        return {
            "ollama": {"available": ollama_up, "models": ollama_models},
            "openrouter": {"configured": bool(openrouter_key)},
        }

    def ask_brain(
        self,
        prompt: str,
        backend: str = "auto",
        model: str = "",
    ) -> dict[str, Any]:
        st = self.get_status()
        sys_msg = (
            f"Eres VIERNES en modo OpenAmika Companion. Estado emocional actual: {st['mood']}, "
            f"energía: {st['energy']}%, nivel de afinidad: {st['level']} ({st['tier']}). "
            "Responde breve, natural y coherente con tu estado emocional."
        )
        b_status = self.brain_status()
        use_backend = backend.lower().strip()
        if use_backend == "auto":
            use_backend = "ollama" if b_status["ollama"]["available"] else "openrouter"

        if use_backend == "ollama":
            if not b_status["ollama"]["available"]:
                return {"ok": False, "backend": "ollama", "reason": "Ollama no está corriendo en 127.0.0.1:11434."}
            chosen_model = model or (b_status["ollama"]["models"][0] if b_status["ollama"]["models"] else "llama3.2")
            payload = json.dumps({
                "model": chosen_model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": prompt},
                ],
            }).encode("utf-8")
            req = Request(
                "http://127.0.0.1:11434/api/chat",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(req, timeout=30.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            reply = (data.get("message") or {}).get("content", "").strip()
            return {"ok": True, "backend": "ollama", "model": chosen_model, "reply": reply}

        if use_backend == "openrouter":
            try:
                keys = json.loads(API_KEYS_FILE.read_text(encoding="utf-8")) if API_KEYS_FILE.exists() else {}
            except Exception:
                keys = {}
            api_key = str(keys.get("openrouter_api_key") or keys.get("OPENROUTER_API_KEY") or "").strip()
            if not api_key:
                return {"ok": False, "backend": "openrouter", "reason": "Falta openrouter_api_key en config/api_keys.json."}
            chosen_model = model or "meta-llama/llama-3.1-8b-instruct:free"
            payload = json.dumps({
                "model": chosen_model,
                "messages": [
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": prompt},
                ],
            }).encode("utf-8")
            req = Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                method="POST",
            )
            with urlopen(req, timeout=25.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            reply = (((data.get("choices") or [{}])[0].get("message") or {}).get("content") or "").strip()
            return {"ok": True, "backend": "openrouter", "model": chosen_model, "reply": reply}

        return {"ok": False, "backend": use_backend, "reason": f"Backend desconocido '{use_backend}'."}


_ENGINE: Optional[CompanionEngine] = None


def get_companion_engine() -> CompanionEngine:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = CompanionEngine()
    return _ENGINE
