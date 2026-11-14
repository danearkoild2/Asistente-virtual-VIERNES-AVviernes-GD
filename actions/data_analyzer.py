"""
Data Analyzer & Trend Prediction Engine
========================================
Real-time data analysis, trend prediction, anomaly detection, and system forecasting.
Leverages numpy, scipy, and sklearn for statistical and predictive analysis.
"""

from __future__ import annotations

import math
import time
import threading
from typing import Any
import numpy as np

try:
    import psutil
    HAVE_PSUTIL = True
except ImportError:
    HAVE_PSUTIL = False


# ── In-Memory System Telemetry Buffer ──────────────────────────────────────────
# Keeps rolling 60 samples (sampled ~every 30 seconds) of system metrics
_SYSTEM_HISTORY: list[dict[str, float]] = []
_MAX_HISTORY_SAMPLES = 60
_SAMPLER_RUNNING = False
_LAST_ACCESSED = 0.0
_LOCK = threading.Lock()


def _sample_once():
    """Take a single snapshot of system metrics safely."""
    if not HAVE_PSUTIL:
        return
    try:
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent if hasattr(psutil, "disk_usage") else 0.0
        now = time.time()
        with _LOCK:
            _SYSTEM_HISTORY.append({
                "timestamp": now,
                "cpu": float(cpu),
                "ram": float(ram),
                "disk": float(disk),
            })
            if len(_SYSTEM_HISTORY) > _MAX_HISTORY_SAMPLES:
                _SYSTEM_HISTORY.pop(0)
    except Exception:
        pass


def _telemetry_sampler_worker():
    """Background worker collecting lightweight telemetry. Auto-suspends after 10 min idle."""
    global _SAMPLER_RUNNING
    while _SAMPLER_RUNNING:
        now = time.time()
        # If no one requested trend data for 10 minutes, suspend sampler to save CPU/battery
        if (now - _LAST_ACCESSED) > 600.0:
            with _LOCK:
                _SAMPLER_RUNNING = False
            break
        _sample_once()
        time.sleep(30.0)


def ensure_sampler_running():
    """Start or keep-alive the telemetry sampler on demand."""
    global _SAMPLER_RUNNING, _LAST_ACCESSED
    _LAST_ACCESSED = time.time()
    if not HAVE_PSUTIL:
        return
    with _LOCK:
        if not _SYSTEM_HISTORY:
            _sample_once()
        if not _SAMPLER_RUNNING:
            _SAMPLER_RUNNING = True
            t = threading.Thread(target=_telemetry_sampler_worker, daemon=True)
            t.start()


def start_telemetry_sampler():
    """Backward-compatible alias for ensure_sampler_running()."""
    ensure_sampler_running()


# ── Statistical & Predictive Engine ───────────────────────────────────────────

def analyze_series(
    data: list[float],
    context_label: str = "Datos",
    forecast_steps: int = 3,
) -> dict[str, Any]:
    """
    Perform deep statistical, trend, and predictive analysis on a numeric time series.
    """
    if not data or len(data) < 2:
        return {
            "error": "Se requieren al menos 2 puntos de datos para analizar tendencias.",
            "summary": "Datos insuficientes.",
        }

    arr = np.array(data, dtype=float)
    n = len(arr)
    x = np.arange(n, dtype=float)

    # 1. Descriptive Statistics
    mean_val = float(np.mean(arr))
    median_val = float(np.median(arr))
    min_val = float(np.min(arr))
    max_val = float(np.max(arr))
    std_val = float(np.std(arr))
    variance_val = float(np.var(arr))
    total_change = float(arr[-1] - arr[0])
    pct_change = float(((arr[-1] - arr[0]) / abs(arr[0]) * 100.0)) if abs(arr[0]) > 1e-9 else 0.0

    # 2. Linear Regression Trend Line (y = m*x + b)
    slope, intercept = np.polyfit(x, arr, 1)
    predicted_current = slope * x + intercept
    
    # Coefficient of Determination R^2
    ss_tot = np.sum((arr - mean_val) ** 2)
    ss_res = np.sum((arr - predicted_current) ** 2)
    r_squared = float(1.0 - (ss_res / ss_tot)) if ss_tot > 1e-9 else 1.0
    r_squared = max(0.0, min(1.0, r_squared))

    # 3. Trend Direction & Classification
    rel_slope = (slope / mean_val) if abs(mean_val) > 1e-9 else slope
    if r_squared > 0.65 and rel_slope > 0.04:
        trend_label = "Crecimiento acelerado (Alcista fuerte)"
        trend_type = "bullish_strong"
    elif rel_slope > 0.01:
        trend_label = "Tendencia alcista moderada"
        trend_type = "bullish_moderate"
    elif r_squared > 0.65 and rel_slope < -0.04:
        trend_label = "Caída pronunciada (Bajista fuerte)"
        trend_type = "bearish_strong"
    elif rel_slope < -0.01:
        trend_label = "Tendencia bajista moderada"
        trend_type = "bearish_moderate"
    else:
        trend_label = "Estable / En rango horizontal"
        trend_type = "stable"

    volatility = (std_val / mean_val * 100.0) if abs(mean_val) > 1e-9 else 0.0
    if volatility > 35.0:
        trend_label += " con Alta Volatilidad"

    # 4. Outlier / Anomaly Detection (Z-Score method)
    anomalies = []
    if std_val > 1e-9:
        z_scores = (arr - mean_val) / std_val
        for idx, (val, z) in enumerate(zip(arr, z_scores)):
            if abs(z) >= 2.0:
                anomalies.append({
                    "index": int(idx),
                    "value": float(val),
                    "z_score": round(float(z), 2),
                    "type": "Pico inusual" if z > 0 else "Caída anómala",
                })

    # 5. Future Trend Projection / Forecast
    forecast_steps = max(1, min(12, int(forecast_steps)))
    future_x = np.arange(n, n + forecast_steps, dtype=float)
    future_preds = slope * future_x + intercept
    
    # Add trend margin based on std error
    margin = float(std_val * 0.8)
    forecast_points = []
    for step_idx, pred in enumerate(future_preds, start=1):
        pred_val = float(pred)
        forecast_points.append({
            "step": step_idx,
            "predicted_value": round(pred_val, 2),
            "range_low": round(pred_val - margin, 2),
            "range_high": round(pred_val + margin, 2),
        })

    # 6. Strategic Recommendations & Suggestions
    suggestions = []
    if trend_type.startswith("bullish"):
        suggestions.append(f"El patrón de {context_label} muestra impulso positivo continuo (+{pct_change:.1f}%). Conviene capitalizar la inercia.")
    elif trend_type.startswith("bearish"):
        suggestions.append(f"Se observa una contracción del {abs(pct_change):.1f}% en {context_label}. Se recomienda auditar posibles cuellos de botella.")
    else:
        suggestions.append(f"{context_label} se mantiene con alta estabilidad operativa (variación del {pct_change:.1f}%).")

    if anomalies:
        suggestions.append(f"Se detectaron {len(anomalies)} anomalía(s) estadística(s) que requieren atención especial.")

    return {
        "context_label": context_label,
        "sample_size": n,
        "mean": round(mean_val, 2),
        "median": round(median_val, 2),
        "min": round(min_val, 2),
        "max": round(max_val, 2),
        "std_dev": round(std_val, 2),
        "pct_change": round(pct_change, 2),
        "slope": round(float(slope), 4),
        "r_squared": round(r_squared, 3),
        "trend_label": trend_label,
        "trend_type": trend_type,
        "volatility_pct": round(volatility, 1),
        "anomalies": anomalies,
        "forecast": forecast_points,
        "suggestions": suggestions,
    }


def analyze_system_trends() -> dict[str, Any]:
    """Analyze real-time system performance trends from rolling telemetry buffer."""
    ensure_sampler_running()
    with _LOCK:
        samples = list(_SYSTEM_HISTORY)

    if not samples:
        # Fallback to current snapshot
        if HAVE_PSUTIL:
            cpu = float(psutil.cpu_percent(interval=0.1))
            ram = float(psutil.virtual_memory().percent)
            return {
                "status": "Monitoreo iniciado recientemente.",
                "current_cpu": f"{cpu}%",
                "current_ram": f"{ram}%",
                "trend": "Recolectando muestras en segundo plano.",
                "suggestion": "El sistema está dentro de los parámetros nominales.",
            }
        return {"error": "psutil no disponible."}

    cpu_vals = [s["cpu"] for s in samples]
    ram_vals = [s["ram"] for s in samples]

    cpu_analysis = analyze_series(cpu_vals, context_label="Uso de CPU", forecast_steps=3)
    ram_analysis = analyze_series(ram_vals, context_label="Uso de RAM", forecast_steps=3)

    # Trend warnings
    warnings = []
    if ram_vals[-1] > 85.0 or (ram_analysis["slope"] > 0.5 and ram_vals[-1] > 70.0):
        warnings.append("Tendencia de memoria al alza. Podría requerirse limpieza de caché o cierre de procesos pesados.")
    if cpu_vals[-1] > 80.0:
        warnings.append("Carga de procesador sostenida por encima del promedio habitual.")

    return {
        "samples_count": len(samples),
        "duration_minutes": round(len(samples) * 0.5, 1),
        "current_cpu": f"{cpu_vals[-1]:.1f}%",
        "current_ram": f"{ram_vals[-1]:.1f}%",
        "cpu_trend": cpu_analysis["trend_label"],
        "ram_trend": ram_analysis["trend_label"],
        "cpu_forecast_next": [f"{p['predicted_value']:.1f}%" for p in cpu_analysis["forecast"]],
        "ram_forecast_next": [f"{p['predicted_value']:.1f}%" for p in ram_analysis["forecast"]],
        "warnings": warnings,
        "summary": (
            f"Telemetría en tiempo real: CPU en {cpu_vals[-1]:.1f}% ({cpu_analysis['trend_label']}), "
            f"RAM en {ram_vals[-1]:.1f}% ({ram_analysis['trend_label']}). "
            + (" ".join(warnings) if warnings else "Rendimiento óptimo sin saturación prevista.")
        ),
    }


def get_trend_summary_for_proactive() -> str:
    """Compact summary of performance & data trends for the ProactiveEngine prompt."""
    try:
        trends = analyze_system_trends()
        if "summary" in trends:
            return trends["summary"]
    except Exception:
        pass
    return ""


# ── Action Handler ─────────────────────────────────────────────────────────────

def data_analyzer_action(
    parameters: dict = None,
    player=None,
    session_memory=None,
) -> str:
    """Execute data analysis and trend prediction."""
    params = parameters or {}
    op = (params.get("operation") or "analyze_trends").strip().lower()
    data = params.get("data")
    context_label = (params.get("context_label") or "Métrica").strip()
    forecast_steps = int(params.get("forecast_steps") or 3)

    if op == "system_trends" or (not data and op in ("analyze_trends", "forecast")):
        # If no explicit data provided, analyze system trends
        res = analyze_system_trends()
        msg = f"📊 Análisis de Telemetría en Tiempo Real:\n{res.get('summary', '')}"
        if player and hasattr(player, "write_log"):
            player.write_log(f"SYS: {msg}")
        return msg

    if isinstance(data, str):
        # Parse comma-separated or space-separated numbers
        try:
            cleaned = data.replace("[", "").replace("]", "").replace(",", " ")
            data = [float(x) for x in cleaned.split() if x.strip()]
        except Exception:
            return f"No pude interpretar la serie de datos numéricos proporcionada: '{data}'."

    if not isinstance(data, list) or len(data) < 2:
        return "Se requiere una lista de al menos 2 números para analizar tendencias y generar predicciones."

    analysis = analyze_series(data, context_label=context_label, forecast_steps=forecast_steps)
    if "error" in analysis:
        return analysis["error"]

    # Format a sleek, executive report
    forecast_str = ", ".join([f"P{p['step']}: {p['predicted_value']}" for p in analysis["forecast"]])
    suggestions_str = " ".join(analysis["suggestions"])

    report = (
        f"📈 Análisis de Tendencia para '{context_label}':\n"
        f"• Estado: {analysis['trend_label']} (R² = {analysis['r_squared']})\n"
        f"• Rango: Mín {analysis['min']} | Máx {analysis['max']} | Promedio {analysis['mean']}\n"
        f"• Variación total: {analysis['pct_change']:+.1f}% | Desviación estándar: {analysis['std_dev']}\n"
        f"• Proyección estimada (próximos {forecast_steps} pasos): [{forecast_str}]\n"
        f"• Sugerencia estratégica: {suggestions_str}"
    )

    if analysis["anomalies"]:
        anom_details = ", ".join([f"#{a['index']} (valor {a['value']})" for a in analysis["anomalies"]])
        report += f"\n⚠️ Anomalías detectadas: {anom_details}."

    if player and hasattr(player, "write_log"):
        player.write_log(f"SYS: {report}")

    return report


TOOL = {
    "name": "data_analyzer",
    "description": (
        "Analiza datos numéricos, series temporales y telemetría en tiempo real. "
        "Calcula regresión lineal, identifica tendencias (alcistas/bajistas/estables), "
        "detecta anomalías estadísticas (outliers), predice valores futuros (forecasting) "
        "y genera recomendaciones estratégicas basadas en datos. "
        "Úsalo cuando el usuario pida analizar tendencias, predecir datos, métricas o rendimiento."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "operation": {
                "type": "STRING",
                "description": "Operación a realizar: 'analyze_trends' (análisis completo), 'forecast' (predicción futura), o 'system_trends' (telemetría de PC en tiempo real).",
            },
            "data": {
                "type": "ARRAY",
                "items": {"type": "NUMBER"},
                "description": "Lista de números a analizar (ejemplo: [10, 14, 18, 25, 32]). Omitir si se analiza telemetría del sistema.",
            },
            "context_label": {
                "type": "STRING",
                "description": "Nombre o descripción de la métrica (ejemplo: 'Ventas semanales', 'Uso de CPU', 'Latencia de red').",
            },
            "forecast_steps": {
                "type": "INTEGER",
                "description": "Cantidad de periodos futuros a predecir (por defecto 3).",
            },
        },
    },
    "handler": data_analyzer_action,
}
