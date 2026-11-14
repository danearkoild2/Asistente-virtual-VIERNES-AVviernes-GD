"""
Action: web_research
====================
Deep autonomous web research tool for Viernes.
Consults SerpApi across multi-engine queries, reads public web pages,
contrasts perspectives and generates synthesized reports with verified citations.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from core.research import ResearchEngine, ResearchReport

logger = logging.getLogger("Viernes.Actions.WebResearch")


def web_research(
    parameters: Optional[Dict[str, Any]] = None,
    player=None,
    speak: Optional[Any] = None,
    **kwargs,
) -> str:
    params = parameters or {}
    topic = str(params.get("topic") or params.get("query") or "").strip()
    category = str(params.get("category") or "general").strip().lower()

    if not topic:
        return "Por favor especifica un tema para investigar."

    if player:
        player.write_log(f"🔬 [Investigación Web] Iniciando estudio sobre: {topic}")

    print(f"[WebResearch] 🚀 Iniciando investigación profunda: topic={topic!r}, cat={category!r}")

    engine = ResearchEngine()

    def on_progress(stage: str, msg: str, data: Dict[str, Any]):
        if player:
            player.write_log(f"◈ {msg}")

    try:
        report: ResearchReport = engine.research(
            topic=topic,
            category=category,
            on_progress=on_progress,
        )

        # Notify UI if method exists on player / window
        if player and hasattr(player, "show_visual_card"):
            import threading
            def _fetch_and_show_visual():
                try:
                    from core.visual_engine import VisualEngine
                    ve = VisualEngine.get_instance()
                    card = ve.evaluate_and_fetch(topic, assistant_response=report.summary, force=True)
                    if card and card.images:
                        player.show_visual_card(card)
                except Exception as ex:
                    logger.warning(f"Error fetching visual card for research: {ex}")

            threading.Thread(target=_fetch_and_show_visual, daemon=True, name="WebResearchVisualWorker").start()

        if player and hasattr(player, "show_research"):
            try:
                player.show_research(report.to_dict())
            except Exception as e:
                logger.warning(f"Error displaying research in UI: {e}")
        elif player and hasattr(player, "show_content"):
            try:
                player.show_content(f"INVESTIGACIÓN: {topic[:30]}", report.full_report)
            except Exception:
                pass

        if player:
            player.write_log(
                f"✅ [Investigación Completada] {len(report.sources)} fuentes analizadas en {report.duration_sec:.1f}s."
            )

        # Build natural voice-ready summary
        output_parts = [
            f"He concluido la investigación sobre '{topic}'.",
            report.summary,
        ]
        if report.key_facts:
            output_parts.append("\nPuntos clave confirmados:")
            for kf in report.key_facts[:3]:
                output_parts.append(f"• {kf}")

        if report.sources:
            output_parts.append(f"\nSe han consultado {len(report.sources)} fuentes verificadas disponibles en el panel de investigación.")

        return "\n".join(output_parts)

    except Exception as e:
        logger.exception("Error executing web research")
        return f"La investigación no pudo completarse debido a un error: {e}"


TOOL = {
    "name": "web_research",
    "description": (
        "Realiza una investigación web autónoma, exhaustiva y estructurada sobre cualquier "
        "tema complejo, actualidad, tecnología, documentación técnica, productos o noticias. "
        "Consulta múltiples motores en SerpApi, lee el contenido de las páginas, compara fuentes, "
        "detecta discrepancias y sintetiza un informe fundamentado con citas directas. "
        "OBLIGATORIO: Antes o al llamar esta función, debes avisar al usuario en voz alta en español "
        "(ej: 'Voy a investigar a fondo sobre eso en internet...', 'Déjame indagar en la red...') "
        "en el mismo turno para que sepa que estás buscando."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "topic": {
                "type": "STRING",
                "description": "Tema, pregunta compleja o aspecto que se desea investigar a fondo."
            },
            "category": {
                "type": "STRING",
                "description": "Categoría de investigación: 'general' (todo), 'news' (noticias recientes), 'scholar' (estudios académicos), 'tech' (documentación y GitHub), 'products' (precios y reviews), 'media' (videos y tutoriales)."
            }
        },
        "required": ["topic"]
    },
    "handler": web_research,
}
