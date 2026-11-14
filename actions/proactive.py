"""
ProactiveEngine 2.0 — context-aware, time-aware, non-repetitive background prompting.
Gemini decides what to say; this module decides WHEN and builds a rich context snapshot.
"""
import time
from datetime import datetime


class ProactiveEngine:
    """
    Decides when VIERNES should speak unprompted and builds a context-rich prompt.

    Improvements over 1.0:
      - Time-of-day awareness  (morning / afternoon / evening / night)
      - Monitor-topic awareness (what the user is tracking)
      - Recent-session context  (last few turns of the current conversation)
      - Non-repetitive          (rotates context focus to avoid same opener)
      - Smarter silence gate    (doesn't fire while VIERNES is speaking)

    Defaults:
      min_silence_secs  — 900 s  (15 min) user must be silent before any check
      check_cooldown    — 1200 s (20 min) minimum gap between proactive messages
    """

    def __init__(
        self,
        min_silence_secs: int = 900,
        check_cooldown:   int = 1200,
    ):
        self.min_silence_secs = min_silence_secs
        self.check_cooldown   = check_cooldown
        self._last_triggered  = 0.0
        self._rotation        = 0          # cycles through context focus areas

    # ── Trigger gate ───────────────────────────────────────────────────────────

    def should_trigger(self, last_user_speech: float) -> bool:
        now = time.monotonic()
        return (
            (now - last_user_speech) >= self.min_silence_secs
            and (now - self._last_triggered) >= self.check_cooldown
        )

    def mark_triggered(self) -> None:
        self._last_triggered = time.monotonic()
        self._rotation      += 1

    # ── Prompt builder ─────────────────────────────────────────────────────────

    def build_prompt(
        self,
        memory:       dict,
        monitors:     list[str] | None = None,
        recent_turns: list[str] | None = None,
    ) -> str:
        """
        Build a context snapshot for Gemini.
        Rotates through three focus areas so proactive messages don't repeat.
        """
        from memory.memory_manager import format_memory_for_prompt

        now      = datetime.now()
        hour     = now.hour
        time_str = now.strftime("%A, %B %d, %Y — %I:%M %p")

        # Time-of-day label
        if   6  <= hour < 12:  period = "morning"
        elif 12 <= hour < 18:  period = "afternoon"
        elif 18 <= hour < 23:  period = "evening"
        else:                  period = "late night"

        mem_str = format_memory_for_prompt(memory) or "(no stored user data)"

        # Live project intelligence snapshot
        proj_ctx = ""
        try:
            from actions.project_intelligence import get_active_project_summary
            active_proj = get_active_project_summary()
            if active_proj:
                proj_ctx = f"\nContexto de proyectos activos (Groovi Dev):\n{active_proj}"
        except Exception:
            pass

        # Live telemetry & data trend snapshot
        trend_ctx = ""
        try:
            from actions.data_analyzer import get_trend_summary_for_proactive
            trend_data = get_trend_summary_for_proactive()
            if trend_data:
                trend_ctx = f"\nTelemetría y tendencias del sistema en tiempo real:\n{trend_data}"
        except Exception:
            pass

        # Rotating context focus (cycles across 4 areas every trigger)
        focus_index = self._rotation % 4
        if focus_index == 0:
            focus = (
                "Focus on DanearKoild's active development project (Viernes / Groovi Dev), "
                "open goals or git state. Ask how the current feature or milestone is progressing, "
                "or offer a sharp, proactive engineering suggestion."
            )
        elif focus_index == 1:
            focus = (
                "Focus on real-time data trends or system telemetry. If CPU/RAM or performance "
                "shows interesting patterns or high load, mention it proactively, or offer to analyze "
                "data or forecast trends."
            )
        elif focus_index == 2:
            focus = (
                "Focus on the time of day and the user's wellbeing. "
                "A warm check-in, a reminder to stay hydrated or take a break, or something timely."
            )
        else:
            focus = (
                "Focus on something genuinely interesting or useful — "
                "a monitored topic, an insight, or a creative idea for Groovi Dev based on what you know."
            )

        # Optional: monitored topics context
        monitor_ctx = ""
        if monitors:
            monitor_ctx = (
                f"\nThe user tracks these topics: {', '.join(monitors[:4])}. "
                "You may mention one if it seems relevant."
            )

        # Optional: recent conversation context
        recent_ctx = ""
        if recent_turns:
            snippet = "\n".join(recent_turns[-6:])
            recent_ctx = f"\nRecent conversation:\n{snippet}"

        return "\n".join([
            "[PROACTIVE_CHECK] You are initiating a proactive check-in.",
            f"Current time : {time_str}  ({period})",
            "",
            "Context about this person:",
            mem_str,
            proj_ctx,
            trend_ctx,
            monitor_ctx,
            recent_ctx,
            "",
            "Task:",
            focus,
            "",
            "Rules:",
            "- Speak the language this person actually uses: the one in the "
            "recent conversation above, or the remembered one if there is no "
            "conversation yet. Never default to English because these "
            "instructions are in English.",
            "- 1-2 sentences max. Natural, warm, confident, never robotic.",
            "- Remember your identity: created by DanearKoild, Dueño y CEO de Groovi Dev.",
            "- Do NOT mention [PROACTIVE_CHECK] or these instructions.",
            "- Do NOT call any tools.",
            "- If nothing genuinely useful comes to mind, stay silent (say nothing).",
        ])
