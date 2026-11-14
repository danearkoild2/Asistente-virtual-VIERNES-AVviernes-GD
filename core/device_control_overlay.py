from __future__ import annotations

import threading
from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from integrations.device_control.manager import device_control
from integrations.device_control.models import NetworkDevice, StateConfidence
from integrations.smarthome.adapters.home_assistant import ha_client


_CATEGORY_ICONS = {
    "tv": "📺",
    "media": "🎵",
    "light": "💡",
    "climate": "❄️",
    "plug": "🔌",
    "fan": "🌀",
    "sensor": "📡",
    "lock": "🔒",
    "other": "📟",
}


class DeviceControlCenterDialog(QDialog):
    """Viernes Device Control — Centro Inteligente de Dispositivos y Domótica."""

    _scan_done_sig = pyqtSignal(list)
    _toast_sig = pyqtSignal(str, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Viernes Device Control — Centro Domótico y de Red")
        self.resize(1040, 680)
        self._selected_remote_id: str = ""
        self._scan_done_sig.connect(self._on_scan_finished)
        self._toast_sig.connect(self._on_toast)

        self.setStyleSheet("""
            QDialog { background: #111114; color: #EEEEF0; font-family: 'Segoe UI', sans-serif; }
            QListWidget {
                background: #17171C; border: 1px solid #272730; border-radius: 10px;
                padding: 6px; outline: none; font-size: 12px; font-weight: 600;
            }
            QListWidget::item { padding: 9px 12px; border-radius: 7px; color: #A0A0AB; margin-bottom: 2px; }
            QListWidget::item:selected { background: #1E1D36; color: #EEEEF0; border-left: 3px solid #6E6AF6; }
            QListWidget::item:hover { background: #1F1F26; color: #FAF9F6; }
            QFrame#Card {
                background: #17171C; border: 1px solid #272730; border-radius: 12px;
            }
            QPushButton {
                background: #1F1F26; color: #EEEEF0; border: 1px solid #272730;
                border-radius: 8px; padding: 7px 13px; font-weight: 600; font-size: 11px;
            }
            QPushButton:hover { background: #272730; border-color: #6E6AF6; }
            QPushButton#Primary { background: #6E6AF6; border-color: #6E6AF6; color: #FAF9F6; }
            QPushButton#Primary:hover { background: #5652D4; }
            QPushButton#Danger { background: #3A1F24; border-color: #F87171; color: #F87171; }
            QLineEdit, QComboBox {
                background: #1A1A21; color: #EEEEF0; border: 1px solid #2E2E3A;
                border-radius: 8px; padding: 7px 10px; font-size: 12px;
            }
            QScrollArea { border: none; background: transparent; }
        """)

        root = QHBoxLayout(self)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(12)

        # Sidebar navigation (11 sections)
        side = QVBoxLayout()
        title = QLabel("⚡ DEVICE CONTROL")
        title.setStyleSheet("font-size: 14px; font-weight: 800; color: #6E6AF6; padding: 4px 6px;")
        side.addWidget(title)

        self._nav = QListWidget()
        self._nav.setFixedWidth(220)
        sections = [
            "🔍  Dispositivos descubiertos",
            "🏠  Mis dispositivos",
            "📺  Televisores",
            "🎵  Multimedia",
            "💡  Iluminación",
            "❄️  Climatización",
            "📡  Sensores",
            "🎮  Control remoto",
            "⚙️  Automatizaciones",
            "📜  Historial de actividad",
            "🌐  Configuración de red",
        ]
        for s in sections:
            self._nav.addItem(QListWidgetItem(s))
        self._nav.setCurrentRow(1)
        self._nav.currentRowChanged.connect(self._on_section_changed)
        side.addWidget(self._nav, 1)

        self._status_lbl = QLabel("Listo · Red autorizada")
        self._status_lbl.setWordWrap(True)
        self._status_lbl.setStyleSheet("font-size: 11px; color: #8B8B99; padding: 4px;")
        side.addWidget(self._status_lbl)

        root.addLayout(side)

        # Main stacked pages
        self._stack = QStackedWidget()
        root.addWidget(self._stack, 1)

        self._build_pages()
        self._refresh_all()

    def _on_toast(self, msg: str, ok: bool) -> None:
        color = "#4ADE80" if ok else "#F87171"
        self._status_lbl.setStyleSheet(f"font-size: 11px; color: {color}; padding: 4px;")
        self._status_lbl.setText(msg)

    def _on_section_changed(self, idx: int) -> None:
        self._stack.setCurrentIndex(idx)
        self._refresh_all()

    def _scrollable_page(self) -> tuple[QWidget, QVBoxLayout]:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)
        scroll.setWidget(inner)
        outer.addWidget(scroll)
        return page, layout

    def _clear_layout(self, layout: QVBoxLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _build_pages(self) -> None:
        # 0: Dispositivos descubiertos
        p0, self._disc_layout = self._scrollable_page()
        hdr0 = QHBoxLayout()
        self._scan_btn = QPushButton("🔍  Escanear red LAN (SSDP / mDNS)")
        self._scan_btn.setObjectName("Primary")
        self._scan_btn.clicked.connect(self._start_scan)
        hdr0.addWidget(self._scan_btn)

        self._manual_ip = QLineEdit()
        self._manual_ip.setPlaceholderText("IP manual (ej. 192.168.1.50)")
        self._manual_name = QLineEdit()
        self._manual_name.setPlaceholderText("Nombre opcional")
        btn_ip = QPushButton("➕  Conectar IP")
        btn_ip.clicked.connect(self._connect_manual_ip)
        hdr0.addWidget(self._manual_ip)
        hdr0.addWidget(self._manual_name)
        hdr0.addWidget(btn_ip)
        w0 = QWidget()
        w0_l = QVBoxLayout(w0)
        w0_l.addLayout(hdr0)
        w0_l.addWidget(p0, 1)
        self._stack.addWidget(w0)

        # 1..6: Mis dispositivos, Televisores, Multimedia, Iluminación, Climatización, Sensores
        self._cat_layouts: dict[int, tuple[str, QVBoxLayout]] = {}
        cat_map = {1: "", 2: "tv", 3: "media", 4: "light", 5: "climate", 6: "sensor"}
        for idx, cat in cat_map.items():
            pg, lay = self._scrollable_page()
            self._cat_layouts[idx] = (cat, lay)
            self._stack.addWidget(pg)

        # 7: Control remoto adaptativo
        self._stack.addWidget(self._build_remote_page())

        # 8: Automatizaciones
        p8, self._auto_layout = self._scrollable_page()
        self._stack.addWidget(p8)

        # 9: Historial de actividad
        p9, self._hist_layout = self._scrollable_page()
        self._stack.addWidget(p9)

        # 10: Configuración de red
        self._stack.addWidget(self._build_network_page())

    def _build_remote_page(self) -> QWidget:
        pg = QWidget()
        lay = QVBoxLayout(pg)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        lay.setSpacing(12)

        top = QHBoxLayout()
        top.addWidget(QLabel("Dispositivo:"))
        self._remote_combo = QComboBox()
        self._remote_combo.currentIndexChanged.connect(self._on_remote_device_changed)
        top.addWidget(self._remote_combo, 1)
        lay.addLayout(top)

        self._remote_info = QLabel("Selecciona un dispositivo emparejado para controlar.")
        self._remote_info.setStyleSheet("color: #A0A0AB; font-size: 12px;")
        self._remote_info.setWordWrap(True)
        lay.addWidget(self._remote_info)

        card = QFrame()
        card.setObjectName("Card")
        grid = QGridLayout(card)
        grid.setSpacing(8)
        grid.setContentsMargins(16, 16, 16, 16)

        def _btn(label: str, cmd: str, r: int, c: int, obj: str = "") -> None:
            b = QPushButton(label)
            if obj:
                b.setObjectName(obj)
            b.clicked.connect(lambda: self._send_remote_cmd(cmd))
            grid.addWidget(b, r, c)

        _btn("⚡ Encender / WoL", "power_on", 0, 0, "Primary")
        _btn("⏻ Apagar", "power_off", 0, 2, "Danger")
        _btn("▲", "up", 1, 1)
        _btn("◀", "left", 2, 0)
        _btn("OK", "ok", 2, 1, "Primary")
        _btn("▶", "right", 2, 2)
        _btn("▼", "down", 3, 1)
        _btn("↩ Atrás", "back", 4, 0)
        _btn("🏠 Inicio", "home", 4, 1)
        _btn("🔇 Mute", "mute", 4, 2)
        _btn("🔉 Vol -", "volume_down", 5, 0)
        _btn("⏯ Play/Pause", "play", 5, 1)
        _btn("🔊 Vol +", "volume_up", 5, 2)
        _btn("HDMI 1", "hdmi1", 6, 0)
        _btn("HDMI 2", "hdmi2", 6, 1)
        _btn("HDMI 3", "hdmi3", 6, 2)
        lay.addWidget(card)

        app_row = QHBoxLayout()
        self._app_input = QLineEdit()
        self._app_input.setPlaceholderText("Abrir aplicación (ej. Netflix, YouTube, Spotify)")
        btn_app = QPushButton("🚀 Abrir App")
        btn_app.setObjectName("Primary")
        btn_app.clicked.connect(lambda: self._send_remote_cmd("launch_app", self._app_input.text().strip()))
        app_row.addWidget(self._app_input, 1)
        app_row.addWidget(btn_app)
        lay.addLayout(app_row)
        return pg

    def _build_network_page(self) -> QWidget:
        pg = QWidget()
        lay = QVBoxLayout(pg)
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        lay.setSpacing(12)

        card = QFrame()
        card.setObjectName("Card")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(16, 16, 16, 16)
        cl.setSpacing(8)
        cl.addWidget(QLabel("Subredes LAN autorizadas (RFC1918, separadas por coma):"))
        self._cidr_edit = QLineEdit(", ".join(device_control._allowed_cidrs))
        btn_cidr = QPushButton("Guardar redes autorizadas")
        btn_cidr.setObjectName("Primary")
        btn_cidr.clicked.connect(self._save_cidrs)
        cl.addWidget(self._cidr_edit)
        cl.addWidget(btn_cidr)

        cl.addWidget(QLabel("Broker MQTT local (opcional):"))
        mqtt_row = QHBoxLayout()
        self._mqtt_host = QLineEdit(str(device_control._mqtt_config.get("host", "")))
        self._mqtt_host.setPlaceholderText("Host MQTT (ej. 192.168.1.10)")
        self._mqtt_port = QLineEdit(str(device_control._mqtt_config.get("port", 1883)))
        self._mqtt_port.setFixedWidth(90)
        btn_mqtt = QPushButton("Guardar MQTT")
        btn_mqtt.clicked.connect(self._save_mqtt)
        mqtt_row.addWidget(self._mqtt_host, 1)
        mqtt_row.addWidget(self._mqtt_port)
        mqtt_row.addWidget(btn_mqtt)
        cl.addLayout(mqtt_row)

        ha_state = "Conectado" if ha_client.is_connected() else "Sin configurar"
        cl.addWidget(QLabel(f"Home Assistant Bridge: {ha_state} ({ha_client.base_url or 'N/A'})"))
        lay.addWidget(card)
        return pg

    def _start_scan(self) -> None:
        self._scan_btn.setEnabled(False)
        self._scan_btn.setText("⏳ Escaneando LAN...")
        threading.Thread(
            target=lambda: self._scan_done_sig.emit(device_control.discover_devices()),
            daemon=True,
        ).start()

    def _on_scan_finished(self, devs: list[NetworkDevice]) -> None:
        self._scan_btn.setEnabled(True)
        self._scan_btn.setText("🔍  Escanear red LAN (SSDP / mDNS)")
        self._toast_sig.emit(f"Escaneo completado: {len(devs)} dispositivos detectados.", True)
        self._refresh_all()

    def _connect_manual_ip(self) -> None:
        ip = self._manual_ip.text().strip()
        if not ip:
            return
        ok, res = device_control.connect_manual_ip(ip, name=self._manual_name.text().strip())
        if ok:
            self._toast_sig.emit(f"Detectado: {res.name} ({res.protocol})", True)  # type: ignore[union-attr]
            self._refresh_all()
        else:
            self._toast_sig.emit(str(res), False)

    def _pair_device(self, device_id: str) -> None:
        ok, msg = device_control.authorize_and_pair(device_id)
        self._toast_sig.emit(msg, ok)
        self._refresh_all()

    def _make_device_card(self, dev: NetworkDevice, discovered_mode: bool = False) -> QFrame:
        card = QFrame()
        card.setObjectName("Card")
        lay = QVBoxLayout(card)
        lay.setContentsMargins(14, 12, 14, 12)
        lay.setSpacing(6)

        top = QHBoxLayout()
        icon = _CATEGORY_ICONS.get(dev.category, "📟")
        name_lbl = QLabel(f"{icon}  {dev.name}")
        name_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #FAF9F6;")
        top.addWidget(name_lbl, 1)

        conf = dev.state_confidence
        if not dev.online:
            badge_txt, badge_col = "SIN RESPUESTA · DESCONOCIDO", "#FBBF24"
        elif conf == StateConfidence.CONFIRMED.value:
            badge_txt, badge_col = "ONLINE · CONFIRMADO", "#4ADE80"
        elif conf == StateConfidence.ESTIMATED.value:
            badge_txt, badge_col = "ONLINE · ESTIMADO", "#60A5FA"
        else:
            badge_txt, badge_col = "ESTADO DESCONOCIDO", "#9CA3AF"
        badge = QLabel(badge_txt)
        badge.setStyleSheet(f"font-size: 10px; font-weight: 700; color: {badge_col};")
        top.addWidget(badge)
        lay.addLayout(top)

        meta = QLabel(
            f"{dev.manufacturer} · {dev.model} | Protocolo: {dev.protocol} | "
            f"IP: {dev.ip or 'N/A'} | MAC: {dev.mac or 'N/A'} | Sala: {dev.room}"
        )
        meta.setStyleSheet("font-size: 11px; color: #A0A0AB;")
        meta.setWordWrap(True)
        lay.addWidget(meta)

        if dev.power_limitations:
            lim = QLabel(f"ℹ️ {dev.power_limitations}")
            lim.setStyleSheet("font-size: 10px; color: #8B8B99;")
            lim.setWordWrap(True)
            lay.addWidget(lim)

        btns = QHBoxLayout()
        if discovered_mode and not dev.paired:
            b_pair = QPushButton("🔐 Autorizar y emparejar")
            b_pair.setObjectName("Primary")
            b_pair.clicked.connect(lambda _, did=dev.id: self._pair_device(did))
            btns.addWidget(b_pair)
        else:
            b_on = QPushButton("⚡ Encender")
            b_on.clicked.connect(lambda _, did=dev.id: self._quick_cmd(did, "power_on"))
            b_off = QPushButton("⏻ Apagar")
            b_off.clicked.connect(lambda _, did=dev.id: self._quick_cmd(did, "power_off"))
            b_rem = QPushButton("🎮 Control")
            b_rem.clicked.connect(lambda _, did=dev.id: self._open_in_remote(did))
            b_ref = QPushButton("🔄 Estado")
            b_ref.clicked.connect(lambda _, did=dev.id: self._refresh_one(did))
            btns.addWidget(b_on)
            btns.addWidget(b_off)
            btns.addWidget(b_rem)
            btns.addWidget(b_ref)
        btns.addStretch(1)
        lay.addLayout(btns)
        return card

    def _quick_cmd(self, device_id: str, cmd: str) -> None:
        ok, msg = device_control.control_device(device_id, cmd, confirmed=True, actor="ui")
        self._toast_sig.emit(msg, ok)
        self._refresh_all()

    def _refresh_one(self, device_id: str) -> None:
        ok, _ = device_control.refresh_device(device_id)
        self._toast_sig.emit("Estado actualizado." if ok else "Sin respuesta (estado marcado como desconocido).", ok)
        self._refresh_all()

    def _open_in_remote(self, device_id: str) -> None:
        self._selected_remote_id = device_id
        self._nav.setCurrentRow(7)

    def _on_remote_device_changed(self) -> None:
        did = self._remote_combo.currentData()
        if did:
            self._selected_remote_id = str(did)
            devs = [d for d in device_control.list_devices() if d.id == self._selected_remote_id]
            if devs:
                d = devs[0]
                self._remote_info.setText(
                    f"{d.name} ({d.protocol}) · IP {d.ip or 'local'} · "
                    f"Capacidades: {', '.join(d.capabilities)} · {d.power_limitations}"
                )

    def _send_remote_cmd(self, cmd: str, value: Any = None) -> None:
        did = self._remote_combo.currentData() or self._selected_remote_id
        if not did:
            self._toast_sig.emit("Selecciona un dispositivo primero.", False)
            return
        ok, msg = device_control.control_device(str(did), cmd, value=value, confirmed=True, actor="remote_ui")
        self._toast_sig.emit(msg, ok)

    def _save_cidrs(self) -> None:
        cidrs = [c.strip() for c in self._cidr_edit.text().split(",") if c.strip()]
        ok, msg = device_control.set_allowed_cidrs(cidrs)
        self._toast_sig.emit(msg, ok)

    def _save_mqtt(self) -> None:
        try:
            port = int(self._mqtt_port.text().strip() or 1883)
        except ValueError:
            port = 1883
        device_control.set_mqtt_config(self._mqtt_host.text().strip(), port=port)
        self._toast_sig.emit("Configuración MQTT guardada.", True)

    def _refresh_all(self) -> None:
        # Discovered
        self._clear_layout(self._disc_layout)
        disc = device_control.list_discovered()
        if not disc:
            self._disc_layout.addWidget(QLabel("Pulsa 'Escanear red LAN' o conecta un dispositivo por IP."))
        for d in disc:
            self._disc_layout.addWidget(self._make_device_card(d, discovered_mode=True))

        # Category tabs
        for _, (cat, lay) in self._cat_layouts.items():
            self._clear_layout(lay)
            devs = device_control.list_devices(category=cat)
            if not devs:
                lay.addWidget(QLabel("No hay dispositivos registrados en esta categoría."))
            for d in devs:
                lay.addWidget(self._make_device_card(d, discovered_mode=False))

        # Remote combo
        self._remote_combo.blockSignals(True)
        self._remote_combo.clear()
        for d in device_control.list_devices():
            self._remote_combo.addItem(f"{_CATEGORY_ICONS.get(d.category, '📟')} {d.name} ({d.protocol})", d.id)
        if self._selected_remote_id:
            idx = self._remote_combo.findData(self._selected_remote_id)
            if idx >= 0:
                self._remote_combo.setCurrentIndex(idx)
        self._remote_combo.blockSignals(False)
        self._on_remote_device_changed()

        # Automations & Scenes
        self._clear_layout(self._auto_layout)
        for sc in device_control._scenes.values():
            c = QFrame()
            c.setObjectName("Card")
            cl = QHBoxLayout(c)
            cl.setContentsMargins(14, 10, 14, 10)
            txt = QVBoxLayout()
            t1 = QLabel(f"✨ {sc.name}")
            t1.setStyleSheet("font-weight: 700; font-size: 13px;")
            t2 = QLabel(sc.description)
            t2.setStyleSheet("color: #A0A0AB; font-size: 11px;")
            txt.addWidget(t1)
            txt.addWidget(t2)
            cl.addLayout(txt, 1)
            b = QPushButton("Ejecutar")
            b.setObjectName("Primary")
            b.clicked.connect(lambda _, sid=sc.id: self._run_scene(sid))
            cl.addWidget(b)
            self._auto_layout.addWidget(c)

        # History
        self._clear_layout(self._hist_layout)
        for ev in device_control.get_history(limit=35):
            lbl = QLabel(f"[{ev.timestamp}] ({ev.status.upper()}) {ev.device_id} · {ev.action} — {ev.detail}")
            lbl.setStyleSheet("font-size: 11px; color: #C4C4CF; padding: 4px 6px; border-bottom: 1px solid #22222A;")
            lbl.setWordWrap(True)
            self._hist_layout.addWidget(lbl)

    def _run_scene(self, scene_id: str) -> None:
        if scene_id == "apagado_general":
            ans = QMessageBox.question(self, "Confirmar Apagado General", "¿Apagar todos los dispositivos?")
            if ans != QMessageBox.StandardButton.Yes:
                return
        ok, msg = device_control.execute_scene(scene_id, confirmed=True, actor="ui")
        self._toast_sig.emit(msg, ok)
        self._refresh_all()
