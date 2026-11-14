"""
Personality & Regional Speech Settings Dialog - VIERNES / Edith
===============================================================
Apartado profesional: 'Personalidad y forma de hablar'
Interfaz gráfica completa para personalizar:
- 10 Variantes regionales y dialectos auténticos.
- 10 Rasgos de personalidad combinables con sliders de intensidad (0-100%).
- Estilo avanzado de comunicación (formalidad, regionalismos, humor, etc.).
- Gestión de perfiles (crear, duplicar, predeterminado, temporal, restaurar).
- Vista previa demostrativa en tiempo real.
"""

from __future__ import annotations

import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QSlider, QFrame, QScrollArea,
    QMessageBox, QInputDialog, QGridLayout, QGroupBox, QTabWidget,
    QPlainTextEdit
)

from core.personality_manager import (
    get_personality_manager, PersonalityProfile, CommunicationStyle,
    DIALECT_SPECS, PERSONALITY_TRAITS
)


def _rgba(hex_color: str, alpha: float) -> str:
    c = QColor(hex_color)
    return f"rgba({c.red()},{c.green()},{c.blue()},{alpha:.3f})"


class PersonalitySettingsDialog(QDialog):
    """Modern dark cybernetic dialog for Personality and Regional Dialect Configuration."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Personalidad, Nacionalidad y Forma de Hablar — VIERNES")
        self.setMinimumSize(700, 780)
        self.resize(740, 820)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        from ui import C, UI_FONT
        self._C = C
        self._UI_FONT = UI_FONT
        self.manager = get_personality_manager()

        self._trait_sliders: dict[str, tuple[QSlider, QLabel]] = {}
        self._is_loading: bool = False

        self._build_ui()
        self._populate_profiles_combo()
        self._load_active_profile_into_ui()

    def _build_ui(self):
        C = self._C
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {C.PANEL};
                color: {C.WHITE};
                font-family: {self._UI_FONT};
            }}
            QLabel {{
                color: {C.TEXT};
                background: transparent;
            }}
            QFrame#Card {{
                background-color: {_rgba(C.PANEL2, 0.95)};
                border: 1px solid {C.BORDER};
                border-radius: 10px;
            }}
            QComboBox {{
                background-color: {_rgba(C.WHITE, 0.06)};
                color: {C.WHITE};
                border: 1px solid {C.BORDER_A};
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 11px;
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {C.PANEL2};
                color: {C.WHITE};
                selection-background-color: {C.PRI};
                selection-color: {C.WHITE};
                border: 1px solid {C.BORDER_B};
            }}
            QSlider::groove:horizontal {{
                height: 6px;
                background: {_rgba(C.WHITE, 0.10)};
                border-radius: 3px;
            }}
            QSlider::sub-page:horizontal {{
                background: {C.PRI};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {C.WHITE};
                border: 1px solid {C.PRI};
                width: 14px;
                margin-top: -4px;
                margin-bottom: -4px;
                border-radius: 7px;
            }}
            QTabWidget::pane {{
                border: 1px solid {C.BORDER};
                background: transparent;
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background: {_rgba(C.WHITE, 0.04)};
                color: {C.TEXT_MED};
                padding: 7px 12px;
                margin-right: 4px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-size: 11px;
                font-weight: 600;
            }}
            QTabBar::tab:selected {{
                background: {_rgba(C.PRI, 0.18)};
                color: {C.PRI};
                border-bottom: 2px solid {C.PRI};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        # ── Header ──────────────────────────────────────────────────────────
        hdr = QHBoxLayout()
        icon = QLabel("🎭")
        icon.setFont(QFont(self._UI_FONT, 20))
        hdr.addWidget(icon)

        hdr_v = QVBoxLayout()
        hdr_v.setSpacing(2)
        title = QLabel("Personalidad y Forma de Hablar")
        title.setFont(QFont(self._UI_FONT, 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {C.WHITE};")
        hdr_v.addWidget(title)

        subtitle = QLabel("Configuración modular de dialectos, acentos, combinaciones de personalidad y comportamiento para Edith.")
        subtitle.setFont(QFont(self._UI_FONT, 8))
        subtitle.setStyleSheet(f"color: {C.TEXT_MED};")
        hdr_v.addWidget(subtitle)
        hdr.addLayout(hdr_v, stretch=1)

        # Badge de estado activo
        self._status_badge = QLabel("Activo")
        self._status_badge.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Bold))
        self._status_badge.setStyleSheet(f"""
            background-color: {_rgba(C.PRI, 0.18)};
            color: {C.PRI};
            border: 1px solid {C.PRI};
            border-radius: 10px;
            padding: 3px 10px;
        """)
        hdr.addWidget(self._status_badge)
        layout.addLayout(hdr)

        # ── Barra de selección de perfil ─────────────────────────────────────
        prof_card = QFrame()
        prof_card.setObjectName("Card")
        prof_lay = QHBoxLayout(prof_card)
        prof_lay.setContentsMargins(12, 8, 12, 8)
        prof_lay.setSpacing(8)

        prof_lbl = QLabel("Perfil Guardado:")
        prof_lbl.setFont(QFont(self._UI_FONT, 9, QFont.Weight.DemiBold))
        prof_lay.addWidget(prof_lbl)

        self._profile_combo = QComboBox()
        self._profile_combo.setFont(QFont(self._UI_FONT, 9))
        self._profile_combo.currentIndexChanged.connect(self._on_profile_combo_changed)
        prof_lay.addWidget(self._profile_combo, stretch=1)

        self._btn_new = QPushButton("＋ Nuevo")
        self._btn_new.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Bold))
        self._btn_new.setStyleSheet(self._btn_style(dim=True))
        self._btn_new.clicked.connect(self._on_new_profile)
        prof_lay.addWidget(self._btn_new)

        self._btn_duplicate = QPushButton("📋 Duplicar")
        self._btn_duplicate.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Bold))
        self._btn_duplicate.setStyleSheet(self._btn_style(dim=True))
        self._btn_duplicate.clicked.connect(self._on_duplicate_profile)
        prof_lay.addWidget(self._btn_duplicate)

        self._btn_restore = QPushButton("🔄 Fábrica")
        self._btn_restore.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Bold))
        self._btn_restore.setStyleSheet(self._btn_style(dim=True))
        self._btn_restore.setToolTip("Restaurar los 10 perfiles predeterminados originales")
        self._btn_restore.clicked.connect(self._on_restore_defaults)
        prof_lay.addWidget(self._btn_restore)

        layout.addWidget(prof_card)

        # ── Pestañas de configuración ─────────────────────────────────────────
        self._tabs = QTabWidget()

        # TAB 1: Dialecto y Región
        self._tab_dialect = self._create_dialect_tab()
        self._tabs.addTab(self._tab_dialect, "🌎  Dialecto y Región")

        # TAB 2: Rasgos de Personalidad (%)
        self._tab_traits = self._create_traits_tab()
        self._tabs.addTab(self._tab_traits, "🧠  Matriz de Personalidad")

        # TAB 3: Comportamiento y Estilo
        self._tab_style = self._create_style_tab()
        self._tabs.addTab(self._tab_style, "⚙️  Estilo y Comportamiento")

        # TAB 4: Vista Previa y Voz
        self._tab_preview = self._create_preview_tab()
        self._tabs.addTab(self._tab_preview, "👁️  Vista Previa y Acento")

        layout.addWidget(self._tabs, stretch=1)

        # ── Barra de botones de acción inferior ───────────────────────────────
        btn_bar = QHBoxLayout()
        btn_bar.setSpacing(10)

        self._btn_temp = QPushButton("Aplicar Solo a esta Conversación")
        self._btn_temp.setFixedHeight(34)
        self._btn_temp.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Medium))
        self._btn_temp.setStyleSheet(self._btn_style(dim=True))
        self._btn_temp.clicked.connect(self._apply_temporary)
        btn_bar.addWidget(self._btn_temp)

        btn_bar.addStretch(1)

        close_btn = QPushButton("Cerrar")
        close_btn.setFixedHeight(34)
        close_btn.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Medium))
        close_btn.setStyleSheet(self._btn_style(dim=True))
        close_btn.clicked.connect(self.close)
        btn_bar.addWidget(close_btn)

        save_btn = QPushButton("Guardar como predeterminado")
        save_btn.setFixedHeight(34)
        save_btn.setFont(QFont(self._UI_FONT, 9, QFont.Weight.DemiBold))
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {C.PRI}; color: {C.WHITE};
                border: none; border-radius: 8px; padding: 0 18px;
            }}
            QPushButton:hover {{
                background-color: {C.PRI_DIM};
            }}
        """)
        save_btn.clicked.connect(self._save_as_default)
        btn_bar.addWidget(save_btn)

        layout.addLayout(btn_bar)

    # ── TAB 1: DIALECTO Y REGIÓN ─────────────────────────────────────────────

    def _create_dialect_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(10)

        lbl_info = QLabel("Configura la nacionalidad, variante regional, forma de trato y voz de VIERNES. Los cambios se aplican inmediatamente en la sesión en vivo.")
        lbl_info.setFont(QFont(self._UI_FONT, 8))
        lbl_info.setStyleSheet(f"color: {self._C.TEXT_MED};")
        lbl_info.setWordWrap(True)
        lay.addWidget(lbl_info)

        # Nacionalidad / Origen cultural
        nat_row = QHBoxLayout()
        nat_lbl = QLabel("Nacionalidad / Origen:")
        nat_lbl.setFont(QFont(self._UI_FONT, 9, QFont.Weight.DemiBold))
        nat_lbl.setFixedWidth(150)
        nat_row.addWidget(nat_lbl)

        self._nationality_combo = QComboBox()
        self._nationality_combo.setEditable(True)
        self._nationality_combo.setFont(QFont(self._UI_FONT, 9))
        for n_item in [
            "", "Costarricense", "Colombiana", "Mexicana", "Argentina",
            "Española", "Venezolana", "Peruana", "Chilena", "Cubana",
            "Estadounidense", "Japonesa", "Neutra / Internacional"
        ]:
            self._nationality_combo.addItem(n_item if n_item else "(Automática según dialecto)", n_item)
        self._nationality_combo.currentTextChanged.connect(self._on_style_param_changed)
        nat_row.addWidget(self._nationality_combo, stretch=1)
        lay.addLayout(nat_row)

        # Dialect selector
        d_row = QHBoxLayout()
        d_lbl = QLabel("Variante Regional:")
        d_lbl.setFont(QFont(self._UI_FONT, 9, QFont.Weight.DemiBold))
        d_lbl.setFixedWidth(150)
        d_row.addWidget(d_lbl)

        self._dialect_combo = QComboBox()
        self._dialect_combo.setFont(QFont(self._UI_FONT, 9))
        for did, dspec in DIALECT_SPECS.items():
            self._dialect_combo.addItem(f"{dspec['name']} ({dspec['region']})", did)
        self._dialect_combo.currentIndexChanged.connect(self._on_dialect_changed)
        d_row.addWidget(self._dialect_combo, stretch=1)
        lay.addLayout(d_row)

        # Forma de trato (Tú / Vos / Usted)
        addr_row = QHBoxLayout()
        addr_lbl = QLabel("Forma de Trato:")
        addr_lbl.setFont(QFont(self._UI_FONT, 9, QFont.Weight.DemiBold))
        addr_lbl.setFixedWidth(150)
        addr_row.addWidget(addr_lbl)

        self._address_combo = QComboBox()
        self._address_combo.setFont(QFont(self._UI_FONT, 9))
        self._address_combo.addItem("Automático según región", "auto")
        self._address_combo.addItem("Tú (Tuteo cercano)", "tuteo")
        self._address_combo.addItem("Vos (Voseo regional)", "voseo")
        self._address_combo.addItem("Usted (Formal / Ejecutivo)", "usted")
        self._address_combo.currentIndexChanged.connect(self._on_style_param_changed)
        addr_row.addWidget(self._address_combo, stretch=1)
        lay.addLayout(addr_row)

        # Voz asociada al perfil
        voice_row = QHBoxLayout()
        voice_lbl = QLabel("Voz de Gemini (Opcional):")
        voice_lbl.setFont(QFont(self._UI_FONT, 9, QFont.Weight.DemiBold))
        voice_lbl.setFixedWidth(150)
        voice_row.addWidget(voice_lbl)

        self._voice_combo = QComboBox()
        self._voice_combo.setFont(QFont(self._UI_FONT, 9))
        for v_lbl, v_val in [
            ("Usar voz global configurada", ""),
            ("Aoede (Cálida, expresiva y clara)", "Aoede"),
            ("Kore (Firme, segura y nítida)", "Kore"),
            ("Zephyr (Brillante, amable y ágil)", "Zephyr"),
            ("Leda (Suave, dulce y juvenil)", "Leda"),
            ("Puck (Energética y juguetona)", "Puck"),
            ("Fenrir (Profunda y directa)", "Fenrir"),
            ("Charon (Seria y analítica)", "Charon"),
        ]:
            self._voice_combo.addItem(v_lbl, v_val)
        voice_row.addWidget(self._voice_combo, stretch=1)
        lay.addLayout(voice_row)

        # Card de descripción del dialecto
        self._dialect_card = QFrame()
        self._dialect_card.setObjectName("Card")
        dc_lay = QVBoxLayout(self._dialect_card)
        dc_lay.setContentsMargins(14, 12, 14, 12)
        dc_lay.setSpacing(6)

        self._dc_title = QLabel("Detalles del Dialecto")
        self._dc_title.setFont(QFont(self._UI_FONT, 10, QFont.Weight.Bold))
        self._dc_title.setStyleSheet(f"color: {self._C.PRI};")
        dc_lay.addWidget(self._dc_title)

        self._dc_desc = QLabel()
        self._dc_desc.setFont(QFont(self._UI_FONT, 8))
        self._dc_desc.setStyleSheet(f"color: {self._C.TEXT};")
        self._dc_desc.setWordWrap(True)
        dc_lay.addWidget(self._dc_desc)

        self._dc_markers = QLabel()
        self._dc_markers.setFont(QFont(self._UI_FONT, 8, QFont.Weight.DemiBold))
        self._dc_markers.setStyleSheet(f"color: {self._C.ACC};")
        self._dc_markers.setWordWrap(True)
        dc_lay.addWidget(self._dc_markers)

        lay.addWidget(self._dialect_card)

        # Idioma complementario
        lang_row = QHBoxLayout()
        lang_lbl = QLabel("Modalidad Lingüística:")
        lang_lbl.setFont(QFont(self._UI_FONT, 9, QFont.Weight.DemiBold))
        lang_lbl.setFixedWidth(150)
        lang_row.addWidget(lang_lbl)

        self._lang_combo = QComboBox()
        self._lang_combo.setFont(QFont(self._UI_FONT, 9))
        self._lang_combo.addItem("Español (Predeterminado)", "es")
        self._lang_combo.addItem("Español + Inglés Tech (Bilingüe)", "es_en")
        self._lang_combo.addItem("Español con expresiones en Japonés (Kawaii)", "es_ja")
        self._lang_combo.addItem("Japonés completo (Kawaii Japanese)", "ja")
        lang_row.addWidget(self._lang_combo, stretch=1)
        lay.addLayout(lang_row)

        lay.addStretch(1)
        return w

    # ── TAB 2: MATRIZ DE PERSONALIDAD (10 RASGOS CON SLIDERS %) ──────────────

    def _create_traits_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(10)

        info = QLabel(
            "Ajusta los porcentajes relativos de cada rasgo. No son mutuamente excluyentes: "
            "puedes combinar varios rasgos (ej. 80% Sarcástica, 40% Cariñosa, 30% Profesional) "
            "para crear una personalidad única y equilibrada."
        )
        info.setFont(QFont(self._UI_FONT, 8))
        info.setStyleSheet(f"color: {self._C.TEXT_MED};")
        info.setWordWrap(True)
        lay.addWidget(info)

        for tid, tinfo in PERSONALITY_TRAITS.items():
            card = QFrame()
            card.setObjectName("Card")
            c_lay = QHBoxLayout(card)
            c_lay.setContentsMargins(12, 6, 12, 6)
            c_lay.setSpacing(10)

            icon_lbl = QLabel(tinfo.get("icon", "◈"))
            icon_lbl.setFont(QFont(self._UI_FONT, 12))
            c_lay.addWidget(icon_lbl)

            info_v = QVBoxLayout()
            info_v.setSpacing(1)
            name_lbl = QLabel(tinfo.get("name", tid))
            name_lbl.setFont(QFont(self._UI_FONT, 9, QFont.Weight.Bold))
            name_lbl.setStyleSheet(f"color: {self._C.WHITE};")
            info_v.addWidget(name_lbl)

            desc_lbl = QLabel(tinfo.get("description", ""))
            desc_lbl.setFont(QFont(self._UI_FONT, 7))
            desc_lbl.setStyleSheet(f"color: {self._C.TEXT_MED};")
            info_v.addWidget(desc_lbl)
            c_lay.addLayout(info_v, stretch=1)

            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(0)
            slider.setFixedWidth(140)

            val_lbl = QLabel("0%")
            val_lbl.setFixedWidth(38)
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            val_lbl.setFont(QFont(self._UI_FONT, 8, QFont.Weight.Bold))
            val_lbl.setStyleSheet(f"color: {self._C.PRI};")

            def _make_change_handler(lbl=val_lbl):
                return lambda val: self._on_slider_value_changed(lbl, val)

            slider.valueChanged.connect(_make_change_handler())
            c_lay.addWidget(slider)
            c_lay.addWidget(val_lbl)

            lay.addWidget(card)
            self._trait_sliders[tid] = (slider, val_lbl)

        scroll.setWidget(w)
        return scroll

    def _on_slider_value_changed(self, lbl: QLabel, val: int):
        lbl.setText(f"{val}%")
        if not self._is_loading:
            self._update_preview()

    # ── TAB 3: ESTILO Y COMPORTAMIENTO ───────────────────────────────────────

    def _create_style_tab(self) -> QWidget:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(10)

        grid = QGridLayout()
        grid.setSpacing(10)

        # 1. Formalidad
        self._combo_formality = self._make_style_combo(["Informal", "Equilibrada", "Formal"], ["informal", "equilibrada", "formal"])
        grid.addWidget(self._make_field_label("Formalidad:"), 0, 0)
        grid.addWidget(self._combo_formality, 0, 1)

        # 2. Regionalismos
        self._combo_reg = self._make_style_combo(["Baja (Sutil)", "Media (Natural)", "Alta (Frecuente)"], ["baja", "media", "alta"])
        grid.addWidget(self._make_field_label("Intensidad de Modismos:"), 0, 2)
        grid.addWidget(self._combo_reg, 0, 3)

        # 3. Humor
        self._combo_humor = self._make_style_combo(["Mínimo (Sobrio)", "Moderado", "Frecuente (Bromista)"], ["minimo", "moderado", "frecuente"])
        grid.addWidget(self._make_field_label("Sentido del Humor:"), 1, 0)
        grid.addWidget(self._combo_humor, 1, 1)

        # 4. Expresividad
        self._combo_express = self._make_style_combo(["Discreta", "Natural", "Muy Expresiva"], ["discreta", "natural", "muy_expresiva"])
        grid.addWidget(self._make_field_label("Expresividad Emocional:"), 1, 2)
        grid.addWidget(self._combo_express, 1, 3)

        # 5. Longitud
        self._combo_length = self._make_style_combo(["Breve y Directa", "Equilibrada", "Detallada"], ["breve", "equilibrada", "detallada"])
        grid.addWidget(self._make_field_label("Longitud de Respuestas:"), 2, 0)
        grid.addWidget(self._combo_length, 2, 1)

        # 6. Cercanía
        self._combo_close = self._make_style_combo(["Distante / Ejecutiva", "Cordial", "Muy Cercana / Familiar"], ["distante", "cordial", "muy_cercana"])
        grid.addWidget(self._make_field_label("Grado de Cercanía:"), 2, 2)
        grid.addWidget(self._combo_close, 2, 3)

        # 7. Emojis
        self._combo_emojis = self._make_style_combo(["Desactivado", "Moderado", "Frecuente"], ["desactivado", "moderado", "frecuente"])
        grid.addWidget(self._make_field_label("Uso de Emojis:"), 3, 0)
        grid.addWidget(self._combo_emojis, 3, 1)

        # 8. Apodos
        self._combo_nicks = self._make_style_combo(["Desactivado", "Ocasional", "Frecuente"], ["desactivado", "ocasional", "frecuente"])
        grid.addWidget(self._make_field_label("Apodos / Trato Afectuoso:"), 3, 2)
        grid.addWidget(self._combo_nicks, 3, 3)

        # 9. Vocabulario
        self._combo_vocab = self._make_style_combo(["Sencillo", "Cotidiano", "Avanzado / Culto"], ["sencillo", "cotidiano", "avanzado"])
        grid.addWidget(self._make_field_label("Nivel de Vocabulario:"), 4, 0)
        grid.addWidget(self._combo_vocab, 4, 1)

        # 10. Iniciativa
        self._combo_init = self._make_style_combo(["Reactiva (Solo responde)", "Equilibrada", "Proactiva (Propone)"], ["reactiva", "equilibrada", "proactiva"])
        grid.addWidget(self._make_field_label("Iniciativa Conversacional:"), 4, 2)
        grid.addWidget(self._combo_init, 4, 3)

        lay.addLayout(grid)

        # Instrucciones Personalizadas (Prompt Libre)
        custom_card = QFrame()
        custom_card.setObjectName("Card")
        c_lay = QVBoxLayout(custom_card)
        c_lay.setContentsMargins(12, 10, 12, 10)
        c_lay.setSpacing(6)
        c_title = QLabel("✍️ Instrucciones Personalizadas (Opcional)")
        c_title.setFont(QFont(self._UI_FONT, 9, QFont.Weight.Bold))
        c_title.setStyleSheet(f"color: {self._C.WHITE};")
        c_lay.addWidget(c_title)

        self._custom_inst_edit = QPlainTextEdit()
        self._custom_inst_edit.setPlaceholderText(
            "Ej. 'Háblame siempre con tono de ingeniera senior, usa 'pura vida' al cerrar tareas, "
            "sé ultra directa y nunca des rodeos...'"
        )
        self._custom_inst_edit.setFixedHeight(78)
        self._custom_inst_edit.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {_rgba(self._C.WHITE, 0.05)};
                color: {self._C.WHITE};
                border: 1px solid {self._C.BORDER};
                border-radius: 6px;
                padding: 6px;
                font-size: 11px;
            }}
        """)
        c_lay.addWidget(self._custom_inst_edit)
        lay.addWidget(custom_card)

        # Jerarquía explicada
        prio_card = QFrame()
        prio_card.setObjectName("Card")
        p_lay = QVBoxLayout(prio_card)
        p_lay.setContentsMargins(12, 10, 12, 10)
        p_lay.setSpacing(4)
        p_title = QLabel("◈ Jerarquía de Prioridad")
        p_title.setFont(QFont(self._UI_FONT, 9, QFont.Weight.Bold))
        p_title.setStyleSheet(f"color: {self._C.PRI};")
        p_lay.addWidget(p_title)

        p_desc = QLabel(
            "Cuando se solicita una tarea técnica (código, archivos, medicina o control del sistema), "
            "la claridad y eficacia tienen prioridad sobre el humor o el sarcasmo. "
            "Edith ejecutará las herramientas con precisión y adaptará su personalidad sin entorpecer el resultado."
        )
        p_desc.setFont(QFont(self._UI_FONT, 8))
        p_desc.setStyleSheet(f"color: {self._C.TEXT_MED};")
        p_desc.setWordWrap(True)
        p_lay.addWidget(p_desc)
        lay.addWidget(prio_card)

        lay.addStretch(1)
        scroll.setWidget(w)
        return scroll

    def _make_field_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setFont(QFont(self._UI_FONT, 8, QFont.Weight.DemiBold))
        lbl.setStyleSheet(f"color: {self._C.WHITE};")
        return lbl

    def _make_style_combo(self, labels: list[str], values: list[str]) -> QComboBox:
        cb = QComboBox()
        cb.setFont(QFont(self._UI_FONT, 8))
        for l, v in zip(labels, values):
            cb.addItem(l, v)
        cb.currentIndexChanged.connect(self._on_style_param_changed)
        return cb

    def _on_style_param_changed(self):
        if not self._is_loading:
            self._update_preview()

    # ── TAB 4: VISTA PREVIA Y ACENTO ─────────────────────────────────────────

    def _create_preview_tab(self) -> QWidget:
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(12)

        # Tarjeta de demostración interactiva
        prev_card = QFrame()
        prev_card.setObjectName("Card")
        p_lay = QVBoxLayout(prev_card)
        p_lay.setContentsMargins(14, 12, 14, 12)
        p_lay.setSpacing(8)

        p_hdr = QHBoxLayout()
        self._prev_title = QLabel("Simulación Demostrativa de Expresión")
        self._prev_title.setFont(QFont(self._UI_FONT, 10, QFont.Weight.Bold))
        self._prev_title.setStyleSheet(f"color: {self._C.PRI};")
        p_hdr.addWidget(self._prev_title)

        prev_tag = QLabel("VISTA PREVIA ORIENTATIVA")
        prev_tag.setFont(QFont(self._UI_FONT, 7, QFont.Weight.Bold))
        prev_tag.setStyleSheet(f"color: {self._C.ACC}; background: {_rgba(self._C.ACC, 0.12)}; border-radius: 4px; padding: 2px 6px;")
        p_hdr.addWidget(prev_tag)
        p_lay.addLayout(p_hdr)

        self._prev_greeting = QLabel()
        self._prev_greeting.setFont(QFont(self._UI_FONT, 9, QFont.Weight.Medium))
        self._prev_greeting.setStyleSheet(f"color: {self._C.WHITE}; background: {_rgba(self._C.WHITE, 0.03)}; border-radius: 6px; padding: 8px;")
        self._prev_greeting.setWordWrap(True)
        p_lay.addWidget(self._prev_greeting)

        self._prev_resp = QLabel()
        self._prev_resp.setFont(QFont(self._UI_FONT, 9))
        self._prev_resp.setStyleSheet(f"color: {self._C.TEXT}; background: {_rgba(self._C.WHITE, 0.03)}; border-radius: 6px; padding: 8px;")
        self._prev_resp.setWordWrap(True)
        p_lay.addWidget(self._prev_resp)

        p_notice = QLabel("Nota: Demostración sintética orientativa. Google Gemini generará respuestas únicas y dinámicas respetando este patrón.")
        p_notice.setFont(QFont(self._UI_FONT, 7))
        p_notice.setStyleSheet(f"color: {self._C.TEXT_MED};")
        p_lay.addWidget(p_notice)

        lay.addWidget(prev_card)

        # Sección de Claridad y Acento de Voz
        voice_card = QFrame()
        voice_card.setObjectName("Card")
        v_lay = QVBoxLayout(voice_card)
        v_lay.setContentsMargins(14, 12, 14, 12)
        v_lay.setSpacing(6)

        v_title = QLabel("🎙️  Sobre la Voz Hablada y los Acentos")
        v_title.setFont(QFont(self._UI_FONT, 9, QFont.Weight.Bold))
        v_title.setStyleSheet(f"color: {self._C.WHITE};")
        v_lay.addWidget(v_title)

        v_desc = QLabel(
            "• **Estilo y Vocabulario Textual**: Gemini adopta el 100% del vocabulario, modismos, voseo y gramática del dialecto seleccionado en cada respuesta.\n"
            "• **Acento Fonético de Audio**: Las voces nativas de Gemini Live hablan un español fluido internacionalmente neutro con la entonación y palabras del texto. "
            "Si deseas acentos fonéticos regionales específicos en el habla (p. ej. acento de España, México o Argentina), puedes seleccionar el motor de voz Microsoft Edge Neural desde la configuración de audio."
        )
        v_desc.setFont(QFont(self._UI_FONT, 8))
        v_desc.setStyleSheet(f"color: {self._C.TEXT_MED};")
        v_desc.setWordWrap(True)
        v_lay.addWidget(v_desc)

        lay.addWidget(voice_card)
        lay.addStretch(1)
        return w

    # ── CARGA Y SINCRONIZACIÓN DE UI ─────────────────────────────────────────

    def _populate_profiles_combo(self):
        self._profile_combo.blockSignals(True)
        self._profile_combo.clear()
        profiles = self.manager.get_all_profiles()
        def_id = self.manager._default_profile_id
        for pid, prof in profiles.items():
            tag = " ★ (Predeterminado)" if pid == def_id else ""
            self._profile_combo.addItem(f"{prof.name}{tag}", pid)
        self._profile_combo.blockSignals(False)

    def _load_active_profile_into_ui(self):
        active = self.manager.get_active_profile()
        self._load_profile(active)

    def _load_profile(self, profile: PersonalityProfile):
        self._is_loading = True
        try:
            # Seleccionar en combo de perfiles
            idx = self._profile_combo.findData(profile.id)
            if idx >= 0:
                self._profile_combo.setCurrentIndex(idx)

            # Nacionalidad, Dialecto, Trato y Voz
            nat_val = (getattr(profile, "nationality", "") or "").strip()
            if nat_val:
                n_idx = self._nationality_combo.findText(nat_val)
                if n_idx >= 0:
                    self._nationality_combo.setCurrentIndex(n_idx)
                else:
                    self._nationality_combo.setCurrentText(nat_val)
            else:
                self._nationality_combo.setCurrentIndex(0)

            d_idx = self._dialect_combo.findData(profile.dialect_id)
            if d_idx >= 0:
                self._dialect_combo.setCurrentIndex(d_idx)
            self._update_dialect_card(profile.dialect_id)

            self._set_combo_by_value(self._address_combo, getattr(profile, "address_form", "auto") or "auto")
            self._set_combo_by_value(self._voice_combo, getattr(profile, "voice_name", "") or "")

            # Idioma
            l_idx = self._lang_combo.findData(profile.language)
            if l_idx >= 0:
                self._lang_combo.setCurrentIndex(l_idx)

            # Instrucciones personalizadas
            self._custom_inst_edit.setPlainText(getattr(profile, "custom_instructions", "") or "")

            # Sliders de rasgos
            for tid, (slider, lbl) in self._trait_sliders.items():
                val = profile.trait_intensities.get(tid, 0)
                slider.setValue(val)
                lbl.setText(f"{val}%")

            # Estilo
            st = profile.style
            self._set_combo_by_value(self._combo_formality, st.formality)
            self._set_combo_by_value(self._combo_reg, st.regionalism_intensity)
            self._set_combo_by_value(self._combo_humor, st.humor)
            self._set_combo_by_value(self._combo_express, st.emotional_expressiveness)
            self._set_combo_by_value(self._combo_length, st.response_length)
            self._set_combo_by_value(self._combo_close, st.closeness)
            self._set_combo_by_value(self._combo_emojis, st.emojis)
            self._set_combo_by_value(self._combo_nicks, st.nicknames)
            self._set_combo_by_value(self._combo_vocab, st.vocabulary)
            self._set_combo_by_value(self._combo_init, st.conversational_initiative)

            # Estado
            if self.manager.is_temporary_active():
                self._status_badge.setText(f"Modo Temporal: {self.manager.get_temporary_reason()[:16]}")
                self._status_badge.setStyleSheet(f"background-color: {_rgba(self._C.ACC, 0.20)}; color: {self._C.ACC}; border: 1px solid {self._C.ACC}; border-radius: 10px; padding: 3px 10px;")
            else:
                self._status_badge.setText("Perfil Predeterminado" if profile.id == self.manager._default_profile_id else "Perfil Guardado")
                self._status_badge.setStyleSheet(f"background-color: {_rgba(self._C.PRI, 0.18)}; color: {self._C.PRI}; border: 1px solid {self._C.PRI}; border-radius: 10px; padding: 3px 10px;")

        finally:
            self._is_loading = False
            self._update_preview()

    def _set_combo_by_value(self, combo: QComboBox, val: str):
        idx = combo.findData(val)
        if idx >= 0:
            combo.setCurrentIndex(idx)

    def _on_dialect_changed(self):
        did = self._dialect_combo.currentData()
        self._update_dialect_card(did)
        if not self._is_loading:
            self._update_preview()

    def _update_dialect_card(self, dialect_id: str):
        dspec = DIALECT_SPECS.get(dialect_id, DIALECT_SPECS["es_latam_neutral"])
        self._dc_title.setText(f"{dspec['name']} — {dspec['region']}")
        self._dc_desc.setText(dspec.get("style_guide", ""))
        markers = ", ".join(dspec.get("key_markers", []))
        self._dc_markers.setText(f"Expresiones clave: {markers}")

    def _update_preview(self):
        prof = self._build_profile_from_ui(profile_id="temp_preview", name="Vista Previa")
        demo = self.manager.generate_demo_preview(prof)
        self._prev_title.setText(f"Demostración: {prof.name} ({demo['dialect_name']})")
        self._prev_greeting.setText(f"💬 Saludo: \"{demo['sample_greeting']}\"")
        self._prev_resp.setText(f"💬 Respuesta a consulta: \"{demo['sample_response']}\"")

    def _build_profile_from_ui(self, profile_id: str = "", name: str = "") -> PersonalityProfile:
        cur_id = profile_id or self._profile_combo.currentData() or "custom"
        cur_name = name or self._profile_combo.currentText().replace(" ★ (Predeterminado)", "").strip()
        dialect_id = self._dialect_combo.currentData()
        language = self._lang_combo.currentData()

        intensities = {}
        for tid, (slider, _) in self._trait_sliders.items():
            intensities[tid] = slider.value()

        style = CommunicationStyle(
            formality=self._combo_formality.currentData(),
            regionalism_intensity=self._combo_reg.currentData(),
            humor=self._combo_humor.currentData(),
            emotional_expressiveness=self._combo_express.currentData(),
            response_length=self._combo_length.currentData(),
            closeness=self._combo_close.currentData(),
            emojis=self._combo_emojis.currentData(),
            nicknames=self._combo_nicks.currentData(),
            vocabulary=self._combo_vocab.currentData(),
            conversational_initiative=self._combo_init.currentData(),
        )

        nat_text = self._nationality_combo.currentText().strip()
        if nat_text.startswith("(Automática"):
            nat_text = ""

        return PersonalityProfile(
            id=cur_id,
            name=cur_name,
            description="Perfil configurado manualmente.",
            dialect_id=dialect_id,
            language=language,
            nationality=nat_text,
            address_form=self._address_combo.currentData() or "auto",
            voice_name=self._voice_combo.currentData() or "",
            custom_instructions=self._custom_inst_edit.toPlainText().strip(),
            trait_intensities=intensities,
            style=style,
            is_custom=True,
        )

    # ── ACCIONES DE PERFILES ─────────────────────────────────────────────────

    def _on_profile_combo_changed(self):
        if self._is_loading:
            return
        pid = self._profile_combo.currentData()
        prof = self.manager.get_profile(pid)
        if prof:
            self._load_profile(prof)

    def _on_new_profile(self):
        name, ok = QInputDialog.getText(self, "Nuevo Perfil", "Nombre para el nuevo perfil de personalidad:")
        if not ok or not name.strip():
            return
        import time
        pid = f"custom_{int(time.time())}"
        prof = self._build_profile_from_ui(profile_id=pid, name=name.strip())
        self.manager.save_profile(prof)
        self._populate_profiles_combo()
        self._load_profile(prof)
        QMessageBox.information(self, "Perfil Creado", f"El perfil '{name}' ha sido creado exitosamente.")

    def _on_duplicate_profile(self):
        cur_id = self._profile_combo.currentData()
        cur_name = self._profile_combo.currentText().replace(" ★ (Predeterminado)", "").strip()
        name, ok = QInputDialog.getText(self, "Duplicar Perfil", "Nombre para la copia:", text=f"{cur_name} (Copia)")
        if not ok or not name.strip():
            return
        new_prof = self.manager.duplicate_profile(cur_id, name)
        if new_prof:
            self._populate_profiles_combo()
            self._load_profile(new_prof)
            QMessageBox.information(self, "Perfil Duplicado", f"Se duplicó el perfil como '{new_prof.name}'.")

    def _on_restore_defaults(self):
        reply = QMessageBox.question(
            self,
            "Restaurar Perfiles de Fábrica",
            "¿Deseas restablecer los 10 perfiles predeterminados a sus valores originales?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.manager.restore_builtin_defaults()
            self._populate_profiles_combo()
            self._load_active_profile_into_ui()
            QMessageBox.information(self, "Restaurado", "Los 10 perfiles predeterminados han sido restaurados.")

    def _apply_temporary(self):
        prof = self._build_profile_from_ui()
        self.manager.apply_temporary_override(prof, reason="Aplicado desde panel (Temporal)")
        self._status_badge.setText("Modo Temporal Activo")
        self._status_badge.setStyleSheet(f"background-color: {_rgba(self._C.ACC, 0.20)}; color: {self._C.ACC}; border: 1px solid {self._C.ACC}; border-radius: 10px; padding: 3px 10px;")
        QMessageBox.information(
            self,
            "Modo Temporal Activado",
            f"El perfil '{prof.name}' se aplicará únicamente a esta conversación.\n"
            f"Al reiniciar la aplicación o pedir 'vuelve a tu personalidad habitual', se recuperará el perfil predeterminado."
        )

    def _save_as_default(self):
        prof = self._build_profile_from_ui()
        self.manager.save_profile(prof, set_as_default=True)
        self._populate_profiles_combo()
        self._load_profile(prof)
        QMessageBox.information(
            self,
            "Personalidad Predeterminada Guardada",
            f"El perfil '{prof.name}' ha sido guardado y establecido como predeterminado.\n"
            f"Permanecerá activo cada vez que inicies VIERNES."
        )

    def _btn_style(self, dim: bool = False) -> str:
        C = self._C
        return f"""
            QPushButton {{
                background-color: {_rgba(C.WHITE, 0.06 if dim else 0.12)};
                color: {C.WHITE};
                border: 1px solid {C.BORDER_A};
                border-radius: 6px;
                padding: 4px 10px;
            }}
            QPushButton:hover {{
                background-color: {_rgba(C.PRI, 0.20)};
                border-color: {C.PRI};
                color: {C.PRI};
            }}
        """
