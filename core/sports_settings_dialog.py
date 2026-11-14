"""
core/sports_settings_dialog.py — Sports TV & Brave AdBlock settings dialog for VIERNES.
"""
from __future__ import annotations

import threading
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.sports_tv import (
    get_adblocker,
    load_settings,
    refresh_index,
    save_settings,
)


def _rgba(hex_str: str, alpha: float) -> str:
    h = hex_str.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


class SportsSettingsDialog(QDialog):
    _refresh_done_sig = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("VIERNES · TV Deportiva y Brave AdBlock")
        self.setFixedSize(580, 690)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        from ui import C, UI_FONT
        self._C = C
        self._UI_FONT = UI_FONT

        self._build_ui()
        self._load_values()
        self._refresh_done_sig.connect(self._on_refresh_done)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh_status)
        self._timer.start(1500)
        self._refresh_status()

    def _build_ui(self) -> None:
        C = self._C
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {C.PANEL};
                color: {C.WHITE};
                font-family: {self._UI_FONT};
            }}
            QLabel {{ color: {C.TEXT}; background: transparent; }}
            QFrame#Card {{
                background-color: {_rgba(C.PANEL2, 0.95)};
                border: 1px solid {C.BORDER};
                border-radius: 12px;
            }}
            QLineEdit, QPlainTextEdit, QComboBox {{
                background-color: {_rgba(C.WHITE, 0.06)};
                border: 1px solid {C.BORDER};
                border-radius: 6px;
                padding: 5px 8px;
                color: {C.WHITE};
            }}
            QComboBox QAbstractItemView {{
                background-color: {C.PANEL2};
                color: {C.WHITE};
                selection-background-color: {_rgba(C.PRI, 0.35)};
            }}
            QCheckBox {{ color: {C.WHITE}; spacing: 8px; }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(12)

        title = QLabel("⚽  TV Deportiva Nativa y Brave AdBlock")
        title.setFont(QFont(self._UI_FONT, 12, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {C.WHITE};")
        root.addWidget(title)

        sub = QLabel(
            "Reproduce canales deportivos desde la web original dentro del HUD "
            "protegido con el motor adblock-rust de Brave (sin publicidad ni popups)."
        )
        sub.setWordWrap(True)
        sub.setFont(QFont(self._UI_FONT, 8))
        sub.setStyleSheet(f"color: {C.TEXT_DIM};")
        root.addWidget(sub)

        # Card 1: Fuente y Enrutamiento
        c1 = QFrame()
        c1.setObjectName("Card")
        l1 = QVBoxLayout(c1)
        l1.setContentsMargins(14, 12, 14, 12)
        l1.setSpacing(8)

        self._chk_enabled = QCheckBox("Detectar automáticamente canales de deportes (ESPN, Fox Sports, TUDN, etc.)")
        l1.addWidget(self._chk_enabled)

        row_url = QHBoxLayout()
        row_url.addWidget(QLabel("Web fuente:"))
        self._edit_url = QLineEdit()
        self._edit_url.setPlaceholderText("https://futbolenvivo.top")
        row_url.addWidget(self._edit_url, stretch=1)
        l1.addLayout(row_url)

        row_route = QHBoxLayout()
        row_route.addWidget(QLabel("Prioridad en deportes:"))
        self._cmb_routing = QComboBox()
        self._cmb_routing.addItem("Solo web deportiva (Predeterminado, sin IPTV-org)", "sports_web")
        self._cmb_routing.addItem("Web deportiva primero + respaldo IPTV-org", "sports_web_then_iptv")
        self._cmb_routing.addItem("Usar solo IPTV-org", "iptv")
        row_route.addWidget(self._cmb_routing, stretch=1)
        l1.addLayout(row_route)

        root.addWidget(c1)

        # Card 2: Brave AdBlock & Reproductor
        c2 = QFrame()
        c2.setObjectName("Card")
        l2 = QVBoxLayout(c2)
        l2.setContentsMargins(14, 12, 14, 12)
        l2.setSpacing(8)

        self._status_lbl = QLabel("Motor AdBlock: verificando...")
        self._status_lbl.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Bold))
        self._status_lbl.setStyleSheet(f"color: {C.PRI};")
        l2.addWidget(self._status_lbl)

        self._chk_adblock = QCheckBox("Activar Brave AdBlock (EasyList + EasyList ES + EasyPrivacy + Brave Lists)")
        self._chk_popups = QCheckBox("Bloquear ventanas emergentes / popunders (createWindow)")
        self._chk_isolate = QCheckBox("Aislar el iframe original del reproductor a pantalla completa en el HUD")
        self._chk_autoplay = QCheckBox("Intentar reproducción automática al cargar el canal")
        for cb in (self._chk_adblock, self._chk_popups, self._chk_isolate, self._chk_autoplay):
            l2.addWidget(cb)

        l2.addWidget(QLabel("Dominios extra bloqueados (separados por coma):"))
        self._edit_hosts = QLineEdit()
        self._edit_hosts.setPlaceholderText("rtxt.org, doubleclick.net")
        l2.addWidget(self._edit_hosts)

        l2.addWidget(QLabel("Listas AdBlock adicionales (URLs, una por línea):"))
        self._edit_lists = QPlainTextEdit()
        self._edit_lists.setFixedHeight(64)
        self._edit_lists.setPlaceholderText("https://ejemplo.com/filtros.txt")
        l2.addWidget(self._edit_lists)

        root.addWidget(c2)

        # Bottom actions
        btn_row = QHBoxLayout()
        self._btn_update = QPushButton("↻  Actualizar Listas Brave + Canales")
        self._btn_update.setFixedHeight(32)
        self._btn_update.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_update.setStyleSheet(
            f"background: {_rgba(C.WHITE, 0.08)}; border: 1px solid {C.BORDER}; "
            f"border-radius: 8px; padding: 0 12px; color: {C.WHITE}; font-weight: bold;"
        )
        self._btn_update.clicked.connect(self._on_refresh_now)
        btn_row.addWidget(self._btn_update)
        btn_row.addStretch()

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setFixedHeight(32)
        btn_cancel.setStyleSheet(
            f"background: {_rgba(C.WHITE, 0.06)}; border: 1px solid {C.BORDER}; "
            f"border-radius: 8px; padding: 0 14px; color: {C.TEXT};"
        )
        btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(btn_cancel)

        btn_save = QPushButton("Guardar")
        btn_save.setFixedHeight(32)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet(
            f"background: {C.PRI}; border: none; border-radius: 8px; "
            f"padding: 0 18px; color: #0B0D12; font-weight: bold;"
        )
        btn_save.clicked.connect(self._on_save)
        btn_row.addWidget(btn_save)

        root.addLayout(btn_row)

    def _load_values(self) -> None:
        cfg = load_settings()
        self._chk_enabled.setChecked(bool(cfg.get("enabled", True)))
        self._edit_url.setText(str(cfg.get("source_url", "https://futbolenvivo.top")))
        idx = self._cmb_routing.findData(cfg.get("sports_routing", "sports_web"))
        self._cmb_routing.setCurrentIndex(max(0, idx))
        self._chk_adblock.setChecked(bool(cfg.get("adblock_enabled", True)))
        self._chk_popups.setChecked(bool(cfg.get("block_popups", True)))
        self._chk_isolate.setChecked(bool(cfg.get("isolate_player", True)))
        self._chk_autoplay.setChecked(bool(cfg.get("autoplay", True)))
        self._edit_hosts.setText(str(cfg.get("extra_blocked_hosts", "rtxt.org")))
        self._edit_lists.setPlainText(str(cfg.get("extra_filter_lists", "")))

    def _refresh_status(self) -> None:
        st = get_adblocker().status()
        if st["backend"] == "brave-adblock":
            self._status_lbl.setText(
                f"🛡️ Motor Brave AdBlock activo · {st['rules']:,} reglas cargadas"
            )
        elif st["installed"] and not st["ready"]:
            self._status_lbl.setText("⏳ Descargando y compilando listas Brave AdBlock...")
        else:
            self._status_lbl.setText("⚠️ Modo respaldo por hosts (adblock no compilado aún)")

    def _on_refresh_now(self) -> None:
        self._save_only()
        self._btn_update.setEnabled(False)
        self._btn_update.setText("Actualizando...")

        def _work():
            chans = refresh_index(force=True)
            ok = get_adblocker().build(force_download=True)
            st = get_adblocker().status()
            msg = (
                f"Listo: {len(chans)} canales indexados · "
                f"{st['rules']:,} reglas Brave ({'OK' if ok else 'fallback'})."
            )
            self._refresh_done_sig.emit(msg)

        threading.Thread(target=_work, daemon=True, name="sports-refresh").start()

    def _on_refresh_done(self, msg: str) -> None:
        self._btn_update.setEnabled(True)
        self._btn_update.setText("↻  Actualizar Listas Brave + Canales")
        self._status_lbl.setText(f"🛡️ {msg}")

    def _save_only(self) -> None:
        save_settings({
            "enabled": self._chk_enabled.isChecked(),
            "source_url": self._edit_url.text().strip() or "https://futbolenvivo.top",
            "sports_routing": self._cmb_routing.currentData(),
            "adblock_enabled": self._chk_adblock.isChecked(),
            "block_popups": self._chk_popups.isChecked(),
            "isolate_player": self._chk_isolate.isChecked(),
            "autoplay": self._chk_autoplay.isChecked(),
            "extra_blocked_hosts": self._edit_hosts.text().strip(),
            "extra_filter_lists": self._edit_lists.toPlainText().strip(),
        })

    def _on_save(self) -> None:
        self._save_only()
        get_adblocker().build_async(force_download=False)
        self.accept()
