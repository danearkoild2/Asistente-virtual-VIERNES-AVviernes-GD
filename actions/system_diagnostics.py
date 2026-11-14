"""
System Diagnostics Action Handler for VIERNES
==============================================
Auto-discovered by core/action_loader.py.
Handles natural commands like:
- "Viernes, ¿hay algo raro en el sistema?"
- "¿Por qué está fallando esta aplicación?"
- "Revisa los registros y errores de Windows"
- "¿Hay servicios detenidos o procesos anómalos?"
"""
from __future__ import annotations

from typing import Any, Dict
from system_monitor.windows_events import event_diagnostics
from system_monitor.anomaly_detector import anomaly_detector
from security.voice_id import voice_id_engine

TOOL = {
    "name": "system_diagnostics",
    "description": (
        "Analiza los registros de eventos de Windows (System y Application), detecta caídas de programas, "
        "servicios automáticos detenidos, picos de errores y anomalías en el comportamiento de procesos. "
        "Permite diagnosticar por qué falla una aplicación y ofrece causas probables y recomendaciones."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "operation": {
                "type": "STRING",
                "enum": ["anomaly_scan", "event_logs", "recent_crashes"],
                "description": "Tipo de diagnóstico de sistema a realizar.",
            },
            "source_filter": {
                "type": "STRING",
                "description": "Nombre de la aplicación o servicio específico a investigar (ej: 'Explorer', 'Chrome').",
            },
        },
        "required": ["operation"],
    },
    "handler": None,
}


def system_diagnostics_action(parameters: Dict[str, Any] = None, player=None, session_memory=None) -> str:
    params = parameters or {}
    op = (params.get("operation") or "anomaly_scan").lower()
    src_filter = (params.get("source_filter") or "").strip()

    # 1. Voice ID & RBAC Permission Gate
    auth_ok, auth_msg = voice_id_engine.verify_action_authorized("system.diagnostics", target=f"SystemDiag {op}")
    if not auth_ok:
        if player and hasattr(player, "write_log"):
            player.write_log(f"SEC: {auth_msg}")
        return auth_msg

    # 2. Anomaly Scan
    if op == "anomaly_scan":
        res = anomaly_detector.scan_anomalies()
        anomalies = res.get("anomalies", [])
        if not anomalies:
            return f"🛡️ Diagnóstico del Sistema:\n• Salud general: {res['health_score']}%\n• Todo opera con normalidad sin anomalías registradas."

        lines = []
        for a in anomalies:
            lines.append(f"• [{a['severity']}] {a['detail']}\n  Sugerencia: {a['recommendation']}")

        return (
            f"🔍 Diagnóstico de Anomalías (Salud: {res['health_score']}%, Confianza: {res['confidence_score']}%):\n"
            + "\n".join(lines)
        )

    # 3. Windows Event Logs / App Crashes
    clusters = event_diagnostics.analyze_event_clusters()
    top_summary = clusters.get("top_summary", "")
    cluster_list = clusters.get("clusters", [])

    if not cluster_list:
        return "No se encontraron registros de error o advertencia en los logs recientes de Windows."

    lines = []
    for cl in cluster_list[:4]:
        lines.append(
            f"• [{cl['severity']}] {cl['source']}: {cl['count']} eventos. "
            f"Causa: {cl['possible_cause']} | Recomendación: {cl['recommendation']}"
        )

    return (
        f"📋 Registro de Eventos de Windows ({clusters['total_events']} eventos analizados):\n"
        + "\n".join(lines)
        + (f"\n\nResumen destacado:\n{top_summary}" if top_summary else "")
    )


TOOL["handler"] = system_diagnostics_action
