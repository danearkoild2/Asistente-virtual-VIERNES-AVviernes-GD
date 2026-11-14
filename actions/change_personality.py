"""
Change Personality & Speaking Style Action
==========================================
Allows Edith / VIERNES to dynamically switch personality profiles,
regional dialects, and speaking modes either temporarily for the current
conversation or permanently when requested by the user.
"""

from __future__ import annotations
from typing import Optional
from core.personality_manager import get_personality_manager, PersonalityProfile


def change_personality_action(
    parameters: dict = None,
    player=None,
    session_memory=None,
    speak=None,
    response=None
) -> str:
    params = parameters or {}
    mode = str(params.get("mode") or params.get("personality") or "").strip().lower()
    temporary = bool(params.get("temporary", True))

    mgr = get_personality_manager()

    # 1. Caso: Restaurar personalidad habitual / predeterminada
    restore_triggers = ["habitual", "normal", "predeterminada", "default", "original", "restaurar", "volver", "reset"]
    if any(r in mode for r in restore_triggers) or not mode:
        mgr.clear_temporary_override()
        active = mgr.get_active_profile()
        return f"He vuelto a mi personalidad habitual ({active.name}). ¿En qué seguimos trabajando?"

    # 2. Búsqueda de coincidencia en perfiles disponibles
    profiles = mgr.get_all_profiles()
    target_prof: Optional[PersonalityProfile] = None

    # Coincidencia exacta de ID
    if mode in profiles:
        target_prof = profiles[mode]

    # Coincidencias por palabras clave
    if not target_prof:
        keywords_map = {
            "tica": "edith_tica_sarcastica",
            "costarricense": "edith_tica_sarcastica",
            "costa rica": "edith_tica_sarcastica",
            "sarcastica": "edith_tica_sarcastica",
            "sarcástica": "edith_tica_sarcastica",
            "paisa": "edith_paisa_bromista",
            "medellin": "edith_paisa_bromista",
            "medellín": "edith_paisa_bromista",
            "bromista": "edith_paisa_bromista",
            "kawaii": "edith_kawaii_tierna",
            "tierna": "edith_kawaii_tierna",
            "anime": "edith_kawaii_tierna",
            "dulce": "edith_kawaii_tierna",
            "profesional": "edith_profesional_ejecutiva",
            "ejecutiva": "edith_profesional_ejecutiva",
            "seria": "edith_profesional_ejecutiva",
            "rioplatense": "edith_rioplatense_astuta",
            "argentina": "edith_rioplatense_astuta",
            "porteña": "edith_rioplatense_astuta",
            "mexicana": "edith_mexicana_alegre",
            "mexico": "edith_mexicana_alegre",
            "méxico": "edith_mexicana_alegre",
            "alegre": "edith_mexicana_alegre",
            "españa": "edith_peninsular_analitica",
            "peninsular": "edith_peninsular_analitica",
            "española": "edith_peninsular_analitica",
            "analitica": "edith_peninsular_analitica",
            "analítica": "edith_peninsular_analitica",
            "cubana": "edith_cubana_calida",
            "cuba": "edith_cubana_calida",
            "chilena": "edith_chilena_relajada",
            "chile": "edith_chilena_relajada",
            "colombiana": "edith_colombiana_neutral",
            "colombia": "edith_colombiana_neutral",
            "neutro": "edith_profesional_ejecutiva",
            "universal": "edith_colombiana_neutral",
        }
        for kw, pid in keywords_map.items():
            if kw in mode:
                target_prof = profiles.get(pid)
                if target_prof:
                    break

    # Si aún no coincide, buscar por nombre
    if not target_prof:
        for pid, prof in profiles.items():
            if mode in prof.name.lower():
                target_prof = prof
                break

    if not target_prof:
        available = ", ".join([p.name for p in list(profiles.values())[:6]])
        return (
            f"No encontré un perfil específico para '{mode}'. "
            f"Perfiles recomendados: {available}. O puedes pedirme volver a mi personalidad habitual."
        )

    if temporary:
        mgr.apply_temporary_override(target_prof, reason=f"Petición de usuario: {mode}")
        return (
            f"¡Entendido! He cambiado temporalmente a mi personalidad '{target_prof.name}'. "
            f"Adoptaré esta forma de hablar para esta conversación. "
            f"Puedes decirme 'vuelve a tu personalidad habitual' cuando quieras regresar."
        )
    else:
        mgr.set_default_profile(target_prof.id)
        return (
            f"¡Listo! He establecido de forma permanente el perfil '{target_prof.name}' "
            f"como mi personalidad predeterminada para todas las sesiones futuras."
        )


TOOL = {
    "name": "change_personality_mode",
    "description": (
        "Changes Edith's personality, speaking style, or regional dialect. "
        "Use when user asks to change mood, personality, or accent (e.g. 'ponte en modo profesional', "
        "'habla como paisa', 'modo tica sarcástica', 'sé kawaii', 'modo seria', 'vuelve a tu personalidad habitual')."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "mode": {
                "type": "STRING",
                "description": (
                    "The requested personality or regional style, e.g. 'profesional', 'tica', 'paisa', "
                    "'kawaii', 'sarcastica', 'mexicana', 'argentina', 'chilena', 'cubana', 'española', "
                    "or 'habitual' / 'normal' to restore the default."
                ),
            },
            "temporary": {
                "type": "BOOLEAN",
                "description": "True to change only for this conversation session (default), False to save permanently as default.",
            },
        },
        "required": ["mode"],
    },
    "handler": change_personality_action,
}
