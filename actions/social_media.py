"""
Social Media Action Handler for VIERNES
=======================================
Auto-discovered by core/action_loader.py.
Handles natural commands like:
- "Viernes, ¿cómo estuvieron nuestras redes ayer?"
- "¿Cuáles fueron las publicaciones con mejor rendimiento?"
- "¿Hay comentarios que requieran atención en YouTube o Instagram?"
"""
from __future__ import annotations

from typing import Any, Dict
from integrations.social.social_manager import social_manager
from security.voice_id import voice_id_engine

TOOL = {
    "name": "social_media",
    "description": (
        "Consulta métricas, estadísticas, publicaciones de alto rendimiento y comentarios "
        "en las redes sociales conectadas (Instagram, Facebook, YouTube, X). Permite obtener un resumen "
        "ejecutivo del rendimiento de ayer o consultar comentarios que necesitan atención."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "operation": {
                "type": "STRING",
                "enum": ["overview", "metrics", "top_posts", "attention_comments"],
                "description": "Tipo de consulta de redes sociales.",
            },
            "platform": {
                "type": "STRING",
                "enum": ["all", "youtube", "instagram", "facebook", "x_twitter"],
                "description": "Plataforma específica o 'all' para resumen general.",
            },
        },
        "required": ["operation"],
    },
    "handler": None,
}


def social_action(parameters: Dict[str, Any] = None, player=None, session_memory=None) -> str:
    params = parameters or {}
    op = (params.get("operation") or "overview").lower()
    platform = (params.get("platform") or "all").lower()

    # 1. Voice ID & RBAC Permission Gate
    auth_ok, auth_msg = voice_id_engine.verify_action_authorized("social.read", target=f"Social {op} {platform}")
    if not auth_ok:
        if player and hasattr(player, "write_log"):
            player.write_log(f"SEC: {auth_msg}")
        return auth_msg

    # 2. Specific Platform Query
    if platform != "all" and platform in social_manager._adapters:
        adapter = social_manager._adapters[platform]
        if not adapter.is_connected():
            return f"La plataforma {adapter.platform_name} no está configurada actualmente. Puedes vincularla en el panel de Integraciones (F8) para consultar información real."

        if op == "metrics":
            m = adapter.get_metrics()
            if platform == "youtube":
                return f"YouTube ({m.get('channel_title', 'Canal')}): {m.get('subscribers', 0):,} suscriptores, {m.get('views', 0):,} vistas totales y {m.get('video_count', 0):,} videos publicados."
            elif platform == "facebook":
                return f"Facebook ({m.get('name', 'Página')}): {m.get('page_likes', 0):,} me gusta y {m.get('followers', 0):,} seguidores."
            elif platform == "x_twitter":
                return f"X (@{m.get('username', 'usuario')}): cuenta activa y verificada."
            elif platform == "instagram":
                return f"Instagram (@{m.get('username', 'usuario')}): cuenta activa y verificada."

        if op == "top_posts":
            posts = adapter.get_recent_posts(limit=3)
            if not posts:
                return f"No encontré publicaciones recientes en {adapter.platform_name}."
            lines = [f"• {p.get('title') or p.get('caption') or p.get('text', '')}" for p in posts]
            return f"Publicaciones recientes en {adapter.platform_name}:\n" + "\n".join(lines)

    # 3. Comments requiring attention
    if op == "attention_comments":
        urgent = social_manager.get_attention_needed_comments()
        if not urgent:
            return "No hay comentarios que requieran atención inmediata en tus redes sociales vinculadas."

        lines = [f"• [{c.get('priority', 'MEDIA')}] {c.get('author')}: \"{c.get('comment')}\"" for c in urgent]
        return "Comentarios destacados que requieren atención:\n" + "\n".join(lines)

    # 4. Cross-platform overview / default
    summary = social_manager.get_cross_platform_summary()
    if player and hasattr(player, "write_log"):
        player.write_log(f"SOCIAL: Resumen de redes entregado.")
    return summary


TOOL["handler"] = social_action
