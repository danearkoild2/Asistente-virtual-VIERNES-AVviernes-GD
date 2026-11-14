"""
Financial Analytics Action for VIERNES
=======================================
Auto-discovered by core/action_loader.py.
Handles natural financial queries:
- "¿Cuánto gasté este mes?"
- "¿En qué estoy gastando más?"
- "Compara septiembre contra octubre"
- "¿Hay algún gasto extraño o anomalía?"
- "Analiza mis suscripciones recurrentes"
"""
from __future__ import annotations

from typing import Any, Dict
from integrations.finance.financial_engine import finance_engine
from security.voice_id import voice_id_engine

TOOL = {
    "name": "financial_analytics",
    "description": (
        "Analiza datos financieros del usuario a partir de movimientos bancarios, estados de cuenta, "
        "archivos CSV o Excel. Permite calcular totales, comparar ingresos vs gastos, detectar categorías "
        "de mayor gasto, identificar gastos recurrentes y encontrar anomalías estadísticas. "
        "NOTA: Viernes es un motor de análisis estrictamente de solo lectura y nunca realiza pagos o transferencias."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "operation": {
                "type": "STRING",
                "enum": ["summary", "top_expenses", "anomalies", "recurring", "compare_periods", "load_file"],
                "description": "Tipo de análisis financiero a ejecutar.",
            },
            "file_path": {
                "type": "STRING",
                "description": "Ruta a un archivo CSV o Excel (.xlsx) con movimientos para cargar.",
            },
            "period1": {
                "type": "STRING",
                "description": "Nombre o mes del primer período a comparar (ej: 'septiembre').",
            },
            "period2": {
                "type": "STRING",
                "description": "Nombre o mes del segundo período a comparar (ej: 'octubre').",
            },
        },
        "required": ["operation"],
    },
    "handler": None,
}


def financial_action(parameters: Dict[str, Any] = None, player=None, session_memory=None) -> str:
    params = parameters or {}
    op = (params.get("operation") or "summary").lower()

    # 1. Voice ID & RBAC Permission Gate (Creator only)
    auth_ok, auth_msg = voice_id_engine.verify_action_authorized("finance.read", target=f"Finance {op}")
    if not auth_ok:
        if player and hasattr(player, "write_log"):
            player.write_log(f"SEC: {auth_msg}")
        return auth_msg

    # 2. Load file if requested
    if op == "load_file":
        f_path = params.get("file_path", "")
        if not f_path:
            return "Por favor especifica la ruta del archivo CSV o Excel a cargar."
        ok, msg = finance_engine.load_file(f_path)
        return msg

    # 3. Financial Summary
    if op in ("summary", "top_expenses"):
        summary = finance_engine.get_summary()
        if "error" in summary:
            return (
                "No hay datos financieros cargados actualmente. Puedes proporcionar un archivo CSV o Excel "
                "con tus transacciones bancarias o arrastrarlo al panel de Finanzas."
            )

        top_cats = "\n".join([f"• {c['category']}: ${c['amount']:,.2f} ({c['pct']}%)" for c in summary["top_categories"][:4]])
        res = (
            f"📊 Resumen Financiero:\n"
            f"• Ingresos totales: ${summary['total_income']:,.2f}\n"
            f"• Gastos totales: ${summary['total_expense']:,.2f}\n"
            f"• Balance neto: ${summary['net_balance']:,.2f} (Tasa de ahorro: {summary['savings_rate_pct']}%)\n\n"
            f"Categorías con mayor gasto:\n{top_cats}"
        )
        return res

    # 4. Anomaly Detection
    if op == "anomalies":
        anomalies = finance_engine.detect_anomalies(threshold_z=2.0)
        if not anomalies:
            return "🔎 Análisis de anomalías: No se detectaron cargos extraños ni transacciones fuera de tus rangos habituales."

        lines = [
            f"• {a['date']} — {a['description']}: ${a['amount']:,.2f} [{a['category']}] ({a['deviation']})"
            for a in anomalies[:5]
        ]
        return (
            f"⚠️ Se detectaron {len(anomalies)} transacciones atípicas o cargos inesperadamente altos:\n"
            + "\n".join(lines)
            + "\nTe sugiero revisar estos movimientos para verificar que correspondan a cargos reconocidos."
        )

    # 5. Recurring Expenses & Subscriptions
    if op == "recurring":
        rec = finance_engine.detect_recurring_expenses()
        if not rec:
            return "No se detectaron pagos recurrentes o suscripciones fijas en el historial cargado."

        lines = [f"• {r['concept']}: ~${r['average_amount']:,.2f} ({r['frequency']})" for r in rec]
        tot = sum(r["average_amount"] for r in rec)
        return f"🔄 Suscripciones y Gastos Recurrentes Detectados (Total est. ~${tot:,.2f}/mes):\n" + "\n".join(lines)

    # 6. Period Comparison
    if op == "compare_periods":
        p1 = params.get("period1", "")
        p2 = params.get("period2", "")
        if not p1 or not p2:
            return "Por favor indica los dos períodos o meses a comparar (ejemplo: septiembre y octubre)."
        comp = finance_engine.compare_periods(p1, p2)
        return comp.get("summary", "No se encontraron transacciones suficientes en esos períodos.")

    return f"Operación financiera '{op}' no reconocida."


TOOL["handler"] = financial_action
