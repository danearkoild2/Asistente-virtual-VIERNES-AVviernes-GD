from __future__ import annotations

import threading
from typing import Any, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStackedWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class CleanYourTvOverlay(QWidget):
    """3-step visual wizard for Clean Your TV (Connect -> Analyse -> Clean & Restore)."""

    closed = pyqtSignal()
    _scan_done_sig = pyqtSignal(object)
    _connect_done_sig = pyqtSignal(object)
    _analyze_done_sig = pyqtSignal(object)
    _clean_done_sig = pyqtSignal(object)
    _restore_done_sig = pyqtSignal(object)

    _OW, _OH = 660, 610

    def __init__(self, initial_ip: str = "", parent=None) -> None:
        super().__init__(parent)
        self._ip = (initial_ip or "").strip()
        self._analysis: dict[str, Any] = {}
        self._pkg_checks: list[tuple[QCheckBox, str]] = []

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(
            "CleanYourTvOverlay { background: #121620; border: 1px solid #36415C; border-radius: 14px; }"
        )

        self._scan_done_sig.connect(self._on_scan_done)
        self._connect_done_sig.connect(self._on_connect_done)
        self._analyze_done_sig.connect(self._on_analyze_done)
        self._clean_done_sig.connect(self._on_clean_done)
        self._restore_done_sig.connect(self._on_restore_done)

        self._build_ui()
        if self._ip:
            self._ip_input.setText(self._ip)
        self._refresh_backups()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(12)

        # Header
        hdr = QHBoxLayout()
        t_col = QVBoxLayout()
        t_col.setSpacing(2)
        title = QLabel("Clean Your TV · Limpieza Segura para Android TV / Google TV")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setStyleSheet("color: #FFFFFF; background: transparent;")
        sub = QLabel("Basado en Clean Your TV (473 perfiles). Sin root, punto de restauración automático y 100% reversible.")
        sub.setFont(QFont("Segoe UI", 8))
        sub.setStyleSheet("color: #94A3B8; background: transparent;")
        t_col.addWidget(title)
        t_col.addWidget(sub)
        hdr.addLayout(t_col)
        hdr.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(
            "QPushButton { background: transparent; color: #94A3B8; border: 1px solid #242B3D; border-radius: 7px; }"
            "QPushButton:hover { color: #FFFFFF; border-color: #36415C; }"
        )
        close_btn.clicked.connect(self.closed.emit)
        hdr.addWidget(close_btn)
        root.addLayout(hdr)

        # 3-Step indicator bar
        step_row = QHBoxLayout()
        step_row.setSpacing(8)
        self._step_btns: list[QPushButton] = []
        for idx, label in enumerate(("1. Conectar TV", "2. Analizar Plan", "3. Limpiar y Restaurar")):
            b = QPushButton(label)
            b.setFixedHeight(30)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _=False, i=idx: self._set_step(i))
            self._step_btns.append(b)
            step_row.addWidget(b)
        root.addLayout(step_row)

        self._stack = QStackedWidget()
        self._stack.addWidget(self._build_step1())
        self._stack.addWidget(self._build_step2())
        self._stack.addWidget(self._build_step3())
        root.addWidget(self._stack, stretch=1)

        self._status_bar = QLabel("Listo. Paso 1: busca tu Android TV en el Wi-Fi o escribe su IP.")
        self._status_bar.setWordWrap(True)
        self._status_bar.setFont(QFont("Segoe UI", 9))
        self._status_bar.setStyleSheet(
            "background: #0B0D12; color: #38BDF8; border: 1px solid #242B3D; border-radius: 8px; padding: 8px 10px;"
        )
        root.addWidget(self._status_bar)

        self._set_step(0)

    def _set_step(self, idx: int) -> None:
        self._stack.setCurrentIndex(idx)
        for i, b in enumerate(self._step_btns):
            if i == idx:
                b.setStyleSheet(
                    "QPushButton { background: #1C1F3B; color: #6366F1; border: 1px solid #6366F1; border-radius: 8px; font-weight: 700; }"
                )
            else:
                b.setStyleSheet(
                    "QPushButton { background: #191F2E; color: #94A3B8; border: 1px solid #242B3D; border-radius: 8px; }"
                    "QPushButton:hover { color: #FFFFFF; }"
                )

    def _build_step1(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 4, 0, 0)
        lay.setSpacing(10)

        top = QHBoxLayout()
        self._ip_input = QLineEdit()
        self._ip_input.setPlaceholderText("IP del Android TV (ej. 192.168.1.45)")
        self._ip_input.setFixedHeight(32)
        self._ip_input.setStyleSheet(
            "QLineEdit { background: #07090D; color: #F1F5F9; border: 1px solid #242B3D; border-radius: 8px; padding: 0 10px; }"
        )
        top.addWidget(self._ip_input, stretch=1)

        self._scan_btn = QPushButton("Escanear Wi-Fi")
        self._scan_btn.setFixedHeight(32)
        self._scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._scan_btn.setStyleSheet(
            "QPushButton { background: #191F2E; color: #F1F5F9; border: 1px solid #36415C; border-radius: 8px; padding: 0 14px; font-weight: 600; }"
        )
        self._scan_btn.clicked.connect(self._do_scan)
        top.addWidget(self._scan_btn)

        self._conn_btn = QPushButton("Conectar y Analizar →")
        self._conn_btn.setFixedHeight(32)
        self._conn_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._conn_btn.setStyleSheet(
            "QPushButton { background: #6366F1; color: #FFFFFF; border: none; border-radius: 8px; padding: 0 14px; font-weight: 700; }"
        )
        self._conn_btn.clicked.connect(self._do_connect_and_analyze)
        top.addWidget(self._conn_btn)
        lay.addLayout(top)

        self._tv_list = QListWidget()
        self._tv_list.setMaximumHeight(110)
        self._tv_list.setStyleSheet(
            "QListWidget { background: #0B0D12; color: #E2E8F0; border: 1px solid #242B3D; border-radius: 8px; padding: 4px; }"
        )
        self._tv_list.itemClicked.connect(self._on_tv_picked)
        lay.addWidget(self._tv_list)

        guide = QTextEdit()
        guide.setReadOnly(True)
        guide.setStyleSheet(
            "QTextEdit { background: #0B0D12; color: #CBD5E1; border: 1px solid #242B3D; border-radius: 8px; padding: 8px; }"
        )
        from core.cleanyourtv import get_remote_instructions
        guide.setPlainText(
            "GUÍA CON EL CONTROL REMOTO:\n\n"
            + get_remote_instructions("enable_adb")
            + "\n\nCuando aparezca en el TV '¿Permitir depuración USB?', marca 'Permitir siempre' y pulsa OK."
        )
        lay.addWidget(guide, stretch=1)
        return w

    def _build_step2(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 4, 0, 0)
        lay.setSpacing(8)

        self._plan_hdr = QLabel("Ejecuta el análisis en el Paso 1 para ver qué anuncios y bloatware tiene tu TV.")
        self._plan_hdr.setWordWrap(True)
        self._plan_hdr.setStyleSheet("color: #E2E8F0; font-weight: 600; background: transparent;")
        lay.addWidget(self._plan_hdr)

        self._pkg_list = QListWidget()
        self._pkg_list.setStyleSheet(
            "QListWidget { background: #0B0D12; color: #E2E8F0; border: 1px solid #242B3D; border-radius: 8px; padding: 4px; }"
        )
        lay.addWidget(self._pkg_list, stretch=1)

        act_row = QHBoxLayout()
        sel_all = QPushButton("Marcar todos")
        sel_all.setFixedHeight(30)
        sel_all.setStyleSheet("QPushButton { background: #191F2E; color: #E2E8F0; border: 1px solid #36415C; border-radius: 7px; padding: 0 12px; }")
        sel_all.clicked.connect(lambda: self._toggle_all_pkgs(True))
        act_row.addWidget(sel_all)

        sel_none = QPushButton("Desmarcar")
        sel_none.setFixedHeight(30)
        sel_none.setStyleSheet("QPushButton { background: #191F2E; color: #E2E8F0; border: 1px solid #36415C; border-radius: 7px; padding: 0 12px; }")
        sel_none.clicked.connect(lambda: self._toggle_all_pkgs(False))
        act_row.addWidget(sel_none)

        act_row.addStretch()

        self._clean_btn = QPushButton("Make it Clean (Limpieza Segura) →")
        self._clean_btn.setFixedHeight(32)
        self._clean_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._clean_btn.setStyleSheet(
            "QPushButton { background: #10B981; color: #FFFFFF; border: none; border-radius: 8px; padding: 0 16px; font-weight: 700; }"
        )
        self._clean_btn.clicked.connect(self._do_clean)
        act_row.addWidget(self._clean_btn)
        lay.addLayout(act_row)
        return w

    def _build_step3(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 4, 0, 0)
        lay.setSpacing(10)

        self._result_box = QTextEdit()
        self._result_box.setReadOnly(True)
        self._result_box.setPlaceholderText("Aquí aparecerá el resumen de limpieza y restauración.")
        self._result_box.setStyleSheet(
            "QTextEdit { background: #0B0D12; color: #E2E8F0; border: 1px solid #242B3D; border-radius: 8px; padding: 8px; }"
        )
        lay.addWidget(self._result_box, stretch=1)

        r_row = QHBoxLayout()
        self._backup_combo = QComboBox()
        self._backup_combo.setFixedHeight(32)
        self._backup_combo.setStyleSheet(
            "QComboBox { background: #07090D; color: #F1F5F9; border: 1px solid #242B3D; border-radius: 8px; padding: 0 8px; }"
        )
        r_row.addWidget(self._backup_combo, stretch=1)

        self._restore_btn = QPushButton("Restaurar Punto Anterior")
        self._restore_btn.setFixedHeight(32)
        self._restore_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._restore_btn.setStyleSheet(
            "QPushButton { background: #F59E0B; color: #090806; border: none; border-radius: 8px; padding: 0 14px; font-weight: 700; }"
        )
        self._restore_btn.clicked.connect(self._do_restore)
        r_row.addWidget(self._restore_btn)
        lay.addLayout(r_row)
        return w

    def _set_status(self, msg: str, color: str = "#38BDF8") -> None:
        self._status_bar.setText(msg)
        self._status_bar.setStyleSheet(
            f"background: #0B0D12; color: {color}; border: 1px solid #242B3D; border-radius: 8px; padding: 8px 10px;"
        )

    def _do_scan(self) -> None:
        self._scan_btn.setEnabled(False)
        self._set_status("Escaneando la red Wi-Fi en busca de Android TVs (puerto ADB 5555)...")

        def _worker():
            from core.cleanyourtv import discover_android_tvs
            self._scan_done_sig.emit(discover_android_tvs())

        threading.Thread(target=_worker, daemon=True).start()

    def _on_scan_done(self, devs: list[dict[str, Any]]) -> None:
        self._scan_btn.setEnabled(True)
        self._tv_list.clear()
        if not devs:
            self._set_status("No se detectaron TVs con depuración de red activa. Sigue la guía del control remoto o ingresa la IP.", "#F59E0B")
            return
        for d in devs:
            it = QListWidgetItem(f"{d.get('model', 'Android TV')} — {d.get('ip')} ({d.get('state')})")
            it.setData(Qt.ItemDataRole.UserRole, d.get("ip"))
            self._tv_list.addItem(it)
        if not self._ip_input.text().strip():
            self._ip_input.setText(devs[0].get("ip", ""))
        self._set_status(f"Se encontraron {len(devs)} dispositivo(s). Selecciona uno y pulsa 'Conectar y Analizar'.", "#10B981")

    def _on_tv_picked(self, item: QListWidgetItem) -> None:
        ip = item.data(Qt.ItemDataRole.UserRole)
        if ip:
            self._ip_input.setText(str(ip))

    def _do_connect_and_analyze(self) -> None:
        ip = self._ip_input.text().strip()
        if not ip:
            self._set_status("Ingresa o selecciona la IP de tu televisor primero.", "#F59E0B")
            return
        self._conn_btn.setEnabled(False)
        self._set_status(f"Conectando y analizando paquetes en {ip}...")

        def _worker():
            from core.cleanyourtv import analyze_tv
            self._analyze_done_sig.emit(analyze_tv(ip))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_connect_done(self, res: dict[str, Any]) -> None:
        self._conn_btn.setEnabled(True)

    def _on_analyze_done(self, res: dict[str, Any]) -> None:
        self._conn_btn.setEnabled(True)
        if not res.get("ok"):
            self._set_status(res.get("message", "Error conectando al TV."), "#F59E0B")
            return

        self._analysis = res
        self._pkg_list.clear()
        self._pkg_checks.clear()

        cands = res.get("candidates") or []
        info = res.get("info") or {}
        self._plan_hdr.setText(
            f"TV: {info.get('manufacturer', '')} {info.get('model', '')} (Android {info.get('android_version', '?')}) · "
            f"Perfil: {res.get('profile_matched')} · {len(cands)} elementos recomendados para desactivar:"
        )
        for c in cands:
            item = QListWidgetItem()
            chk = QCheckBox(f"[{c['category']}] {c['package']} — {c['description']}")
            chk.setChecked(True)
            chk.setStyleSheet("color: #E2E8F0; background: transparent;")
            self._pkg_list.addItem(item)
            self._pkg_list.setItemWidget(item, chk)
            self._pkg_checks.append((chk, c["package"]))

        self._set_status(res.get("message", "Análisis listo."), "#10B981")
        self._set_step(1)

    def _toggle_all_pkgs(self, state: bool) -> None:
        for chk, _ in self._pkg_checks:
            chk.setChecked(state)

    def _do_clean(self) -> None:
        ip = self._ip_input.text().strip()
        selected = [pkg for chk, pkg in self._pkg_checks if chk.isChecked()]
        if not selected:
            self._set_status("Selecciona al menos un paquete para limpiar.", "#F59E0B")
            return
        self._clean_btn.setEnabled(False)
        self._set_status(f"Creando punto de restauración y desactivando {len(selected)} paquetes de forma segura...")

        def _worker():
            from core.cleanyourtv import clean_tv
            self._clean_done_sig.emit(clean_tv(ip, selected))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_clean_done(self, res: dict[str, Any]) -> None:
        self._clean_btn.setEnabled(True)
        self._set_step(2)
        self._refresh_backups()
        if not res.get("ok"):
            self._set_status(res.get("message", "Error durante la limpieza."), "#F43F5E")
            return
        disabled = res.get("disabled") or []
        failed = res.get("failed") or []
        lines = [res.get("message", ""), ""]
        if disabled:
            lines.append("Desactivados:")
            lines.extend(f"  ✓ {p}" for p in disabled)
        if failed:
            lines.append("\nOmitidos:")
            lines.extend(f"  - {f['package']}: {f['error']}" for f in failed)
        self._result_box.setPlainText("\n".join(lines))
        self._set_status(res.get("message", "Limpieza completada."), "#10B981")

    def _refresh_backups(self) -> None:
        from core.cleanyourtv import list_backups
        self._backup_combo.clear()
        for b in list_backups():
            lbl = f"{b.get('filename')} ({len(b.get('packages', []))} pkgs)"
            self._backup_combo.addItem(lbl, b.get("filename"))

    def _do_restore(self) -> None:
        ip = self._ip_input.text().strip()
        bfile = str(self._backup_combo.currentData() or "")
        if not ip or not bfile:
            self._set_status("Ingresa la IP del TV y selecciona un punto de restauración.", "#F59E0B")
            return
        self._restore_btn.setEnabled(False)
        self._set_status(f"Restaurando paquetes desde {bfile}...")

        def _worker():
            from core.cleanyourtv import restore_tv
            self._restore_done_sig.emit(restore_tv(ip, backup_file=bfile))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_restore_done(self, res: dict[str, Any]) -> None:
        self._restore_btn.setEnabled(True)
        if res.get("ok"):
            self._result_box.setPlainText(res.get("message", "Restauración completada."))
            self._set_status(res.get("message", "Restaurado."), "#10B981")
        else:
            self._set_status(res.get("message", "No se pudo restaurar."), "#F43F5E")
