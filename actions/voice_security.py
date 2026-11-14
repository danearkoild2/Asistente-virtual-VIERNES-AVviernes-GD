"""
Voice Identification & Security Action Handler for VIERNES
===========================================================
Auto-discovered by core/action_loader.py.
Handles natural commands like:
- "Viernes, ¿quién está hablando?"
- "Muestra el historial de auditoría de seguridad"
- "Activa / desactiva el modo seguro"
- "Muestra los usuarios registrados y sus permisos"
"""
from __future__ import annotations

from typing import Any, Dict
from security.voice_id import voice_id_engine
from security.rbac import rbac
from security.safe_mode import is_safe_mode, set_safe_mode
from security.audit_logger import get_recent_audit_logs

TOOL = {
    "name": "voice_security",
    "description": (
        "Gestiona la identificación biométrica de voz, el control de acceso por roles (RBAC), "
        "el Modo Seguro y el historial de auditoría de acciones de Viernes."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "operation": {
                "type": "STRING",
                "enum": ["who_am_i", "list_users", "toggle_safe_mode", "view_audit_logs"],
                "description": "Acción de seguridad o identificación a realizar.",
            },
            "safe_mode_enabled": {
                "type": "BOOLEAN",
                "description": "Estado deseado para el Modo Seguro cuando la operación es toggle_safe_mode.",
            },
        },
        "required": ["operation"],
    },
    "handler": None,
}


def voice_security_action(parameters: Dict[str, Any] = None, player=None, session_memory=None) -> str:
    params = parameters or {}
    op = (params.get("operation") or "who_am_i").lower()

    # 1. Who am I / Active Speaker
    if op == "who_am_i":
        info = voice_id_engine.get_active_speaker_info()
        creator_tag = " (Creador / Administrador Principal)" if info["is_creator"] else ""
        return (
            f"🎙️ Identificación de Voz:\n"
            f"• Usuario activo: {info['speaker']}{creator_tag}\n"
            f"• Rol de seguridad: {info['role']}\n"
            f"• Nivel de confianza biométrica: {int(info['confidence'] * 100)}%"
        )

    # 2. List Users & RBAC Roles
    if op == "list_users":
        users = rbac.get_users()
        lines = []
        for name, data in users.items():
            enrolled = "✓ Enrolado" if data.get("voice_enrolled") else "No enrolado"
            lines.append(f"• {name} — Rol: {data.get('role')} ({enrolled})")
        return "👥 Usuarios y Roles de Seguridad Registrados:\n" + "\n".join(lines)

    # 3. Toggle Safe Mode
    if op == "toggle_safe_mode":
        curr = is_safe_mode()
        req_state = params.get("safe_mode_enabled", not curr)
        set_safe_mode(req_state)
        state_txt = "ACTIVADO" if req_state else "DESACTIVADO"
        return f"🛡️ Modo Seguro {state_txt}. {'Las acciones críticas requerirán confirmación explícita.' if req_state else 'Confirmaciones automáticas desactivadas.'}"

    # 4. View Audit Logs
    if op == "view_audit_logs":
        logs = get_recent_audit_logs(limit=5)
        if not logs:
            return "El historial de auditoría de seguridad está limpio."
        lines = []
        for log in logs:
            lines.append(f"[{log['timestamp']}] {log['user']} ({log['role']}) ➔ {log['action']} [{log['result']}]")
        return "📜 Registro de Auditoría de Acciones Recientes:\n" + "\n".join(lines)

    return f"Operación de seguridad '{op}' no reconocida."


TOOL["handler"] = voice_security_action
