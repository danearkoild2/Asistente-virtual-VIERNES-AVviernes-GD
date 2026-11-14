"""
Integrations Hub Overlay for VIERNES
=====================================
Comprehensive, interactive control center for all advanced integrations:
Gmail, Social Media, Financial Analytics, Smart Home, Real-Time Translation,
Voice Identification & RBAC, Safe Mode, Security Audit, and System Diagnostics.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPixmap
from PyQt6.QtWidgets import (
    QDialog, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QScrollArea, QTabWidget, QTextEdit, QVBoxLayout, QWidget,
    QFileDialog, QMessageBox, QComboBox, QInputDialog
)

from integrations.gmail.gmail_client import gmail
from integrations.social.social_manager import social_manager
from integrations.finance.financial_engine import finance_engine
from integrations.smarthome.smarthome_manager import smarthome
from integrations.smarthome.adapters.home_assistant import ha_client
from integrations.translation.translator import translator
from security.voice_id import voice_id_engine
from security.rbac import rbac
from security.safe_mode import is_safe_mode, set_safe_mode
from security.audit_logger import get_recent_audit_logs, record_audit
from system_monitor.windows_events import event_diagnostics
from system_monitor.anomaly_detector import anomaly_detector


class IntegrationsHubOverlay(QDialog):
    """Unified modal overlay for all advanced integrations."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Viernes — Centro de Integraciones y Seguridad")
        self.setModal(True)
        self.resize(880, 620)
        self.setStyleSheet("""
            QDialog {
                background: #17171C;
                color: #EEEEF0;
                border: 1px solid #272730;
            }
            QTabWidget::pane {
                border: 1px solid #272730;
                background: #111114;
                border-radius: 10px;
            }
            QTabBar::tab {
                background: #1F1F26;
                color: #A0A0AB;
                padding: 9px 16px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 600;
                font-size: 11px;
                font-family: 'Segoe UI', sans-serif;
            }
            QTabBar::tab:selected {
                background: #1E1D36;
                color: #6E6AF6;
                border-bottom: 2px solid #6E6AF6;
            }
            QTabBar::tab:hover {
                color: #FAF9F6;
            }
            QPushButton {
                background: #1F1F26;
                color: #EEEEF0;
                border: 1px solid #272730;
                border-radius: 8px;
                padding: 6px 14px;
                font-weight: 600;
                font-size: 11px;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background: #272730;
                border-color: #6E6AF6;
            }
            QPushButton#PrimaryAction {
                background: #6E6AF6;
                border-color: #6E6AF6;
                color: #FAF9F6;
            }
            QPushButton#PrimaryAction:hover {
                background: #5652D4;
            }
            QPushButton#DangerAction {
                background: #3A1F24;
                border-color: #F87171;
                color: #F87171;
            }
            QPushButton#DangerAction:hover {
                background: #52232B;
                color: #FAF9F6;
            }
            QFrame.CardFrame {
                background: #1F1F26;
                border: 1px solid #272730;
                border-radius: 10px;
                padding: 12px;
            }
            QLineEdit, QTextEdit, QComboBox {
                background: #0C0C0E;
                color: #EEEEF0;
                border: 1px solid #272730;
                border-radius: 6px;
                padding: 6px 10px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border: 1px solid #6E6AF6;
            }
        """)

        main_lay = QVBoxLayout(self)
        main_lay.setContentsMargins(18, 16, 18, 16)
        main_lay.setSpacing(12)

        # Header Title
        hdr_layout = QHBoxLayout()
        title_lbl = QLabel("Centro de integraciones y seguridad")
        title_lbl.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #FAF9F6;")
        hdr_layout.addWidget(title_lbl)
        hdr_layout.addStretch()

        btn_close = QPushButton("Cerrar")
        btn_close.clicked.connect(self.accept)
        hdr_layout.addWidget(btn_close)
        main_lay.addLayout(hdr_layout)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.addTab(self._build_gmail_tab(), "✉️ Gmail")
        self.tabs.addTab(self._build_social_tab(), "🌐 Redes Sociales")
        self.tabs.addTab(self._build_finance_tab(), "💰 Finanzas")
        self.tabs.addTab(self._build_smarthome_tab(), "🏠 Smart Home")
        self.tabs.addTab(self._build_translation_tab(), "🗣️ Traducción")
        self.tabs.addTab(self._build_voice_id_tab(), "🎙️ Voice ID & RBAC")
        self.tabs.addTab(self._build_security_tab(), "🛡️ Seguridad & Logs")
        self.tabs.addTab(self._build_system_tab(), "🖥️ Diagnóstico")
        main_lay.addWidget(self.tabs)

    # ── 1. GMAIL TAB ──────────────────────────────────────────────────────────
    def _build_gmail_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        # Status Banner
        status_box = QFrame()
        status_box.setProperty("class", "CardFrame")
        s_lay = QHBoxLayout(status_box)

        self._gmail_status_lbl = QLabel()
        self._update_gmail_status_label()
        s_lay.addWidget(self._gmail_status_lbl)
        s_lay.addStretch()

        btn_inbox = QPushButton("🌐 Abrir Gmail")
        btn_inbox.clicked.connect(lambda: gmail.open_in_gmail())
        s_lay.addWidget(btn_inbox)

        btn_disconnect = QPushButton("Desconectar")
        btn_disconnect.setObjectName("DangerAction")
        btn_disconnect.clicked.connect(self._on_gmail_disconnect)
        s_lay.addWidget(btn_disconnect)

        lay.addWidget(status_box)

        # Google SMTP / IMAP Configuration Card
        cfg_box = QFrame()
        cfg_box.setProperty("class", "CardFrame")
        c_lay = QVBoxLayout(cfg_box)
        c_lay.setSpacing(8)

        lbl_cfg_title = QLabel("CONFIGURACIÓN GOOGLE SMTP / IMAP DIRECTA")
        lbl_cfg_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        lbl_cfg_title.setStyleSheet("color: #38bdf8;")
        c_lay.addWidget(lbl_cfg_title)

        lbl_hint = QLabel(
            "Usa tu correo @gmail.com y una Contraseña de Aplicación de 16 caracteres generada en:\n"
            "myaccount.google.com/apppasswords. Funciona de inmediato sin trabas ni puertos de OAuth."
        )
        lbl_hint.setStyleSheet("color: #94a3b8; font-size: 11px;")
        c_lay.addWidget(lbl_hint)

        # Email row
        r1 = QHBoxLayout()
        r1.addWidget(QLabel("Correo Gmail:"))
        self._gmail_email_input = QLineEdit(gmail.account or "")
        self._gmail_email_input.setPlaceholderText("ejemplo@gmail.com")
        self._gmail_email_input.setStyleSheet("background: #020617; border: 1px solid #334155; padding: 6px; border-radius: 4px; color: #f8fafc;")
        r1.addWidget(self._gmail_email_input)
        c_lay.addLayout(r1)

        # Password row
        r2 = QHBoxLayout()
        r2.addWidget(QLabel("Contraseña de Aplicación:"))
        self._gmail_pass_input = QLineEdit()
        self._gmail_pass_input.setPlaceholderText("xxxx xxxx xxxx xxxx (16 caracteres)")
        self._gmail_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._gmail_pass_input.setStyleSheet("background: #020617; border: 1px solid #334155; padding: 6px; border-radius: 4px; color: #f8fafc;")
        r2.addWidget(self._gmail_pass_input)

        btn_show_pass = QPushButton("👁️")
        btn_show_pass.setFixedWidth(36)
        btn_show_pass.setToolTip("Mostrar / Ocultar contraseña")
        btn_show_pass.clicked.connect(self._toggle_gmail_pass_visibility)
        r2.addWidget(btn_show_pass)
        c_lay.addLayout(r2)

        # Action Buttons
        btn_row = QHBoxLayout()
        btn_save = QPushButton("🔗 Guardar y Probar Conexión (SMTP + IMAP)")
        btn_save.setObjectName("PrimaryAction")
        btn_save.clicked.connect(self._on_gmail_save_and_test)
        btn_row.addWidget(btn_save)

        btn_test_mail = QPushButton("✉️ Enviar Correo de Prueba")
        btn_test_mail.clicked.connect(self._on_gmail_send_test_email)
        btn_row.addWidget(btn_test_mail)

        btn_row.addStretch()
        c_lay.addLayout(btn_row)

        lay.addWidget(cfg_box)

        # Recent Emails Box
        lbl_recent = QLabel("BANDEJA DE ENTRADA Y CORREOS RECIENTES")
        lbl_recent.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        lbl_recent.setStyleSheet("color: #94a3b8;")
        lay.addWidget(lbl_recent)

        self._gmail_preview = QTextEdit()
        self._gmail_preview.setReadOnly(True)
        self._gmail_preview.setStyleSheet("background: #020617; border: 1px solid #1e293b; color: #cbd5e1; font-family: Consolas, monospace;")
        self._refresh_gmail_preview()
        lay.addWidget(self._gmail_preview, stretch=1)

        btn_refresh = QPushButton("↻ Actualizar Correos")
        btn_refresh.clicked.connect(self._refresh_gmail_preview)
        lay.addWidget(btn_refresh, alignment=Qt.AlignmentFlag.AlignRight)

        return w

    def _toggle_gmail_pass_visibility(self):
        if self._gmail_pass_input.echoMode() == QLineEdit.EchoMode.Password:
            self._gmail_pass_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self._gmail_pass_input.setEchoMode(QLineEdit.EchoMode.Password)

    def _update_gmail_status_label(self):
        st = gmail.get_status()
        if st["connected"]:
            self._gmail_status_lbl.setText(f"🟢 CONECTADO (Google SMTP/IMAP) — Cuenta: {st['account']}")
            self._gmail_status_lbl.setStyleSheet("color: #4ade80; font-weight: bold;")
        else:
            self._gmail_status_lbl.setText("⚪ NO CONECTADO (Configura tu correo y contraseña de aplicación)")
            self._gmail_status_lbl.setStyleSheet("color: #94a3b8; font-weight: bold;")

    def _on_gmail_save_and_test(self):
        email_val = self._gmail_email_input.text().strip()
        pass_val = self._gmail_pass_input.text().strip()

        if not email_val or not pass_val:
            QMessageBox.warning(self, "Gmail SMTP", "Por favor ingresa tanto tu correo Gmail como la contraseña de aplicación de 16 letras.")
            return

        ok, msg = gmail.set_credentials(email_val, pass_val)
        if ok:
            QMessageBox.information(self, "Google SMTP / IMAP Conectado", msg)
        else:
            QMessageBox.critical(self, "Error de Conexión Google", msg)

        self._update_gmail_status_label()
        self._refresh_gmail_preview()

    def _on_gmail_send_test_email(self):
        if not gmail.is_connected():
            QMessageBox.warning(self, "Gmail", "Primero debes conectar y guardar tus credenciales de Google SMTP.")
            return

        target_to, ok = QInputDialog.getText(
            self,
            "Enviar Correo de Prueba",
            "Destinatario (puedes enviar a ti mismo):",
            text=gmail.account
        )
        if ok and target_to.strip():
            sent_ok, msg = gmail.send_email(
                to=target_to.strip(),
                subject="Prueba de Integración VIERNES — Google SMTP",
                body=f"Hola,\n\nEste es un mensaje de prueba enviado exitosamente desde VIERNES mediante Google SMTP directo.\n\nFecha y hora: {Path(__file__).name}\nEstado: Operacional."
            )
            if sent_ok:
                QMessageBox.information(self, "Correo Enviado", f"Correo de prueba enviado con éxito a {target_to.strip()}.")
            else:
                QMessageBox.critical(self, "Fallo al Enviar", f"No se pudo enviar el correo: {msg}")

    def _on_gmail_disconnect(self):
        gmail.disconnect()
        self._gmail_email_input.clear()
        self._gmail_pass_input.clear()
        self._update_gmail_status_label()
        self._refresh_gmail_preview()
        QMessageBox.information(self, "Gmail", "Cuenta desconectada exitosamente y credenciales eliminadas.")

    def _refresh_gmail_preview(self):
        emails = gmail.list_recent_emails(max_results=8)
        if not emails:
            self._gmail_preview.setPlainText("No hay correos para mostrar o la bandeja está vacía.")
            return

        lines = []
        for i, m in enumerate(emails, 1):
            unread_badge = "🔴 NUEVO" if m.get("unread") else "⚪ LEÍDO"
            lines.append(f"[{i}] {unread_badge} | {m.get('date', '')}")
            lines.append(f"    De: {m.get('sender', '')}")
            lines.append(f"    Asunto: {m.get('subject', '')}")
            snippet = m.get('snippet', '')
            if snippet:
                lines.append(f"    Resumen: {snippet[:120]}...")
            lines.append("-" * 70)
        self._gmail_preview.setPlainText("\n".join(lines))

    # ── 2. SOCIAL MEDIA TAB ───────────────────────────────────────────────────
    def _build_social_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        # Overview Header
        summary_box = QFrame()
        summary_box.setProperty("class", "CardFrame")
        sb_lay = QVBoxLayout(summary_box)
        lbl_title = QLabel("RESUMEN MULTIPLATAFORMA DE RENDIMIENTO")
        lbl_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color: #38bdf8;")
        sb_lay.addWidget(lbl_title)

        self._social_summary_lbl = QLabel(social_manager.get_cross_platform_summary())
        self._social_summary_lbl.setWordWrap(True)
        self._social_summary_lbl.setStyleSheet("color: #f1f5f9; font-size: 12px; margin-top: 4px;")
        sb_lay.addWidget(self._social_summary_lbl)
        lay.addWidget(summary_box)

        # Platform Cards Grid
        self._social_grid_lay = QHBoxLayout()
        self._refresh_social_cards()
        lay.addLayout(self._social_grid_lay)

        # YouTube Setup Card
        yt_card = QFrame()
        yt_card.setProperty("class", "CardFrame")
        yt_lay = QVBoxLayout(yt_card)
        yt_lay.setSpacing(6)

        yt_title = QLabel("VINCULACIÓN DIRECTA DE YOUTUBE (DATA API V3)")
        yt_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        yt_title.setStyleSheet("color: #ef4444;")
        yt_lay.addWidget(yt_title)

        creds = social_manager.get_credentials().get("youtube", {})
        r_yt1 = QHBoxLayout()
        r_yt1.addWidget(QLabel("YouTube API Key:"))
        self._yt_api_key_input = QLineEdit(creds.get("api_key", ""))
        self._yt_api_key_input.setPlaceholderText("AIzaSy...")
        self._yt_api_key_input.setStyleSheet("background: #020617; border: 1px solid #334155; padding: 5px; border-radius: 4px; color: #f8fafc;")
        r_yt1.addWidget(self._yt_api_key_input)
        yt_lay.addLayout(r_yt1)

        r_yt2 = QHBoxLayout()
        r_yt2.addWidget(QLabel("Channel ID:"))
        self._yt_channel_input = QLineEdit(creds.get("channel_id", ""))
        self._yt_channel_input.setPlaceholderText("UCxxxxxxxxxxxxxxxx")
        self._yt_channel_input.setStyleSheet("background: #020617; border: 1px solid #334155; padding: 5px; border-radius: 4px; color: #f8fafc;")
        r_yt2.addWidget(self._yt_channel_input)
        yt_lay.addLayout(r_yt2)

        btn_yt_save = QPushButton("🔗 Guardar y Conectar Canal de YouTube")
        btn_yt_save.setObjectName("PrimaryAction")
        btn_yt_save.clicked.connect(self._on_save_youtube)
        yt_lay.addWidget(btn_yt_save, alignment=Qt.AlignmentFlag.AlignRight)

        lay.addWidget(yt_card)

        # Comments Requiring Attention
        lbl_c = QLabel("COMENTARIOS Y MENSAJES QUE REQUIEREN ATENCIÓN")
        lbl_c.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        lbl_c.setStyleSheet("color: #94a3b8;")
        lay.addWidget(lbl_c)

        self._social_comments = QTextEdit()
        self._social_comments.setReadOnly(True)
        self._social_comments.setStyleSheet("background: #020617; border: 1px solid #1e293b; color: #cbd5e1;")
        self._refresh_social_comments()
        lay.addWidget(self._social_comments, stretch=1)

        return w

    def _refresh_social_cards(self):
        while self._social_grid_lay.count():
            item = self._social_grid_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for p in social_manager.get_platforms_status():
            p_card = QFrame()
            p_card.setProperty("class", "CardFrame")
            pc_lay = QVBoxLayout(p_card)
            p_name = QLabel(p["name"])
            p_name.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            p_name.setStyleSheet("color: #f8fafc;")
            pc_lay.addWidget(p_name)

            if p["connected"]:
                status_str = "🟢 Conectado"
                color_css = "color: #4ade80;"
            else:
                status_str = "⚪ No configurado"
                color_css = "color: #94a3b8;"

            p_st = QLabel(status_str)
            p_st.setStyleSheet(f"{color_css} font-size: 11px; font-weight: bold;")
            pc_lay.addWidget(p_st)
            self._social_grid_lay.addWidget(p_card)

    def _refresh_social_comments(self):
        urgent = social_manager.get_attention_needed_comments()
        if urgent:
            c_lines = [f"• [{c.get('priority', 'MEDIA')}] {c.get('author')}: \"{c.get('comment')}\"" for c in urgent]
            self._social_comments.setPlainText("\n".join(c_lines))
        else:
            self._social_comments.setPlainText("No hay comentarios pendientes en tus cuentas conectadas.")

    def _on_save_youtube(self):
        api_k = self._yt_api_key_input.text().strip()
        ch_id = self._yt_channel_input.text().strip()

        ok, msg = social_manager.set_youtube_credentials(api_k, ch_id)
        if ok:
            QMessageBox.information(self, "YouTube Conectado", msg)
        else:
            QMessageBox.warning(self, "Error YouTube", msg)

        self._refresh_social_cards()
        self._refresh_social_comments()
        self._social_summary_lbl.setText(social_manager.get_cross_platform_summary())

    # ── 3. FINANCIAL TAB ──────────────────────────────────────────────────────
    def _build_finance_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        # Actions Bar
        act_bar = QHBoxLayout()
        btn_load = QPushButton("📁 Cargar Archivo CSV o Excel (.xlsx)")
        btn_load.setObjectName("PrimaryAction")
        btn_load.clicked.connect(self._on_load_finance_file)
        act_bar.addWidget(btn_load)
        act_bar.addStretch()

        sec_notice = QLabel("🔒 Modo Solo Lectura: Viernes nunca realiza pagos ni transferencias.")
        sec_notice.setStyleSheet("color: #eab308; font-size: 11px; font-weight: bold;")
        act_bar.addWidget(sec_notice)
        lay.addLayout(act_bar)

        # Summary Display
        self._finance_display = QTextEdit()
        self._finance_display.setReadOnly(True)
        self._finance_display.setStyleSheet("background: #020617; border: 1px solid #1e293b; color: #cbd5e1; font-family: Consolas, monospace;")
        self._update_finance_view()
        lay.addWidget(self._finance_display, stretch=1)

        return w

    def _on_load_finance_file(self):
        fpath, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo Financiero", "", "Archivos Financieros (*.csv *.xlsx *.tsv)")
        if fpath:
            ok, msg = finance_engine.load_file(fpath)
            QMessageBox.information(self, "Finanzas", msg)
            self._update_finance_view()

    def _update_finance_view(self):
        summary = finance_engine.get_summary()
        if "error" in summary:
            self._finance_display.setPlainText(
                "No hay datos financieros cargados.\n\n"
                "Para comenzar el análisis, haz clic en 'Cargar Archivo CSV o Excel (.xlsx)'\n"
                "o proporciona un estado de cuenta con fechas, conceptos e importes."
            )
            return

        anomalies = finance_engine.detect_anomalies()
        recurring = finance_engine.detect_recurring_expenses()

        lines = [
            "=" * 70,
            "                   INFORME FINANCIERO Y PRESUPUESTAL",
            "=" * 70,
            f"Transacciones analizadas: {summary['transaction_count']}",
            f"Ingresos Totales:        ${summary['total_income']:,.2f}",
            f"Gastos Totales:          ${summary['total_expense']:,.2f}",
            f"Balance Neto:            ${summary['net_balance']:,.2f}",
            f"Tasa de Ahorro:          {summary['savings_rate_pct']}%",
            "-" * 70,
            "DESGLOSE POR CATEGORÍAS:",
        ]
        for c in summary["top_categories"]:
            lines.append(f"  • {c['category']:<32} ${c['amount']:>10,.2f} ({c['pct']}%)")

        lines.extend(["-" * 70, "SUSCRIPCIONES Y GASTOS RECURRENTES:"])
        for r in recurring:
            lines.append(f"  • {r['concept']:<32} ~${r['average_amount']:>10,.2f} ({r['frequency']})")

        lines.extend(["-" * 70, "ALERTAS DE ANOMALÍAS O CARGOS EXTRAÑOS:"])
        if anomalies:
            for a in anomalies:
                lines.append(f"  ⚠️ {a['date']} | {a['description']:<26} ${a['amount']:>8,.2f} ({a['deviation']})")
        else:
            lines.append("  ✓ No se detectaron anomalías ni cargos atípicos.")

        self._finance_display.setPlainText("\n".join(lines))

    # ── 4. SMART HOME TAB ─────────────────────────────────────────────────────
    def _build_smarthome_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        # Home Assistant Setup Frame
        ha_box = QFrame()
        ha_box.setProperty("class", "CardFrame")
        ha_lay = QVBoxLayout(ha_box)
        ha_lay.setSpacing(6)

        ha_title = QLabel("CONEXIÓN A HARDWARE FÍSICO (HOME ASSISTANT REST API)")
        ha_title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        ha_title.setStyleSheet("color: #38bdf8;")
        ha_lay.addWidget(ha_title)

        ha_hint = QLabel(
            "Conecta tu instancia de Home Assistant (ej: http://homeassistant.local:8123) con un Token de Acceso\n"
            "de larga duración para controlar tus bombillas, enchufes y cerraduras físicas reales."
        )
        ha_hint.setStyleSheet("color: #94a3b8; font-size: 11px;")
        ha_lay.addWidget(ha_hint)

        r_ha1 = QHBoxLayout()
        r_ha1.addWidget(QLabel("URL Base:"))
        self._ha_url_input = QLineEdit(ha_client.base_url or "http://homeassistant.local:8123")
        self._ha_url_input.setStyleSheet("background: #020617; border: 1px solid #334155; padding: 5px; border-radius: 4px; color: #f8fafc;")
        r_ha1.addWidget(self._ha_url_input)
        ha_lay.addLayout(r_ha1)

        r_ha2 = QHBoxLayout()
        r_ha2.addWidget(QLabel("Token de Acceso:"))
        self._ha_tok_input = QLineEdit(ha_client.token or "")
        self._ha_tok_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._ha_tok_input.setPlaceholderText("eyJhbGciOiJIUzI1NiIsIn...")
        self._ha_tok_input.setStyleSheet("background: #020617; border: 1px solid #334155; padding: 5px; border-radius: 4px; color: #f8fafc;")
        r_ha2.addWidget(self._ha_tok_input)
        ha_lay.addLayout(r_ha2)

        r_ha_btns = QHBoxLayout()
        self._ha_status_lbl = QLabel()
        self._update_ha_status_label()
        r_ha_btns.addWidget(self._ha_status_lbl)
        r_ha_btns.addStretch()

        btn_ha_connect = QPushButton("🔗 Probar y Sincronizar")
        btn_ha_connect.setObjectName("PrimaryAction")
        btn_ha_connect.clicked.connect(self._on_ha_connect)
        r_ha_btns.addWidget(btn_ha_connect)

        btn_ha_disco = QPushButton("Desconectar HA")
        btn_ha_disco.setObjectName("DangerAction")
        btn_ha_disco.clicked.connect(self._on_ha_disconnect)
        r_ha_btns.addWidget(btn_ha_disco)
        ha_lay.addLayout(r_ha_btns)

        lay.addWidget(ha_box)

        # Quick Scenes
        sc_lay = QHBoxLayout()
        lbl_sc = QLabel("ESCENAS RÁPIDAS:")
        lbl_sc.setStyleSheet("font-weight: bold; color: #94a3b8;")
        sc_lay.addWidget(lbl_sc)

        for sc_id, sc_name in [("noche", "🌙 Modo Noche"), ("cine", "🎬 Modo Cine"), ("despertar", "☀️ Despertar")]:
            btn = QPushButton(sc_name)
            btn.clicked.connect(lambda _, s=sc_id: self._on_scene_clicked(s))
            sc_lay.addWidget(btn)
        sc_lay.addStretch()
        lay.addLayout(sc_lay)

        # Devices Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        cont = QWidget()
        self._dev_layout = QVBoxLayout(cont)
        self._dev_layout.setSpacing(8)
        self._refresh_smarthome_devices()
        scroll.setWidget(cont)
        lay.addWidget(scroll, stretch=1)

        return w

    def _update_ha_status_label(self):
        if ha_client.is_connected():
            self._ha_status_lbl.setText("🟢 Home Assistant Vinculado")
            self._ha_status_lbl.setStyleSheet("color: #4ade80; font-weight: bold;")
        else:
            self._ha_status_lbl.setText("⚪ Modo Simulado / Local")
            self._ha_status_lbl.setStyleSheet("color: #94a3b8; font-weight: bold;")

    def _on_ha_connect(self):
        url = self._ha_url_input.text().strip()
        tok = self._ha_tok_input.text().strip()

        ok, msg = ha_client.test_connection(url, tok)
        if ok:
            ha_client.save_credentials(url, tok)
            sync_ok, sync_msg = smarthome.sync_home_assistant()
            QMessageBox.information(self, "Home Assistant Conectado", f"{msg}\n\n{sync_msg}")
        else:
            QMessageBox.warning(self, "Error Home Assistant", msg)

        self._update_ha_status_label()
        self._refresh_smarthome_devices()

    def _on_ha_disconnect(self):
        ha_client.disconnect()
        self._ha_tok_input.clear()
        self._update_ha_status_label()
        self._refresh_smarthome_devices()
        QMessageBox.information(self, "Home Assistant", "Desconectado. Volviendo a simulación local persistente.")

    def _on_scene_clicked(self, scene_id: str):
        ok, msg = smarthome.execute_scene(scene_id)
        self._refresh_smarthome_devices()
        QMessageBox.information(self, "Escena Smart Home", msg)

    def _refresh_smarthome_devices(self):
        while self._dev_layout.count():
            item = self._dev_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        devs = smarthome.list_devices()
        for d in devs:
            row = QFrame()
            row.setProperty("class", "CardFrame")
            r_lay = QHBoxLayout(row)

            provider_tag = " [HA]" if d.get("provider") == "home_assistant" else " [Local]"
            info = QLabel(f"<b>{d['name']}</b> ({d['room']}){provider_tag} — <i>{d['type']}</i>")
            info.setStyleSheet("color: #e2e8f0; font-size: 11px;")
            r_lay.addWidget(info)
            r_lay.addStretch()

            if d["type"] == "lock":
                is_locked = d["state"].get("locked", True)
                btn = QPushButton("🔒 Bloqueada" if is_locked else "🔓 Abierta")
                btn.clicked.connect(lambda _, dev_id=d["id"], locked=is_locked: self._toggle_lock(dev_id, not locked))
                r_lay.addWidget(btn)
            elif d["type"] == "thermostat":
                curr_t = d["state"].get("temperature", 22.0)
                target_t = d["state"].get("target", 21.0)
                t_lbl = QLabel(f"🌡️ {curr_t}°C (Obj: {target_t}°C)")
                t_lbl.setStyleSheet("color: #38bdf8; font-weight: bold;")
                r_lay.addWidget(t_lbl)

                btn_minus = QPushButton("➖ 0.5°")
                btn_minus.clicked.connect(lambda _, dev_id=d["id"], t=target_t: self._adjust_temp(dev_id, t - 0.5))
                r_lay.addWidget(btn_minus)

                btn_plus = QPushButton("➕ 0.5°")
                btn_plus.clicked.connect(lambda _, dev_id=d["id"], t=target_t: self._adjust_temp(dev_id, t + 0.5))
                r_lay.addWidget(btn_plus)
            elif d["type"] == "light":
                is_on = d["is_on"]
                btn_p = QPushButton("Encendido" if is_on else "Apagado")
                btn_p.setObjectName("PrimaryAction" if is_on else "")
                btn_p.clicked.connect(lambda _, dev_id=d["id"], on=is_on: self._toggle_power(dev_id, not on))
                r_lay.addWidget(btn_p)

                # Brightness buttons
                for pct in [25, 50, 100]:
                    btn_b = QPushButton(f"{pct}%")
                    btn_b.setFixedWidth(40)
                    btn_b.clicked.connect(lambda _, dev_id=d["id"], b=pct: self._set_brightness(dev_id, b))
                    r_lay.addWidget(btn_b)
            else:
                is_on = d["is_on"]
                btn = QPushButton("Encendido" if is_on else "Apagado")
                btn.setObjectName("PrimaryAction" if is_on else "")
                btn.clicked.connect(lambda _, dev_id=d["id"], on=is_on: self._toggle_power(dev_id, not on))
                r_lay.addWidget(btn)

            self._dev_layout.addWidget(row)

    def _toggle_power(self, dev_id: str, new_power: bool):
        smarthome.set_device_state(dev_id, {"power": new_power})
        self._refresh_smarthome_devices()

    def _set_brightness(self, dev_id: str, brightness: int):
        smarthome.set_device_state(dev_id, {"power": True, "brightness": brightness})
        self._refresh_smarthome_devices()

    def _adjust_temp(self, dev_id: str, new_target: float):
        smarthome.set_device_state(dev_id, {"target": round(new_target, 1)})
        self._refresh_smarthome_devices()

    def _toggle_lock(self, dev_id: str, lock_state: bool):
        if not lock_state:
            confirm = QMessageBox.question(
                self,
                "Confirmación de Seguridad",
                "Esta acción desbloqueará una cerradura física del hogar. ¿Deseas autorizar la apertura?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm != QMessageBox.StandardButton.Yes:
                return
        smarthome.set_device_state(dev_id, {"locked": lock_state}, confirmed=True)
        self._refresh_smarthome_devices()

    # ── 5. TRANSLATION TAB ────────────────────────────────────────────────────
    def _build_translation_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        ctrl_lay = QHBoxLayout()
        ctrl_lay.addWidget(QLabel("Idioma Destino:"))
        self._tl_combo = QComboBox()
        self._tl_combo.addItems(["Inglés (en)", "Español (es)", "Francés (fr)", "Alemán (de)", "Italiano (it)", "Japonés (ja)"])
        ctrl_lay.addWidget(self._tl_combo)
        ctrl_lay.addStretch()

        btn_trans = QPushButton("🌐 Traducir Texto")
        btn_trans.setObjectName("PrimaryAction")
        btn_trans.clicked.connect(self._on_translate_click)
        ctrl_lay.addWidget(btn_trans)
        lay.addLayout(ctrl_lay)

        self._trans_input = QLineEdit()
        self._trans_input.setPlaceholderText("Escribe aquí el texto a traducir (se detectará el idioma de origen automáticamente)...")
        self._trans_input.setStyleSheet("background: #020617; border: 1px solid #1e293b; color: #f8fafc; padding: 8px;")
        lay.addWidget(self._trans_input)

        self._trans_card_view = QTextEdit()
        self._trans_card_view.setReadOnly(True)
        self._trans_card_view.setStyleSheet("background: #020617; border: 1px solid #1e293b; color: #38bdf8; font-family: Consolas, monospace; font-size: 13px;")
        self._trans_card_view.setPlainText("El resultado de la traducción en vivo se mostrará aquí.")
        lay.addWidget(self._trans_card_view, stretch=1)

        return w

    def _on_translate_click(self):
        txt = self._trans_input.text().strip()
        if not txt:
            return
        combo_txt = self._tl_combo.currentText()
        target_code = combo_txt.split("(")[-1].replace(")", "").strip()
        res = translator.translate(txt, target_lang=target_code)
        card = translator.format_live_card(res)
        self._trans_card_view.setPlainText(card)

    # ── 6. VOICE ID & RBAC TAB ────────────────────────────────────────────────
    def _build_voice_id_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        # Active Speaker Status
        info_box = QFrame()
        info_box.setProperty("class", "CardFrame")
        ib_lay = QHBoxLayout(info_box)

        act = voice_id_engine.get_active_speaker_info()
        self._spk_lbl = QLabel(f"🎙️ HABLANTE ACTIVO: {act['speaker']} (Rol: {act['role']} | Confianza: {int(act['confidence']*100)}%)")
        self._spk_lbl.setStyleSheet("color: #4ade80; font-weight: bold; font-size: 12px;")
        ib_lay.addWidget(self._spk_lbl)
        ib_lay.addStretch()

        btn_enroll = QPushButton("Enrolar Muestra de Voz")
        btn_enroll.clicked.connect(self._on_enroll_voice)
        ib_lay.addWidget(btn_enroll)
        lay.addWidget(info_box)

        # RBAC Roles Table
        lbl_users = QLabel("USUARIOS REGISTRADOS Y PERMISOS RBAC")
        lbl_users.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        lbl_users.setStyleSheet("color: #94a3b8;")
        lay.addWidget(lbl_users)

        self._rbac_view = QTextEdit()
        self._rbac_view.setReadOnly(True)
        self._rbac_view.setStyleSheet("background: #020617; border: 1px solid #1e293b; color: #cbd5e1; font-family: Consolas, monospace;")
        self._refresh_rbac_view()
        lay.addWidget(self._rbac_view, stretch=1)

        return w

    def _on_enroll_voice(self):
        QMessageBox.information(
            self,
            "Enrolamiento de Voz",
            "Habla hacia tu micrófono durante 3 segundos para calibrar el perfil acústico de Jesús (Creador)."
        )

    def _refresh_rbac_view(self):
        users = rbac.get_users()
        lines = [
            f"{'USUARIO':<16} {'ROL':<12} {'ESTADO DE VOZ':<16} {'PERMISOS DESTACADOS'}",
            "=" * 70,
        ]
        for name, data in users.items():
            enrolled = "✓ Calibrado" if data.get("voice_enrolled") else "⚪ No enrolado"
            role = data.get("role", "GUEST")
            perms = "Gmail, Finanzas, SmartHome, Sistema" if role == "CREATOR" else ("SmartHome Seguro, Traducción" if role == "USER" else "Traducción, Consultas")
            lines.append(f"{name:<16} {role:<12} {enrolled:<16} {perms}")
        self._rbac_view.setPlainText("\n".join(lines))

    # ── 7. SECURITY & AUDIT TAB ───────────────────────────────────────────────
    def _build_security_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        # Safe mode toggle bar
        sm_bar = QHBoxLayout()
        self._safe_mode_lbl = QLabel(f"🛡️ MODO SEGURO: {'ACTIVADO' if is_safe_mode() else 'DESACTIVADO'}")
        self._safe_mode_lbl.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 12px;")
        sm_bar.addWidget(self._safe_mode_lbl)
        sm_bar.addStretch()

        btn_toggle_sm = QPushButton("Alternar Modo Seguro")
        btn_toggle_sm.clicked.connect(self._on_toggle_safe_mode)
        sm_bar.addWidget(btn_toggle_sm)
        lay.addLayout(sm_bar)

        # Audit logs view
        lbl_audit = QLabel("HISTORIAL DE AUDITORÍA Y TRAZABILIDAD DE ACCIONES")
        lbl_audit.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        lbl_audit.setStyleSheet("color: #94a3b8;")
        lay.addWidget(lbl_audit)

        self._audit_view = QTextEdit()
        self._audit_view.setReadOnly(True)
        self._audit_view.setStyleSheet("background: #020617; border: 1px solid #1e293b; color: #cbd5e1; font-family: Consolas, monospace; font-size: 11px;")
        self._refresh_audit_logs()
        lay.addWidget(self._audit_view, stretch=1)

        btn_refresh_audit = QPushButton("↻ Actualizar Historial")
        btn_refresh_audit.clicked.connect(self._refresh_audit_logs)
        lay.addWidget(btn_refresh_audit, alignment=Qt.AlignmentFlag.AlignRight)

        return w

    def _on_toggle_safe_mode(self):
        new_val = not is_safe_mode()
        set_safe_mode(new_val)
        self._safe_mode_lbl.setText(f"🛡️ MODO SEGURO: {'ACTIVADO' if new_val else 'DESACTIVADO'}")
        record_audit("SAFE_MODE_TOGGLE", result="SUCCESS", metadata={"enabled": new_val})
        self._refresh_audit_logs()

    def _refresh_audit_logs(self):
        logs = get_recent_audit_logs(limit=25)
        lines = []
        for l in logs:
            res_col = "🟢" if l.get("result") == "SUCCESS" else ("🔴" if l.get("result") == "DENIED" else "🟡")
            lines.append(f"[{l.get('timestamp')}] {res_col} {l.get('user')} ({l.get('role')}) ➔ {l.get('action')} | Destino: {l.get('target')}")
            if l.get("reason"):
                lines.append(f"    Razón: {l.get('reason')}")
        self._audit_view.setPlainText("\n".join(lines) if lines else "Sin registros de auditoría aún.")

    # ── 8. SYSTEM DIAGNOSTICS TAB ─────────────────────────────────────────────
    def _build_system_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        # Health header
        hl_box = QFrame()
        hl_box.setProperty("class", "CardFrame")
        hl_lay = QHBoxLayout(hl_box)

        res = anomaly_detector.scan_anomalies()
        self._health_lbl = QLabel(f"🖥️ SALUD DEL SISTEMA: {res['health_score']:.0f}%")
        self._health_lbl.setStyleSheet("color: #4ade80; font-weight: bold; font-size: 13px;")
        hl_lay.addWidget(self._health_lbl)
        hl_lay.addStretch()

        btn_scan = QPushButton("🔍 Escanear Ahora")
        btn_scan.setObjectName("PrimaryAction")
        btn_scan.clicked.connect(self._on_scan_system)
        hl_lay.addWidget(btn_scan)
        lay.addWidget(hl_box)

        # Diagnostics output
        self._diag_view = QTextEdit()
        self._diag_view.setReadOnly(True)
        self._diag_view.setStyleSheet("background: #020617; border: 1px solid #1e293b; color: #cbd5e1; font-family: Consolas, monospace; font-size: 11px;")
        self._update_system_diag_view(res)
        lay.addWidget(self._diag_view, stretch=1)

        return w

    def _on_scan_system(self):
        res = anomaly_detector.scan_anomalies()
        self._health_lbl.setText(f"🖥️ SALUD DEL SISTEMA: {res['health_score']:.0f}%")
        self._update_system_diag_view(res)

    def _update_system_diag_view(self, res: Dict[str, Any]):
        clusters = event_diagnostics.analyze_event_clusters()
        lines = [
            "=" * 70,
            f"          DIAGNÓSTICO DE REGISTROS DE EVENTOS Y ANOMALÍAS",
            "=" * 70,
            res.get("summary", ""),
            "-" * 70,
            "ANOMALÍAS ACTIVAS DETECTADAS:",
        ]
        for a in res.get("anomalies", []):
            lines.append(f"  • [{a['severity']}] {a['detail']}")
            lines.append(f"    Sugerencia: {a['recommendation']}")

        lines.extend(["-" * 70, "RESUMEN DE ERRORES Y ADVERTENCIAS DE WINDOWS (SYSTEM & APPLICATION):"])
        for cl in clusters.get("clusters", [])[:6]:
            lines.append(f"  • {cl['source']} ({cl['count']} eventos): {cl['possible_cause']}")

        self._diag_view.setPlainText("\n".join(lines))
