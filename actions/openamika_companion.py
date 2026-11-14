"""
actions/openamika_companion.py — Native OpenAmika (zeekk0/OpenAmika) companion tool.

Integrates OpenAmika's Live2D/VRM emotional companion state machine, persistent
affinity & relationship progression, interactive reactions (headpat, poke,
compliment, cheer, sleep, wake), and secondary local/cloud brain bridge
(Ollama / OpenRouter).
"""
from __future__ import annotations

from typing import Any

from core.companion_engine import MOOD_TO_AVATAR, get_companion_engine


def openamika_companion(parameters: dict[str, Any] = None, player=None, **_) -> str:
    params = parameters or {}
    action = str(params.get("action") or "status").strip().lower()
    interaction = str(params.get("interaction") or "chat").strip().lower()
    mood = str(params.get("mood") or "").strip().lower()
    prompt = str(params.get("prompt") or "").strip()
    backend = str(params.get("backend") or "auto").strip().lower()
    model = str(params.get("model") or "").strip()
    note = str(params.get("note") or "").strip()

    eng = get_companion_engine()

    if action == "status":
        st = eng.get_status()
        return (
            f"OpenAmika Companion State:\n"
            f"  • Mood: {st['mood']} | Energy: {st['energy']}%\n"
            f"  • Affinity: {st['affinity_points']}/1000 (Level {st['level']} · {st['tier']})\n"
            f"  • Streak: {st['streak_days']} day(s) | Interactions: {st['total_interactions']} "
            f"(Headpats: {st['headpats']}, Compliments: {st['compliments']})"
        )

    if action == "interact":
        res = eng.interact(interaction, note=note, player=player)
        st = res["state"]
        tier_note = f" LEVEL UP -> {st['tier']}!" if res.get("tier_up") else ""
        return (
            f"Companion reaction '{res['interaction']}' applied "
            f"(avatar emotion={res['emotion']}, gesture={res['gesture']}). "
            f"Mood: {st['mood']}, Energy: {st['energy']}%, "
            f"Affinity: {st['affinity_points']} ({st['tier']}).{tier_note}"
        )

    if action == "set_mood":
        if not mood or mood not in MOOD_TO_AVATAR:
            return f"Valid moods: {', '.join(sorted(MOOD_TO_AVATAR.keys()))}."
        st = eng.set_mood(mood, player=player)
        return f"Companion mood set to '{st['mood']}' and synchronized with Live2D/VRM avatar."

    if action == "brain_status":
        bs = eng.brain_status()
        ol = bs["ollama"]
        or_st = bs["openrouter"]
        ol_models = ", ".join(ol["models"]) if ol["models"] else "none"
        return (
            f"OpenAmika Secondary Brains:\n"
            f"  • Ollama: {'ONLINE' if ol['available'] else 'OFFLINE'} (models: {ol_models})\n"
            f"  • OpenRouter: {'CONFIGURED' if or_st['configured'] else 'NOT CONFIGURED'}"
        )

    if action == "ask_brain":
        if not prompt:
            return "Provide a 'prompt' for the secondary companion brain."
        res = eng.ask_brain(prompt, backend=backend, model=model)
        if not res.get("ok"):
            return f"Secondary brain ({res.get('backend')}) failed: {res.get('reason')}"
        return f"[{res['backend']}:{res['model']}] {res['reply']}"

    if action == "reset_affinity":
        st = eng.reset_state()
        return f"OpenAmika companion state reset (Affinity: {st['affinity_points']}, Mood: {st['mood']})."

    return f"Unknown openamika_companion action '{action}'."


TOOL = {
    "name": "openamika_companion",
    "description": (
        "OpenAmika Live2D/VRM AI Companion engine (zeekk0/OpenAmika). Manages "
        "persistent emotional mood, energy, affinity/relationship progression "
        "(Level & Tier), interactive companion reactions (headpat, poke, "
        "compliment, cheer, sleep, wake) synced with Live2D/VRM expressions and "
        "gestures, plus optional secondary Ollama/OpenRouter companion brain. "
        "Use when the user interacts affectionately (headpat, praise, poke), "
        "asks about VIERNES's mood/affinity/energy, wants to change companion "
        "mood, or query the local Ollama/OpenRouter companion brain."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": (
                    "'status' (default): mood, energy, affinity level & tier; "
                    "'interact': trigger companion reaction & avatar animation; "
                    "'set_mood': set emotional state; 'brain_status': check "
                    "Ollama/OpenRouter; 'ask_brain': query Ollama/OpenRouter "
                    "with companion state; 'reset_affinity': reset progress."
                ),
                "enum": [
                    "status",
                    "interact",
                    "set_mood",
                    "brain_status",
                    "ask_brain",
                    "reset_affinity",
                ],
            },
            "interaction": {
                "type": "STRING",
                "description": "For action='interact': interaction type.",
                "enum": ["headpat", "poke", "compliment", "cheer", "chat", "sleep", "wake"],
            },
            "mood": {
                "type": "STRING",
                "description": "For action='set_mood': target mood.",
                "enum": sorted(MOOD_TO_AVATAR.keys()),
            },
            "prompt": {
                "type": "STRING",
                "description": "For action='ask_brain': prompt to send to Ollama/OpenRouter.",
            },
            "backend": {
                "type": "STRING",
                "description": "For action='ask_brain': 'auto', 'ollama', or 'openrouter'.",
                "enum": ["auto", "ollama", "openrouter"],
            },
            "model": {
                "type": "STRING",
                "description": "Optional model name for Ollama or OpenRouter.",
            },
            "note": {
                "type": "STRING",
                "description": "Optional short note recorded in companion interaction history.",
            },
        },
        "required": ["action"],
    },
    "handler": openamika_companion,
}
