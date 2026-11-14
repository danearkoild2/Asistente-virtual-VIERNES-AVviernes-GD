"""
Financial Analytics Engine for VIERNES
=======================================
Performs deep quantitative, statistical, and categorical analysis of personal
and business financial records (CSV, TSV, and Excel .xlsx).
Strict Security Rule: READ-ONLY analysis. Never executes automated transfers or payments.
"""
from __future__ import annotations

import csv
import io
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
try:
    import openpyxl
    HAVE_OPENPYXL = True
except ImportError:
    HAVE_OPENPYXL = False

from security.audit_logger import record_audit
from security.rbac import rbac
from core.notifications import notify, LEVEL_INFO, LEVEL_WARNING

# Standard categories and recognition patterns
CATEGORY_RULES = {
    "Alimentación y Supermercado": ["super", "walmart", "oxxo", "costco", "restaurante", "ubereats", "rappi", "cafeteria", "comida", "mercado"],
    "Vivienda y Servicios": ["luz", "cfe", "agua", "gas", "internet", "renta", "telmex", "totalplay", "hipoteca", "mantenimiento"],
    "Transporte": ["uber", "didi", "gasolina", "peaje", "estacionamiento", "taller", "metro", "pasaje", "autobus"],
    "Suscripciones y Software": ["netflix", "spotify", "youtube", "amazon prime", "chatgpt", "github", "google storage", "apple", "adobe"],
    "Salud y Bienestar": ["farmacia", "medico", "hospital", "dentista", "gimnasio", "consulta", "laboratorio"],
    "Compras y Ocio": ["amazon", "mercadolibre", "liverpool", "cine", "ropa", "tienda", "juego", "steam"],
    "Ingresos y Nómina": ["nomina", "deposito", "transferencia recibida", "pago cliente", "honorarios", "sueldo", "rendimiento"],
}


class FinancialEngine:
    """Core financial analytics, anomaly detection, and budgetary tracking system."""

    def __init__(self):
        self._transactions: List[Dict[str, Any]] = []
        self._budgets: Dict[str, float] = {
            "Alimentación y Supermercado": 8000.0,
            "Vivienda y Servicios": 6000.0,
            "Suscripciones y Software": 1500.0,
            "Transporte": 3500.0,
            "Compras y Ocio": 4000.0,
        }

    def load_file(self, file_path_str: str) -> Tuple[bool, str]:
        """Load and parse transactions from a CSV, TSV, or Excel (.xlsx) file."""
        p = Path(file_path_str.strip('"').strip("'"))
        if not p.exists():
            return False, f"El archivo no existe: '{p}'"

        ext = p.suffix.lower()
        try:
            if ext in (".csv", ".txt", ".tsv"):
                return self._parse_csv(p)
            elif ext in (".xlsx", ".xlsm"):
                if not HAVE_OPENPYXL:
                    return False, "La biblioteca 'openpyxl' no está disponible para procesar archivos Excel."
                return self._parse_excel(p)
            else:
                return False, f"Formato no soportado: '{ext}'. Utiliza CSV o Excel (.xlsx)."
        except Exception as e:
            return False, f"Error al procesar archivo financiero: {e}"

    def load_from_text(self, text_content: str) -> Tuple[bool, str]:
        """Parse raw CSV/table text passed directly."""
        try:
            reader = csv.reader(io.StringIO(text_content.strip()))
            rows = [r for r in reader if r]
            if len(rows) < 2:
                return False, "Datos insuficientes (se requiere encabezado y al menos 1 fila)."
            return self._ingest_rows(rows[0], rows[1:])
        except Exception as e:
            return False, f"Error interpretando texto financiero: {e}"

    def _parse_csv(self, path: Path) -> Tuple[bool, str]:
        for enc in ("utf-8", "latin-1", "cp1252"):
            try:
                with open(path, "r", encoding=enc) as f:
                    # Detect delimiter
                    sample = f.read(2048)
                    f.seek(0)
                    dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
                    reader = csv.reader(f, dialect)
                    rows = [r for r in reader if r]
                if len(rows) >= 2:
                    return self._ingest_rows(rows[0], rows[1:], source_name=path.name)
            except Exception:
                continue
        return False, f"No se pudo decodificar el archivo CSV '{path.name}'."

    def _parse_excel(self, path: Path) -> Tuple[bool, str]:
        wb = openpyxl.load_workbook(str(path), data_only=True)
        sheet = wb.active
        rows = list(sheet.iter_rows(values_only=True))
        if len(rows) < 2:
            return False, "La hoja de Excel está vacía."
        header = [str(c or "") for c in rows[0]]
        data = [[str(c or "") for c in r] for r in rows[1:]]
        return self._ingest_rows(header, data, source_name=path.name)

    def _ingest_rows(self, header: List[str], data_rows: List[List[Any]], source_name: str = "Datos") -> Tuple[bool, str]:
        header_lower = [str(h).lower() for h in header]

        # Locate columns
        date_col = next((i for i, h in enumerate(header_lower) if any(k in h for k in ("fecha", "date", "dia"))), 0)
        desc_col = next((i for i, h in enumerate(header_lower) if any(k in h for k in ("concepto", "descrip", "detalle", "comercio", "name"))), 1)
        amt_col = next((i for i, h in enumerate(header_lower) if any(k in h for k in ("monto", "importe", "amount", "valor", "cantidad", "total"))), 2)
        cat_col = next((i for i, h in enumerate(header_lower) if any(k in h for k in ("categor", "tipo", "rubro"))), None)

        parsed = []
        for row in data_rows:
            if len(row) <= max(date_col, desc_col, amt_col):
                continue
            date_raw = str(row[date_col]).strip()
            desc_raw = str(row[desc_col]).strip()
            amt_str = str(row[amt_col]).replace("$", "").replace(",", "").replace(" ", "").strip()
            if not amt_str or not desc_raw:
                continue

            try:
                amt = float(amt_str)
            except ValueError:
                continue

            # Classify category
            if cat_col is not None and cat_col < len(row) and str(row[cat_col]).strip():
                category = str(row[cat_col]).strip()
            else:
                category = self._auto_classify(desc_raw, amt)

            parsed.append({
                "date": date_raw,
                "description": desc_raw,
                "amount": amt,
                "category": category,
                "is_income": (amt > 0 and category == "Ingresos y Nómina") or ("nomina" in desc_raw.lower() or "abono" in desc_raw.lower()),
            })

        if not parsed:
            return False, "No se encontraron transacciones válidas en el archivo."

        self._transactions = parsed
        record_audit("FINANCIAL_INGEST", target=source_name, result="SUCCESS", metadata={"records": len(parsed)})
        return True, f"Se cargaron exitosamente {len(parsed)} movimientos desde '{source_name}'."

    def _auto_classify(self, description: str, amount: float) -> str:
        d = description.lower()
        for cat, keywords in CATEGORY_RULES.items():
            if any(k in d for k in keywords):
                return cat
        return "Gastos Generales"

    def get_summary(self) -> Dict[str, Any]:
        """Generate high-level financial health summary, income vs expense, and net balance."""
        if not self._transactions:
            return {"error": "No hay transacciones cargadas para analizar."}

        total_income = 0.0
        total_expense = 0.0
        by_category: Dict[str, float] = {}

        for t in self._transactions:
            amt = abs(t["amount"])
            if t["is_income"]:
                total_income += amt
            else:
                total_expense += amt
                cat = t["category"]
                by_category[cat] = by_category.get(cat, 0.0) + amt

        net_balance = total_income - total_expense
        savings_rate = (net_balance / total_income * 100.0) if total_income > 0 else 0.0

        # Sorted spending categories
        sorted_cats = sorted(by_category.items(), key=lambda x: x[1], reverse=True)
        top_cats = [{"category": c, "amount": round(a, 2), "pct": round(a / max(total_expense, 1.0) * 100.0, 1)} for c, a in sorted_cats]

        return {
            "transaction_count": len(self._transactions),
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "net_balance": round(net_balance, 2),
            "savings_rate_pct": round(savings_rate, 1),
            "top_categories": top_cats,
            "highest_spending_category": sorted_cats[0][0] if sorted_cats else "N/A",
        }

    def detect_anomalies(self, threshold_z: float = 2.0) -> List[Dict[str, Any]]:
        """Identify statistical anomalies (unusually large or unexpected charges) using Z-score."""
        expenses = [abs(t["amount"]) for t in self._transactions if not t["is_income"]]
        if len(expenses) < 4:
            return []

        arr = np.array(expenses, dtype=float)
        mean_val = float(np.mean(arr))
        std_val = float(np.std(arr))
        if std_val < 1e-4:
            return []

        anomalies = []
        for t in self._transactions:
            if t["is_income"]:
                continue
            amt = abs(t["amount"])
            z = (amt - mean_val) / std_val
            if z >= threshold_z:
                anomalies.append({
                    "date": t["date"],
                    "description": t["description"],
                    "amount": round(amt, 2),
                    "category": t["category"],
                    "z_score": round(float(z), 2),
                    "deviation": f"{round(amt / max(mean_val, 1.0), 1)}x sobre el promedio habitual",
                })

        return sorted(anomalies, key=lambda x: x["amount"], reverse=True)

    def detect_recurring_expenses(self) -> List[Dict[str, Any]]:
        """Detect subscriptions and recurring payments across the transactions."""
        seen: Dict[str, List[float]] = {}
        for t in self._transactions:
            if t["is_income"]:
                continue
            # Normalize desc (first 2 words)
            words = re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ ]", " ", t["description"]).split()
            key = " ".join(words[:2]).lower() if words else t["description"].lower()
            seen.setdefault(key, []).append(abs(t["amount"]))

        recurring = []
        for key, amounts in seen.items():
            if len(amounts) >= 2:
                # Check consistency
                std = float(np.std(amounts))
                if std < 50.0:  # Consistent price
                    avg_amt = float(np.mean(amounts))
                    recurring.append({
                        "concept": key.title(),
                        "frequency": f"{len(amounts)} veces detectado",
                        "average_amount": round(avg_amt, 2),
                        "estimated_monthly": round(avg_amt, 2),
                    })
        return recurring

    def compare_periods(self, period1_keyword: str, period2_keyword: str) -> Dict[str, Any]:
        """Compare two timeframes or months (e.g. 'septiembre' vs 'octubre')."""
        p1 = [t for t in self._transactions if period1_keyword.lower() in t["date"].lower()]
        p2 = [t for t in self._transactions if period2_keyword.lower() in t["date"].lower()]

        exp1 = sum(abs(t["amount"]) for t in p1 if not t["is_income"])
        exp2 = sum(abs(t["amount"]) for t in p2 if not t["is_income"])
        diff = exp2 - exp1
        pct = (diff / max(exp1, 1.0) * 100.0) if exp1 > 0 else 0.0

        return {
            "period_1": {"name": period1_keyword.capitalize(), "expenses": round(exp1, 2), "count": len(p1)},
            "period_2": {"name": period2_keyword.capitalize(), "expenses": round(exp2, 2), "count": len(p2)},
            "difference": round(diff, 2),
            "percentage_change": round(pct, 1),
            "summary": (
                f"En {period2_keyword.capitalize()} gastaste ${exp2:,.2f} frente a ${exp1:,.2f} en {period1_keyword.capitalize()} "
                f"({'+' if diff > 0 else ''}{pct:.1f}% de variación)."
            ),
        }


# Global Financial Engine singleton
finance_engine = FinancialEngine()
