"""
System Anomaly Detection Subsystem for VIERNES
==============================================
Analyzes process states, stopped critical Windows services, and error frequency spikes.
Computes system health scores (0-100%) and generates calibrated anomaly reports.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional
import psutil

from system_monitor.windows_events import event_diagnostics
from core.notifications import notify, LEVEL_WARNING, LEVEL_CRITICAL


class SystemAnomalyDetector:
    """Intelligent anomaly detector across system events, services, and processes."""

    def __init__(self):
        self._last_analysis: Dict[str, Any] = {}

    def scan_anomalies(self) -> Dict[str, Any]:
        """
        Run deep anomaly audit:
        1. Windows Event spikes
        2. Stopped automatic services
        3. High resource / runaway processes
        """
        anomalies = []
        confidence_score = 0.0

        # 1. Event Spikes
        clusters = event_diagnostics.analyze_event_clusters()
        for cl in clusters.get("clusters", [])[:3]:
            if cl["count"] >= 5:
                anomalies.append({
                    "type": "EVENT_SPIKE",
                    "target": cl["source"],
                    "severity": cl["severity"],
                    "count": cl["count"],
                    "detail": f"Frecuencia anómala de errores ({cl['count']} eventos) en '{cl['source']}'.",
                    "recommendation": cl["recommendation"],
                })
                confidence_score = max(confidence_score, 85.0)

        # 2. Windows Services Check (Auto-start services currently stopped)
        stopped_auto_services = []
        if hasattr(psutil, "win_service_iter"):
            try:
                for s in psutil.win_service_iter():
                    info = s.as_dict()
                    start_type = info.get("start_type", "")
                    status = info.get("status", "")
                    # 'automatic' and 'stopped'
                    if start_type == "automatic" and status == "stopped":
                        name = info.get("name", "")
                        # Ignore common non-critical services
                        if name.lower() not in ("trustedinstaller", "sppsvc", "wuauserv", "edgeupdate", "googleupdatem"):
                            stopped_auto_services.append(name)
            except Exception as e:
                print(f"[AnomalyDetector] Service scan error: {e}")

        if stopped_auto_services:
            sample_serv = stopped_auto_services[:3]
            anomalies.append({
                "type": "STOPPED_SERVICE",
                "target": ", ".join(sample_serv),
                "severity": "WARNING",
                "count": len(stopped_auto_services),
                "detail": f"Se detectaron {len(stopped_auto_services)} servicios automáticos detenidos ({', '.join(sample_serv)}).",
                "recommendation": "Verificar en 'services.msc' si requieren reinicio manual.",
            })
            confidence_score = max(confidence_score, 70.0)

        # 3. High CPU / Runaway Process Detection
        heavy_procs = []
        try:
            for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
                try:
                    cpu_p = p.info.get("cpu_percent") or 0.0
                    mem_p = p.info.get("memory_percent") or 0.0
                    if cpu_p > 80.0 or mem_p > 40.0:
                        heavy_procs.append({
                            "name": p.info.get("name", "Unknown"),
                            "pid": p.info.get("pid"),
                            "cpu": round(cpu_p, 1),
                            "mem": round(mem_p, 1),
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception:
            pass

        if heavy_procs:
            p_top = heavy_procs[0]
            anomalies.append({
                "type": "RESOURCE_HOG",
                "target": f"{p_top['name']} (PID {p_top['pid']})",
                "severity": "WARNING",
                "count": 1,
                "detail": (
                    f"Detecté un consumo inusual en el proceso '{p_top['name']}' (CPU: {p_top['cpu']}%, RAM: {p_top['mem']}%). "
                    "No puedo determinar por sí solo que sea perjudicial, pero recomiendo revisar su actividad."
                ),
                "recommendation": "Comprobar si está realizando alguna tarea en segundo plano o finalizar la tarea si no responde.",
            })
            confidence_score = max(confidence_score, 75.0)

        # Overall Health Score (100 is pristine)
        penalty = min(80.0, len(anomalies) * 20.0 + (15.0 if confidence_score > 80 else 0.0))
        health_score = round(100.0 - penalty, 0)

        result = {
            "health_score": health_score,
            "anomaly_detected": len(anomalies) > 0,
            "anomalies_count": len(anomalies),
            "confidence_score": round(confidence_score, 1),
            "anomalies": anomalies,
            "summary": (
                f"Estado del Sistema: Salud {health_score:.0f}%. "
                + (f"Se identificaron {len(anomalies)} anomalías que merecen atención." if anomalies else "Todos los parámetros y servicios operan dentro de los rangos nominales.")
            ),
        }
        self._last_analysis = result

        if anomalies:
            notify(
                "Anomalía del Sistema",
                f"Detectadas {len(anomalies)} anomalías (Salud: {health_score:.0f}%).",
                LEVEL_WARNING,
                "SYSTEM"
            )

        return result


# Global Anomaly Detector singleton
anomaly_detector = SystemAnomalyDetector()
