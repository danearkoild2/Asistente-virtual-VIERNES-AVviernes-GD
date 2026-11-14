"""
Viernes — Advanced Research UI Overlay Panel
=============================================
Futuristic, cyberpunk-themed interactive research panel.
Provides:
- Universal multi-engine query input with category selection
- Live multi-stage progress tracking (Plan -> SerpApi -> Read -> Synthesize)
- Interactive sources list with domain badges and direct browser links
- Formatted markdown report viewer with clickable citations
- Single URL extractor tab (Web Fetch)
- SerpApi API key configuration dialog
"""

from __future__ import annotations

import os
import threading
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from PyQt6.QtCore import QSize, Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QColor, QDesktopServices, QFont, QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QTabWidget,
    QTextBrowser,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from core.research.researcher import ResearchEngine, ResearchReport
from core.research.serpapi_client import SerpApiClient
from core.research.web_reader import WebReader
from memory.config_manager import get_serpapi_key, save_serpapi_key


class ResearchOverlay(QWidget):
    """Full-featured floating/modal research workstation inside Viernes."""

    research_completed = pyqtSignal(object)
    research_progress = pyqtSignal(str, str, object)
    close_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ResearchOverlay")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.hide()

        self._serp = SerpApiClient.get_instance()
        self._reader = WebReader()
        self._engine = ResearchEngine(self._serp, self._reader)
        self._current_report: Optional[ResearchReport] = None
        self._is_running = False

        self._setup_ui()
        self.research_progress.connect(self._on_progress_ui)
        self.research_completed.connect(self._on_completed_ui)

    def _setup_ui(self):
        # Contemporary editorial theme styling
        self.setStyleSheet("""
            QWidget#ResearchOverlay {
                background: #17171C;
                border: 1px solid #272730;
                border-radius: 14px;
            }
            QLabel {
                color: #EEEEF0;
                background: transparent;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit, QComboBox, QTextEdit, QTextBrowser {
                background: #0C0C0E;
                color: #EEEEF0;
                border: 1px solid #272730;
                border-radius: 8px;
                padding: 6px 10px;
                font-family: 'Segoe UI', sans-serif;
                selection-background-color: #6E6AF6;
            }
            QLineEdit:focus, QComboBox:focus, QTextBrowser:focus {
                border: 1px solid #6E6AF6;
            }
            QPushButton {
                background: #1F1F26;
                color: #EEEEF0;
                border: 1px solid #272730;
                border-radius: 8px;
                padding: 6px 12px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: 600;
            }
            QPushButton:hover {
                background: #272730;
                border-color: #6E6AF6;
                color: #FAF9F6;
            }
            QPushButton:pressed {
                background: #1E1D36;
            }
            QTabWidget::pane {
                border: 1px solid #272730;
                background: #111114;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #1F1F26;
                color: #A0A0AB;
                border: 1px solid #272730;
                border-bottom: none;
                padding: 7px 14px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
                font-weight: 600;
            }
            QTabBar::tab:selected {
                background: #1E1D36;
                color: #6E6AF6;
                border-color: #6E6AF6;
            }
            QProgressBar {
                border: 1px solid #272730;
                border-radius: 4px;
                background: #0C0C0E;
                text-align: center;
                color: #EEEEF0;
                height: 14px;
                font-size: 9px;
                font-family: 'Segoe UI', sans-serif;
            }
            QProgressBar::chunk {
                background: #6E6AF6;
                border-radius: 3px;
            }
            QScrollBar:vertical {
                background: transparent; width: 6px; border: none;
            }
            QScrollBar::handle:vertical {
                background: #353542; border-radius: 3px; min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #6E6AF6;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        # ── 1. Top Header ────────────────────────────────────────────────────
        hdr = QHBoxLayout()
        hdr.setSpacing(8)

        title_lbl = QLabel("Investigación web avanzada")
        title_lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #FAF9F6;")
        hdr.addWidget(title_lbl)

        hdr.addStretch()

        self._status_badge = QLabel()
        self._status_badge.setFont(QFont("Segoe UI", 8, QFont.Weight.DemiBold))
        self._refresh_key_badge()
        hdr.addWidget(self._status_badge)

        self._key_cfg_btn = QPushButton("Clave API")
        self._key_cfg_btn.setFixedHeight(26)
        self._key_cfg_btn.setFont(QFont("Segoe UI", 8))
        self._key_cfg_btn.clicked.connect(self._prompt_key_dialog)
        hdr.addWidget(self._key_cfg_btn)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(26, 26)
        close_btn.setStyleSheet("""
            QPushButton {
                background: #1F1F26; color: #A0A0AB; border: 1px solid #272730; border-radius: 6px; padding: 0;
            }
            QPushButton:hover { background: #3A1F24; color: #F87171; border-color: #F87171; }
        """)
        close_btn.clicked.connect(self.hide)
        hdr.addWidget(close_btn)

        layout.addLayout(hdr)

        # Separator
        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setStyleSheet("color: #272730;")
        layout.addWidget(sep1)

        # ── 2. Search & Engine Controls ──────────────────────────────────────
        search_box = QHBoxLayout()
        search_box.setSpacing(8)

        self._query_input = QLineEdit()
        self._query_input.setPlaceholderText("Introduce tema a investigar (ej: Avances recientes en computación cuántica)...")
        self._query_input.setFixedHeight(34)
        self._query_input.setFont(QFont("Segoe UI", 9))
        self._query_input.returnPressed.connect(self._start_research)
        search_box.addWidget(self._query_input, stretch=4)

        self._cat_combo = QComboBox()
        self._cat_combo.setFixedHeight(34)
        self._cat_combo.setFont(QFont("Segoe UI", 8))
        self._cat_combo.addItem("🌐 Universal / Web", "general")
        self._cat_combo.addItem("📰 Noticias recientes", "news")
        self._cat_combo.addItem("🎓 Scholar & Papers", "scholar")
        self._cat_combo.addItem("💻 Tech & GitHub", "tech")
        self._cat_combo.addItem("🛍 Productos & Precios", "products")
        self._cat_combo.addItem("🎬 Videos / YouTube", "media")
        search_box.addWidget(self._cat_combo, stretch=2)

        self._btn_start = QPushButton("Investigar")
        self._btn_start.setFixedHeight(34)
        self._btn_start.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
        self._btn_start.setStyleSheet("""
            QPushButton {
                background: #6E6AF6; color: #FAF9F6; border: none; border-radius: 8px; padding: 0 14px;
            }
            QPushButton:hover { background: #5652D4; }
        """)
        self._btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_start.clicked.connect(self._start_research)
        search_box.addWidget(self._btn_start, stretch=1)

        layout.addLayout(search_box)

        # ── 3. Live Progress Tracker & Subqueries Chips ───────────────────────
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setTextVisible(True)
        self._progress_bar.setFormat("Listo para investigar")
        self._progress_bar.setFixedHeight(14)
        layout.addWidget(self._progress_bar)

        self._chips_label = QLabel("Subconsultas: (esperando consulta)")
        self._chips_label.setFont(QFont("Segoe UI", 8))
        self._chips_label.setStyleSheet("color: #A0A0AB; padding: 2px 0;")
        self._chips_label.setWordWrap(True)
        layout.addWidget(self._chips_label)

        # ── 4. Main Tabs (Report, Sources, URL Reader) ────────────────────────
        self._tabs = QTabWidget()

        # Tab 1: Synthesized Report View
        self._report_browser = QTextBrowser()
        self._report_browser.setOpenExternalLinks(True)
        self._report_browser.setFont(QFont("Segoe UI", 9))
        self._report_browser.setPlaceholderText("El informe detallado de investigación con citas verificadas aparecerá aquí.")
        self._tabs.addTab(self._report_browser, "📄 Informe sintetizado")

        # Tab 2: Sources Interactive List
        self._sources_scroll = QScrollArea()
        self._sources_scroll.setWidgetResizable(True)
        self._sources_widget = QWidget()
        self._sources_layout = QVBoxLayout(self._sources_widget)
        self._sources_layout.setContentsMargins(8, 8, 8, 8)
        self._sources_layout.setSpacing(6)
        self._sources_layout.addStretch()
        self._sources_scroll.setWidget(self._sources_widget)
        self._tabs.addTab(self._sources_scroll, "🌐 Fuentes consultadas (0)")

        # Tab 3: Direct Web Fetch
        url_fetch_tab = QWidget()
        uf_lay = QVBoxLayout(url_fetch_tab)
        uf_lay.setContentsMargins(10, 10, 10, 10)
        uf_lay.setSpacing(8)

        uf_hdr = QHBoxLayout()
        self._url_input = QLineEdit()
        self._url_input.setPlaceholderText("https://ejemplo.com/articulo-o-noticia...")
        self._url_input.setFixedHeight(30)
        uf_hdr.addWidget(self._url_input, stretch=4)

        btn_fetch = QPushButton("Leer y extraer")
        btn_fetch.setFixedHeight(30)
        btn_fetch.clicked.connect(self._fetch_single_url)
        uf_hdr.addWidget(btn_fetch, stretch=1)
        uf_lay.addLayout(uf_hdr)

        self._url_result_browser = QTextBrowser()
        self._url_result_browser.setOpenExternalLinks(True)
        self._url_result_browser.setFont(QFont("Segoe UI", 9))
        self._url_result_browser.setPlaceholderText("El contenido limpio de la página extraída se mostrará aquí...")
        uf_lay.addWidget(self._url_result_browser, stretch=1)

        self._tabs.addTab(url_fetch_tab, "🔍 Lector de URL específica")

        layout.addWidget(self._tabs, stretch=1)

        # ── 5. Action Footer ─────────────────────────────────────────────────
        foot = QHBoxLayout()
        foot.setSpacing(8)

        self._time_lbl = QLabel("Duración: --")
        self._time_lbl.setFont(QFont("Segoe UI", 8))
        self._time_lbl.setStyleSheet("color: #6E6E7A;")
        foot.addWidget(self._time_lbl)

        foot.addStretch()

        btn_copy = QPushButton("Copiar informe")
        btn_copy.setFixedHeight(28)
        btn_copy.setFont(QFont("Segoe UI", 8))
        btn_copy.clicked.connect(self._copy_report)
        foot.addWidget(btn_copy)

        btn_save = QPushButton("Guardar Markdown")
        btn_save.setFixedHeight(28)
        btn_save.setFont(QFont("Segoe UI", 8))
        btn_save.clicked.connect(self._save_report)
        foot.addWidget(btn_save)

        layout.addLayout(foot)

    def _refresh_key_badge(self):
        if self._serp.is_configured():
            self._status_badge.setText("● SerpApi activo")
            self._status_badge.setStyleSheet("color: #34D399; background: rgba(52, 211, 153, 0.12); border: 1px solid rgba(52, 211, 153, 0.35); border-radius: 6px; padding: 2px 8px;")
        else:
            self._status_badge.setText("○ Modo alternativo (DDG)")
            self._status_badge.setStyleSheet("color: #E07A5F; background: rgba(224, 122, 95, 0.12); border: 1px solid rgba(224, 122, 95, 0.35); border-radius: 6px; padding: 2px 8px;")

    def _prompt_key_dialog(self):
        from PyQt6.QtWidgets import QInputDialog
        cur_key = get_serpapi_key()
        masked = (cur_key[:6] + "..." + cur_key[-4:]) if len(cur_key) > 10 else cur_key
        text, ok = QInputDialog.getText(
            self,
            "Configurar SerpApi",
            "Introduce tu clave de API de SerpApi (https://serpapi.com):\n(Si se deja en blanco, Viernes utilizará el motor alternativo)",
            QLineEdit.EchoMode.Normal,
            cur_key
        )
        if ok:
            save_serpapi_key(text.strip())
            self._refresh_key_badge()
            QMessageBox.information(self, "SerpApi", "Configuración de clave de búsqueda actualizada exitosamente.")

    def _start_research(self):
        topic = self._query_input.text().strip()
        if not topic:
            return
        if self._is_running:
            return

        self._is_running = True
        self._btn_start.setEnabled(False)
        self._btn_start.setText("⌛ INVESTIGANDO...")
        self._progress_bar.setValue(5)
        self._progress_bar.setFormat("Iniciando investigación...")
        self._report_browser.setPlaceholderText("Investigación en curso, consultando fuentes...")
        self._report_browser.clear()
        self._clear_sources_list()

        category = self._cat_combo.currentData() or "general"

        def _worker():
            def _prog(stage, msg, data):
                self.research_progress.emit(stage, msg, data)

            try:
                report = self._engine.research(
                    topic=topic,
                    category=category,
                    on_progress=_prog,
                )
                self.research_completed.emit(report)
            except Exception as e:
                self.research_progress.emit("ERROR", f"Error: {e}", {})
                self.research_completed.emit(None)

        threading.Thread(target=_worker, daemon=True).start()

    def _on_progress_ui(self, stage: str, msg: str, data: Any):
        self._progress_bar.setFormat(msg)
        if stage == "PLANNING":
            self._progress_bar.setValue(15)
        elif stage == "PLANNED":
            self._progress_bar.setValue(25)
            sqs = data.get("sub_queries", [])
            if sqs:
                self._chips_label.setText("Subconsultas: " + " | ".join(f"[Q: {q}]" for q in sqs))
        elif stage == "SEARCHING":
            self._progress_bar.setValue(45)
        elif stage == "SEARCH_DONE":
            self._progress_bar.setValue(60)
        elif stage == "READING":
            idx = data.get("index", 1)
            total = data.get("total", 1)
            pct = 60 + int((idx / max(total, 1)) * 25)
            self._progress_bar.setValue(min(pct, 85))
        elif stage == "ANALYZING":
            self._progress_bar.setValue(90)
        elif stage == "COMPLETE":
            self._progress_bar.setValue(100)
            self._progress_bar.setFormat("Investigación completada")

    def _on_completed_ui(self, report: Optional[ResearchReport]):
        self._is_running = False
        self._btn_start.setEnabled(True)
        self._btn_start.setText("🔬 INVESTIGAR")

        if not report:
            self._progress_bar.setFormat("Fallo en la investigación")
            return

        self._current_report = report
        self._time_lbl.setText(f"Duración: {report.duration_sec:.1f}s | Motor: {report.provider}")

        # Render Markdown report
        self._report_browser.setMarkdown(report.full_report)

        # Render Sources list
        self._render_sources_list(report.sources)

        # Switch to Report tab
        self._tabs.setCurrentIndex(0)

    def _clear_sources_list(self):
        while self._sources_layout.count() > 1:
            item = self._sources_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._tabs.setTabText(1, "🌐 Fuentes Consultadas (0)")

    def _render_sources_list(self, sources: List[Dict[str, Any]]):
        self._clear_sources_list()
        self._tabs.setTabText(1, f"🌐 Fuentes consultadas ({len(sources)})")

        for s in sources:
            card = QWidget()
            card.setStyleSheet("""
                background: #17171C;
                border: 1px solid #272730;
                border-radius: 8px;
                padding: 6px;
            """)
            c_lay = QVBoxLayout(card)
            c_lay.setContentsMargins(10, 8, 10, 8)
            c_lay.setSpacing(4)

            top = QHBoxLayout()
            badge = QLabel(f"[{s.get('id', 1)}] {s.get('domain', '')}")
            badge.setFont(QFont("Segoe UI", 8, QFont.Weight.DemiBold))
            badge.setStyleSheet("color: #6E6AF6; background: #1E1D36; border: 1px solid #6E6AF6; border-radius: 4px; padding: 1px 6px;")
            top.addWidget(badge)
            top.addStretch()

            link_btn = QPushButton("Abrir enlace")
            link_btn.setFixedHeight(22)
            link_btn.setFont(QFont("Segoe UI", 8))
            link_url = s.get("link", "")
            link_btn.clicked.connect(lambda _, u=link_url: QDesktopServices.openUrl(QUrl(u)))
            top.addWidget(link_btn)
            c_lay.addLayout(top)

            title_l = QLabel(s.get("title", ""))
            title_l.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))
            title_l.setStyleSheet("color: #FAF9F6;")
            title_l.setWordWrap(True)
            c_lay.addWidget(title_l)

            if s.get("snippet"):
                snip_l = QLabel(s.get("snippet", ""))
                snip_l.setFont(QFont("Segoe UI", 8))
                snip_l.setStyleSheet("color: #A0A0AB;")
                snip_l.setWordWrap(True)
                c_lay.addWidget(snip_l)

            self._sources_layout.insertWidget(self._sources_layout.count() - 1, card)

    def _fetch_single_url(self):
        url = self._url_input.text().strip()
        if not url:
            return

        self._url_result_browser.setMarkdown(f"⏳ Extrayendo contenido de: {url}...")

        def _worker():
            page = self._reader.fetch_page(url, try_playwright_if_empty=True)
            if page.error:
                res = f"### ❌ Error al leer la página\nURL: {url}\n\nDetalle: {page.error}"
            else:
                res = (
                    f"### 📄 {page.title}\n"
                    f"**URL:** [{url}]({url})  \n"
                    f"**Palabras extraídas:** {page.word_count}  \n"
                    f"**Modo:** {'Dinámico (Playwright JS)' if page.is_dynamic else 'Estático (HTTP HTML)'}\n\n"
                    f"---\n\n{page.text}"
                )
            self.research_progress.emit("URL_FETCH_DONE", res, {})

        def on_ui(stage, res, data):
            if stage == "URL_FETCH_DONE":
                self._url_result_browser.setMarkdown(res)

        self.research_progress.connect(on_ui)
        threading.Thread(target=_worker, daemon=True).start()

    def _copy_report(self):
        if self._current_report:
            QApplication.clipboard().setText(self._current_report.full_report)
            QMessageBox.information(self, "Portapapeles", "Informe copiado al portapapeles.")

    def _save_report(self):
        if not self._current_report:
            return
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Informe de Investigación",
            f"Informe_{self._current_report.topic[:20].replace(' ', '_')}.md",
            "Markdown (*.md);;Texto (*.txt)"
        )
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self._current_report.full_report)
                QMessageBox.information(self, "Guardado", f"Informe guardado en:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo: {e}")

    def display_report(self, report_dict: Dict[str, Any]):
        """Load and display an externally completed research report (e.g. from voice command)."""
        report = ResearchReport(
            topic=report_dict.get("topic", ""),
            category=report_dict.get("category", "general"),
            sub_queries=report_dict.get("sub_queries", []),
            sources=report_dict.get("sources", []),
            summary=report_dict.get("summary", ""),
            full_report=report_dict.get("full_report", ""),
            key_facts=report_dict.get("key_facts", []),
            contradictions=report_dict.get("contradictions", []),
            duration_sec=float(report_dict.get("duration_sec", 0.0)),
            provider=report_dict.get("provider", "SerpApi"),
        )
        self._query_input.setText(report.topic)
        self._on_completed_ui(report)
        self.show()
        self.raise_()
