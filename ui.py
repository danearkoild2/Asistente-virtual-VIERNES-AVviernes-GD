from __future__ import annotations

import json
import logging
import math
import os
import platform
import random
import subprocess
import sys
import threading
import time
from datetime import datetime, date
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=FutureWarning, module=r".*pynvml.*")

import psutil

if platform.system() == "Windows":
    _WIN_HIDE: dict = {"creationflags": subprocess.CREATE_NO_WINDOW}
else:
    _WIN_HIDE: dict = {}

# Qt's video backend prints the ffmpeg stream banner — codec, bitrate, the
# whole signed googlevideo URL — to the console for every stream it opens. That
# is two screenfuls per video, it looks like an error to anyone reading the log,
# and it puts a URL carrying the viewer's IP address into a terminal people
# paste into bug reports. Silenced here, before Qt initialises its logging.
# An explicit setting from the user is left alone.
os.environ.setdefault("QT_LOGGING_RULES", "qt.multimedia.*=false;qt.rhi.*=false;qt.webenginecontext.*=false")
os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--use-angle=d3d11 --ignore-gpu-blocklist --enable-webgl")

try:
    import PyQt6.QtWebEngineWidgets  # noqa: F401
except ImportError:
    pass

from PyQt6.QtCore import (
    QCoreApplication, QEasingCurve, QEvent, QLineF, QMimeData, QObject, QParallelAnimationGroup, QPointF,
    QPoint, QPropertyAnimation, QRect, QRectF, QSize, QSizeF, Qt, QTimer,
    QUrl, pyqtSignal,
)

try:
    QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts, True)
except Exception:
    pass
from PyQt6.QtGui import (
    QBrush, QColor, QConicalGradient, QCursor, QDragEnterEvent, QDropEvent, QFont,
    QFontDatabase, QKeySequence, QLinearGradient, QPainter, QPainterPath,
    QPen, QPixmap, QRadialGradient, QShortcut,
)
# Video playback for the HUD. Part of PyQt6, so it costs no new dependency —
# but the multimedia plugins are a separate piece of the Qt install and can be
# absent on a stripped-down system, so a failure here disables one feature
# rather than stopping VIERNES from starting.
try:
    from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
    from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
    HAVE_VIDEO = True
except Exception as _e:            # noqa: BLE001 - reported, never fatal
    QAudioOutput = QMediaPlayer = QGraphicsVideoItem = None
    HAVE_VIDEO = False
    print(f"[Video] playback unavailable ({_e}) — the HUD will not show video.")

from PyQt6.QtWidgets import (
    QApplication, QComboBox, QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenu, QPushButton, QScrollArea, QSizePolicy, QSplitter,
    QGraphicsScene, QGraphicsView, QGraphicsDropShadowEffect, QGraphicsOpacityEffect,
    QStackedWidget, QTextEdit, QVBoxLayout, QWidget, QProgressBar,
)

try:
    from core.avatar import HoloAvatar
except Exception:      # pragma: no cover — HUD must never die over cosmetics
    HoloAvatar = None

try:
    from core.vrm import VRMWidget
except Exception as _e_vrm_imp:
    print(f"[VRM 3D] Import error: {_e_vrm_imp}")
    VRMWidget = None

try:
    from core.live2d import Live2DWidget, NativeLive2DWidget
except Exception:
    Live2DWidget = None
    NativeLive2DWidget = None

try:
    from core.visual_panel import EdithVisualPanel
    from core.visual_engine import VisualCardData, VisualEngine
except Exception as _ve_imp_err:
    EdithVisualPanel = None
    VisualCardData = None
    VisualEngine = None
    print(f"[VisualPanel] Import error: {_ve_imp_err}")

def _base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent

BASE_DIR   = _base_dir()
CONFIG_DIR = BASE_DIR / "config"
API_FILE            = CONFIG_DIR / "api_keys.json"
VIDEO_SETTINGS_FILE = CONFIG_DIR / "video_settings.json"


def _read_full_config() -> dict:
    """Read api_keys.json config dict. Returns {} on any error."""
    try:
        return json.loads(API_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _load_video_muted() -> bool:
    """Return persisted mute preference for the internal video player (default False)."""
    try:
        data = json.loads(VIDEO_SETTINGS_FILE.read_text(encoding="utf-8"))
        return bool(data.get("video_muted", False))
    except Exception:
        return False


def _save_video_muted(muted: bool) -> None:
    """Persist the internal video player mute preference across videos and restarts."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        VIDEO_SETTINGS_FILE.write_text(
            json.dumps({"video_muted": bool(muted)}, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass


# Single source of truth for the release name — the window title, the header
# badge and the readme must never disagree again.
APP_VERSION  = "Viernes Studio"
APP_PROTOCOL = "VIERNES-STUDIO"

_DEFAULT_W, _DEFAULT_H = 1260, 800
_MIN_W,     _MIN_H     = 980, 640
_LEFT_W   = 224
_RIGHT_W  = 408
_HEADER_H = 58

_OS = platform.system()  # "Windows" | "Darwin" | "Linux"

# Modern system typography — the native UI face of each OS.
UI_FONT = {"Windows": "Segoe UI", "Darwin": "Helvetica Neue"}.get(_OS, "Noto Sans")


class C:
    BG        = "#111114"   # Deep warm architectural carbon
    PANEL     = "#17171C"   # Primary elevated surface
    PANEL2    = "#1F1F26"   # Secondary elevated surface / card
    BORDER    = "#272730"   # Hairline structural divider
    BORDER_B  = "#353542"   # Interactive / focused border
    BORDER_A  = "#1E1E25"   # Subtle inner separator
    PRI       = "#6E6AF6"   # Editorial Indigo primary accent
    PRI_DIM   = "#5652D4"   # Muted / pressed primary
    PRI_GHO   = "#1E1D36"   # Soft translucent selection / tint
    ACC       = "#E07A5F"   # Warm Terracotta secondary accent (speaking/warmth)
    ACC2      = "#EAB308"   # Warm Amber (thinking/processing)
    GREEN     = "#34D399"   # Refined Emerald (listening/active)
    GREEN_D   = "#10B981"   # Deep Emerald
    RED       = "#F87171"   # Soft Coral Red (muted/alerts)
    MUTED_C   = "#F87171"
    TEXT      = "#EEEEF0"   # Warm Alabaster primary text
    TEXT_DIM  = "#6E6E7A"   # Muted metadata / captions
    TEXT_MED  = "#A0A0AB"   # Balanced secondary text
    WHITE     = "#FAF9F6"   # Crisp off-white
    DARK      = "#0C0C0E"   # Inset input / well background
    BAR_BG    = "#25252E"   # Subtle progress track


# Keys tied to the accent colour — architectural carbon surfaces and semantic status colours stay fixed
_HUE_LINKED = (
    "PRI", "PRI_DIM", "PRI_GHO",
)
_PALETTE_DEFAULTS: dict[str, str] = {k: getattr(C, k) for k in _HUE_LINKED}

DEFAULT_UI_COLOR = _PALETTE_DEFAULTS["PRI"]

THEME_PRESETS = [
    ("indigo",     "Índigo Editorial",  "#6E6AF6"),
    ("terracotta", "Terracota Cálido",  "#E07A5F"),
    ("sage",       "Salvia Natural",    "#34D399"),
    ("amber",      "Ámbar Estudio",     "#D97706"),
    ("ocean",      "Azul Atlántico",    "#38BDF8"),
    ("rose",       "Rosa Cuarzo",       "#F472B6"),
]

def cycle_ui_theme(current_hex: str) -> tuple[str, str, str]:
    """Cycle to next theme preset: returns (key, label, hex)."""
    cur = (current_hex or "").strip().lower()
    for idx, (k, name, hex_val) in enumerate(THEME_PRESETS):
        if hex_val.lower() == cur:
            return THEME_PRESETS[(idx + 1) % len(THEME_PRESETS)]
    return THEME_PRESETS[0]

def get_theme_label(current_hex: str) -> str:
    """Return friendly label for given hex color."""
    cur = (current_hex or "").strip().lower()
    for k, name, hex_val in THEME_PRESETS:
        if hex_val.lower() == cur:
            return name
    return f"Personalizado ({cur[:7]})"


def apply_ui_accent(accent_hex: str) -> bool:
    """
    Re-derives the whole teal-family palette from the chosen accent colour
    (hue shift — brightness/saturation ratios are preserved, design stays intact).
    Painted elements (HUD, waveform, metrics) pick up the new colour on the next
    frame; stylesheet-based panels pick it up when they are rebuilt.
    """
    import colorsys

    accent_hex = (accent_hex or "").strip().lower()
    if not (accent_hex.startswith("#") and len(accent_hex) == 7):
        return False
    try:
        int(accent_hex[1:], 16)
    except ValueError:
        return False

    def _hsv(h: str) -> tuple[float, float, float]:
        r = int(h[1:3], 16) / 255
        g = int(h[3:5], 16) / 255
        b = int(h[5:7], 16) / 255
        return colorsys.rgb_to_hsv(r, g, b)

    base_h            = _hsv(_PALETTE_DEFAULTS["PRI"])[0]
    acc_h, acc_s, _av = _hsv(accent_hex)
    dh   = acc_h - base_h
    grey = acc_s < 0.08   # near-grey accent → the whole theme is desaturated

    for key, hex0 in _PALETTE_DEFAULTS.items():
        h, s, v = _hsv(hex0)
        if grey:
            s *= 0.15
        r, g, b = colorsys.hsv_to_rgb((h + dh) % 1.0, s, v)
        setattr(C, key, "#{:02x}{:02x}{:02x}".format(
            int(r * 255 + 0.5), int(g * 255 + 0.5), int(b * 255 + 0.5)))
    return True


def current_palette() -> dict[str, str]:
    """A snapshot of the accent-linked colours currently on class C."""
    return {k: getattr(C, k) for k in _HUE_LINKED}


_ALL_PALETTE_KEYS = (
    "BG", "PANEL", "PANEL2", "BORDER", "BORDER_B", "BORDER_A",
    "PRI", "PRI_DIM", "PRI_GHO", "ACC", "ACC2",
    "GREEN", "GREEN_D", "RED", "MUTED_C",
    "TEXT", "TEXT_DIM", "TEXT_MED", "WHITE", "DARK", "BAR_BG",
)


def full_palette_snapshot() -> dict[str, str]:
    """Snapshot of all colour tokens currently on class C."""
    return {k: getattr(C, k) for k in _ALL_PALETTE_KEYS}


def apply_full_palette(pal: dict[str, str]) -> None:
    """Apply a complete theme palette dictionary to class C."""
    for k in _ALL_PALETTE_KEYS:
        if k in pal and isinstance(pal[k], str):
            setattr(C, k, pal[k])


def retheme_all_widgets(old: dict[str, str], new: dict[str, str]) -> None:
    """
    LIVE full theme change. Replaces the old palette colours with the new ones
    in EVERY widget's stylesheet across the app and repaints them. This way the
    colour change applies INSTANTLY across the whole interface — panels, buttons,
    borders included — not just the painted elements. No restart needed.
    """
    mapping = {old[k].lower(): new[k].lower()
               for k in old if old[k].lower() != new.get(k, old[k]).lower()}
    if not mapping:
        return
    app = QApplication.instance()
    if app is None:
        return
    for w in app.allWidgets():
        try:
            ss = w.styleSheet()
            if ss:
                s2 = ss
                for o, n in mapping.items():
                    if o in s2:
                        s2 = s2.replace(o, n)
                if s2 != ss:
                    w.setStyleSheet(s2)
            w.update()
        except Exception:
            pass


def qcol(h: str, a: int = 255) -> QColor:
    c = QColor(h); c.setAlpha(a); return c


def _rgba(hex_: str, a: float) -> str:
    c = QColor(hex_)
    return f"rgba({c.red()},{c.green()},{c.blue()},{a})"


def _ss_row(on: bool = False, accent: bool = False) -> str:
    """Drawer / list row button: quiet by default, tinted when on."""
    if on:
        fg, bg, bd, hv = C.GREEN, _rgba(C.GREEN, 0.12), _rgba(C.GREEN, 0.28), _rgba(C.GREEN, 0.20)
    elif accent:
        fg, bg, bd, hv = C.PRI, _rgba(C.PRI, 0.12), _rgba(C.PRI, 0.26), _rgba(C.PRI, 0.20)
    else:
        fg, bg, bd, hv = C.TEXT_MED, "transparent", "transparent", _rgba(C.WHITE, 0.05)
    return f"""
        QPushButton {{
            background: {bg}; color: {fg}; border: 1px solid {bd};
            border-radius: 8px; text-align: left; padding: 0 12px;
            font-weight: 500;
        }}
        QPushButton:hover {{ background: {hv}; color: {C.WHITE}; border-color: {C.BORDER_B}; }}
        QPushButton:disabled {{ color: {C.TEXT_DIM}; }}
    """


def _ss_icon() -> str:
    return f"""
        QPushButton {{
            background: {C.PANEL}; color: {C.TEXT_MED};
            border: 1px solid {C.BORDER}; border-radius: 9px;
        }}
        QPushButton:hover {{
            background: {C.PANEL2}; color: {C.WHITE};
            border-color: {C.BORDER_B};
        }}
        QPushButton:checked {{
            background: {_rgba(C.PRI, 0.15)}; color: {C.PRI};
            border-color: {_rgba(C.PRI, 0.42)};
        }}
    """


def _ss_tool() -> str:
    return f"""
        QPushButton {{
            background: transparent; color: {C.TEXT_MED};
            border: 1px solid transparent; border-radius: 8px; padding: 0 13px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background: {_rgba(C.WHITE, 0.05)}; color: {C.WHITE};
        }}
        QPushButton:checked {{
            background: {C.PANEL2}; color: {C.WHITE};
            border: 1px solid {C.BORDER_B};
        }}
    """


def _ss_drawer() -> str:
    return f"""
        QWidget#QuickDrawer {{
            background: {C.PANEL};
            border: 1px solid {C.BORDER_B};
            border-radius: 12px;
        }}
    """


def _ss_soft_btn(color: str) -> str:
    return f"""
        QPushButton {{
            background: {_rgba(color, 0.12)}; color: {color};
            border: 1px solid {_rgba(color, 0.25)}; border-radius: 9px; padding: 0 12px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background: {_rgba(color, 0.20)};
            border-color: {_rgba(color, 0.45)};
            color: {C.WHITE};
        }}
        QPushButton:pressed {{ background: {_rgba(color, 0.28)}; }}
    """


_APP_SS = f"""
    QToolTip {{
        background: {C.PANEL2}; color: {C.TEXT};
        border: 1px solid {C.BORDER_B}; border-radius: 6px; padding: 5px 9px;
    }}
    QScrollBar:vertical {{
        background: transparent; width: 6px; margin: 0px; border: none;
    }}
    QScrollBar::handle:vertical {{
        background: {C.BORDER_B}; border-radius: 3px; min-height: 24px;
    }}
    QScrollBar::handle:vertical:hover {{
        background: {C.TEXT_DIM};
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: transparent; }}
"""


# ── Windows GPU via NVML DLL (no subprocess, no console window) ──────────────
_nvml_lib: object = None   # cached ctypes DLL
_nvml_ok:  object = None   # None=untested, True=works, False=unavailable


def _nvml_gpu_windows() -> float:
    """Return NVIDIA GPU utilisation % using nvml.dll directly — zero subprocess."""
    global _nvml_lib, _nvml_ok
    if _nvml_ok is False:
        return -1.0
    try:
        import ctypes

        class _Util(ctypes.Structure):
            _fields_ = [("gpu", ctypes.c_uint), ("memory", ctypes.c_uint)]

        if _nvml_lib is None:
            for dll_name in ("nvml", r"C:\Windows\System32\nvml.dll"):
                try:
                    lib = ctypes.WinDLL(dll_name)
                    lib.nvmlInit_v2()
                    _nvml_lib = lib
                    break
                except Exception:
                    continue

        if _nvml_lib is None:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=FutureWarning)
                import pynvml  # type: ignore
            pynvml.nvmlInit()
            h = pynvml.nvmlDeviceGetHandleByIndex(0)
            _nvml_ok = True
            return float(pynvml.nvmlDeviceGetUtilizationRates(h).gpu)

        dev = ctypes.c_void_p()
        _nvml_lib.nvmlDeviceGetHandleByIndex_v2(0, ctypes.byref(dev))
        util = _Util()
        _nvml_lib.nvmlDeviceGetUtilizationRates(dev, ctypes.byref(util))
        _nvml_ok = True
        return float(util.gpu)
    except Exception:
        _nvml_ok = False
        return -1.0


class _SysMetrics:
    def __init__(self):
        self.cpu  = 0.0
        self.mem  = 0.0
        self.net  = 0.0   
        self.gpu  = -1.0  
        self.tmp  = -1.0  
        self._lock = threading.Lock()
        self._last_net = psutil.net_io_counters()
        self._last_net_t = time.time()
        self._running = True
        # Probe caches — GPU (NVML) and temperature (WMI) are the expensive
        # queries; initialise their handles once and reuse them instead of
        # rebuilding a connection on every poll.
        self._slow_tick = 0            # gpu/temp refreshed every 3rd cycle
        self._pynvml    = None         # cached pynvml module + device handle
        self._pynvml_h  = None
        self._pynvml_ok = None         # None=untested, False=unavailable here
        self._nv_unix   = None         # cached (lib, dev) for Linux/macOS NVML
        self._wmi_conn  = None         # cached WMI connection (creating one is slow)
        self._wmi_ok    = None         # None=untested, False=unavailable here
        self._paused    = False
        self._low_power = False
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()

    def pause(self):
        """Suspend hardware telemetry collection when window is minimized."""
        self._paused = True

    def resume(self):
        """Resume hardware telemetry collection when window is restored."""
        self._paused = False

    def set_low_power(self, enabled: bool):
        """Slow down polling to 8s during sleeping / idle states."""
        self._low_power = bool(enabled)

    def _loop(self):
        while self._running:
            if self._paused:
                time.sleep(3.0)
                continue
            try:
                self._update()
            except Exception:
                pass
            interval = 8.0 if self._low_power else 2.0
            time.sleep(interval)

    def _update(self):
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent

        nc  = psutil.net_io_counters()
        now = time.time()
        dt  = now - self._last_net_t
        if dt > 0:
            sent = (nc.bytes_sent - self._last_net.bytes_sent) / dt
            recv = (nc.bytes_recv - self._last_net.bytes_recv) / dt
            net  = (sent + recv) / (1024 * 1024)
        else:
            net = 0.0
        self._last_net   = nc
        self._last_net_t = now

        # GPU and temperature change slowly and are the most expensive probes
        # (NVML / WMI) — refresh them every 3rd cycle (~6 s) instead of every
        # cycle, reusing the previous reading in between.
        self._slow_tick = (self._slow_tick + 1) % 3
        if self._slow_tick == 1:
            gpu = self._get_gpu()
            tmp = self._get_temp()
        else:
            gpu = self.gpu
            tmp = self.tmp

        with self._lock:
            self.cpu = cpu
            self.mem = mem
            self.net = net
            self.gpu = gpu
            self.tmp = tmp

    def _get_gpu(self) -> float:
        # pynvml — subprocess-free; initialise once and reuse the handle.
        # Re-initialising NVML on every poll is slow, so cache it and stop
        # retrying pynvml entirely once it proves unavailable here.
        if self._pynvml_ok is not False:
            try:
                if self._pynvml_h is None:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", category=FutureWarning)
                        import pynvml  # type: ignore
                    pynvml.nvmlInit()
                    self._pynvml    = pynvml
                    self._pynvml_h  = pynvml.nvmlDeviceGetHandleByIndex(0)
                    self._pynvml_ok = True
                return float(self._pynvml.nvmlDeviceGetUtilizationRates(self._pynvml_h).gpu)
            except Exception:
                self._pynvml_ok = False

        # Windows: nvml.dll via ctypes (already cached in _nvml_gpu_windows)
        if _OS == "Windows":
            return _nvml_gpu_windows()

        # Linux / macOS: libnvidia-ml shared lib via ctypes — init once, reuse
        try:
            import ctypes

            class _Util(ctypes.Structure):
                _fields_ = [("gpu", ctypes.c_uint), ("memory", ctypes.c_uint)]

            if self._nv_unix is None:
                _lib = "libnvidia-ml.so.1" if _OS == "Linux" else "libnvidia-ml.dylib"
                nv = ctypes.CDLL(_lib)
                nv.nvmlInit_v2()
                dev = ctypes.c_void_p()
                nv.nvmlDeviceGetHandleByIndex_v2(0, ctypes.byref(dev))
                self._nv_unix = (nv, dev)

            nv, dev = self._nv_unix
            u = _Util()
            nv.nvmlDeviceGetUtilizationRates(dev, ctypes.byref(u))
            return float(u.gpu)
        except Exception:
            pass

        return -1.0   # N/A — zero subprocess on all platforms

    def _get_temp(self) -> float:
        # psutil — works on Linux; occasionally Windows with driver support
        try:
            temps = psutil.sensors_temperatures()
            for name in ["coretemp", "k10temp", "cpu_thermal", "acpitz",
                         "cpu-thermal", "zenpower", "it8688"]:
                if name in temps and temps[name]:
                    return temps[name][0].current
            for entries in temps.values():
                if entries:
                    return entries[0].current
        except Exception:
            pass

        # Windows: wmi module (pure Python COM, zero subprocess). Reuse a single
        # connection — building a fresh wmi.WMI() on every poll spins up a COM
        # connection each time and is very slow. Give up after one failure.
        if _OS == "Windows" and self._wmi_ok is not False:
            try:
                if self._wmi_conn is None:
                    import wmi  # type: ignore
                    self._wmi_conn = wmi.WMI(namespace="root/wmi")
                tz = self._wmi_conn.MSAcpi_ThermalZoneTemperature()
                if tz:
                    return (tz[0].CurrentTemperature / 10.0) - 273.15
            except Exception:
                self._wmi_ok   = False
                self._wmi_conn = None

        return -1.0   # N/A — zero subprocess on all platforms

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "cpu": self.cpu,
                "mem": self.mem,
                "net": self.net,
                "gpu": self.gpu,
                "tmp": self.tmp,
            }


_metrics = _SysMetrics()


class MiniEqualizer(QWidget):
    """Animated 3-bar mini cybernetic equalizer to show live music streaming."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(18, 18)
        self.color = QColor("#1ed760")
        self._values = [6, 12, 8]
        self._phase = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(110)
        self._timer.timeout.connect(self._step)

    def start_anim(self, color_hex: str = "#1ed760"):
        self.color = QColor(color_hex)
        if not self._timer.isActive():
            self._timer.start()

    def stop_anim(self):
        self._timer.stop()
        self._values = [3, 3, 3]
        self.update()

    def _step(self):
        self._phase += 0.40
        self._values = [
            max(3, int(8 + 6 * math.sin(self._phase))),
            max(3, int(11 + 7 * math.sin(self._phase + 1.2))),
            max(3, int(7 + 5 * math.sin(self._phase + 2.5))),
        ]
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(self.color))
        bw = 3.2
        spacing = 2.4
        for i, val in enumerate(self._values):
            x = 1.0 + i * (bw + spacing)
            y = 17 - val
            p.drawRoundedRect(QRectF(x, y, bw, val), 1.2, 1.2)
        p.end()


class MusicMiniWidget(QFrame):
    """
    Compact, cybernetic glassmorphic mini-widget displayed at the top-left of the HUD
    whenever Spotify or YouTube is actively playing music.
    Shows track title, artist, platform badge (Spotify green / YouTube red),
    animated mini equalizer bars, and album art thumbnail.
    Clicking expands the full Edith visual card.
    """

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MusicMiniWidget")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(46)
        self.setMinimumWidth(220)
        self.setMaximumWidth(295)

        # Drop shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 5, 10, 5)
        layout.setSpacing(8)

        # 1. Thumbnail / Platform icon label
        self._thumb_lbl = QLabel(self)
        self._thumb_lbl.setFixedSize(34, 34)
        self._thumb_lbl.setStyleSheet("background: rgba(0, 0, 0, 0.45); border-radius: 6px;")
        self._thumb_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._thumb_lbl)

        # 2. Track & Platform details
        info_lay = QVBoxLayout()
        info_lay.setContentsMargins(0, 1, 0, 1)
        info_lay.setSpacing(1)

        # Title line
        self._title_lbl = QLabel("Sin reproducción", self)
        self._title_lbl.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self._title_lbl.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        info_lay.addWidget(self._title_lbl)

        # Platform + Artist line
        sub_row = QHBoxLayout()
        sub_row.setContentsMargins(0, 0, 0, 0)
        sub_row.setSpacing(5)

        self._badge_lbl = QLabel("SPOTIFY", self)
        self._badge_lbl.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        sub_row.addWidget(self._badge_lbl)

        self._artist_lbl = QLabel("", self)
        self._artist_lbl.setFont(QFont("Segoe UI", 8))
        self._artist_lbl.setStyleSheet("color: #94a3b8; background: transparent; border: none;")
        sub_row.addWidget(self._artist_lbl)
        sub_row.addStretch()

        info_lay.addLayout(sub_row)
        layout.addLayout(info_lay, stretch=1)

        # 3. Animated mini equalizer
        self._eq = MiniEqualizer(self)
        layout.addWidget(self._eq)

        self._current_track = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def update_track(self, track):
        self._current_track = track
        title = track.title or "Sin título"
        artist = track.artist or ""
        platform_key = getattr(track, "platform_key", "spotify").lower()

        # Elide long title
        fm = self._title_lbl.fontMetrics()
        elided_title = fm.elidedText(title, Qt.TextElideMode.ElideRight, 165)
        self._title_lbl.setText(elided_title)

        # Elide long artist
        fm_a = self._artist_lbl.fontMetrics()
        elided_artist = fm_a.elidedText(f"• {artist}" if artist else "", Qt.TextElideMode.ElideRight, 105)
        self._artist_lbl.setText(elided_artist)

        # Platform theme styling
        if platform_key == "youtube":
            color_accent = "#F87171"
            badge_text = "▶ YouTube"
        else:  # spotify
            color_accent = "#34D399"
            badge_text = "● Spotify"

        self._badge_lbl.setText(badge_text)
        self._badge_lbl.setStyleSheet(f"color: {color_accent}; font-weight: 600; background: transparent; border: none;")

        self.setStyleSheet(f"""
            QFrame#MusicMiniWidget {{
                background: rgba(23, 23, 28, 0.94);
                border: 1px solid {C.BORDER_B};
                border-radius: 10px;
            }}
            QFrame#MusicMiniWidget:hover {{
                border-color: {color_accent};
                background: rgba(31, 31, 38, 0.98);
            }}
        """)

        # Thumbnail rendering with rounded corners
        if track.thumbnail_path and Path(track.thumbnail_path).exists():
            pm = QPixmap(str(track.thumbnail_path))
            if not pm.isNull():
                scaled = pm.scaled(34, 34, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                rounded = QPixmap(34, 34)
                rounded.fill(Qt.GlobalColor.transparent)
                p = QPainter(rounded)
                p.setRenderHint(QPainter.RenderHint.Antialiasing, True)
                path = QPainterPath()
                path.addRoundedRect(0, 0, 34, 34, 6, 6)
                p.setClipPath(path)
                p.drawPixmap(0, 0, scaled)
                p.end()
                self._thumb_lbl.setPixmap(rounded)
            else:
                self._thumb_lbl.setText("🎵")
        else:
            self._thumb_lbl.setText("🎵")

        # Equalizer animation
        if track.status == "PLAYING":
            self._eq.start_anim(color_accent)
        else:
            self._eq.stop_anim()

        self.setToolTip(f"Reproduciendo: {title} ({track.platform})\nClick para abrir tarjeta visual completa")


class _OverlayEventFilter(QObject):
    """Reliably catches hide or close events from overlay widgets to unregister them."""
    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self._callback = callback

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Type.Hide, QEvent.Type.Close):
            try:
                self._callback(obj)
            except Exception:
                pass
        return False


class HudCanvas(QWidget):
    _music_track_sig = pyqtSignal(object)

    def __init__(self, face_path: str, assistant_name: str = "Viernes", parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        self.setMinimumSize(300, 300)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.muted    = False
        self.speaking = False
        self.state    = "INITIALISING"
        self._assistant_name = assistant_name

        # The holographic head that fills the HUD. If it could not be imported
        # we fall back to the old glowing core so the panel is never empty.
        self._avatar = None
        if HoloAvatar is not None:
            try:
                self._avatar = HoloAvatar()
            except Exception:
                self._avatar = None

        # Edith Live2D Pro (Native C++ / OpenGL or fallback WebEngine)
        self._live2d_widget = None

        if NativeLive2DWidget is not None:
            try:
                from core.live2d.native_widget import LIVE2D_NATIVE_AVAILABLE
            except Exception:
                LIVE2D_NATIVE_AVAILABLE = False

            if LIVE2D_NATIVE_AVAILABLE:
                try:
                    self._live2d_widget = NativeLive2DWidget(self)
                    self._live2d_widget.model_error.connect(self._on_live2d_error)
                    print("[Live2D] Using Native C++ Cubism OpenGL engine for Edith.")
                except Exception as _e_nat:
                    print(f"[Live2D] Native engine not available ({_e_nat}), trying web engine...")
                    self._live2d_widget = None

        if self._live2d_widget is None and Live2DWidget is not None:
            try:
                self._live2d_widget = Live2DWidget(self)
                self._live2d_widget.model_error.connect(self._on_live2d_web_error)
                print("[Live2D] Using WebEngine (PixiJS + Cubism Core) for Edith.")
            except Exception as _e:
                print(f"[Live2D] Error creating Live2DWidget: {_e}")
                self._live2d_widget = None

        if self._live2d_widget is not None:
            try:
                from memory.config_manager import (
                    get_edith_autonomy_enabled,
                    get_edith_spontaneity_level,
                    get_edith_mood
                )
                self._live2d_widget.set_autonomy_enabled(get_edith_autonomy_enabled())
                self._live2d_widget.set_spontaneity_level(get_edith_spontaneity_level())
                self._live2d_widget.set_mood(get_edith_mood())
            except Exception:
                pass

        # 3D VRM engine disabled for maximum performance (only Live2D & Holograma Core)
        self._vrm_widget = None

        # Edith Contextual Visual Intelligence Panel (positioned to the right of Edith)
        self._visual_panel = None
        if EdithVisualPanel is not None:
            try:
                self._visual_panel = EdithVisualPanel(self)
                self._visual_panel.panel_closed.connect(self._on_visual_panel_closed)
            except Exception as _vpe:
                print(f"[VisualPanel] Error creating EdithVisualPanel: {_vpe}")
                self._visual_panel = None

        # Which centrepiece to draw: "edith_live2d" or "core"
        try:
            from memory.config_manager import get_hud_style, save_hud_style
            self.hud_style = get_hud_style()
            if self.hud_style not in ("edith_live2d", "core"):
                self.hud_style = "edith_live2d"
                save_hud_style(self.hud_style)
        except Exception:
            self.hud_style = "edith_live2d"

        self._active_overlays = set()
        self._explicit_overlay = False
        self._overlay_active = False

        # Tony-Stark holographic floating screens (tool-activity animation)
        self._holo_overlay = None
        try:
            from core.holo_screens import HoloScreensOverlay
            self._holo_overlay = HoloScreensOverlay(self, gesture_cb=self.trigger_gesture)
        except Exception as _he:
            print(f"[HoloScreens] disabled: {_he}")

        QTimer.singleShot(80, lambda: self.set_hud_style(self.hud_style))
        self._core_phase = 0.0

        # Real-time top-left Now Playing Mini-Widget (for Spotify & YouTube)
        self._current_media_track = None
        self._music_pill = MusicMiniWidget(self)
        self._music_pill.clicked.connect(self._on_music_pill_clicked)
        self._music_pill.hide()
        self._music_track_sig.connect(self._on_music_track_updated)

        self._media_poll_timer = QTimer(self)
        self._media_poll_timer.setInterval(3500)
        self._media_poll_timer.timeout.connect(self._poll_background_media)
        self._media_poll_timer.start()

        self._tick       = 0
        self._scale      = 1.0
        self._tgt_scale  = 1.0
        self._halo       = 55.0
        self._tgt_halo   = 55.0
        self._last_t     = time.time()
        self._step_t     = time.time()
        self._blink      = True
        self._blink_tick = 0

        # Rescaled-face cache: the smooth rescale is expensive, so we keep the
        # last result and only rebuild it when the (quantised) size changes.

        # Static grid-dot layer, pre-rendered once per size/theme into a pixmap
        # so paintEvent blits it in one call instead of thousands of drawPoint()s.
        self._grid_cache: QPixmap | None = None
        self._grid_key = None
        self._show_grid = True
        self._glass_glow = True
        # Repaint throttle counter (idle frames drop to ~20 Hz — see _step()).
        self._paint_tick = 0

        # Multi-time-of-day & pro studio room backgrounds
        self._room_bgs: dict[str, QPixmap] = {}
        viernes_dir = Path(__file__).resolve().parent / "viernes"
        for tag in ["morning", "day", "sunset", "night"]:
            bg_p = viernes_dir / f"room_bg_{tag}.jpg"
            if bg_p.exists():
                pm = QPixmap(str(bg_p))
                if not pm.isNull():
                    self._room_bgs[tag] = pm
        for key, fname in (
            ("penthouse_night", "bg_penthouse.jpg"),
            ("command_bridge", "bg_command.jpg"),
            ("zen_loft", "bg_loft.jpg"),
        ):
            bg_p = viernes_dir / fname
            if bg_p.exists():
                pm = QPixmap(str(bg_p))
                if not pm.isNull():
                    self._room_bgs[key] = pm

        # Fallback room_bg.jpg if night not loaded
        if "night" not in self._room_bgs:
            default_p = viernes_dir / "room_bg.jpg"
            if default_p.exists():
                pm = QPixmap(str(default_p))
                if not pm.isNull():
                    self._room_bgs["night"] = pm

        self._bg_mode = "aurora_atmos"
        self._bg_dim = 0.42
        self._bg_glow = 0.65
        self._custom_bg_path = ""
        self._custom_bg_pixmap: QPixmap | None = None
        self._current_bg_key = self.get_current_tod()
        self._target_bg_key = self._current_bg_key
        self._bg_blend_progress = 1.0
        self._room_bg = self._room_bgs.get(self._current_bg_key, None)

        self._particles = []

        # Live audio reactivity: _live_amp is written from the audio threads
        # (0.0–1.0), _amp_disp is the smoothed value the paint code reads.
        self._live_amp  = 0.0
        self._amp_disp  = 0.0
        # (frames, start_time, hop) posted by the playback thread — see
        # push_visemes(). None means "no schedule; use the plain level".
        self._visemes = None
        self._vis_i = None        # first schedule frame not yet handed to the mouth
        self._base_scale = 1.0    # slow "breathing" target; amp is added per-frame
        self._base_halo  = 55.0

        self._zen_mode = False
        self._init_zen_overlay()

        self._paused = False
        self._low_power = False

        self._tmr = QTimer(self)
        self._tmr.timeout.connect(self._step)
        self._tmr.start(33)

    def _target_timer_ms(self) -> int:
        if getattr(self, "_low_power", False) or getattr(self, "state", "") == "SLEEPING":
            return 120
        if getattr(self, "state", "") in ("SPEAKING", "LISTENING", "THINKING"):
            return 16
        return 33

    def pause(self) -> None:
        """Window minimized: suspend Live2D rendering and stop HUD timer."""
        self._paused = True
        if getattr(self, "_live2d_widget", None) is not None:
            try:
                self._live2d_widget.pause()
            except Exception:
                pass
        self._tmr.stop()

    def resume(self) -> None:
        """Window restored: resume Live2D rendering and restore timer."""
        self._paused = False
        if getattr(self, "_live2d_widget", None) is not None:
            try:
                self._live2d_widget.resume()
            except Exception:
                pass
        if not getattr(self, "_overlay_active", False):
            self._tmr.start(self._target_timer_ms())

    def set_low_power(self, enabled: bool) -> None:
        """Slow timer when sleeping."""
        self._low_power = bool(enabled)
        if not getattr(self, "_paused", False) and not getattr(self, "_overlay_active", False):
            self._tmr.start(self._target_timer_ms())

    def register_overlay(self, ov: QWidget) -> None:
        """Register an active overlay widget to ensure the avatar is hidden while it is shown."""
        if ov is None:
            return
        self._active_overlays.add(ov)
        self._apply_overlay_hide(True)

        try:
            ov.destroyed.connect(lambda *_: self.unregister_overlay(ov))
        except Exception:
            pass
        if hasattr(ov, "closed"):
            try:
                ov.closed.connect(lambda *_: self.unregister_overlay(ov))
            except Exception:
                pass

        try:
            filt = _OverlayEventFilter(self.unregister_overlay, ov)
            ov.installEventFilter(filt)
            ov._hud_overlay_filter = filt
        except Exception:
            pass

    def unregister_overlay(self, ov: QWidget) -> None:
        """Unregister an overlay and restore avatar if no other overlays are active."""
        if ov in self._active_overlays:
            self._active_overlays.discard(ov)
        self._update_overlay_state()

    def set_overlay_active(self, active: bool) -> None:
        """Explicit toggle for overlays/dialogs that run modally (e.g. exec())."""
        self._explicit_overlay = bool(active)
        self._update_overlay_state()

    def _update_overlay_state(self) -> None:
        # Prune only destroyed or explicitly hidden overlays
        alive = set()
        for w in list(self._active_overlays):
            try:
                if w is not None and w.isVisible():
                    alive.add(w)
            except (RuntimeError, Exception):
                pass
        self._active_overlays = alive

        should_hide = bool(self._explicit_overlay or len(self._active_overlays) > 0)
        self._apply_overlay_hide(should_hide)

    def _apply_overlay_hide(self, should_hide: bool) -> None:
        if getattr(self, "_overlay_active", False) == should_hide:
            return
        self._overlay_active = should_hide
        if should_hide:
            self._tmr.stop()
        elif not getattr(self, "_paused", False):
            self._tmr.start(self._target_timer_ms())

        for wid in (getattr(self, "_live2d_widget", None), getattr(self, "_vrm_widget", None)):
            if wid is not None:
                try:
                    if should_hide:
                        wid.hide()
                        wid.pause()
                except Exception:
                    pass

        if not should_hide:
            try:
                if self.hud_style == "edith_live2d" and getattr(self, "_live2d_widget", None):
                    self._update_vrm_geometry()
                    self._live2d_widget.show()
                    self._live2d_widget.resume()
                    self._live2d_widget.raise_()
                elif self.hud_style == "vrm_3d" and getattr(self, "_vrm_widget", None):
                    self._update_vrm_geometry()
                    self._vrm_widget.show()
                    self._vrm_widget.resume()
                    self._vrm_widget.raise_()
            except Exception:
                pass
        self.update()

    def get_current_tod(self) -> str:
        """Return the active backdrop key based on mode and system clock."""
        mode = getattr(self, "_bg_mode", "aurora_atmos")
        if mode in ("studio", "studio_pro", "aurora_atmos", "orbital_horizon", "neural_mesh", "custom_image"):
            return mode
        if mode != "auto" and hasattr(self, "_room_bgs") and mode in self._room_bgs:
            return mode
        from datetime import datetime as _dt
        hour = _dt.now().hour
        if 6 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "day"
        elif 18 <= hour < 21:
            return "sunset"
        else:
            return "night"

    def cycle_bg_mode(self) -> str:
        """Cycle through pro studio & room background modes."""
        modes = [
            "aurora_atmos", "studio_pro", "orbital_horizon", "neural_mesh",
            "penthouse_night", "command_bridge", "zen_loft", "auto",
        ]
        idx = (modes.index(self._bg_mode) + 1) % len(modes) if self._bg_mode in modes else 0
        self.set_bg_mode(modes[idx])
        return self._bg_mode

    def set_bg_mode(self, mode: str) -> None:
        """Set background mode with smooth cross-fade transition."""
        valid = (
            "studio", "studio_pro", "aurora_atmos", "orbital_horizon", "neural_mesh",
            "penthouse_night", "command_bridge", "zen_loft", "custom_image",
            "auto", "morning", "day", "sunset", "night",
        )
        self._bg_mode = mode if mode in valid else "aurora_atmos"
        tod = self.get_current_tod()
        if tod != self._target_bg_key:
            self._current_bg_key = self._target_bg_key
            self._target_bg_key = tod
            self._bg_blend_progress = 0.0
        self._update_bg_button_text()
        self.update()

    def set_custom_bg_path(self, path: str) -> None:
        path = (path or "").strip()
        if path == self._custom_bg_path and self._custom_bg_pixmap is not None:
            return
        self._custom_bg_path = path
        if path and Path(path).exists():
            pm = QPixmap(path)
            self._custom_bg_pixmap = pm if not pm.isNull() else None
        else:
            self._custom_bg_pixmap = None
        self.update()

    def set_backdrop_params(self, dim: float, glow: float) -> None:
        self._bg_dim = max(0.0, min(0.9, float(dim)))
        self._bg_glow = max(0.0, min(1.0, float(glow)))
        self.update()

    def _update_bg_button_text(self) -> None:
        names = {
            "studio": "Estudio limpio",
            "studio_pro": "Estudio Pro",
            "aurora_atmos": "Aurora Atmosférica",
            "orbital_horizon": "Horizonte Orbital",
            "neural_mesh": "Malla Neural",
            "penthouse_night": "Penthouse Nocturno",
            "command_bridge": "Puente Comando",
            "zen_loft": "Loft Arquitectónico",
            "custom_image": "Imagen Propia",
            "auto": "Auto (hora real)",
            "morning": "Mañana",
            "day": "Día",
            "sunset": "Atardecer",
            "night": "Noche",
        }
        lbl = names.get(self._bg_mode, "Aurora")
        if hasattr(self, "_btn_zen_bg"):
            self._btn_zen_bg.setText(f"Ambiente: {lbl}")
        win = self.window()
        if hasattr(win, "_bg_tod_btn"):
            win._bg_tod_btn.setText(f"🌅   Ambiente: {lbl}")

    def _init_zen_overlay(self) -> None:
        self._zen_overlay = QWidget(self)
        self._zen_overlay.setObjectName("ZenOverlay")
        self._zen_overlay.setStyleSheet(f"""
            QWidget#ZenOverlay {{
                background: rgba(23, 23, 28, 0.92);
                border: 1px solid {C.BORDER_B};
                border-radius: 10px;
            }}
            QPushButton {{
                background: transparent;
                color: {C.TEXT_MED};
                border: 1px solid transparent;
                border-radius: 7px;
                padding: 5px 11px;
                font-family: '{UI_FONT}';
                font-size: 11px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background: {C.PANEL2};
                color: {C.WHITE};
                border-color: {C.BORDER_B};
            }}
            QPushButton#CloseZen {{
                color: {C.RED};
            }}
            QPushButton#CloseZen:hover {{
                background: rgba(248, 113, 113, 0.14);
                color: {C.WHITE};
                border-color: rgba(248, 113, 113, 0.35);
            }}
        """)
        lay = QHBoxLayout(self._zen_overlay)
        lay.setContentsMargins(6, 4, 6, 4)
        lay.setSpacing(4)

        self._btn_zen_bg = QPushButton("Ambiente: Auto (hora real)")
        self._btn_zen_bg.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_zen_bg.clicked.connect(self._zen_cycle_bg)
        lay.addWidget(self._btn_zen_bg)

        self._btn_zen_fs = QPushButton("⛶  Pantalla completa  ·  F11")
        self._btn_zen_fs.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_zen_fs.clicked.connect(self._zen_toggle_fs)
        lay.addWidget(self._btn_zen_fs)

        self._btn_zen_exit = QPushButton("✕  Salir de vista enfoque  ·  F10")
        self._btn_zen_exit.setObjectName("CloseZen")
        self._btn_zen_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_zen_exit.clicked.connect(self._zen_exit_mode)
        lay.addWidget(self._btn_zen_exit)

        self._zen_overlay.hide()

    def _zen_cycle_bg(self) -> None:
        self.cycle_bg_mode()

    def _update_vrm_geometry(self) -> None:
        w = self.width()
        h = self.height()
        is_zen = getattr(self, "_zen_mode", False)

        vis_active = getattr(self, "_visual_panel", None) and self._visual_panel.isVisible()

        win = self.window()
        avatar_drawer = getattr(win, "_avatar_drawer", None)
        drawer_active = avatar_drawer is not None and avatar_drawer.isVisible()

        for wid in (getattr(self, "_live2d_widget", None), getattr(self, "_vrm_widget", None)):
            if wid is not None:
                if is_zen:
                    wid.setGeometry(0, 0, w, h)
                else:
                    l2d_h = max(100, int(h - 58))
                    if vis_active:
                        pw = self._visual_panel.width()
                        target_x = max(240, w - pw - 20)
                        wid.setGeometry(0, 10, target_x, l2d_h)
                    elif drawer_active:
                        try:
                            g_pt = avatar_drawer.mapToGlobal(QPoint(avatar_drawer.width(), 0))
                            pt = self.mapFromGlobal(g_pt)
                            drawer_right = max(0, pt.x())
                        except Exception:
                            drawer_right = getattr(avatar_drawer, "_WIDTH", 370) + 18
                        start_x = drawer_right + 14
                        target_w = max(240, w - start_x)
                        wid.setGeometry(start_x, 10, target_w, l2d_h)
                    else:
                        wid.setGeometry(0, 10, w, l2d_h)

                if getattr(self, "_overlay_active", False):
                    wid.hide()

        if hasattr(self, "_zen_overlay") and is_zen:
            self._zen_overlay.raise_()
        if getattr(self, "_visual_panel", None) and self._visual_panel.isVisible():
            self._position_visual_panel()
        if getattr(self, "_music_pill", None):
            if drawer_active:
                self._music_pill.hide()
            elif self._music_pill.isVisible() or getattr(self, "_music_active", False):
                self._music_pill.show()
                self._position_music_pill()

    def _position_visual_panel(self) -> None:
        if not getattr(self, "_visual_panel", None):
            return
        w = self.width()
        h = self.height()
        min_w = getattr(EdithVisualPanel, "MIN_W", 320) if EdithVisualPanel else 320
        max_w = getattr(EdithVisualPanel, "MAX_W", 440) if EdithVisualPanel else 440
        pw = max(min_w, min(max_w, int(w * 0.44)))
        ph = min(int(h * 0.92), 540)
        self._visual_panel.setFixedSize(pw, ph)

        px = max(20, w - pw - 24)
        py = max(16, (h - ph) // 2)
        self._visual_panel.move(px, py)
        self._visual_panel.raise_()

    def _position_music_pill(self) -> None:
        """Positions the compact Now Playing music widget in the top-left corner."""
        if getattr(self, "_music_pill", None):
            self._music_pill.move(20, 20)
            self._music_pill.raise_()

    def _poll_background_media(self) -> None:
        """Non-blocking background thread to query Windows GSMTC active media."""
        def _check():
            try:
                from core.media_detector import MediaDetector
                track = MediaDetector.get_instance().get_current_media(force_fetch_art=True)
                self._music_track_sig.emit(track)
            except Exception:
                pass

        threading.Thread(target=_check, daemon=True, name="MediaPollWorker").start()

    def _on_music_track_updated(self, track: Any) -> None:
        """Updates or hides the top-left music pill based on real-time Windows playback."""
        # STRICT USER CONSTRAINT: Solo si es Youtube o Spotify
        if track and track.status == "PLAYING" and getattr(track, "platform_key", "") in ("spotify", "youtube"):
            self._current_media_track = track
            self._music_pill.update_track(track)
            self._position_music_pill()
            if not self._music_pill.isVisible():
                self._music_pill.show()
                self._music_pill.raise_()
        else:
            self._current_media_track = None
            if self._music_pill.isVisible():
                self._music_pill.hide()

    def _on_music_pill_clicked(self) -> None:
        """Expands the full Edith visual card when clicking the top-left music pill."""
        if getattr(self, "_current_media_track", None):
            from core.media_detector import MediaDetector
            card = MediaDetector.get_instance().build_visual_card(self._current_media_track)
            self.show_visual_card(card)

    def show_visual_card(self, card_data: object) -> None:
        """Display the contextual visual panel to the right of Edith."""
        if not getattr(self, "_visual_panel", None) or card_data is None:
            return
        w = self.width()
        h = self.height()
        min_w = getattr(EdithVisualPanel, "MIN_W", 320) if EdithVisualPanel else 320
        max_w = getattr(EdithVisualPanel, "MAX_W", 440) if EdithVisualPanel else 440
        pw = max(min_w, min(max_w, int(w * 0.44)))
        ph = min(int(h * 0.92), 540)
        self._visual_panel.setFixedSize(pw, ph)

        target_x = max(20, w - pw - 24)
        target_y = max(16, (h - ph) // 2)

        # 1. Notify Edith Live2D to slide left and glance right
        if getattr(self, "_live2d_widget", None) and self.hud_style == "edith_live2d":
            self._live2d_widget.set_presentation_mode(True)
            self._live2d_widget.glance(0.48, -0.05, 3.5)

        # 2. Check if assistant is currently speaking
        speech_active = getattr(self, "speaking", False) or getattr(self.parent(), "speaking", False)

        # 3. Render and animate the visual panel
        self._visual_panel.display_card(card_data, target_x, target_y, speech_active=speech_active)
        self._visual_panel.raise_()

    def notify_speech_finished(self) -> None:
        """Propagate speech finished signal to the visual panel."""
        if getattr(self, "_visual_panel", None) and self._visual_panel.isVisible():
            self._visual_panel.notify_speech_finished()

    def hide_visual_card(self) -> None:
        if getattr(self, "_visual_panel", None) and self._visual_panel.isVisible():
            self._visual_panel.animate_hide()

    def _on_visual_panel_closed(self) -> None:
        # Gracefully return Edith to center
        if getattr(self, "_live2d_widget", None):
            self._live2d_widget.set_presentation_mode(False)

    def set_hud_style(self, style: str) -> None:
        if style not in ("edith_live2d", "core"):
            style = "edith_live2d"
        self.hud_style = style
        is_zen = hasattr(self, "_zen_overlay") and getattr(self, "_zen_mode", False)

        # Edith Live2D
        if getattr(self, "_live2d_widget", None):
            if style == "edith_live2d":
                self._update_vrm_geometry()
                if not getattr(self, "_overlay_active", False):
                    self._live2d_widget.show()
                    self._live2d_widget.resume()
                    self._live2d_widget.raise_()
                if is_zen:
                    self._zen_overlay.raise_()
            else:
                self._live2d_widget.pause()
                self._live2d_widget.hide()

        self.update()

    def _on_live2d_error(self, msg: str) -> None:
        print(f"[Live2D] Error: {msg}")
        if NativeLive2DWidget is not None and isinstance(self._live2d_widget, NativeLive2DWidget) and Live2DWidget is not None:
            print("[Live2D] Falling back from Native OpenGL to WebEngine Live2D...")
            try:
                old_w = self._live2d_widget
                self._live2d_widget = Live2DWidget(self)
                self._live2d_widget.model_error.connect(self._on_live2d_web_error)
                try:
                    from memory.config_manager import (
                        get_edith_autonomy_enabled,
                        get_edith_spontaneity_level,
                        get_edith_mood
                    )
                    self._live2d_widget.set_autonomy_enabled(get_edith_autonomy_enabled())
                    self._live2d_widget.set_spontaneity_level(get_edith_spontaneity_level())
                    self._live2d_widget.set_mood(get_edith_mood())
                except Exception:
                    pass
                old_w.hide()
                old_w.deleteLater()
                self._update_vrm_geometry()
                if not getattr(self, "_overlay_active", False):
                    self._live2d_widget.show()
                    self._live2d_widget.raise_()
                win = self.window()
                if hasattr(win, "_log"):
                    win._log.append_log("SYS: Edith Live2D cambiando a motor web optimizado.")
                return
            except Exception as _e:
                print(f"[Live2D] Fallback to WebEngine also failed: {_e}")

        self._on_live2d_web_error(msg)

    def _on_live2d_web_error(self, msg: str) -> None:
        print(f"[Live2D] Final fallback: {msg}")
        self.set_hud_style("core")
        try:
            from memory.config_manager import save_hud_style
            save_hud_style("core")
            win = self.window()
            if hasattr(win, "_log"):
                win._log.append_log(f"SYS: Edith Live2D fallback ({msg}). Activado Holograma Core.")
            if hasattr(win, "_refresh_hud_btn"):
                win._refresh_hud_btn()
        except Exception:
            pass

    def set_zen_mode(self, enabled: bool) -> None:
        self._zen_mode = bool(enabled)
        self._update_vrm_geometry()
        if self._zen_mode:
            self._position_zen_overlay()
            self._zen_overlay.show()
            self._zen_overlay.raise_()
        else:
            self._zen_overlay.hide()
        self.update()

    def _position_zen_overlay(self) -> None:
        if hasattr(self, "_zen_overlay") and self._zen_mode:
            self._zen_overlay.adjustSize()
            ow = self._zen_overlay.sizeHint().width()
            oh = self._zen_overlay.sizeHint().height()
            self._zen_overlay.setGeometry(self.width() - ow - 16, 16, ow, oh)
            self._zen_overlay.raise_()

    def _zen_toggle_fs(self) -> None:
        win = self.window()
        if hasattr(win, "_toggle_fullscreen"):
            win._toggle_fullscreen()
            if hasattr(self, "_btn_zen_fs"):
                self._btn_zen_fs.setText("🗗 VENTANA [F11]" if win.isFullScreen() else "⛶ PANTALLA COMPLETA [F11]")

    def _zen_exit_mode(self) -> None:
        win = self.window()
        if hasattr(win, "_toggle_avatar_only"):
            win._toggle_avatar_only()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_vrm_geometry()
        self._position_zen_overlay()
        self._position_music_pill()

    def mouseDoubleClickEvent(self, event):
        win = self.window()
        if hasattr(win, "_toggle_avatar_only"):
            win._toggle_avatar_only()

    def mousePressEvent(self, event):
        if getattr(self, "_overlay_active", False):
            return
        super().mousePressEvent(event)

        # Interactive click-to-react on Edith 3D VRM!
        if getattr(self, "_vrm_widget", None) is not None and self.hud_style == "vrm_3d":
            pos = event.position()
            dx = abs(pos.x() - (self.width() / 2.0))
            if dx < (self.width() * 0.45):
                if self.state == "SLEEPING":
                    win = self.window()
                    if hasattr(win, "_tap_wake_manual") and getattr(win, "_wake_state", lambda: {})().get("enabled"):
                        win._tap_wake_manual()
                    else:
                        self.set_state("LISTENING")
                else:
                    vrm_gestures = ["WAVE_HELLO", "EXPLAIN", "THINKING", "NOD_AGREE", "HEAD_SHAKE"]
                    vrm_emos = ["happy", "surprised", "relaxed"]
                    self._vrm_widget.set_emotion(random.choice(vrm_emos), 0.85, 3.0)
                    self._vrm_widget.trigger_gesture(random.choice(vrm_gestures), 3.0)
                return

        # Interactive click-to-react on Edith Live2D!
        if getattr(self, "_live2d_widget", None) is not None and self.hud_style == "edith_live2d":
            pos = event.position()
            dx = abs(pos.x() - (self.width() / 2.0))
            if dx < (self.width() * 0.45):
                if self.state == "SLEEPING":
                    win = self.window()
                    if hasattr(win, "_tap_wake_manual") and getattr(win, "_wake_state", lambda: {})().get("enabled"):
                        win._tap_wake_manual()
                    else:
                        self.set_state("LISTENING")
                else:
                    edith_clicks = [
                        ("polite", "ELEGANT_BOW"),
                        ("thinking", "THINKING_DEEP"),
                        ("cheerful", "AGREE_WARM_NOD"),
                        ("happy", "WELCOME_PRESENT"),
                        ("curious", "ATTENTIVE_LEAN"),
                        ("calm", "CALM_BREATHE"),
                        ("cheerful", "HAIR_ADJUST"),
                        ("proud_smug", "CONFIDENT_CROSS"),
                        ("happy", "GREETING_WAVE"),
                        ("curious", "HEAD_TILT_CURIOUS"),
                        ("shy", "SHY_HIDE"),
                        ("happy", "ENCOURAGE_CLAP"),
                    ]
                    emo, act = random.choice(edith_clicks)
                    self._live2d_widget.set_emotion(emo, intensity=0.85, duration=3.2)
                    self._live2d_widget.trigger_action(act)
                return


        # Interactive click-to-react on avatar!
        if self._avatar is not None and self.hud_style == "face":
            pos = event.position()
            dx = abs(pos.x() - (self.width() / 2.0))
            if dx < (self.width() * 0.42):
                if getattr(self._avatar, "is_sleeping", False):
                    # Asleep: gently wake her up with cyberpunk glitch transition!
                    win = self.window()
                    if hasattr(win, "_tap_wake_manual") and getattr(win, "_wake_state", lambda: {})().get("enabled"):
                        win._tap_wake_manual()
                    else:
                        self._avatar.wake()
                        self.state = "LISTENING"
                    self.update()
                    return
                if hasattr(self._avatar, "play_action"):
                    reactions = [
                        "giggle", "blush_shy", "greeting_wave", "excited_sparkle",
                        "proud_smug", "happy_cheer", "curious", "wink_left", "wink_right"
                    ]
                    self._avatar.play_action(random.choice(reactions), duration=2.2)
                    self.update()

    def glance(self, dx: float, dy: float, hold: float = 1.1) -> None:
        """Ask the avatar to look somewhere for a moment."""
        try:
            if getattr(self, "_vrm_widget", None) is not None and self.hud_style == "vrm_3d":
                self._vrm_widget.glance(dx, dy, hold)
            elif getattr(self, "_live2d_widget", None) is not None and self.hud_style == "edith_live2d":
                self._live2d_widget.glance(dx, dy, hold)
            elif self._avatar is not None:
                self._avatar.glance(dx, dy, hold)
        except Exception:
            pass

    def set_emotion(self, name: str, intensity: float = 1.0, duration: float = 0.0) -> None:
        if getattr(self, "_live2d_widget", None) is not None:
            self._live2d_widget.set_emotion(name, intensity, duration)
        if getattr(self, "_vrm_widget", None) is not None:
            self._vrm_widget.set_emotion(name, intensity, duration)

    def trigger_action(self, name: str) -> None:
        if getattr(self, "_live2d_widget", None) is not None:
            self._live2d_widget.trigger_action(name)
        if getattr(self, "_vrm_widget", None) is not None:
            self._vrm_widget.trigger_action(name)

    def set_semantic_intent(self, intent: str, metadata: dict | None = None) -> None:
        if getattr(self, "_live2d_widget", None) is not None:
            self._live2d_widget.set_semantic_intent(intent, metadata)
        if getattr(self, "_vrm_widget", None) is not None:
            self._vrm_widget.set_semantic_intent(intent, metadata)

    def trigger_gesture(self, name: str, duration: float = 0.0, intensity: float = 1.0) -> None:
        if getattr(self, "_live2d_widget", None) is not None:
            self._live2d_widget.trigger_gesture(name, duration, intensity)
        if getattr(self, "_vrm_widget", None) is not None:
            self._vrm_widget.trigger_gesture(name, duration, intensity)

    def interrupt_gestures(self) -> None:
        if getattr(self, "_live2d_widget", None) is not None:
            self._live2d_widget.interrupt_gestures()
        if getattr(self, "_vrm_widget", None) is not None:
            self._vrm_widget.interrupt_gestures()

    def set_float_mode(self, mode: str) -> None:
        if getattr(self, "_live2d_widget", None) is not None:
            self._live2d_widget.set_float_mode(mode)
        if getattr(self, "_vrm_widget", None) is not None:
            self._vrm_widget.set_float_mode(mode)

    def notify_task_completed(self) -> None:
        if getattr(self, "_live2d_widget", None) is not None:
            self._live2d_widget.notify_task_completed()
        if getattr(self, "_vrm_widget", None) is not None:
            self._vrm_widget.notify_task_completed()

    def notify_task_error(self, error_msg: str = "") -> None:
        if getattr(self, "_live2d_widget", None) is not None:
            self._live2d_widget.notify_task_error(error_msg)
        if getattr(self, "_vrm_widget", None) is not None:
            self._vrm_widget.notify_task_error(error_msg)

    def set_speaking(self, speaking: bool) -> None:
        was_speaking = getattr(self, "speaking", False)
        self.speaking = bool(speaking)
        if getattr(self, "_live2d_widget", None) is not None:
            self._live2d_widget.set_speaking(speaking)
        if getattr(self, "_vrm_widget", None) is not None:
            self._vrm_widget.set_speaking(speaking)
        if hasattr(self, "hud") and hasattr(self.hud, "set_speaking"):
            self.hud.set_speaking(speaking)
        if was_speaking and not speaking:
            if hasattr(self, "hud") and hasattr(self.hud, "notify_speech_finished"):
                self.hud.notify_speech_finished()

    def set_state(self, state: str) -> None:
        self.state = str(state)
        if getattr(self, "_live2d_widget", None) is not None:
            self._live2d_widget.set_state(state)
        if getattr(self, "_vrm_widget", None) is not None:
            self._vrm_widget.set_state(state)

    def set_level(self, level: float) -> None:
        self.set_audio_level(level)
        if getattr(self, "_live2d_widget", None) is not None:
            self._live2d_widget.set_level(level)
        if getattr(self, "_vrm_widget", None) is not None:
            self._vrm_widget.set_level(level)

    def push_level(self, level: float) -> None:
        self.set_level(level)

    def push_visemes(self, frames, hop: float, at: float) -> None:
        """Thread-safe: hand over a schedule of (level, openness, width) frames.

        The playback thread writes up to 200 ms of audio in one go, so a single
        averaged level would only move the mouth five times a second — enough to
        flap, nowhere near enough to articulate. It instead posts the whole
        slice's worth of 20 ms frames here and `_step()` plays them out against
        the wall clock, in step with the audio going to the speakers.

        `at` is the wall-clock time this batch will *begin to sound*, which the
        caller tracks as a playback cursor. It is not the time of the call, and
        the difference is the whole point: `stream.write` returns once the buffer
        accepts the samples, so consecutive batches are handed over far faster
        than they play. Anchoring each one to "now" made every batch start while
        its predecessor was still sounding, so each schedule replaced the last
        after a couple of frames and the mouth only ever played the opening
        instant of every 200 ms — the reason it did not match the words.

        Successive batches are therefore *appended* into one continuous
        timeline, not swapped in. A paragraph is one schedule; the mouth stops
        falling into a gap at every chunk boundary and having to climb back out.
        """
        try:
            if not frames:
                return
            hop = max(1e-3, float(hop))
            at = float(at)
            new = list(frames)
            cur = self._visemes
            if cur is not None:
                old, t0, ohop = cur
                if abs(ohop - hop) < 1e-6:
                    # Where in the existing timeline does this batch land?
                    i = int(round((at - t0) / hop))
                    if 0 <= i <= len(old) + 1:
                        # Continues (or slightly overlaps) what is already
                        # queued: extend rather than restart. Drop whatever has
                        # already been played so the list cannot grow without
                        # bound over a long reply.
                        merged = old[:i] + new
                        played = int((time.time() - t0) / hop) - 2
                        if played > 60:
                            merged = merged[played:]
                            t0 += played * hop
                            if self._vis_i is not None:
                                self._vis_i = max(0, self._vis_i - played)
                        self._visemes = (merged, t0, hop)
                        return
            self._visemes = (new, at, hop)
            self._vis_i = None
        except Exception:
            pass

    def set_audio_level(self, level: float) -> None:
        """Thread-safe entry point for the audio threads. Stores the louder of
        the incoming level and the current value so brief gaps between chunks
        don't make the waveform stutter; _step() decays it back down."""
        try:
            lv = float(level)
        except (TypeError, ValueError):
            return
        if lv < 0.0:
            lv = 0.0
        elif lv > 1.0:
            lv = 1.0
        if lv > self._live_amp:
            self._live_amp = lv

    def _make_grid(self, W: int, H: int) -> QPixmap:
        """Pre-render the static grid-dot background into a transparent pixmap so
        paintEvent can blit it once per frame instead of running a nested
        drawPoint() loop across the whole widget every 16 ms."""
        pm = QPixmap(max(1, W), max(1, H))
        pm.fill(Qt.GlobalColor.transparent)
        gp = QPainter(pm)
        gp.setPen(QPen(qcol(C.PRI_GHO), 1))
        for x in range(0, W, 48):
            for y in range(0, H, 48):
                gp.drawPoint(x, y)
        gp.end()
        return pm

    def _step(self):
        if getattr(self, "_paused", False):
            return
        self._tick += 1
        now = time.time()

        # ── Live audio reactivity ────────────────────────────────────────────
        # A viseme schedule, if one is playing, gives both the level and the
        # mouth shape for this exact instant; otherwise fall back to the peak
        # level the audio threads pushed in.
        v_open = v_wide = v_level = None
        v_seq = None
        sched = self._visemes
        if sched is not None:
            frames, t0, hop = sched
            i = int((now - t0) / hop)
            if 0 <= i < len(frames):
                # Hand over *every* frame since the last tick, not just the one
                # under the cursor. This timer runs at 60 Hz but the paint is
                # throttled and the machine may be busy, so a tick can span two
                # or three 20 ms frames — and a consonant closure is only two
                # frames long. Sampling one and discarding the rest is how the
                # closures between words went missing.
                j = self._vis_i if self._vis_i is not None else i
                v_seq = frames[max(0, j):i + 1]
                self._vis_i = max(j, i + 1)
                v_level, v_open, v_wide = frames[i]
                if v_seq:
                    peak = max(f[0] for f in v_seq)
                    if peak > self._live_amp:
                        self._live_amp = peak
            elif i >= len(frames):
                self._visemes = None        # schedule spent
                self._vis_i = None

        # Audio threads push peaks into _live_amp; decay it toward silence so
        # gaps between chunks fade out instead of freezing, then smooth it.
        self._live_amp *= 0.86
        self._amp_disp += (self._live_amp - self._amp_disp) * 0.45
        amp = self._amp_disp

        # The avatar animates off the very same smoothed level the waveform
        # uses — one audio source, so the mouth can never drift out of sync.
        dt = now - self._step_t
        self._step_t = now

        # Dynamic Time-of-Day background check & smooth transition
        if self._tick % 120 == 0:
            tod = self.get_current_tod()
            if tod != self._target_bg_key:
                self.set_bg_mode(self._bg_mode)

        if self._bg_blend_progress < 1.0:
            self._bg_blend_progress = min(1.0, self._bg_blend_progress + dt * 1.8)
            if self._bg_blend_progress >= 1.0:
                self._current_bg_key = self._target_bg_key

        # Integrated, not derived from absolute time: multiplying wall-clock by
        # a rate that changes with state jumps the rings the instant VIERNES
        # starts talking. Same lesson the head's sway taught.
        self._core_phase += min(0.10, max(0.0, dt))

        win = self.window()
        if hasattr(win, "_voice_monitor") and win._voice_monitor is not None:
            win._voice_monitor.step(dt, amp, speaking=self.speaking, muted=self.muted, state=self.state)

        if getattr(self, "_live2d_widget", None) is not None and self.hud_style == "edith_live2d":
            last_amp = getattr(self, "_last_l2d_amp", -1.0)
            if abs(amp - last_amp) > 0.008 or (amp > 0.01 and self.speaking):
                self._live2d_widget.set_level(amp)
                self._last_l2d_amp = amp
            if getattr(self, "_last_l2d_speaking", None) != self.speaking:
                self._live2d_widget.set_speaking(self.speaking)
                self._last_l2d_speaking = self.speaking
            if getattr(self, "_last_l2d_state", None) != self.state:
                self._live2d_widget.set_state(self.state)
                self._last_l2d_state = self.state
        else:
            # Reactor core: slow "breathing" base target, lifted by the level.
            if now - self._last_t > (0.12 if self.speaking else 0.5):
                if self.speaking:
                    self._base_scale = 1.03
                    self._base_halo  = 122.0
                elif self.muted:
                    self._base_scale = random.uniform(0.998, 1.002)
                    self._base_halo  = random.uniform(15, 28)
                else:
                    self._base_scale = random.uniform(1.001, 1.008)
                    self._base_halo  = random.uniform(48, 68)
                self._last_t = now

            if self.muted:
                self._tgt_scale, self._tgt_halo = self._base_scale, self._base_halo
            elif self.speaking:
                self._tgt_scale = self._base_scale + amp * 0.13
                self._tgt_halo  = self._base_halo  + amp * 95.0
            else:
                self._tgt_scale = self._base_scale + amp * 0.06
                self._tgt_halo  = self._base_halo  + amp * 75.0

            sp = 0.38 if self.speaking else (0.30 if amp > 0.02 else 0.15)
            self._scale += (self._tgt_scale - self._scale) * sp
            self._halo  += (self._tgt_halo  - self._halo)  * sp

        self._blink_tick += 1
        if self._blink_tick >= 38:
            self._blink = not self._blink
            self._blink_tick = 0
            _blinked = True
        else:
            _blinked = False

        # Repaint throttling — advancing the animation state above is cheap at
        # 60 Hz, but the paint is heavy. Active (speaking, audio, thinking) runs
        # at ~30 Hz, which is the frame rate animation has used for talking
        # characters forever and is indistinguishable here; idle drops to ~20 Hz
        # so a sleeping HUD stops pinning a CPU core. The visuals stay smooth
        # either way because the animation state keeps stepping at 60 Hz.
        self._paint_tick = (self._paint_tick + 1) % 6
        if self.hud_style == "edith_live2d" and not getattr(self, "_overlay_active", False):
            # Live2D renders in its own accelerated surface; parent HUD only needs LED blink updates.
            if _blinked and self._on_screen():
                self.update()
            return

        active = (self.speaking or amp > 0.02
                  or self.state in ("THINKING", "PROCESSING"))
        if _blinked or (self._paint_tick % 2 == 0 if active
                        else self._paint_tick % 3 == 0):
            if self._on_screen():
                self.update()

    def _on_screen(self) -> bool:
        """True only when this canvas can actually be seen by the user."""
        try:
            if not self.isVisible():
                return False
            win = self.window()
            return not (win.isMinimized() or win.isHidden())
        except Exception:
            return True      # never let a visibility check stop the HUD drawing

    # ── reactor core ─────────────────────────────────────────────────────────
    # The centrepiece for anyone who did not want a face looking back at them.
    # Built from the same budget as the head — software QPainter, no GPU — and
    # from the same principle: everything on it means something. The rings turn
    # at a rate the state sets, the spectrum ring is the real audio level, and
    # the core brightens with the voice. Nothing here is decoration that moves
    # for its own sake, which is what made the old glowing orb feel dead.

    def _core_colours(self):
        if self.muted:
            return qcol(C.MUTED_C), qcol(C.MUTED_C)
        if self.speaking:
            return qcol(C.PRI), qcol(C.ACC)
        if self.state in ("THINKING", "PROCESSING"):
            return qcol(C.PRI), qcol(C.ACC2)
        if self.state == "LISTENING":
            return qcol(C.PRI), qcol(C.GREEN)
        return qcol(C.PRI), qcol(C.PRI_DIM)

    def _paint_core(self, p: QPainter, cx: float, cy: float, r: float,
                    W: float = 0.0, H: float = 0.0):
        """Draw an organic, harmonic acoustic orb at (cx, cy) with outer radius r."""
        main, acc = self._core_colours()
        bg = qcol(C.BG)
        amp = self._amp_disp
        t = self._core_phase
        live = (self.speaking or amp > 0.04) and not self.muted

        def blend(col: QColor, a: float) -> QColor:
            k = max(0.0, min(1.0, a))
            return QColor(int(bg.red()   + (col.red()   - bg.red())   * k),
                          int(bg.green() + (col.green() - bg.green()) * k),
                          int(bg.blue()  + (col.blue()  - bg.blue())  * k))

        p.setBrush(Qt.BrushStyle.NoBrush)

        # 1. Soft atmospheric aura
        lift = 1.0 + 0.50 * amp + (0.15 if self.speaking else 0.0)
        p.setPen(Qt.PenStyle.NoPen)
        for gr, a0, a1 in ((r * 0.72, 0.24, 0.0), (r * 0.36, 0.30, 0.0)):
            g = QRadialGradient(cx, cy, gr)
            g.setColorAt(0.00, blend(main, min(0.90, a0 * lift)))
            g.setColorAt(0.50, blend(main, min(0.90, a0 * lift * 0.45)))
            g.setColorAt(1.00, blend(main, a1))
            p.setBrush(QBrush(g))
            p.drawEllipse(QRectF(cx - gr, cy - gr, gr * 2, gr * 2))
        p.setBrush(Qt.BrushStyle.NoBrush)

        # 2. Concentric calm breathing rings
        for rr, a in ((0.96, 0.22), (0.82, 0.14), (0.64, 0.18)):
            breathe = 1.0 + 0.015 * math.sin(t * 1.4 + rr * 4.0) + amp * 0.05
            rad = r * rr * breathe
            p.setPen(QPen(blend(main, a), 1.1))
            p.drawEllipse(QRectF(cx - rad, cy - rad, rad * 2, rad * 2))

        # 3. Smooth orbital arcs
        rate = 0.7 + (1.4 if self.state in ("THINKING", "PROCESSING") else 0.0) \
                   + (0.9 if self.speaking else 0.0)
        for k, (rr, span, count, dirn, col, a, wid) in enumerate((
                (0.90, 110, 2, +1, acc,  0.55, 1.8),
                (0.74, 140, 1, -1, main, 0.36, 1.4),
                (0.56, 95,  2, +1, acc,  0.32, 1.3))):
            rad = r * rr
            p.setPen(QPen(blend(col, a), wid))
            box = QRectF(cx - rad, cy - rad, rad * 2, rad * 2)
            base = (t * rate * (8 + k * 5) * dirn) % 360.0
            for sgm in range(count):
                p.drawArc(box, int((base + sgm * (360.0 / count)) * 16),
                          int(span * 16))

        # 4. Subtle harmonic audio ring
        n = 48
        ring = r * 0.40
        spikes = []
        for i in range(n):
            a = math.radians(i * (360.0 / n))
            ca, sa = math.cos(a), math.sin(a)
            wob = 0.5 + 0.5 * math.sin(t * 2.0 + i * 0.38)
            idle = 0.012 + 0.008 * math.sin(t * 1.1 + i * 0.6)
            h = r * (idle + (amp * 0.16 * wob if live else 0.0))
            spikes.append(QLineF(cx + ca * ring, cy + sa * ring,
                                 cx + ca * (ring + h), cy + sa * (ring + h)))
        p.setPen(QPen(blend(acc if live else main, 0.28 + 0.45 * amp), 1.5))
        p.drawLines(spikes)

        # 5. Inner core ring & assistant name
        inner = r * 0.34
        p.setPen(QPen(blend(acc, 0.35 + 0.40 * amp), 1.4))
        p.drawEllipse(QRectF(cx - inner, cy - inner, inner * 2, inner * 2))

        name = self._assistant_name or ""
        if name:
            space = max(1.0, r * 0.015)
            fsz = max(8, int(min(r * 0.095,
                                 (inner * 1.70) / max(1, len(name)) * 1.5 - space)))
            f = QFont(UI_FONT, fsz, QFont.Weight.DemiBold)
            f.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, space)
            p.setFont(f)
            p.setPen(QPen(blend(qcol(C.WHITE), 0.75 + 0.25 * min(1.0, amp * 2)), 1))
            p.drawText(QRectF(cx - r, cy - fsz, r * 2, fsz * 2),
                       Qt.AlignmentFlag.AlignCenter, name)

    def paintEvent(self, _):
        p = QPainter(self)
        if not p.isActive():      # device not ready (e.g. 0-size during layout) — skip cleanly
            return
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), qcol(C.BG))

        W, H = self.width(), self.height()
        cx, cy = W / 2, H / 2
        fw = min(W, H)

        # ── Render Animated Studio / Architectural Backdrop ──────────────────
        tod = self._target_bg_key or self.get_current_tod()
        if tod == "custom_image" and getattr(self, "_custom_bg_pixmap", None) is not None:
            bg_target = self._custom_bg_pixmap
        else:
            bg_target = self._room_bgs.get(tod, None)
        bg_curr = self._room_bgs.get(self._current_bg_key, bg_target)

        if bg_target and not bg_target.isNull():
            p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            bg_w, bg_h = bg_target.width(), bg_target.height()
            scale = max(W / bg_w, H / bg_h) * 1.04
            draw_w, draw_h = bg_w * scale, bg_h * scale

            para_x = getattr(self._avatar, "yaw", 0.0) * -0.45 if self._avatar else 0.0
            para_y = getattr(self._avatar, "pitch", 0.0) * -0.35 if self._avatar else 0.0
            bg_x = (W - draw_w) / 2.0 + para_x
            bg_y = (H - draw_h) / 2.0 + para_y
            dst_rect = QRectF(bg_x, bg_y, draw_w, draw_h)

            if self._bg_blend_progress < 1.0 and bg_curr and bg_curr != bg_target:
                p.setOpacity(1.0 - self._bg_blend_progress)
                p.drawPixmap(dst_rect, bg_curr, QRectF(0, 0, bg_curr.width(), bg_curr.height()))
                p.setOpacity(self._bg_blend_progress)
                p.drawPixmap(dst_rect, bg_target, QRectF(0, 0, bg_target.width(), bg_target.height()))
                p.setOpacity(1.0)
            else:
                p.drawPixmap(dst_rect, bg_target, QRectF(0, 0, bg_w, bg_h))

            # Configurable dimmer + theme-aware atmospheric vignette
            dim_alpha = int(max(0.0, min(0.9, getattr(self, "_bg_dim", 0.42))) * 255)
            if dim_alpha > 0:
                p.fillRect(self.rect(), QColor(6, 8, 13, dim_alpha))

            amb_base = qcol(C.PRI if not self.speaking else C.ACC)
            glow_k = getattr(self, "_bg_glow", 0.65)
            light_alpha = int((34 + 14 * math.sin(self._tick * 0.04) + 20 * self._amp_disp) * glow_k)
            ambient_grad = QRadialGradient(cx, cy * 0.8, max(W, H) * 0.78)
            ambient_grad.setColorAt(0.0, QColor(amb_base.red(), amb_base.green(), amb_base.blue(), min(140, light_alpha)))
            ambient_grad.setColorAt(0.7, QColor(8, 10, 15, 70))
            ambient_grad.setColorAt(1.0, QColor(4, 6, 10, 175))
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(QBrush(ambient_grad))
            p.drawRect(self.rect())

            if getattr(self, "_show_grid", True):
                _gkey = (W, H, C.BORDER)
                if self._grid_cache is None or self._grid_key != _gkey:
                    self._grid_cache = self._make_grid(W, H)
                    self._grid_key = _gkey
                p.setOpacity(0.45)
                p.drawPixmap(0, 0, self._grid_cache)
                p.setOpacity(1.0)

        else:
            # High-precision Procedural Studio / Aurora / Orbital / Neural Backdrops
            from core.hud_backdrop import paint_procedural_backdrop
            proc_mode = tod if tod in ("aurora_atmos", "studio_pro", "orbital_horizon", "neural_mesh") else "studio_pro"
            glow_k = getattr(self, "_bg_glow", 0.65) if getattr(self, "_glass_glow", True) else 0.15
            paint_procedural_backdrop(
                p, QRectF(self.rect()), proc_mode,
                C.BG, C.PANEL, C.PRI, C.ACC,
                self._tick, self._amp_disp, self.speaking,
                glow_strength=glow_k,
            )

            if getattr(self, "_show_grid", True):
                _gkey = (W, H, C.BORDER)
                if self._grid_cache is None or self._grid_key != _gkey:
                    self._grid_cache = self._make_grid(W, H)
                    self._grid_key = _gkey
                p.drawPixmap(0, 0, self._grid_cache)

        # ── Avatar / Stage Centrepiece ──────────────────────────────────────
        _band_t = 16.0
        _band_h = max(60.0, H - 32.0 - _band_t)
        if getattr(self, "_overlay_active", False):
            # Overlay active — suspend avatar rendering so dialogs/menus/QRs are 100% unobstructed
            pass
        elif self.hud_style in ("edith_live2d", "vrm_3d"):
            # Edith Live2D Pro & Edith 3D VRM are rendered smoothly in WebEngine/OpenGL
            pass
        elif self._avatar is not None and self.hud_style == "face":
            _r_head = min(fw * 0.38, _band_h / (self._avatar.SPAN + 0.08))
            _head_cy = _band_t + (_band_h - self._avatar.SPAN * _r_head) / 2.0 + _r_head

            if self.muted:
                _main = _acc = qcol(C.MUTED_C)
            else:
                _main = qcol(C.PRI)
                if self.speaking:
                    _acc = qcol(C.ACC)
                elif self.state in ("THINKING", "PROCESSING"):
                    _acc = qcol(C.ACC2)
                elif self.state == "LISTENING":
                    _acc = qcol(C.GREEN)
                else:
                    _acc = qcol(C.PRI)
            self._avatar.paint(p, cx, _head_cy, _r_head, _main, _acc, qcol(C.BG),
                               canvas_w=W, canvas_h=H, zen_mode=self._zen_mode)

        elif self.hud_style == "core":
            _r = min(W * 0.44, (H - 36.0) / 2.0)
            self._paint_core(p, cx, cy, _r, W, H)

        # ── Subtle Architectural Viewport Border ────────────────────────────
        p.setPen(QPen(qcol(C.BORDER_B, 110), 1.0))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(QRectF(0.5, 0.5, W - 1.0, H - 1.0), 14.0, 14.0)

        p.end()   # end deterministically so the backing store never flushes an active painter


class VoiceVisualizerWidget(QWidget):
    """Editorial voice presence and real-time acoustic waveform monitor."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = "LISTENING"
        self._speaking = False
        self._muted = False
        self._amp = 0.0
        self._tick = 0
        self._blink = False

        self.N = 21  # Number of bars (odd for symmetric center)
        self._peak_bars = [0.0] * self.N
        self._peak_hold = [0] * self.N

        self.setFixedHeight(108)
        self.setMinimumWidth(140)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Estado de voz y micrófono  [Clic o F4 para silenciar / activar]")

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        win = self.window()
        if hasattr(win, "_toggle_mute"):
            win._toggle_mute()

    def set_state(self, state: str):
        self._state = str(state or "LISTENING")
        self.update()

    def set_muted(self, muted: bool):
        self._muted = bool(muted)
        self.update()

    def set_speaking(self, speaking: bool):
        self._speaking = bool(speaking)
        self.update()

    def step(self, dt: float, amp: float, speaking: bool = False, muted: bool = False, state: str = "LISTENING"):
        self._amp = float(amp)
        self._speaking = bool(speaking)
        self._muted = bool(muted)
        if state:
            self._state = str(state)
        self._tick += 1
        if self._tick % 28 == 0:
            self._blink = not self._blink
        for i in range(self.N):
            if self._peak_hold[i] > 0:
                self._peak_hold[i] -= 1
            else:
                self._peak_bars[i] = max(0.0, self._peak_bars[i] - 1.1)
        win = self.window()
        if win and (win.isMinimized() or win.isHidden()):
            return
        if not self.isHidden():
            self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        if not p.isActive():
            return
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()

        # ── 1. Clean Editorial Status Pill ─────────────────────────────────────
        badge_h = 24.0
        badge_y = 2.0

        if self._muted:
            txt, col = "Micrófono silenciado", qcol(C.MUTED_C)
            dot_c = QColor(C.MUTED_C)
        elif self._speaking:
            txt, col = "Hablando ahora", qcol(C.ACC)
            dot_c = QColor(C.ACC)
        elif self._state == "SLEEPING":
            txt, col = "En reposo", qcol(C.TEXT_MED)
            dot_c = QColor(C.TEXT_DIM)
        elif self._state == "THINKING":
            txt, col = "Razonando…", qcol(C.ACC2)
            dot_c = QColor(C.ACC2)
        elif self._state == "PROCESSING":
            txt, col = "Procesando…", qcol(C.ACC2)
            dot_c = QColor(C.ACC2)
        elif self._state == "LISTENING":
            txt, col = "Escucha activa", qcol(C.GREEN)
            dot_c = QColor(C.GREEN)
        else:
            txt, col = "Disponible", qcol(C.PRI)
            dot_c = QColor(C.PRI)

        badge_rect = QRectF(2.0, badge_y, W - 4.0, badge_h)
        bg_col = QColor(dot_c.red(), dot_c.green(), dot_c.blue(), 22)
        p.setBrush(QBrush(bg_col))
        border_col = QColor(dot_c.red(), dot_c.green(), dot_c.blue(), 75)
        p.setPen(QPen(border_col, 1.0))
        p.drawRoundedRect(badge_rect, 8.0, 8.0)

        # Status dot + label
        p.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        p.setPen(QPen(col, 1))
        p.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, f"●  {txt}")

        # ── 2. Minimalist Symmetric Acoustic Waveform ──────────────────────────
        bw = 4.0
        gap = 3.0
        tot_w = self.N * (bw + gap) - gap
        wx0 = (W - tot_w) / 2.0
        cy = badge_y + badge_h + 30.0
        amp = self._amp
        mid = (self.N - 1) / 2.0

        for i in range(self.N):
            if self._muted:
                hgt = 3.0
                bar_c = qcol(C.BORDER_B)
            else:
                dist = abs(i - mid) / mid
                env = (1.0 - dist) ** 0.70
                shimmer = 0.65 + 0.35 * math.sin(self._tick * 0.16 + i * 0.60)
                idle = 4.0 + 2.0 * math.sin(self._tick * 0.07 + i * 0.45)

                if self._state == "SLEEPING":
                    hgt = 3.0 + 1.0 * math.sin(self._tick * 0.04 + i * 0.35)
                    bar_c = qcol(C.BORDER_B)
                elif self._state in ("THINKING", "PROCESSING"):
                    sweep = math.sin(self._tick * 0.12 - i * 0.40)
                    hgt = max(4.0, 18.0 * max(0.0, sweep))
                    bar_c = qcol(C.ACC2)
                else:
                    hgt = max(4.0, min(36.0, idle + amp * 34.0 * env * shimmer))
                    if amp > 0.03:
                        bar_c = qcol(C.ACC if self._speaking else C.GREEN)
                    else:
                        bar_c = qcol(C.PRI)

            bar_x = wx0 + i * (bw + gap)
            bar_y = cy - hgt / 2.0

            p.setBrush(QBrush(bar_c))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(QRectF(bar_x, bar_y, bw, hgt), 2.0, 2.0)

        # ── 3. Subtle Bottom Caption ───────────────────────────────────────────
        bot_y = H - 18.0
        p.setFont(QFont(UI_FONT, 8))
        if self._muted:
            sub_txt = "Clic o F4 para activar micrófono"
            sub_c = qcol(C.MUTED_C)
        elif self._speaking:
            sub_txt = "Respuesta de voz en curso"
            sub_c = qcol(C.TEXT_MED)
        else:
            sub_txt = "Canal de voz listo  ·  F4 silenciar"
            sub_c = qcol(C.TEXT_DIM)

        p.setPen(QPen(sub_c, 1))
        p.drawText(QRectF(4.0, bot_y, W - 8.0, 16.0),
                   Qt.AlignmentFlag.AlignCenter, sub_txt)

        p.end()

class MetricBar(QWidget):

    def __init__(self, label: str, color: str = C.PRI, parent=None):
        super().__init__(parent)
        self._label = label
        self._color = color
        self._value = 0.0       # 0–100
        self._text  = "--"
        self.setFixedHeight(22)
        self.setMinimumWidth(80)

    def set_value(self, pct: float, text: str):
        v = max(0.0, min(100.0, pct))
        if v == self._value and text == self._text:
            return          # unchanged — skip the repaint
        self._value = v
        self._text  = text
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        if not p.isActive():
            return
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        W, H = self.width(), self.height()

        if self._value > 85:
            c1 = qcol(C.RED)
        elif self._value > 70:
            c1 = qcol(C.ACC)
        else:
            c1 = qcol(self._color)

        # Label text
        p.setFont(QFont(UI_FONT, 8))
        p.setPen(QPen(qcol(C.TEXT_MED), 1))
        p.drawText(QRectF(0, 0, W * 0.62, 13),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._label)

        # Value text
        p.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        p.setPen(QPen(qcol(C.TEXT) if self._text != "--" else qcol(C.TEXT_DIM), 1))
        p.drawText(QRectF(W * 0.55, 0, W * 0.45, 13),
                   Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, self._text)

        # Clean progress track
        track_h = 3.0
        track_y = 15.5
        track_rect = QRectF(0, track_y, W, track_h)

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(qcol(C.BAR_BG)))
        p.drawRoundedRect(track_rect, 1.5, 1.5)

        fill_w = max(0.0, min(float(W), W * (self._value / 100.0)))
        if fill_w > 1.5:
            p.setBrush(QBrush(c1))
            p.drawRoundedRect(QRectF(0, track_y, fill_w, track_h), 1.5, 1.5)

        p.end()


class WeatherWidget(QWidget):
    """Real-time cybernetic weather display card widget for the sidebar."""

    weather_updated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.weather_updated.connect(self._on_weather_data)
        self._is_loading = False

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Clima en tiempo real (Click para actualizar)")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        # Header: location tag and refresh icon
        loc_row = QHBoxLayout()
        loc_row.setSpacing(4)
        self._loc_lbl = QLabel("📍 Sarchí, Costa Rica")
        self._loc_lbl.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        self._loc_lbl.setStyleSheet(f"color: {C.PRI}; background: transparent; border: none;")
        loc_row.addWidget(self._loc_lbl)
        loc_row.addStretch()

        self._refresh_icon = QLabel("🔄")
        self._refresh_icon.setFont(QFont(UI_FONT, 8))
        self._refresh_icon.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent; border: none;")
        loc_row.addWidget(self._refresh_icon)
        lay.addLayout(loc_row)

        # Main row: Big Weather Icon + Temp + Condition
        main_row = QHBoxLayout()
        main_row.setSpacing(10)

        self._icon_lbl = QLabel("🌤️")
        self._icon_lbl.setFont(QFont(UI_FONT, 22))
        self._icon_lbl.setStyleSheet("background: transparent; border: none;")
        main_row.addWidget(self._icon_lbl)

        temp_v = QVBoxLayout()
        temp_v.setSpacing(1)
        self._temp_lbl = QLabel("--°C")
        self._temp_lbl.setFont(QFont(UI_FONT, 16, QFont.Weight.Bold))
        self._temp_lbl.setStyleSheet(f"color: {C.WHITE}; background: transparent; border: none;")
        temp_v.addWidget(self._temp_lbl)

        self._cond_lbl = QLabel("Consultando clima...")
        self._cond_lbl.setFont(QFont(UI_FONT, 8))
        self._cond_lbl.setStyleSheet(f"color: {C.ACC2}; background: transparent; border: none;")
        temp_v.addWidget(self._cond_lbl)
        main_row.addLayout(temp_v)
        main_row.addStretch()
        lay.addLayout(main_row)

        # Subtle micro-separator
        ln = QFrame(); ln.setFixedHeight(1)
        ln.setStyleSheet(f"background: {C.BORDER_A}; border: none;")
        lay.addWidget(ln)

        # Telemetry metrics row: Sensación, Humedad, Viento
        def _kv(key: str, val_lbl: QLabel):
            row = QHBoxLayout(); row.setSpacing(6)
            k = QLabel(key); k.setFont(QFont(UI_FONT, 8))
            k.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent; border: none;")
            val_lbl.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
            val_lbl.setStyleSheet(f"color: {C.TEXT}; background: transparent; border: none;")
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row.addWidget(k); row.addStretch(); row.addWidget(val_lbl)
            lay.addLayout(row)

        self._feels_lbl = QLabel("--")
        self._humidity_lbl = QLabel("--")
        self._wind_lbl = QLabel("--")
        _kv("Sensación", self._feels_lbl)
        _kv("Humedad", self._humidity_lbl)
        _kv("Viento", self._wind_lbl)

        # 15-minute auto-refresh timer
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.refresh_weather)
        self._timer.start(15 * 60 * 1000)

        # Initial fetch delayed 400ms to avoid slowing initial window presentation
        QTimer.singleShot(400, self.refresh_weather)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.refresh_weather()

    def refresh_weather(self):
        if self._is_loading:
            return
        self._is_loading = True
        self._cond_lbl.setText("Actualizando...")

        def _fetch():
            try:
                city = "Sarchi"
                display_name = "Sarchí, Costa Rica"
                try:
                    from memory.memory_manager import load_memory
                    mem = load_memory()
                    pref_city = mem.get("preferences", {}).get("default_weather_city", {}).get("value")
                    loc = mem.get("identity", {}).get("location", {}).get("value")
                    if pref_city:
                        city = pref_city.strip()
                        display_name = loc.strip() if loc else city.title()
                    elif loc:
                        parts = loc.split(",")
                        city = parts[0].strip()
                        display_name = loc.strip()
                except Exception:
                    pass

                import urllib.request, urllib.parse, json
                encoded = urllib.parse.quote(city)
                url = f"https://wttr.in/{encoded}?format=j1"
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "curl/7.68.0", "Accept": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=3.5) as resp:
                    data = json.loads(resp.read().decode("utf-8"))

                curr = data["current_condition"][0]
                temp_c = curr.get("temp_C", "--")
                feels_c = curr.get("FeelsLikeC", temp_c)
                humidity = curr.get("humidity", "--")
                wind_kmh = curr.get("windspeedKmph", "--")
                raw_desc = curr.get("weatherDesc", [{}])[0].get("value", "Despejado")

                from actions.weather_report import _translate_condition
                cond_es = _translate_condition(raw_desc)

                res = {
                    "city": city,
                    "display_name": display_name,
                    "temp_c": f"{temp_c}°C",
                    "feels_c": f"{feels_c}°C",
                    "humidity": f"{humidity}%",
                    "wind_kmh": f"{wind_kmh} km/h",
                    "condition": cond_es,
                    "icon": self._get_icon(cond_es),
                }
                self.weather_updated.emit(res)
            except Exception as e:
                print(f"[WeatherWidget] Error fetching weather: {e}")
                self.weather_updated.emit({"error": str(e)})

        threading.Thread(target=_fetch, daemon=True).start()

    def _on_weather_data(self, data: dict):
        self._is_loading = False
        if "error" in data:
            self._cond_lbl.setText("Sin conexión")
            return

        self._loc_lbl.setText(f"📍 {data['display_name']}")
        self._temp_lbl.setText(data["temp_c"])
        self._icon_lbl.setText(data["icon"])
        self._cond_lbl.setText(data["condition"])
        self._feels_lbl.setText(data["feels_c"])
        self._humidity_lbl.setText(data["humidity"])
        self._wind_lbl.setText(data["wind_kmh"])

    @staticmethod
    def _get_icon(desc: str) -> str:
        d = (desc or "").lower()
        if any(w in d for w in ("soleado", "despejado", "sunny", "clear")):
            return "☀️"
        if any(w in d for w in ("parcialmente", "partly")):
            return "⛅"
        if any(w in d for w in ("tormenta", "thunder", "eléctrica")):
            return "⛈️"
        if any(w in d for w in ("llovizna", "drizzle")):
            return "🌦️"
        if any(w in d for w in ("lluvia", "rain", "chubascos", "shower", "aguacero")):
            return "🌧️"
        if any(w in d for w in ("neblina", "niebla", "mist", "fog")):
            return "🌫️"
        if any(w in d for w in ("nieve", "snow", "granizo", "ice")):
            return "❄️"
        if any(w in d for w in ("nublado", "cloudy", "overcast", "cubierto")):
            return "☁️"
        return "🌤️"


class LogWidget(QTextEdit):
    """Conversation + system log rendered as a calm, chat-style transcript.

    Messages are inserted whole (the old per-character typing effect ran a
    6 ms timer and a cursor round-trip per glyph — pure overhead on the UI
    thread). Consecutive lines from the same speaker are grouped under one
    name header, system lines are small and dim.
    """
    _sig = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.document().setMaximumBlockCount(800)
        self.document().setDocumentMargin(4)
        self.setFont(QFont(UI_FONT, 10))
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(f"""
            QTextEdit {{
                background: transparent; color: {C.TEXT};
                border: none; selection-background-color: {C.PRI_GHO};
            }}
            QScrollBar:vertical {{ background: transparent; width: 6px; margin: 2px; border: none; }}
            QScrollBar::handle:vertical {{ background: {C.BORDER_B}; border-radius: 3px; min-height: 24px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: transparent; }}
        """)
        self._ai_name_lc = "viernes"   # updated when assistant name changes
        self._last_speaker: str | None = None
        self._sig.connect(self._append)

    def append_log(self, text: str):
        self._sig.emit(str(text))

    def clear(self):
        super().clear()
        self._last_speaker = None

    def _classify(self, raw: str) -> tuple[str, str]:
        tl = raw.lower()
        for pfx in (f"{self._ai_name_lc}:", "viernes:", "viernes:"):
            if tl.startswith(pfx):
                return "ai", raw[len(pfx):]
        if tl.startswith("you:"):
            return "you", raw[4:]
        if tl.startswith("file:"):
            return "file", raw[5:]
        if tl.startswith("err:"):
            return "err", raw[4:]
        if tl.startswith("sys:"):
            return ("err" if "error" in tl or "failed" in tl else "sys"), raw[4:]
        return ("err" if "err" in tl[:8] else "sys"), raw

    def _append(self, text: str):
        import html as _html
        raw = (text or "").strip()
        if not raw:
            return
        kind, body = self._classify(raw)
        esc = _html.escape(body.strip()).replace("\n", "<br>")
        ts = time.strftime("%H:%M")
        if kind in ("you", "ai"):
            if kind == "you":
                html_block = (
                    f'<div style="margin-top:10px; margin-bottom:4px; margin-left:26px; '
                    f'background:{C.PANEL2}; border:1px solid {C.BORDER_B}; '
                    f'border-radius:12px 12px 4px 12px; padding:9px 13px;">'
                    f'<table width="100%" cellpadding="0" cellspacing="0" border="0">'
                    f'<tr><td style="color:{C.TEXT_MED}; font-weight:600; font-size:8pt;">Tú</td>'
                    f'<td align="right" style="color:{C.TEXT_DIM}; font-size:7.5pt;">{ts}</td></tr>'
                    f'</table>'
                    f'<p style="margin-top:4px; margin-bottom:0px; color:{C.WHITE}; font-size:9.5pt; line-height:142%;">{esc}</p>'
                    f'</div>'
                )
            else:
                ai_name = (self._ai_name_lc or "Viernes").title()
                html_block = (
                    f'<div style="margin-top:10px; margin-bottom:4px; margin-right:12px; '
                    f'background:{C.PANEL}; border-left:2.5px solid {C.PRI}; '
                    f'border-top:1px solid {C.BORDER}; border-right:1px solid {C.BORDER}; '
                    f'border-bottom:1px solid {C.BORDER}; border-radius:4px 12px 12px 4px; padding:10px 13px;">'
                    f'<table width="100%" cellpadding="0" cellspacing="0" border="0">'
                    f'<tr><td style="color:{C.PRI}; font-weight:600; font-size:8.5pt;">{ai_name}</td>'
                    f'<td align="right" style="color:{C.TEXT_DIM}; font-size:7.5pt;">{ts}</td></tr>'
                    f'</table>'
                    f'<p style="margin-top:4px; margin-bottom:0px; color:{C.TEXT}; font-size:9.5pt; line-height:145%;">{esc}</p>'
                    f'</div>'
                )
            self._last_speaker = kind
        else:
            col = {"err": C.RED, "file": C.GREEN}.get(kind, C.TEXT_DIM)
            badge = {"err": "Aviso", "file": "Archivo", "sys": "Sistema"}.get(kind, "Sistema")
            html_block = (
                f'<div style="margin-top:5px; margin-bottom:5px; padding:4px 8px; '
                f'background:{C.DARK}; border:1px solid {C.BORDER_A}; border-radius:7px; font-size:8pt;">'
                f'<span style="color:{col}; font-weight:600; font-size:7pt; background:{_rgba(col, 0.12)}; '
                f'border:1px solid {_rgba(col, 0.25)}; border-radius:4px; padding:1px 5px;">{badge}</span>'
                f'<span style="color:{C.TEXT_DIM}; font-size:7.5pt;">&nbsp;&nbsp;{ts}&nbsp;·&nbsp;</span>'
                f'<span style="color:{C.TEXT_MED if kind == "sys" else col};">{esc}</span>'
                f'</div>'
            )
            self._last_speaker = None
        self.append(html_block)
        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())

_FILE_ICONS = {
    "image":   ("🖼", "#6E6AF6"), "video":   ("🎬", "#E07A5F"),
    "audio":   ("🎵", "#A855F7"), "pdf":     ("📄", "#F87171"),
    "word":    ("📝", "#38BDF8"), "excel":   ("📊", "#34D399"),
    "code":    ("💻", "#EAB308"), "archive": ("📦", "#FB923C"),
    "pptx":    ("📊", "#E07A5F"), "text":    ("📃", "#A0A0AB"),
    "data":    ("🔧", "#6E6AF6"), "unknown": ("📎", "#9E9EA9"),
}
_EXT_TO_CAT = {
    **dict.fromkeys(["jpg","jpeg","png","gif","webp","bmp","tiff","svg","ico"], "image"),
    **dict.fromkeys(["mp4","avi","mov","mkv","wmv","flv","webm","m4v"],         "video"),
    **dict.fromkeys(["mp3","wav","ogg","m4a","aac","flac","wma","opus"],        "audio"),
    **dict.fromkeys(["pdf"],                                                     "pdf"),
    **dict.fromkeys(["doc","docx"],                                              "word"),
    **dict.fromkeys(["xls","xlsx","ods"],                                        "excel"),
    **dict.fromkeys(["ppt","pptx"],                                              "pptx"),
    **dict.fromkeys(["py","js","ts","jsx","tsx","html","css","java","c","cpp",
                     "cs","go","rs","rb","php","swift","kt","sh","sql","lua"],   "code"),
    **dict.fromkeys(["zip","rar","tar","gz","7z","bz2","xz"],                   "archive"),
    **dict.fromkeys(["txt","md","rst","log"],                                    "text"),
    **dict.fromkeys(["csv","tsv","json","xml"],                                  "data"),
}

def _file_category(path: Path) -> str:
    return _EXT_TO_CAT.get(path.suffix.lower().lstrip("."), "unknown")

def _fmt_size(size: int) -> str:
    if   size < 1024:    return f"{size} B"
    elif size < 1024**2: return f"{size/1024:.1f} KB"
    elif size < 1024**3: return f"{size/1024**2:.1f} MB"
    else:                return f"{size/1024**3:.1f} GB"


class FileDropZone(QWidget):
    file_selected = pyqtSignal(str)
    file_cleared  = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(52)
        self._current_file: str | None = None
        self._hovering  = False
        self._drag_over = False
        self._dash_offset = 0.0
        self._anim_tmr = QTimer(self)
        self._anim_tmr.timeout.connect(self._animate)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self._canvas = _DropCanvas(self)
        layout.addWidget(self._canvas)

    def _animate(self):
        if not (self._hovering or self._drag_over):
            self._anim_tmr.stop()
            return
        self._dash_offset = (self._dash_offset + 0.8) % 20
        self._canvas.update()

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()
            self._drag_over = True
            if not self._anim_tmr.isActive():
                self._anim_tmr.start(40)
            self._canvas.update()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dragLeaveEvent(self, e):
        self._drag_over = False
        if not self._hovering and self._anim_tmr.isActive():
            self._anim_tmr.stop()
        self._canvas.update()

    def dropEvent(self, e: QDropEvent):
        self._drag_over = False
        if not self._hovering and self._anim_tmr.isActive():
            self._anim_tmr.stop()
        urls = e.mimeData().urls()
        if urls:
            e.acceptProposedAction()
            path = urls[0].toLocalFile()
            if path and Path(path).is_file():
                self._set_file(path)
        self._canvas.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._browse()

    def enterEvent(self, e):
        self._hovering = True
        if not self._anim_tmr.isActive():
            self._anim_tmr.start(40)
        self._canvas.update()

    def leaveEvent(self, e):
        self._hovering = False
        if not self._drag_over and self._anim_tmr.isActive():
            self._anim_tmr.stop()
        self._canvas.update()

    def current_file(self) -> str | None:
        return self._current_file

    def clear_file(self):
        self._current_file = None
        self._canvas.update()
        self.file_cleared.emit()

    def _browse(self):
        _asst = (_read_full_config().get("assistant_name") or "Viernes").strip()
        path, _ = QFileDialog.getOpenFileName(
            self.window() or self, f"Seleccionar archivo para {_asst}", str(Path.home()),
            "Todos los archivos (*.*);;"
            "Imágenes (*.jpg *.jpeg *.png *.gif *.webp *.bmp *.svg);;"
            "Documentos (*.pdf *.docx *.txt *.md *.pptx);;"
            "Datos (*.csv *.xlsx *.json *.xml);;"
            "Código (*.py *.js *.ts *.html *.css *.java *.cpp *.go);;"
            "Audio (*.mp3 *.wav *.ogg *.m4a *.aac *.flac);;"
            "Video (*.mp4 *.avi *.mov *.mkv *.wmv *.webm);;"
            "Comprimidos (*.zip *.rar *.tar *.gz *.7z)",
        )
        if path and Path(path).is_file():
            self._set_file(path)

    def _set_file(self, path: str):
        self._current_file = path
        self._canvas.update()
        self.file_selected.emit(path)

    def set_file_silent(self, path: str):
        """Update the displayed file without emitting file_selected (used for remote uploads)."""
        self._current_file = path
        self._canvas.update()


class _DropCanvas(QWidget):
    def __init__(self, zone: FileDropZone):
        super().__init__(zone)
        self._z = zone
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        self._z.dragEnterEvent(e)

    def dragMoveEvent(self, e):
        self._z.dragMoveEvent(e)

    def dragLeaveEvent(self, e):
        self._z.dragLeaveEvent(e)

    def dropEvent(self, e):
        self._z.dropEvent(e)

    def paintEvent(self, _):
        p = QPainter(self)
        if not p.isActive():
            return
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        z    = self._z
        W, H = self.width(), self.height()
        pad  = 1
        rect = QRectF(pad, pad, W - pad * 2, H - pad * 2)

        bg_col = qcol(C.PRI_GHO if z._drag_over else (C.BORDER_A if z._hovering else C.PANEL2))
        p.setBrush(QBrush(bg_col)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(rect, 10, 10)

        if z._current_file:   border_col = qcol(C.GREEN, 200)
        elif z._drag_over:    border_col = qcol(C.PRI, 230)
        elif z._hovering:     border_col = qcol(C.BORDER_B, 200)
        else:                 border_col = qcol(C.BORDER, 160)

        pen = QPen(border_col, 1.5, Qt.PenStyle.DashLine)
        pen.setDashOffset(z._dash_offset)
        p.setPen(pen); p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(rect, 10, 10)

        if z._current_file and Path(z._current_file).exists():
            self._paint_file(p, W, H)
        elif z._drag_over:
            self._paint_drag_over(p, W, H)
        else:
            self._paint_idle(p, W, H, z._hovering)

        p.end()

    def _paint_idle(self, p, W, H, hover):
        cx, cy = 28.0, H / 2
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(qcol(C.PRI_GHO)))
        p.drawEllipse(QPointF(cx, cy), 13, 13)
        p.setPen(QPen(qcol(C.PRI if hover else C.TEXT_MED), 1.6))
        p.drawLine(QPointF(cx, cy + 5), QPointF(cx, cy - 5))
        p.drawLine(QPointF(cx - 4, cy - 1), QPointF(cx, cy - 5))
        p.drawLine(QPointF(cx + 4, cy - 1), QPointF(cx, cy - 5))
        f = QFont(UI_FONT, 9, QFont.Weight.DemiBold)
        p.setFont(f)
        p.setPen(QPen(qcol(C.WHITE if hover else C.TEXT), 1))
        p.drawText(QRectF(52, cy - 14, W - 60, 15),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                   "Adjuntar o arrastrar archivo")
        p.setFont(QFont(UI_FONT, 8))
        p.setPen(QPen(qcol(C.TEXT_DIM), 1))
        p.drawText(QRectF(52, cy + 1, W - 60, 14),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                   "Imágenes, documentos, audio o código")

    def _paint_drag_over(self, p, W, H):
        cx, cy = W / 2, H / 2
        p.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        p.setPen(QPen(qcol(C.PRI), 1))
        p.drawText(QRectF(0, 0, W, H), Qt.AlignmentFlag.AlignCenter, "⬇  Soltar archivo para adjuntar")

    def _paint_file(self, p, W, H):
        path = Path(self._z._current_file)
        cat  = _file_category(path)
        icon, icon_col = _FILE_ICONS.get(cat, _FILE_ICONS["unknown"])
        try:
            size_str = _fmt_size(path.stat().st_size)
        except Exception:
            size_str = ""
        ext_str  = path.suffix.upper().lstrip(".") or "ARCHIVO"

        block_x, block_w = 8, 42
        p.setFont(QFont("Segoe UI Emoji", 17) if _OS == "Windows" else QFont("Arial", 17))
        p.setPen(QPen(qcol(icon_col), 1))
        p.drawText(QRectF(block_x, 0, block_w, H), Qt.AlignmentFlag.AlignCenter, icon)

        tx = block_x + block_w + 4
        tw = W - tx - 34

        p.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        p.setPen(QPen(qcol(C.WHITE), 1))
        name = path.name if len(path.name) <= 34 else path.name[:31] + "…"
        p.drawText(QRectF(tx, H * 0.16, tw, 16),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, name)

        p.setFont(QFont(UI_FONT, 8))
        p.setPen(QPen(qcol(C.TEXT_DIM), 1))
        p.drawText(QRectF(tx, H * 0.16 + 16, tw, 14),
                   Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                   f"{ext_str}  ·  {size_str}")

        p.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        p.setPen(QPen(qcol(C.RED, 180), 1))
        p.drawText(QRectF(W - 32, 0, 26, H), Qt.AlignmentFlag.AlignCenter, "✕")

    def mousePressEvent(self, e):
        z = self._z
        if z._current_file and e.pos().x() > self.width() - 34:
            z.clear_file()
        else:
            z.mousePressEvent(e)


class _CameraPreview(QWidget):
    """Floating overlay that shows live or captured camera preview."""

    _W, _H = 248, 190

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            _CameraPreview {{
                background: rgba(23, 23, 28, 246);
                border: 1px solid {C.BORDER_B};
                border-radius: 10px;
            }}
        """)
        self.setFixedWidth(self._W)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(8, 6, 8, 8)
        lay.setSpacing(4)

        hdr = QHBoxLayout()
        title = QLabel("●  Vista de cámara")
        title.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        title.setStyleSheet(f"color: {C.TEXT}; background: transparent;")
        hdr.addWidget(title)
        hdr.addStretch()
        self._user_closed = False
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(18, 18)
        close_btn.setFont(QFont(UI_FONT, 8))
        close_btn.setStyleSheet(
            f"color: {C.TEXT_DIM}; background: transparent; border: none;"
        )
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self._on_user_close)
        hdr.addWidget(close_btn)
        lay.addLayout(hdr)

        self._img_lbl = QLabel()
        self._img_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._img_lbl.setStyleSheet("background: transparent;")
        lay.addWidget(self._img_lbl)

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)

        self.hide()

    def _on_user_close(self):
        self._user_closed = True
        self.hide()

    def show_frame(self, img_bytes: bytes, continuous: bool = False) -> None:
        if continuous and getattr(self, "_user_closed", False):
            return
        px = QPixmap()
        px.loadFromData(img_bytes)
        if not px.isNull():
            max_w = self._W - 12
            scaled = px.scaled(
                max_w, 160,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self._img_lbl.setPixmap(scaled)
            if not getattr(self, "_sized", False):
                self._img_lbl.setFixedSize(scaled.width(), scaled.height())
                self.adjustSize()
                self._sized = True
        self.show()
        self.raise_()
        if continuous:
            self._timer.stop()
        else:
            self._timer.start(6_000)   # auto-dismiss after 6 s for snapshots


class SetupOverlay(QWidget):
    done = pyqtSignal(str, str)
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            SetupOverlay {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER_B};
                border-radius: 14px;
            }}
        """)

        detected = {"darwin": "mac", "windows": "windows"}.get(
            _OS.lower(), "linux"
        )
        self._sel_os = detected

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 22, 30, 22)
        layout.setSpacing(8)

        def _lbl(txt, font_size=9, bold=False, color=C.TEXT,
                 align=Qt.AlignmentFlag.AlignCenter):
            w = QLabel(txt)
            w.setAlignment(align)
            w.setFont(QFont(UI_FONT, int(round(font_size)),
                            QFont.Weight.DemiBold if bold else QFont.Weight.Normal))
            w.setStyleSheet(f"color: {color}; background: transparent;")
            return w

        layout.addWidget(_lbl("Configuración inicial de Viernes", 13, True, color=C.WHITE))
        layout.addWidget(_lbl("Prepara el entorno antes de comenzar.", 9, color=C.TEXT_MED))
        layout.addSpacing(6)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {C.BORDER};"); layout.addWidget(sep)
        layout.addSpacing(4)

        layout.addWidget(_lbl("Clave API de Google Gemini", 8, True, color=C.TEXT_MED,
                               align=Qt.AlignmentFlag.AlignLeft))
        self._key_input = QLineEdit()
        self._key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._key_input.setPlaceholderText("AIza…")
        self._key_input.setFont(QFont(UI_FONT, 10))
        self._key_input.setFixedHeight(34)
        self._key_input.setStyleSheet(f"""
            QLineEdit {{
                background: {C.DARK}; color: {C.TEXT};
                border: 1px solid {C.BORDER}; border-radius: 8px; padding: 4px 10px;
            }}
            QLineEdit:focus {{ border: 1px solid {C.PRI}; }}
        """)
        layout.addWidget(self._key_input)
        layout.addSpacing(12)

        sep2 = QFrame(); sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet(f"color: {C.BORDER};"); layout.addWidget(sep2)
        layout.addSpacing(4)

        layout.addWidget(_lbl("Sistema operativo", 8, True, color=C.TEXT_MED,
                               align=Qt.AlignmentFlag.AlignLeft))
        det_name = {"windows": "Windows", "mac": "macOS", "linux": "Linux"}[detected]
        layout.addWidget(_lbl(f"Detectado automáticamente: {det_name}", 8, color=C.TEXT_DIM,
                               align=Qt.AlignmentFlag.AlignLeft))

        os_row = QHBoxLayout(); os_row.setSpacing(6)
        self._os_btns: dict[str, QPushButton] = {}
        for key, label in [("windows","⊞  Windows"),("mac","  macOS"),("linux","🐧  Linux")]:
            btn = QPushButton(label)
            btn.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
            btn.setFixedHeight(32)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, k=key: self._sel(k))
            os_row.addWidget(btn)
            self._os_btns[key] = btn
        layout.addLayout(os_row)
        self._sel(detected)
        layout.addSpacing(12)

        init_btn = QPushButton("Comenzar con Viernes")
        init_btn.setFont(QFont(UI_FONT, 10, QFont.Weight.DemiBold))
        init_btn.setFixedHeight(38)
        init_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        init_btn.setStyleSheet(f"""
            QPushButton {{
                background: {C.PRI}; color: {C.WHITE};
                border: none; border-radius: 8px;
            }}
            QPushButton:hover {{
                background: {C.PRI_DIM};
            }}
        """)
        init_btn.clicked.connect(self._submit)
        layout.addWidget(init_btn)

    def _sel(self, key: str):
        self._sel_os = key
        for k, btn in self._os_btns.items():
            if k == key:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {C.PRI_GHO}; color: {C.PRI};
                        border: 1px solid {C.PRI}; border-radius: 8px; font-weight: 600;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {C.DARK}; color: {C.TEXT_DIM};
                        border: 1px solid {C.BORDER}; border-radius: 8px;
                    }}
                    QPushButton:hover {{ color: {C.TEXT}; border: 1px solid {C.BORDER_B}; }}
                """)

    def _submit(self):
        key = self._key_input.text().strip()
        if not key:
            self._key_input.setStyleSheet(
                self._key_input.styleSheet() +
                f" QLineEdit {{ border: 1px solid {C.RED}; }}"
            )
            return
        self.done.emit(key, self._sel_os)

    def hideEvent(self, e):
        super().hideEvent(e)
        self.closed.emit()

    def closeEvent(self, e):
        super().closeEvent(e)
        self.closed.emit()


class HueWheel(QWidget):
    """
    Circular colour picker. The user drags the handle (small white circle)
    around the wheel to choose from ALL hues. The filled circle in the centre
    is a live preview of the selected colour.
    """

    hue_picked    = pyqtSignal(str)   # while dragging (live)
    hue_committed = pyqtSignal(str)   # when the handle is released

    _RING = 16   # ring thickness (px)

    def __init__(self, initial_hex: str = DEFAULT_UI_COLOR, parent=None):
        super().__init__(parent)
        self.setFixedSize(148, 148)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._hue  = 0.53
        self._drag = False
        self.set_color(initial_hex)

    # ── API ──────────────────────────────────────────────────────────────────
    def color(self) -> str:
        return QColor.fromHsvF(self._hue, 1.0, 1.0).name()

    def set_color(self, hex_str: str):
        c = QColor((hex_str or "").strip())
        if c.isValid() and c.hsvHueF() >= 0:
            self._hue = c.hsvHueF()
            self.update()

    # ── geometry helpers ─────────────────────────────────────────────────────
    def _ring_rect(self) -> QRectF:
        m = self._RING / 2 + 3
        return QRectF(self.rect()).adjusted(m, m, -m, -m)

    def _hue_from_pos(self, pos: QPointF) -> float:
        c  = QRectF(self.rect()).center()
        dx = pos.x() - c.x()
        dy = c.y() - pos.y()          # screen y goes down — flip to math axis
        ang = math.atan2(dy, dx)      # [-π, π], counter-clockwise
        return (ang / (2 * math.pi)) % 1.0

    # ── drawing ──────────────────────────────────────────────────────────────
    def paintEvent(self, _):
        p = QPainter(self)
        if not p.isActive():
            return
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect   = self._ring_rect()
        center = rect.center()

        grad = QConicalGradient(center, 0)
        for i in range(0, 361, 20):
            grad.setColorAt(i / 360.0, QColor.fromHsvF((i % 360) / 360.0, 1.0, 1.0))
        p.setPen(QPen(QBrush(grad), self._RING))
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(rect)

        # centre preview circle
        preview = QColor.fromHsvF(self._hue, 1.0, 1.0)
        inner   = rect.adjusted(30, 30, -30, -30)
        p.setPen(QPen(qcol(C.BORDER_B), 1))
        p.setBrush(QBrush(preview))
        p.drawEllipse(inner)

        # draggable handle
        r   = rect.width() / 2
        ang = self._hue * 2 * math.pi
        hx  = center.x() + r * math.cos(ang)
        hy  = center.y() - r * math.sin(ang)
        p.setPen(QPen(QColor("#00060a"), 2))
        p.setBrush(QBrush(QColor("#ffffff")))
        p.drawEllipse(QPointF(hx, hy), 7.5, 7.5)
        p.end()

    # ── fare ─────────────────────────────────────────────────────────────────
    def mousePressEvent(self, e):
        self._drag = True
        self._hue  = self._hue_from_pos(e.position())
        self.update()
        self.hue_picked.emit(self.color())

    def mouseMoveEvent(self, e):
        if self._drag:
            self._hue = self._hue_from_pos(e.position())
            self.update()
            self.hue_picked.emit(self.color())

    def mouseReleaseEvent(self, e):
        if self._drag:
            self._drag = False
            self.hue_committed.emit(self.color())


class CustomizeOverlay(QWidget):
    """Floating overlay — change assistant name, user name, UI colour, and voice engine."""

    # assistant_name, user_name, ui_color, voice, tts_engine, el_key, el_voice
    saved = pyqtSignal(str, str, str, str, str, str, str)
    closed = pyqtSignal()
    _OW, _OH = 440, 680

    def __init__(self, assistant_name="Viernes", user_name="",
                 ui_color=DEFAULT_UI_COLOR, voice="",
                 tts_engine="gemini", el_key="", el_voice="", parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            CustomizeOverlay {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER_B};
                border-radius: 14px;
            }}
        """)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 18, 24, 18)
        lay.setSpacing(8)

        def _lbl(txt, fs=9, bold=False, color=C.TEXT, align=Qt.AlignmentFlag.AlignCenter):
            w = QLabel(txt); w.setAlignment(align)
            w.setFont(QFont(UI_FONT, int(round(fs)),
                            QFont.Weight.DemiBold if bold else QFont.Weight.Normal))
            w.setStyleSheet(f"color: {color}; background: transparent;")
            return w

        _fs = (f"QLineEdit {{ background: {C.DARK}; color: {C.TEXT}; "
               f"border: 1px solid {C.BORDER}; border-radius: 8px; padding: 4px 10px; }}"
               f"QLineEdit:focus {{ border: 1px solid {C.PRI}; }}")

        lay.addWidget(_lbl("Personalizar asistente", 12, True, color=C.WHITE))
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {C.BORDER}; margin: 2px 0;")
        lay.addWidget(sep)

        lay.addWidget(_lbl("Nombre del asistente", 9, True, color=C.TEXT_MED,
                            align=Qt.AlignmentFlag.AlignLeft))
        self._name_input = QLineEdit(assistant_name)
        self._name_input.setFont(QFont(UI_FONT, 10))
        self._name_input.setFixedHeight(32)
        self._name_input.setStyleSheet(_fs)
        lay.addWidget(self._name_input)

        lay.addSpacing(4)
        lay.addWidget(_lbl("Tu nombre (opcional)", 9, True,
                            color=C.TEXT_MED, align=Qt.AlignmentFlag.AlignLeft))
        self._user_input = QLineEdit(user_name)
        self._user_input.setPlaceholderText("Ej. Daniel (en blanco para trato automático)")
        self._user_input.setFont(QFont(UI_FONT, 10))
        self._user_input.setFixedHeight(32)
        self._user_input.setStyleSheet(_fs)
        lay.addWidget(self._user_input)

        # ── Voice Engine: Gemini Live vs ElevenLabs Flash vs Edge Neural vs Coqui XTTS-v2 ──
        lay.addSpacing(4)
        lay.addWidget(_lbl("Motor de voz en tiempo real", 9, True, color=C.TEXT_MED,
                            align=Qt.AlignmentFlag.AlignLeft))
        self._sel_engine = tts_engine if tts_engine in ("gemini", "elevenlabs", "edgetts", "coqui_xtts") else "gemini"
        engine_row = QHBoxLayout(); engine_row.setSpacing(5)
        self._engine_gemini_btn = QPushButton("Gemini Live")
        self._engine_eleven_btn = QPushButton("ElevenLabs")
        self._engine_edge_btn   = QPushButton("Edge Neural")
        self._engine_coqui_btn  = QPushButton("Coqui XTTS-v2")
        for b in (self._engine_gemini_btn, self._engine_eleven_btn, self._engine_edge_btn, self._engine_coqui_btn):
            b.setCheckable(True)
            b.setFixedHeight(28)
            b.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            engine_row.addWidget(b)
        lay.addLayout(engine_row)
        self._engine_gemini_btn.clicked.connect(lambda: self._set_engine("gemini"))
        self._engine_eleven_btn.clicked.connect(lambda: self._set_engine("elevenlabs"))
        self._engine_edge_btn.clicked.connect(lambda: self._set_engine("edgetts"))
        self._engine_coqui_btn.clicked.connect(lambda: self._set_engine("coqui_xtts"))

        _combo_style = f"""
            QComboBox {{
                background: {C.DARK}; color: {C.TEXT};
                border: 1px solid {C.BORDER}; border-radius: 8px;
                padding: 2px 8px;
            }}
            QComboBox:hover {{ border-color: {C.PRI}; }}
            QComboBox QAbstractItemView {{
                background: {C.PANEL}; color: {C.TEXT};
                selection-background-color: {C.PRI_GHO}; selection-color: {C.PRI};
                border: 1px solid {C.BORDER_B};
            }}
        """

        # ── Assistant voice — Gemini prebuilt voices + Acoustic Style ─────────
        from memory.config_manager import (
            AVAILABLE_VOICES, DEFAULT_VOICE, VOICE_METADATA,
            ELEVENLABS_PRESET_VOICES, EDGE_SPANISH_VOICES,
            GEMINI_VOICE_STYLES, get_voice_style, get_edge_voice,
        )
        self._gemini_voice_widget = QWidget()
        gv_lay = QVBoxLayout(self._gemini_voice_widget)
        gv_lay.setContentsMargins(0, 0, 0, 0)
        gv_lay.setSpacing(4)

        gv_hdr = QHBoxLayout()
        gv_hdr.addWidget(_lbl("VOZ NATIVA GEMINI LIVE (30 VOCES + MODULACIÓN ACÚSTICA)", 8, True, color=C.TEXT_DIM,
                              align=Qt.AlignmentFlag.AlignLeft))
        gv_hdr.addStretch()
        gv_lay.addLayout(gv_hdr)

        self._sel_voice = (voice or DEFAULT_VOICE)
        if self._sel_voice not in AVAILABLE_VOICES:
            self._sel_voice = DEFAULT_VOICE

        # Quick access pills for top voices
        quick_voices = ["Aoede", "Kore", "Leda", "Zephyr", "Puck", "Charon"]
        self._voice_btns: dict[str, QPushButton] = {}
        quick_row = QHBoxLayout(); quick_row.setSpacing(4)
        for _v in quick_voices:
            meta = VOICE_METADATA.get(_v, ("Femenina", ""))
            gender_sym = "♀" if meta[0] == "Femenina" else "♂"
            b = QPushButton(f"{gender_sym} {_v}")
            b.setCheckable(True)
            b.setFixedHeight(24)
            b.setFont(QFont(UI_FONT, 8, QFont.Weight.Bold))
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setToolTip(f"{meta[0]} — {meta[1]}")
            b.clicked.connect(lambda _=False, name=_v: self._on_voice_pick(name))
            self._voice_btns[_v] = b
            quick_row.addWidget(b)
        gv_lay.addLayout(quick_row)

        # Full 30-voice dropdown selector
        self._voice_combo = QComboBox()
        self._voice_combo.setFont(QFont(UI_FONT, 8))
        self._voice_combo.setFixedHeight(26)
        self._voice_combo.setStyleSheet(_combo_style)
        for _v in AVAILABLE_VOICES:
            meta = VOICE_METADATA.get(_v, ("Neutral", "Voz estándar"))
            gender_sym = "♀" if meta[0] == "Femenina" else "♂"
            display_str = f"{gender_sym} {_v} — [{meta[0]}] {meta[1]}"
            self._voice_combo.addItem(display_str, _v)

        idx = AVAILABLE_VOICES.index(self._sel_voice) if self._sel_voice in AVAILABLE_VOICES else 0
        self._voice_combo.setCurrentIndex(idx)
        self._voice_combo.currentIndexChanged.connect(self._on_combo_voice_changed)
        gv_lay.addWidget(self._voice_combo)

        # Acoustic Style selector for Gemini Live
        gv_lay.addWidget(_lbl("MODULACIÓN DE TIMBRE Y ESTILO VOCAL (GEMINI LIVE)", 7, color=C.TEXT_DIM,
                              align=Qt.AlignmentFlag.AlignLeft))
        self._style_combo = QComboBox()
        self._style_combo.setFont(QFont(UI_FONT, 8))
        self._style_combo.setFixedHeight(26)
        self._style_combo.setStyleSheet(_combo_style)
        curr_style = get_voice_style()
        style_keys = list(GEMINI_VOICE_STYLES.keys())
        for sk in style_keys:
            s_title, _ = GEMINI_VOICE_STYLES[sk]
            self._style_combo.addItem(f"🎚️ {s_title}", sk)
        if curr_style in style_keys:
            self._style_combo.setCurrentIndex(style_keys.index(curr_style))
        gv_lay.addWidget(self._style_combo)

        # Active voice description indicator
        meta_curr = VOICE_METADATA.get(self._sel_voice, ("Femenina", "Natural"))
        self._voice_desc_lbl = _lbl(f"▸ Activa: {self._sel_voice} [{meta_curr[0]}] — {meta_curr[1]}", 7,
                                    color=C.PRI, align=Qt.AlignmentFlag.AlignLeft)
        gv_lay.addWidget(self._voice_desc_lbl)

        lay.addWidget(self._gemini_voice_widget)
        self._refresh_voice_btns()

        # ── ElevenLabs Flash v2.5 configuration inputs ────────────────────────
        self._eleven_widget = QWidget()
        el_lay = QVBoxLayout(self._eleven_widget)
        el_lay.setContentsMargins(0, 0, 0, 0)
        el_lay.setSpacing(4)

        el_top = QHBoxLayout()
        el_top.addWidget(_lbl("ELEVENLABS API KEY (FLASH v2.5 STREAMING ~200ms)", 8, color=C.TEXT_DIM,
                              align=Qt.AlignmentFlag.AlignLeft))
        el_top.addStretch()
        self._el_sync_btn = QPushButton("🔄 Cargar Mis Voces")
        self._el_sync_btn.setFixedHeight(22)
        self._el_sync_btn.setFont(QFont(UI_FONT, 7, QFont.Weight.Bold))
        self._el_sync_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._el_sync_btn.setStyleSheet(f"""
            QPushButton {{
                background: {C.PRI_GHO}; color: {C.PRI};
                border: 1px solid {C.PRI_DIM}; border-radius: 6px; padding: 0 8px;
            }}
            QPushButton:hover {{ border-color: {C.PRI}; }}
        """)
        self._el_sync_btn.clicked.connect(self._sync_elevenlabs_voices)
        el_top.addWidget(self._el_sync_btn)
        el_lay.addLayout(el_top)

        self._el_key_input = QLineEdit(el_key)
        self._el_key_input.setPlaceholderText("sk_... (ElevenLabs API Key)")
        self._el_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self._el_key_input.setFont(QFont(UI_FONT, 9))
        self._el_key_input.setFixedHeight(26)
        self._el_key_input.setStyleSheet(_fs)
        el_lay.addWidget(self._el_key_input)

        el_lay.addWidget(_lbl("CATÁLOGO DE VOCES ELEVENLABS (O PEGA UN VOICE ID ABAJO)", 7,
                              color=C.TEXT_DIM, align=Qt.AlignmentFlag.AlignLeft))
        self._el_voice_combo = QComboBox()
        self._el_voice_combo.setFont(QFont(UI_FONT, 8))
        self._el_voice_combo.setFixedHeight(26)
        self._el_voice_combo.setStyleSheet(_combo_style)
        for vid, (vname, vgen, vdesc) in ELEVENLABS_PRESET_VOICES.items():
            gsym = "♀" if vgen == "Femenina" else "♂"
            self._el_voice_combo.addItem(f"{gsym} {vname} — [{vgen}] {vdesc}", vid)

        self._el_voice_input = QLineEdit(el_voice or "21m00Tcm4TlvDq8ikWAM")
        self._el_voice_input.setPlaceholderText("e.g. 21m00Tcm4TlvDq8ikWAM")
        self._el_voice_input.setFont(QFont(UI_FONT, 8))
        self._el_voice_input.setFixedHeight(26)
        self._el_voice_input.setStyleSheet(_fs)

        curr_el_vid = (el_voice or "21m00Tcm4TlvDq8ikWAM").strip()
        preset_ids = list(ELEVENLABS_PRESET_VOICES.keys())
        if curr_el_vid in preset_ids:
            self._el_voice_combo.setCurrentIndex(preset_ids.index(curr_el_vid))
        self._el_voice_combo.currentIndexChanged.connect(self._on_el_combo_changed)

        el_lay.addWidget(self._el_voice_combo)
        el_lay.addWidget(self._el_voice_input)
        lay.addWidget(self._eleven_widget)

        # ── Microsoft Edge Neural TTS (Free, 17 Latin/Spanish Voices) ────────
        self._edge_widget = QWidget()
        ed_lay = QVBoxLayout(self._edge_widget)
        ed_lay.setContentsMargins(0, 0, 0, 0)
        ed_lay.setSpacing(4)
        ed_lay.addWidget(_lbl("VOCES NEURALES LATINAS Y ESPAÑOLAS (100% GRATIS — SIN API KEY)", 8, True,
                              color=C.TEXT_DIM, align=Qt.AlignmentFlag.AlignLeft))
        self._edge_combo = QComboBox()
        self._edge_combo.setFont(QFont(UI_FONT, 8))
        self._edge_combo.setFixedHeight(28)
        self._edge_combo.setStyleSheet(_combo_style)
        curr_edge = get_edge_voice()
        edge_ids = list(EDGE_SPANISH_VOICES.keys())
        for evid in edge_ids:
            ename, egen, edesc = EDGE_SPANISH_VOICES[evid]
            gsym = "♀" if egen == "Femenina" else "♂"
            self._edge_combo.addItem(f"{gsym} {ename} — {edesc}", evid)
        if curr_edge in edge_ids:
            self._edge_combo.setCurrentIndex(edge_ids.index(curr_edge))
        ed_lay.addWidget(self._edge_combo)
        ed_lay.addWidget(_lbl("▸ Streaming por cláusulas en tiempo real (~250ms) con acentos regionales.", 7,
                              color=C.PRI, align=Qt.AlignmentFlag.AlignLeft))
        lay.addWidget(self._edge_widget)

        self._set_engine(self._sel_engine)

        # ── UI colour — colour wheel ─────────────────────────────────────────
        lay.addSpacing(4)
        # ── Coqui XTTS-v2 (idiap/coqui-ai-TTS) Local & Voice Cloning ──────────
        from memory.config_manager import COQUI_XTTS_SPEAKERS, get_coqui_config
        from core.tts import is_coqui_installed
        _cq_cfg = get_coqui_config()
        self._coqui_widget = QWidget()
        cq_lay = QVBoxLayout(self._coqui_widget)
        cq_lay.setContentsMargins(0, 0, 0, 0)
        cq_lay.setSpacing(5)
        cq_lay.addWidget(_lbl("COQUI XTTS-v2 (LOCAL · GRATUITO · CLONACIÓN DE VOZ)", 8, True,
                              color=C.TEXT_DIM, align=Qt.AlignmentFlag.AlignLeft))

        cq_top = QHBoxLayout(); cq_top.setSpacing(6)
        self._coqui_speaker_combo = QComboBox()
        self._coqui_speaker_combo.setFont(QFont(UI_FONT, 9))
        self._coqui_speaker_combo.setFixedHeight(28)
        self._coqui_speaker_combo.setStyleSheet(_combo_style)
        for spk in COQUI_XTTS_SPEAKERS:
            self._coqui_speaker_combo.addItem(spk, spk)
        c_idx = self._coqui_speaker_combo.findData(_cq_cfg.get("speaker", "Ana Florence"))
        if c_idx >= 0:
            self._coqui_speaker_combo.setCurrentIndex(c_idx)
        cq_top.addWidget(self._coqui_speaker_combo, stretch=2)

        self._coqui_lang_combo = QComboBox()
        self._coqui_lang_combo.setFont(QFont(UI_FONT, 9))
        self._coqui_lang_combo.setFixedHeight(28)
        self._coqui_lang_combo.setStyleSheet(_combo_style)
        for lc, lname in (("es", "Español"), ("en", "Inglés"), ("pt", "Portugués"), ("fr", "Francés")):
            self._coqui_lang_combo.addItem(lname, lc)
        l_idx = self._coqui_lang_combo.findData(_cq_cfg.get("language", "es"))
        if l_idx >= 0:
            self._coqui_lang_combo.setCurrentIndex(l_idx)
        cq_top.addWidget(self._coqui_lang_combo, stretch=1)
        cq_lay.addLayout(cq_top)

        wav_row = QHBoxLayout(); wav_row.setSpacing(6)
        self._coqui_wav_input = QLineEdit(_cq_cfg.get("speaker_wav", ""))
        self._coqui_wav_input.setPlaceholderText("Audio .wav/.mp3 para clonar voz (opcional)")
        self._coqui_wav_input.setFont(QFont(UI_FONT, 9))
        self._coqui_wav_input.setFixedHeight(28)
        self._coqui_wav_input.setStyleSheet(_fs)
        wav_row.addWidget(self._coqui_wav_input, stretch=1)

        wav_pick = QPushButton("Audio…")
        wav_pick.setFixedHeight(28)
        wav_pick.setCursor(Qt.CursorShape.PointingHandCursor)
        wav_pick.setStyleSheet(
            f"QPushButton {{ background: {C.PANEL2}; color: {C.TEXT}; border: 1px solid {C.BORDER}; border-radius: 7px; padding: 0 10px; }}"
            f"QPushButton:hover {{ border-color: {C.PRI}; }}"
        )
        wav_pick.clicked.connect(self._pick_coqui_wav)
        wav_row.addWidget(wav_pick)
        cq_lay.addLayout(wav_row)

        inst_row = QHBoxLayout(); inst_row.setSpacing(6)
        _cq_ok = is_coqui_installed()
        self._coqui_status_lbl = QLabel(
            "● Motor idiap/coqui-ai-TTS listo" if _cq_ok else "○ Requiere instalar coqui-tts"
        )
        self._coqui_status_lbl.setFont(QFont(UI_FONT, 8))
        self._coqui_status_lbl.setStyleSheet(f"color: {C.GREEN if _cq_ok else C.ACC2}; background: transparent;")
        inst_row.addWidget(self._coqui_status_lbl, stretch=1)

        self._coqui_install_btn = QPushButton("Instalar coqui-tts")
        self._coqui_install_btn.setFixedHeight(24)
        self._coqui_install_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._coqui_install_btn.setVisible(not _cq_ok)
        self._coqui_install_btn.setStyleSheet(
            f"QPushButton {{ background: {C.PRI_GHO}; color: {C.PRI}; border: 1px solid {C.PRI}; border-radius: 6px; padding: 0 10px; font-weight: 600; }}"
        )
        self._coqui_install_btn.clicked.connect(self._install_coqui_pkg)
        inst_row.addWidget(self._coqui_install_btn)
        cq_lay.addLayout(inst_row)
        lay.addWidget(self._coqui_widget)

        clr_hdr = QHBoxLayout()
        clr_hdr.addWidget(_lbl("Color de acento de la interfaz", 9, True,
                               color=C.TEXT_MED, align=Qt.AlignmentFlag.AlignLeft))
        clr_hdr.addStretch()
        df_btn = QPushButton("Por defecto")
        df_btn.setFixedSize(78, 22)
        df_btn.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        df_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        df_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {C.TEXT_MED};
                border: 1px solid {C.BORDER}; border-radius: 6px;
            }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
        """)
        df_btn.clicked.connect(lambda: self._set_color(DEFAULT_UI_COLOR))
        clr_hdr.addWidget(df_btn)
        lay.addLayout(clr_hdr)

        self._initial_color = (ui_color or DEFAULT_UI_COLOR).strip().lower()
        self._sel_color     = self._initial_color
        self.on_preview     = None   # callable(hex) — live preview; MainWindow wires it

        self._wheel = HueWheel(self._sel_color)
        wheel_row = QHBoxLayout()
        wheel_row.addStretch(); wheel_row.addWidget(self._wheel); wheel_row.addStretch()
        lay.addLayout(wheel_row)
        self._wheel.hue_picked.connect(self._on_wheel_pick)
        self._wheel.hue_committed.connect(self._on_wheel_commit)

        self._hex_input = QLineEdit(self._sel_color)
        self._hex_input.setPlaceholderText("#6E6AF6  (color hexadecimal)")
        self._hex_input.setFont(QFont(UI_FONT, 10))
        self._hex_input.setFixedHeight(28)
        self._hex_input.setStyleSheet(_fs)
        self._hex_input.textEdited.connect(self._on_hex_edited)
        lay.addWidget(self._hex_input)

        lay.addSpacing(6)
        btn_row = QHBoxLayout(); btn_row.setSpacing(8)

        save_btn = QPushButton("Guardar cambios")
        save_btn.setFixedHeight(34)
        save_btn.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background: {C.PRI}; color: {C.WHITE};
                border: none; border-radius: 8px;
            }}
            QPushButton:hover {{ background: {C.PRI_DIM}; }}
        """)
        save_btn.clicked.connect(self._save)
        btn_row.addWidget(save_btn)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setFixedHeight(34)
        cancel_btn.setFont(QFont(UI_FONT, 9))
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {C.TEXT_MED};
                border: 1px solid {C.BORDER}; border-radius: 8px;
            }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
        """)
        cancel_btn.clicked.connect(self._cancel)
        btn_row.addWidget(cancel_btn)
        lay.addLayout(btn_row)

    # ── voice selection ──────────────────────────────────────────────────────
    def _on_el_combo_changed(self, index: int):
        vid = self._el_voice_combo.itemData(index)
        if vid and hasattr(self, "_el_voice_input"):
            self._el_voice_input.setText(str(vid))

    def _sync_elevenlabs_voices(self):
        key = self._el_key_input.text().strip()
        if not key:
            self._el_sync_btn.setText("⚠️ Falta API Key")
            return
        self._el_sync_btn.setText("⏳ Cargando...")
        QApplication.processEvents()
        try:
            from core.tts import fetch_elevenlabs_voices
            voices = fetch_elevenlabs_voices(key)
            if voices:
                self._el_voice_combo.blockSignals(True)
                self._el_voice_combo.clear()
                curr_vid = self._el_voice_input.text().strip()
                sel_idx = 0
                for idx, (vid, vname, vgen, vdesc) in enumerate(voices):
                    gsym = "♀" if vgen == "Femenina" else ("♂" if vgen == "Masculina" else "🎙️")
                    self._el_voice_combo.addItem(f"{gsym} {vname} — [{vgen}] {vdesc}", vid)
                    if vid == curr_vid:
                        sel_idx = idx
                self._el_voice_combo.setCurrentIndex(sel_idx)
                self._el_voice_combo.blockSignals(False)
                if voices and not curr_vid:
                    self._el_voice_input.setText(voices[0][0])
                self._el_sync_btn.setText(f"✅ {len(voices)} Voces")
            else:
                self._el_sync_btn.setText("⚠️ 0 Voces")
        except Exception:
            self._el_sync_btn.setText("❌ Error API Key")

    def _on_combo_voice_changed(self, index: int):
        from memory.config_manager import AVAILABLE_VOICES
        if 0 <= index < len(AVAILABLE_VOICES):
            self._on_voice_pick(AVAILABLE_VOICES[index], from_combo=True)

    def _on_voice_pick(self, name: str, from_combo: bool = False):
        from memory.config_manager import AVAILABLE_VOICES, VOICE_METADATA
        if name in AVAILABLE_VOICES:
            self._sel_voice = name
            if not from_combo and hasattr(self, "_voice_combo"):
                self._voice_combo.blockSignals(True)
                idx = AVAILABLE_VOICES.index(name)
                self._voice_combo.setCurrentIndex(idx)
                self._voice_combo.blockSignals(False)
            if hasattr(self, "_voice_desc_lbl"):
                meta = VOICE_METADATA.get(name, ("Neutral", "Voz estándar"))
                self._voice_desc_lbl.setText(f"▸ Activa: {name} [{meta[0]}] — {meta[1]}")
            self._refresh_voice_btns()

    def _refresh_voice_btns(self):
        """Highlight the selected voice pill; dim the rest."""
        for name, b in self._voice_btns.items():
            on = (name == self._sel_voice)
            b.setChecked(on)
            if on:
                b.setStyleSheet(f"""
                    QPushButton {{ background: {C.PRI_GHO}; color: {C.PRI};
                        border: 1px solid {C.PRI}; border-radius: 8px; }}
                """)
            else:
                b.setStyleSheet(f"""
                    QPushButton {{ background: transparent; color: {C.TEXT_MED};
                        border: 1px solid {C.BORDER}; border-radius: 8px; }}
                    QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
                """)

    # ── colour flow ──────────────────────────────────────────────────────────
    def _set_color(self, hx: str, update_wheel: bool = True, preview: bool = True):
        """Updates the selected colour; hex box + wheel stay in sync, theme is live-previewed."""
        self._sel_color = hx.strip().lower()
        self._hex_input.blockSignals(True)
        self._hex_input.setText(self._sel_color)
        self._hex_input.blockSignals(False)
        if update_wheel:
            self._wheel.set_color(self._sel_color)
        if preview and self.on_preview:
            self.on_preview(self._sel_color)

    def _on_wheel_pick(self, hx: str):
        # While dragging: update the hex box, don't apply the theme yet
        self._sel_color = hx
        self._hex_input.blockSignals(True)
        self._hex_input.setText(hx)
        self._hex_input.blockSignals(False)

    def _on_wheel_commit(self, hx: str):
        # Handle released → live-preview the whole interface
        self._set_color(hx, update_wheel=False)

    def _on_hex_edited(self, text: str):
        t = text.strip().lower()
        if t.startswith("#") and len(t) == 7:
            try:
                int(t[1:], 16)
            except ValueError:
                return
            self._set_color(t, update_wheel=True, preview=True)

    def _pick_coqui_wav(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar audio de referencia (6-15s)", "",
            "Audio (*.wav *.mp3 *.ogg *.flac)"
        )
        if path:
            self._coqui_wav_input.setText(path)

    def _install_coqui_pkg(self):
        self._coqui_install_btn.setEnabled(False)
        self._coqui_install_btn.setText("Instalando…")
        self._coqui_status_lbl.setText("⏳ Instalando coqui-tts (idiap/coqui-ai-TTS)…")
        self._coqui_status_lbl.setStyleSheet(f"color: {C.ACC2}; background: transparent;")

        def _worker():
            import subprocess, sys
            try:
                proc = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "coqui-tts"],
                    capture_output=True, text=True, timeout=600,
                )
                ok = proc.returncode == 0
            except Exception:
                ok = False

            def _done():
                if ok:
                    self._coqui_status_lbl.setText("● Motor idiap/coqui-ai-TTS instalado")
                    self._coqui_status_lbl.setStyleSheet(f"color: {C.GREEN}; background: transparent;")
                    self._coqui_install_btn.hide()
                else:
                    self._coqui_status_lbl.setText("✕ Error instalando — ejecuta: pip install coqui-tts")
                    self._coqui_status_lbl.setStyleSheet(f"color: {C.RED}; background: transparent;")
                    self._coqui_install_btn.setEnabled(True)
                    self._coqui_install_btn.setText("Reintentar")

            QTimer.singleShot(0, _done)

        threading.Thread(target=_worker, daemon=True).start()

    def _set_engine(self, engine: str):
        self._sel_engine = engine
        self._gemini_voice_widget.setVisible(engine == "gemini")
        self._eleven_widget.setVisible(engine == "elevenlabs")
        self._edge_widget.setVisible(engine == "edgetts")
        if hasattr(self, "_coqui_widget"):
            self._coqui_widget.setVisible(engine == "coqui_xtts")
        self._engine_gemini_btn.setChecked(engine == "gemini")
        self._engine_eleven_btn.setChecked(engine == "elevenlabs")
        self._engine_edge_btn.setChecked(engine == "edgetts")
        self._engine_coqui_btn.setChecked(engine == "coqui_xtts")

        for btn, active in (
            (self._engine_gemini_btn, engine == "gemini"),
            (self._engine_eleven_btn, engine == "elevenlabs"),
            (self._engine_edge_btn,   engine == "edgetts"),
            (self._engine_coqui_btn,  engine == "coqui_xtts"),
        ):
            if active:
                btn.setStyleSheet(f"""
                    QPushButton {{ background: {C.PRI_GHO}; color: {C.PRI};
                        border: 1px solid {C.PRI}; border-radius: 8px; }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{ background: transparent; color: {C.TEXT_MED};
                        border: 1px solid {C.BORDER}; border-radius: 8px; }}
                    QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
                """)

    def _cancel(self):
        # If a preview was applied, revert to the colour from launch
        if self.on_preview and self._sel_color != self._initial_color:
            self.on_preview(self._initial_color)
        self.hide()

    def _save(self):
        from memory.config_manager import save_edge_voice, save_voice_style, save_coqui_config
        name = self._name_input.text().strip() or "Viernes"
        user = self._user_input.text().strip()
        el_key = self._el_key_input.text().strip()
        el_voice = self._el_voice_input.text().strip() or "21m00Tcm4TlvDq8ikWAM"
        if hasattr(self, "_edge_combo"):
            evid = self._edge_combo.currentData()
            if evid:
                save_edge_voice(str(evid))
        if hasattr(self, "_style_combo"):
            st_key = self._style_combo.currentData()
            if st_key:
                save_voice_style(str(st_key))
        if hasattr(self, "_coqui_speaker_combo"):
            save_coqui_config(
                str(self._coqui_speaker_combo.currentData() or "Ana Florence"),
                self._coqui_wav_input.text().strip(),
                str(self._coqui_lang_combo.currentData() or "es"),
            )
        self.saved.emit(name, user, self._sel_color or DEFAULT_UI_COLOR,
                        self._sel_voice, self._sel_engine, el_key, el_voice)
        self.hide()

    def hideEvent(self, e):
        super().hideEvent(e)
        self.closed.emit()

    def closeEvent(self, e):
        super().closeEvent(e)
        self.closed.emit()


class PluginManagerOverlay(QWidget):
    """Floating overlay — lists discovered plugins with per-plugin ON/OFF toggles."""

    _OW = 420

    def __init__(self, plugins: list[dict], parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            PluginManagerOverlay {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER_B};
                border-radius: 12px;
            }}
        """)
        self.setFixedWidth(self._OW)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(6)

        hdr = QLabel("Gestor de extensiones")
        hdr.setFont(QFont(UI_FONT, 12, QFont.Weight.DemiBold))
        hdr.setStyleSheet(f"color: {C.WHITE}; background: transparent;")
        lay.addWidget(hdr)
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {C.BORDER}; margin: 2px 0;")
        lay.addWidget(sep)

        if not plugins:
            empty = QLabel("No se encontraron extensiones en /plugins.")
            empty.setFont(QFont(UI_FONT, 8))
            empty.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent;")
            lay.addWidget(empty)

        for p in plugins:
            lay.addLayout(self._build_row(p))

        lay.addSpacing(4)
        close_btn = QPushButton("Cerrar")
        close_btn.setFixedHeight(32)
        close_btn.setFont(QFont(UI_FONT, 9))
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {C.TEXT_MED};
                border: 1px solid {C.BORDER}; border-radius: 8px;
            }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
        """)
        close_btn.clicked.connect(self.hide)
        lay.addWidget(close_btn)
        self.adjustSize()

    def _build_row(self, p: dict) -> QHBoxLayout:
        row = QHBoxLayout(); row.setSpacing(6)

        label_text = p["name"] if p["valid"] else f"{p['name']}  (⚠ {p['file']})"
        lbl = QLabel(label_text)
        lbl.setFont(QFont(UI_FONT, 8))
        lbl.setStyleSheet(f"color: {C.TEXT if p['valid'] else C.TEXT_DIM}; background: transparent;")
        lbl.setToolTip(p["description"] if p["valid"] else p["error"])
        lbl.setWordWrap(False)
        row.addWidget(lbl, stretch=1)

        btn = QPushButton()
        btn.setFixedSize(72, 24)
        btn.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        if not p["valid"]:
            btn.setText("Error")
            btn.setEnabled(False)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; color: {C.TEXT_DIM};
                    border: 1px solid {C.BORDER}; border-radius: 6px;
                }}
            """)
        else:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self._style_toggle(btn, p["enabled"])
            btn.clicked.connect(lambda _, name=p["name"], b=btn: self._toggle(name, b))
        row.addWidget(btn)
        return row

    def _style_toggle(self, btn: QPushButton, enabled: bool):
        if enabled:
            btn.setText("Activo")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {_rgba(C.GREEN, 0.14)}; color: {C.GREEN};
                    border: 1px solid {_rgba(C.GREEN, 0.40)}; border-radius: 6px;
                }}
                QPushButton:hover {{ background: {_rgba(C.GREEN, 0.22)}; }}
            """)
        else:
            btn.setText("Inactivo")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; color: {C.TEXT_DIM};
                    border: 1px solid {C.BORDER}; border-radius: 6px;
                }}
                QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
            """)

    def _toggle(self, name: str, btn: QPushButton):
        from memory.config_manager import get_plugin_enabled, save_plugin_enabled
        new_val = not get_plugin_enabled(name)
        save_plugin_enabled(name, new_val)
        self._style_toggle(btn, new_val)

    def hideEvent(self, e):
        super().hideEvent(e)
        self.closed.emit()

    def closeEvent(self, e):
        super().closeEvent(e)
        self.closed.emit()


class _HudOverlay(QWidget):
    """Base for the floating panels placed by hand over the HUD.

    They are children of the central widget but sit in no layout, so Qt never
    invalidates the region they occupy when they hide or shrink: the HUD keeps
    painting around them and their last frame stays on screen as a ghost. Any
    overlay positioned with _centre_overlay needs this."""

    closed = pyqtSignal()

    def hideEvent(self, e):
        p = self.parentWidget()
        if p is not None:
            # Repaint exactly what we were covering, before we stop covering it.
            p.update(self.geometry())
        self.closed.emit()
        super().hideEvent(e)

    def closeEvent(self, e):
        p = self.parentWidget()
        if p is not None:
            p.update(self.geometry())
        self.closed.emit()
        super().closeEvent(e)


class ConfirmBanner(_HudOverlay):
    """The gate in front of an action that cannot be taken back."""

    answered = pyqtSignal(bool)
    _OW = 430

    def __init__(self, title: str, detail: str, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            ConfirmBanner {{
                background: {C.PANEL};
                border: 1px solid {C.ACC};
                border-radius: 12px;
            }}
        """)
        self.setFixedWidth(self._OW)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(8)

        hdr = QLabel("Confirmar acción")
        hdr.setFont(QFont(UI_FONT, 11, QFont.Weight.DemiBold))
        hdr.setStyleSheet(f"color: {C.ACC}; background: transparent;")
        lay.addWidget(hdr)

        ttl = QLabel(title)
        ttl.setWordWrap(True)
        ttl.setFont(QFont(UI_FONT, 10, QFont.Weight.DemiBold))
        ttl.setStyleSheet(f"color: {C.TEXT}; background: transparent;")
        lay.addWidget(ttl)

        if detail:
            dtl = QLabel(detail)
            dtl.setWordWrap(True)
            dtl.setFont(QFont(UI_FONT, 9))
            dtl.setStyleSheet(f"color: {C.TEXT_MED}; background: transparent;")
            lay.addWidget(dtl)

        row = QHBoxLayout(); row.setSpacing(8)

        yes = QPushButton("Confirmar")
        yes.setFixedHeight(34)
        yes.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        yes.setCursor(Qt.CursorShape.PointingHandCursor)
        yes.setStyleSheet(f"""
            QPushButton {{ background: {_rgba(C.ACC, 0.14)}; color: {C.ACC};
                border: 1px solid {C.ACC}; border-radius: 8px; }}
            QPushButton:hover {{ background: {_rgba(C.ACC, 0.24)}; }}
        """)
        yes.clicked.connect(lambda: self.answered.emit(True))
        row.addWidget(yes)

        no = QPushButton("Cancelar")
        no.setFixedHeight(34)
        no.setFont(QFont(UI_FONT, 9))
        no.setCursor(Qt.CursorShape.PointingHandCursor)
        no.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {C.TEXT_MED};
                border: 1px solid {C.BORDER}; border-radius: 8px; }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
        """)
        no.clicked.connect(lambda: self.answered.emit(False))
        row.addWidget(no)
        lay.addLayout(row)

        no.setDefault(True)
        no.setFocus()


class AudioDeviceOverlay(_HudOverlay):
    """Choose which microphone VIERNES listens to and which speakers it uses."""

    picked = pyqtSignal()      # emitted after Apply, when something changed
    _OW = 460

    def __init__(self, parent=None):
        super().__init__(parent)
        from core.audio_devices import list_devices, DEFAULT_LABEL
        from memory.config_manager import get_input_device, get_output_device

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            AudioDeviceOverlay {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER_B};
                border-radius: 14px;
            }}
        """)
        self.setFixedWidth(self._OW)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(22, 18, 22, 18)
        lay.setSpacing(8)

        hdr = QLabel("Dispositivos de audio")
        hdr.setFont(QFont(UI_FONT, 12, QFont.Weight.DemiBold))
        hdr.setStyleSheet(f"color: {C.WHITE}; background: transparent;")
        lay.addWidget(hdr)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {C.BORDER}; margin: 2px 0;")
        lay.addWidget(sep)

        _combo_css = (
            f"QComboBox {{ background: {C.DARK}; color: {C.TEXT}; "
            f"border: 1px solid {C.BORDER}; border-radius: 8px; padding: 4px 10px; }}"
            f"QComboBox:hover {{ border-color: {C.BORDER_B}; }}"
            f"QComboBox QAbstractItemView {{ background: {C.PANEL}; color: {C.TEXT}; "
            f"selection-background-color: {C.PRI_GHO}; border: 1px solid {C.BORDER}; }}"
        )

        def _row(label: str, kind: str, current: str) -> QComboBox:
            cap = QLabel(label)
            cap.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
            cap.setStyleSheet(f"color: {C.TEXT_MED}; background: transparent;")
            lay.addWidget(cap)

            box = QComboBox()
            box.setFont(QFont(UI_FONT, 9))
            box.setFixedHeight(32)
            box.setStyleSheet(_combo_css)
            box.addItem(DEFAULT_LABEL, "")
            for name in list_devices(kind):
                box.addItem(name, name)
            idx = box.findData(current) if current else 0
            box.setCurrentIndex(idx if idx >= 0 else 0)
            if current and idx < 0:
                box.addItem(f"{current}  (no conectado)", current)
                box.setCurrentIndex(box.count() - 1)
            lay.addWidget(box)
            return box

        _asst = (_read_full_config().get("assistant_name") or "Viernes").strip()
        self._in_box  = _row(f"Micrófono de entrada para {_asst}",
                             "input", get_input_device())
        lay.addSpacing(4)
        self._out_box = _row(f"Altavoces de salida para {_asst}",
                             "output", get_output_device())

        note = QLabel("Al aplicar se reconectará el flujo de audio conservando la conversación actual.")
        note.setWordWrap(True)
        note.setFont(QFont(UI_FONT, 8))
        note.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent;")
        lay.addSpacing(4)
        lay.addWidget(note)

        row = QHBoxLayout(); row.setSpacing(8)
        ok = QPushButton("Aplicar")
        ok.setFixedHeight(34)
        ok.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        ok.setCursor(Qt.CursorShape.PointingHandCursor)
        ok.setStyleSheet(f"""
            QPushButton {{ background: {C.PRI}; color: {C.WHITE};
                border: none; border-radius: 8px; }}
            QPushButton:hover {{ background: {C.PRI_DIM}; }}
        """)
        ok.clicked.connect(self._apply)
        row.addWidget(ok)

        cancel = QPushButton("Cerrar")
        cancel.setFixedHeight(34)
        cancel.setFont(QFont(UI_FONT, 9))
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {C.TEXT_MED};
                border: 1px solid {C.BORDER}; border-radius: 8px; }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
        """)
        cancel.clicked.connect(self.hide)
        row.addWidget(cancel)
        lay.addLayout(row)

    def _apply(self):
        from memory.config_manager import (
            get_input_device, get_output_device,
            save_input_device, save_output_device,
        )
        new_in  = self._in_box.currentData()  or ""
        new_out = self._out_box.currentData() or ""
        changed = (new_in != get_input_device()) or (new_out != get_output_device())
        save_input_device(new_in)
        save_output_device(new_out)
        self.hide()
        if changed:
            self.picked.emit()


class MemoryOverlay(_HudOverlay):
    """Everything VIERNES has stored about you, and when it learned it."""

    _OW = 520

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            MemoryOverlay {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER_B};
                border-radius: 14px;
            }}
        """)
        self.setFixedWidth(self._OW)

        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(22, 18, 22, 18)
        self._lay.setSpacing(6)
        self._rebuild()

    def _clear_layout(self):
        while self._lay.count():
            item = self._lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.hide()
                w.deleteLater()
                continue
            sub = item.layout()
            if sub is not None:
                while sub.count():
                    si = sub.takeAt(0)
                    sw = si.widget()
                    if sw is not None:
                        sw.hide()
                        sw.deleteLater()
                sub.deleteLater()

    def _settle(self, before):
        self._lay.invalidate()
        self._lay.activate()
        self.updateGeometry()
        self.adjustSize()

        p = self.parentWidget()
        if p is None:
            self.update()
            return
        self.move(max(0, (p.width()  - self.width())  // 2),
                  max(0, (p.height() - self.height()) // 2))
        p.update(before.united(self.geometry()))
        self.update()

    def _rebuild(self):
        before = self.geometry()
        self._clear_layout()

        from memory.memory_manager import all_entries_for_ui

        _asst = (_read_full_config().get("assistant_name") or "Viernes").strip()
        hdr = QLabel(f"Memoria personal de {_asst}")
        hdr.setFont(QFont(UI_FONT, 12, QFont.Weight.DemiBold))
        hdr.setStyleSheet(f"color: {C.WHITE}; background: transparent;")
        self._lay.addWidget(hdr)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {C.BORDER}; margin: 2px 0;")
        self._lay.addWidget(sep)

        rows = all_entries_for_ui()

        cap = QLabel(f"{len(rows)} recuerdos almacenados localmente en memory/long_term.json.")
        cap.setWordWrap(True)
        cap.setFont(QFont(UI_FONT, 8))
        cap.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent;")
        self._lay.addWidget(cap)

        if not rows:
            empty = QLabel("Aún no hay recuerdos registrados.")
            empty.setFont(QFont(UI_FONT, 9))
            empty.setStyleSheet(f"color: {C.TEXT_MED}; background: transparent; padding: 8px 0;")
            self._lay.addWidget(empty)
        else:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setFixedHeight(min(420, 34 * len(rows) + 10))
            scroll.setStyleSheet(
                f"QScrollArea {{ border: 1px solid {C.BORDER}; border-radius: 8px; "
                f"background: {C.DARK}; }}"
            )
            inner = QWidget()
            ilay  = QVBoxLayout(inner)
            ilay.setContentsMargins(8, 8, 8, 8)
            ilay.setSpacing(4)

            for r in rows:
                line = QHBoxLayout(); line.setSpacing(6)
                txt = QLabel(f"<b>{r['key'].replace('_', ' ')}</b> "
                             f"<span style='color:{C.TEXT_MED}'>— {r['value']}</span>")
                txt.setWordWrap(True)
                txt.setFont(QFont(UI_FONT, 9))
                txt.setStyleSheet(f"color: {C.TEXT}; background: transparent;")
                line.addWidget(txt, 1)

                meta = QLabel(f"{r['category'][:4]} · {r['updated'] or '—'}")
                meta.setFont(QFont(UI_FONT, 8))
                meta.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent;")
                line.addWidget(meta)

                rm = QPushButton("✕")
                rm.setFixedSize(22, 22)
                rm.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
                rm.setCursor(Qt.CursorShape.PointingHandCursor)
                rm.setToolTip("Eliminar recuerdo")
                rm.setStyleSheet(f"""
                    QPushButton {{ background: transparent; color: {C.TEXT_DIM};
                        border: 1px solid {C.BORDER}; border-radius: 6px; }}
                    QPushButton:hover {{ color: {C.RED}; border-color: {C.RED}; }}
                """)
                rm.clicked.connect(
                    lambda _=False, c=r["category"], k=r["key"]: self._forget(c, k))
                line.addWidget(rm)

                holder = QWidget()
                holder.setLayout(line)
                ilay.addWidget(holder)

            ilay.addStretch()
            scroll.setWidget(inner)
            self._lay.addWidget(scroll)

        close = QPushButton("Cerrar")
        close.setFixedHeight(32)
        close.setFont(QFont(UI_FONT, 9))
        close.setCursor(Qt.CursorShape.PointingHandCursor)
        close.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {C.TEXT_MED};
                border: 1px solid {C.BORDER}; border-radius: 8px; }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
        """)
        close.clicked.connect(self.hide)
        self._lay.addWidget(close)

        self._settle(before)
        QTimer.singleShot(0, lambda g=before: self._settle(g))

    def _forget(self, category: str, key: str):
        from memory.memory_manager import forget
        forget(key, category)
        QTimer.singleShot(0, self._rebuild)


class BooksLibraryOverlay(_HudOverlay):
    """
    Biblioteca Cognitiva y Asimilación de Personalidad.
    Muestra los libros leídos, enseñanzas, citas y la personalidad activa (hábitos,
    emociones, estilo de vida) que Viernes ha adquirido de su lectura.
    Permite cargar nuevos libros/PDFs con un clic para aprender de ellos.
    """
    _OW = 640
    book_learned_sig = pyqtSignal(dict)
    error_sig = pyqtSignal(str)
    status_sig = pyqtSignal(str)

    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            BooksLibraryOverlay {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER_B};
                border-radius: 14px;
            }}
        """)
        self.setFixedWidth(self._OW)
        self._main_window = main_window
        self.book_learned_sig.connect(self._on_book_learned)
        self.error_sig.connect(self._on_error)
        self.status_sig.connect(self._on_status)

        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(20, 16, 20, 16)
        self._lay.setSpacing(8)
        self._rebuild()

    def _clear_layout(self):
        while self._lay.count():
            item = self._lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.hide()
                w.deleteLater()
                continue
            sub = item.layout()
            if sub is not None:
                while sub.count():
                    si = sub.takeAt(0)
                    sw = si.widget()
                    if sw is not None:
                        sw.hide()
                        sw.deleteLater()
                sub.deleteLater()

    def _settle(self, before):
        self._lay.invalidate()
        self._lay.activate()
        self.updateGeometry()
        self.adjustSize()
        p = self.parentWidget()
        if p is None:
            self.update()
            return
        self.move(max(0, (p.width() - self.width()) // 2),
                  max(0, (p.height() - self.height()) // 2))
        p.update(before.united(self.geometry()))
        self.update()

    def _rebuild(self):
        before = self.geometry()
        self._clear_layout()

        from memory.book_knowledge import load_library
        lib = load_library()
        books = list(lib.get("books", {}).values())
        persona = lib.get("active_persona", {})
        stats = lib.get("stats", {})

        total_books = len(books)
        total_pages = stats.get("total_pages_read", 0)
        habits_count = len(persona.get("lifestyle_habits", []))

        # ── Encabezado ──────────────────────────────────────────────────────────
        hdr_row = QHBoxLayout()
        hdr_box = QVBoxLayout()
        title_lbl = QLabel("Biblioteca cognitiva y lecturas")
        title_lbl.setFont(QFont(UI_FONT, 12, QFont.Weight.DemiBold))
        title_lbl.setStyleSheet(f"color: {C.WHITE}; background: transparent;")
        sub_lbl = QLabel("Libros estudiados, enseñanzas clave y rasgos asimilados")
        sub_lbl.setFont(QFont(UI_FONT, 9))
        sub_lbl.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent;")
        hdr_box.addWidget(title_lbl)
        hdr_box.addWidget(sub_lbl)
        hdr_row.addLayout(hdr_box)
        hdr_row.addStretch()

        x_btn = QPushButton("✕")
        x_btn.setFixedSize(26, 26)
        x_btn.setFont(QFont(UI_FONT, 10, QFont.Weight.DemiBold))
        x_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        x_btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {C.TEXT_MED}; border: 1px solid {C.BORDER}; border-radius: 6px; }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.PRI}; background: {C.PANEL2}; }}
        """)
        x_btn.clicked.connect(self.hide)
        hdr_row.addWidget(x_btn)
        self._lay.addLayout(hdr_row)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {C.BORDER}; margin: 2px 0;")
        self._lay.addWidget(sep)

        # ── Barra de Estadísticas y Acción de Aprendizaje ───────────────────────
        bar_row = QHBoxLayout()
        stats_lbl = QLabel(f"📖 {total_books} Libros  ·  📄 {total_pages} Páginas  ·  🏃 {habits_count} Hábitos")
        stats_lbl.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        stats_lbl.setStyleSheet(f"""
            QLabel {{
                color: {C.TEXT}; background: {C.DARK};
                border: 1px solid {C.BORDER}; border-radius: 6px; padding: 4px 10px;
            }}
        """)
        bar_row.addWidget(stats_lbl)
        bar_row.addStretch()

        self._learn_btn = QPushButton("➕  Leer y memorizar libro (PDF / Doc)")
        self._learn_btn.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        self._learn_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._learn_btn.setFixedHeight(30)
        self._learn_btn.setStyleSheet(f"""
            QPushButton {{
                background: {C.PRI}; color: {C.WHITE};
                border: none; border-radius: 8px; padding: 0 12px;
            }}
            QPushButton:hover {{ background: {C.PRI_DIM}; }}
        """)
        self._learn_btn.clicked.connect(self._pick_and_learn_book)
        bar_row.addWidget(self._learn_btn)
        self._lay.addLayout(bar_row)

        self._status_lbl = QLabel("")
        self._status_lbl.setFont(QFont(UI_FONT, 8))
        self._status_lbl.setStyleSheet(f"color: {C.ACC2}; background: transparent; padding: 2px 0;")
        self._status_lbl.setWordWrap(True)
        self._status_lbl.hide()
        self._lay.addWidget(self._status_lbl)

        # ── Área de Desplazamiento ─────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        max_h = 420
        if self.parentWidget():
            max_h = min(480, max(260, self.parentWidget().height() - 210))
        scroll.setFixedHeight(max_h)
        scroll.setStyleSheet(f"""
            QScrollArea {{ background: {C.DARK}; border: 1px solid {C.BORDER}; border-radius: 10px; }}
            QScrollBar:vertical {{ background: {C.DARK}; width: 6px; border-radius: 3px; margin: 2px; }}
            QScrollBar::handle:vertical {{ background: {C.BORDER_B}; border-radius: 3px; min-height: 24px; }}
            QScrollBar::handle:vertical:hover {{ background: {C.PRI}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        """)

        container = QWidget()
        container.setStyleSheet("background: transparent;")
        c_lay = QVBoxLayout(container)
        c_lay.setContentsMargins(10, 10, 10, 10)
        c_lay.setSpacing(12)

        # ── SECCIÓN 1: Personalidad, Estilo de Vida y Emociones Asimiladas ─────
        persona_box = QFrame()
        persona_box.setStyleSheet(f"""
            QFrame {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER};
                border-radius: 10px;
                padding: 8px;
            }}
        """)
        p_lay = QVBoxLayout(persona_box)
        p_lay.setSpacing(6)

        p_hdr = QLabel("Temperamento y síntesis cognitiva")
        p_hdr.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        p_hdr.setStyleSheet(f"color: {C.PRI}; border: none; background: transparent;")
        p_lay.addWidget(p_hdr)

        emo_txt = persona.get("emotional_profile") or "Equilibrada, reflexiva y analítica."
        emo_lbl = QLabel(f"<b>Perfil Emocional:</b> {emo_txt}")
        emo_lbl.setFont(QFont(UI_FONT, 8))
        emo_lbl.setWordWrap(True)
        emo_lbl.setStyleSheet(f"color: {C.TEXT}; border: none; background: transparent;")
        p_lay.addWidget(emo_lbl)

        style_txt = persona.get("conversational_style") or "Elocuente, empática y natural en español latino."
        style_lbl = QLabel(f"<b>Estilo Conversacional:</b> {style_txt}")
        style_lbl.setFont(QFont(UI_FONT, 8))
        style_lbl.setWordWrap(True)
        style_lbl.setStyleSheet(f"color: {C.TEXT_MED}; border: none; background: transparent;")
        p_lay.addWidget(style_lbl)

        habits = persona.get("lifestyle_habits", [])
        if habits:
            hab_hdr = QLabel("<b>Hábitos y Estilo de Vida Incorporados:</b>")
            hab_hdr.setFont(QFont(UI_FONT, 8))
            hab_hdr.setStyleSheet(f"color: {C.TEXT}; border: none; background: transparent; margin-top: 4px;")
            p_lay.addWidget(hab_hdr)

            chips_flow = QHBoxLayout()
            chips_flow.setSpacing(4)
            # Mostrar hasta 5 hábitos principales
            for h in habits[:6]:
                chip = QLabel(f"✓ {h}")
                chip.setFont(QFont(UI_FONT, 7))
                chip.setStyleSheet(f"""
                    QLabel {{
                        background: {C.PANEL2}; color: {C.TEXT_MED};
                        border: 1px solid {C.BORDER}; border-radius: 6px;
                        padding: 2px 6px;
                    }}
                """)
                chip.setWordWrap(True)
                chips_flow.addWidget(chip)
            chips_flow.addStretch()
            p_lay.addLayout(chips_flow)

        quotes = persona.get("favorite_quotes", [])
        if quotes:
            q_lbl = QLabel(f"<i>Sabiduría Guía: {quotes[0]}</i>")
            q_lbl.setFont(QFont(UI_FONT, 8))
            q_lbl.setWordWrap(True)
            q_lbl.setStyleSheet(f"color: {C.ACC2}; border: none; background: transparent; margin-top: 2px;")
            p_lay.addWidget(q_lbl)

        c_lay.addWidget(persona_box)

        # ── SECCIÓN 2: Libros Memorizados ───────────────────────────────────────
        b_hdr = QLabel(f"Colección de libros en memoria ({total_books})")
        b_hdr.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        b_hdr.setStyleSheet(f"color: {C.TEXT_MED}; background: transparent; margin-top: 4px;")
        c_lay.addWidget(b_hdr)

        if not books:
            empty_card = QFrame()
            empty_card.setStyleSheet(f"""
                QFrame {{
                    background: {C.PANEL}; border: 1px dashed {C.BORDER};
                    border-radius: 8px; padding: 16px;
                }}
            """)
            ec_lay = QVBoxLayout(empty_card)
            ec_msg = QLabel(
                "Aún no he leído ningún libro en mi memoria.<br><br>"
                "• Haz clic en <b>'➕ Leer y memorizar libro (PDF / Doc)'</b> arriba para seleccionar un PDF.<br>"
                "• O pídeme por voz o chat: <i>'Viernes, lee el libro que descargué'</i>.<br><br>"
                "¡Al estudiar libros, asimilaré sus ideas y adaptaré mi personalidad, hábitos y emociones!"
            )
            ec_msg.setFont(QFont(UI_FONT, 8))
            ec_msg.setStyleSheet(f"color: {C.TEXT_MED}; border: none; background: transparent;")
            ec_msg.setWordWrap(True)
            ec_lay.addWidget(ec_msg)
            c_lay.addWidget(empty_card)
        else:
            for b in books:
                card = QFrame()
                card.setStyleSheet(f"""
                    QFrame {{
                        background: {C.PANEL2};
                        border: 1px solid {C.BORDER};
                        border-radius: 8px;
                        padding: 10px;
                    }}
                """)
                card_lay = QVBoxLayout(card)
                card_lay.setSpacing(4)

                top_row = QHBoxLayout()
                b_title = QLabel(f"📘  {b.get('title')}")
                b_title.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
                b_title.setStyleSheet(f"color: {C.WHITE}; border: none; background: transparent;")
                top_row.addWidget(b_title)
                top_row.addStretch()

                genre_badge = QLabel(f"{b.get('genre', 'General')}")
                genre_badge.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
                genre_badge.setStyleSheet(f"""
                    background: {C.PRI_GHO}; color: {C.PRI};
                    border: 1px solid {C.PRI_DIM}; border-radius: 5px; padding: 1px 6px;
                """)
                top_row.addWidget(genre_badge)
                card_lay.addLayout(top_row)

                meta_lbl = QLabel(f"Autor: <b>{b.get('author')}</b>  ·  {b.get('pages_read', 1)} págs  ·  Leído el {b.get('learned_at', '')}")
                meta_lbl.setFont(QFont(UI_FONT, 7))
                meta_lbl.setStyleSheet(f"color: {C.TEXT_DIM}; border: none; background: transparent;")
                card_lay.addWidget(meta_lbl)

                summary = b.get("summary", "")
                if summary:
                    sum_lbl = QLabel(summary[:280] + ("..." if len(summary) > 280 else ""))
                    sum_lbl.setFont(QFont(UI_FONT, 8))
                    sum_lbl.setWordWrap(True)
                    sum_lbl.setStyleSheet(f"color: {C.TEXT}; border: none; background: transparent;")
                    card_lay.addWidget(sum_lbl)

                teachings = b.get("core_teachings", [])
                if teachings:
                    t_str = "<b>Enseñanza clave:</b> " + teachings[0]
                    if len(teachings) > 1:
                        t_str += f"<br><b>Principio adicional:</b> {teachings[1]}"
                    t_lbl = QLabel(t_str)
                    t_lbl.setFont(QFont(UI_FONT, 8))
                    t_lbl.setWordWrap(True)
                    t_lbl.setStyleSheet(f"color: {C.TEXT_MED}; border: none; background: transparent; margin-top: 3px;")
                    card_lay.addWidget(t_lbl)

                impact = b.get("personality_impact", {})
                emo_imp = impact.get("emotions", "")
                if emo_imp:
                    imp_lbl = QLabel(f"🎭 <i>Impacto emocional:</i> {emo_imp}")
                    imp_lbl.setFont(QFont(UI_FONT, 7))
                    imp_lbl.setWordWrap(True)
                    imp_lbl.setStyleSheet(f"color: {C.ACC2}; border: none; background: transparent;")
                    card_lay.addWidget(imp_lbl)

                bot_row = QHBoxLayout()
                bot_row.addStretch()
                del_btn = QPushButton("🗑  Olvidar libro")
                del_btn.setFont(QFont(UI_FONT, 8))
                del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                del_btn.setStyleSheet(f"""
                    QPushButton {{ background: transparent; color: {C.TEXT_DIM}; border: 1px solid {C.BORDER}; border-radius: 6px; padding: 2px 8px; }}
                    QPushButton:hover {{ color: {C.RED}; border-color: {C.RED}; }}
                """)
                b_id = b.get("id")
                del_btn.clicked.connect(lambda _, bid=b_id: self._forget_book(bid))
                bot_row.addWidget(del_btn)
                card_lay.addLayout(bot_row)

                c_lay.addWidget(card)

        scroll.setWidget(container)
        self._lay.addWidget(scroll)

        # ── Botón Inferior de Cerrar ───────────────────────────────────────────
        close_btn = QPushButton("Cerrar")
        close_btn.setFixedHeight(32)
        close_btn.setFont(QFont(UI_FONT, 9))
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {C.TEXT_MED}; border: 1px solid {C.BORDER}; border-radius: 8px; }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
        """)
        close_btn.clicked.connect(self.hide)
        self._lay.addWidget(close_btn)

        self._settle(before)
        QTimer.singleShot(0, lambda g=before: self._settle(g))

    def _pick_and_learn_book(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Libro o Documento PDF para que Viernes lo aprenda",
            "",
            "Libros y Documentos (*.pdf *.txt *.docx *.epub *.md);;Archivos PDF (*.pdf);;Todos los archivos (*.*)",
        )
        if not file_path:
            return

        p = Path(file_path)
        self._learn_btn.setEnabled(False)
        self._learn_btn.setText("⏳  Leyendo y asimilando...")
        self._status_lbl.setText(f"📖 Viernes está leyendo '{p.name}', analizando sus enseñanzas y asimilándolas...")
        self._status_lbl.show()

        if self._main_window and hasattr(self._main_window, "hud") and self._main_window.hud:
            try:
                self._main_window.hud.set_emotion("curious", intensity=0.9, duration=15.0)
                if hasattr(self._main_window.hud, "trigger_action"):
                    self._main_window.hud.trigger_action("HEAD_TILT_CURIOUS")
            except Exception:
                pass

        def _worker():
            try:
                from memory.book_knowledge import extract_text_from_file, synthesize_and_learn
                text, pages, fmt = extract_text_from_file(p)
                if len(text.strip()) < 120:
                    self.error_sig.emit(f"El archivo '{p.name}' no contiene texto legible (posible PDF escaneado sólo con imágenes).")
                    return
                book_data = synthesize_and_learn(text, p.name, pages)
                self.book_learned_sig.emit(book_data)
            except Exception as e:
                self.error_sig.emit(str(e))

        threading.Thread(target=_worker, daemon=True, name="BookLearnerWorker").start()

    def _on_status(self, msg: str):
        self._status_lbl.setText(msg)
        self._status_lbl.show()

    def _on_book_learned(self, book_data: dict):
        self._learn_btn.setEnabled(True)
        self._learn_btn.setText("➕  Leer y memorizar libro (PDF / Doc)")
        title = book_data.get("title", "Libro")
        author = book_data.get("author", "")
        self._status_lbl.setText(f"✨ ¡'{title}' asimilado con éxito! Tu personalidad y estilo de vida han evolucionado.")
        self._status_lbl.show()

        if self._main_window:
            if hasattr(self._main_window, "_log"):
                self._main_window._log.append_log(f"📚 [Libro Memorizado] '{title}' ({author}). Hábitos y emociones actualizados.")
            if hasattr(self._main_window, "hud") and self._main_window.hud:
                try:
                    self._main_window.hud.set_emotion("happy", intensity=1.0, duration=5.0)
                    if hasattr(self._main_window.hud, "trigger_action"):
                        self._main_window.hud.trigger_action("ELEGANT_BOW")
                except Exception:
                    pass
            if hasattr(self._main_window, "show_visual_card"):
                try:
                    teachings = book_data.get("core_teachings", [])
                    card = {
                        "type": "book",
                        "title": title,
                        "artist": f"Autor: {author}",
                        "platform": "Biblioteca Cognitiva",
                        "tag": "LIBRO MEMORIZADO",
                        "preview": teachings[0] if teachings else "Asimilado con éxito en la memoria.",
                        "details": f"{book_data.get('pages_read', 1)} páginas analizadas y asimiladas a mi personalidad.",
                    }
                    self._main_window.show_visual_card(card)
                except Exception:
                    pass

        QTimer.singleShot(400, self._rebuild)

    def _on_error(self, err_msg: str):
        self._learn_btn.setEnabled(True)
        self._learn_btn.setText("➕  Leer y memorizar libro (PDF / Doc)")
        self._status_lbl.setText(f"⚠️ Error al aprender del libro: {err_msg}")
        self._status_lbl.show()

    def _forget_book(self, book_id: str):
        from memory.book_knowledge import delete_book
        delete_book(book_id)
        if self._main_window and hasattr(self._main_window, "_log"):
            self._main_window._log.append_log("SYS: Libro eliminado de la biblioteca cognitiva.")
        QTimer.singleShot(0, self._rebuild)


class ClipboardPanel(QWidget):

    """Floating panel shown when text is copied — offers quick Viernes actions."""

    action_requested = pyqtSignal(str)
    _W, _H = 340, 114

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            ClipboardPanel {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER_B};
                border-radius: 10px;
            }}
        """)
        self.setFixedWidth(self._W)
        self._clip_text = ""

        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 8, 10, 8)
        lay.setSpacing(5)

        hdr = QHBoxLayout(); hdr.setSpacing(4)
        icon_lbl = QLabel("Portapapeles detectado")
        icon_lbl.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        icon_lbl.setStyleSheet(f"color: {C.PRI}; background: transparent;")
        hdr.addWidget(icon_lbl); hdr.addStretch()
        x_btn = QPushButton("✕")
        x_btn.setFixedSize(18, 18)
        x_btn.setFont(QFont(UI_FONT, 8))
        x_btn.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent; border: none;")
        x_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        x_btn.clicked.connect(self.hide)
        hdr.addWidget(x_btn)
        lay.addLayout(hdr)

        self._preview = QLabel()
        self._preview.setFont(QFont(UI_FONT, 8))
        self._preview.setStyleSheet(f"""
            color: {C.TEXT}; background: {C.DARK};
            border: 1px solid {C.BORDER}; border-radius: 6px; padding: 4px 8px;
        """)
        self._preview.setWordWrap(False)
        self._preview.setFixedHeight(28)
        lay.addWidget(self._preview)

        btn_row = QHBoxLayout(); btn_row.setSpacing(5)
        _bs = (f"QPushButton {{ background: {C.PANEL2}; color: {C.TEXT_MED}; "
               f"border: 1px solid {C.BORDER}; border-radius: 6px; }}"
               f"QPushButton:hover {{ color: {C.WHITE}; border-color: {C.PRI}; }}")
        for label, cmd_fmt in [
            ("Traducir",  "Traduce este texto: {text}"),
            ("Resumir",   "Resume este texto: {text}"),
            ("Explicar",  "Explica esto: {text}"),
            ("Corregir",  "Corrige la ortografía y redacción de este texto: {text}"),
        ]:
            b = QPushButton(label)
            b.setFixedHeight(24)
            b.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setStyleSheet(_bs)
            b.clicked.connect(lambda _, c=cmd_fmt: self._trigger(c))
            btn_row.addWidget(b)
        lay.addLayout(btn_row)

        self._dismiss_timer = QTimer(self)
        self._dismiss_timer.setSingleShot(True)
        self._dismiss_timer.timeout.connect(self.hide)
        self.hide()

    def _trigger(self, cmd_fmt: str):
        if self._clip_text:
            self.action_requested.emit(cmd_fmt.format(text=self._clip_text[:800]))
        self.hide()

    def show_clipboard(self, text: str):
        self._clip_text = text
        preview = text[:58].replace('\n', ' ')
        if len(text) > 58:
            preview += "…"
        self._preview.setText(f'"{preview}"')
        self.show(); self.raise_()
        self._dismiss_timer.start(8000)


PLUGIN_CATEGORIES = {
    # SISTEMA & HARDWARE
    "battery_advisor": "SISTEMA",
    "hardware_temperature_alert": "SISTEMA",
    "system_cleaner": "SISTEMA",
    "shutdown_timer": "SISTEMA",
    "gaming_mode": "SISTEMA",
    "window_layout_manager": "SISTEMA",
    "privacy_lock": "SISTEMA",
    "webcam_sentinel": "SISTEMA",
    "screen_color_night_light": "SISTEMA",
    "peripheral_battery_sentinel": "SISTEMA",
    "bluetooth_auto_mesh": "SISTEMA",

    # PRODUCTIVIDAD & TRABAJO
    "pomodoro_timer": "PRODUCTIVIDAD",
    "clipboard_history_vault": "PRODUCTIVIDAD",
    "clipboard_translator": "PRODUCTIVIDAD",
    "pdf_summary_extractor": "PRODUCTIVIDAD",
    "quick_regex_tester": "PRODUCTIVIDAD",
    "downloads_organizer": "PRODUCTIVIDAD",
    "duplicate_file_finder": "PRODUCTIVIDAD",
    "voice_journal": "PRODUCTIVIDAD",
    "unit_converter": "PRODUCTIVIDAD",
    "error_explainer": "PRODUCTIVIDAD",
    "git_assistant": "PRODUCTIVIDAD",

    # RED & SEGURIDAD
    "speedtest_pro": "RED & SEG",
    "network_diagnostic": "RED & SEG",
    "temp_mail_burner": "RED & SEG",
    "url_unmasker": "RED & SEG",
    "github_trending_radar": "RED & SEG",
    "qr_generator_reader": "RED & SEG",
    "password_vault_generator": "RED & SEG",
    "virustotal_file_scanner": "RED & SEG",
    "local_network_auditor": "RED & SEG",
    "whois_domain_dns_lookup": "RED & SEG",

    # MULTIMEDIA, AUDIO & BIENESTAR
    "spotify_smart_controller": "MULTIMEDIA",
    "ambient_sound": "MULTIMEDIA",
    "image_optimizer": "MULTIMEDIA",
    "steam_deal_hunter": "MULTIMEDIA",
    "crypto_stock_tracker": "MULTIMEDIA",
    "breathing_coach": "MULTIMEDIA",
    "wellness_reminder": "MULTIMEDIA",
    "game_decider": "MULTIMEDIA",
    "rembg_background_remover": "MULTIMEDIA",
}

def get_plugin_category(name: str) -> str:
    return PLUGIN_CATEGORIES.get(name, "GENERAL")


class PluginSettingsOverlay(QWidget):
    """Floating overlay — Master-Detail Two-Column Plugin Manager & Config Hub.

    Organized, clean, and spacious layout:
    - Left Column: Search box, Category filter tabs, and compact selectable plugin list.
    - Right Column: Dedicated inspector for the selected plugin with description, live testing console, and parameters.
    """

    _test_done = pyqtSignal(str, bool, str)
    _run_done  = pyqtSignal(str, str)
    closed     = pyqtSignal()
    _OW = 860

    def __init__(self, sections: list[dict], plugins: list[dict] = None, parent=None, runner=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            PluginSettingsOverlay {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER_B};
                border-radius: 14px;
            }}
        """)
        self._sections = sections or []
        self._plugins = sorted(plugins or [], key=lambda p: p.get("name", "").lower())
        self._runner = runner
        self._selected_plugin_name: str | None = None
        self._active_category = "TODOS"

        self._widgets: dict[tuple, object] = {}
        self._types:   dict[tuple, str]    = {}
        self._list_item_widgets: dict[str, QFrame] = {}
        self._test_output_text:  dict[str, str]    = {}
        self._status_labels:     dict[str, QLabel] = {}

        self._test_done.connect(self._on_test_done)
        self._run_done.connect(self._on_run_done)

        self._fs = (f"QLineEdit {{ background: {C.DARK}; color: {C.TEXT}; "
                    f"border: 1px solid {C.BORDER}; border-radius: 8px; padding: 4px 10px; }}"
                    f"QLineEdit:focus {{ border: 1px solid {C.PRI}; }}")

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 16, 18, 16)
        root.setSpacing(10)

        # ── TOP BAR: Header + Category Filters ───────────────────────────────
        top_row = QHBoxLayout(); top_row.setSpacing(10)
        title_box = QVBoxLayout(); title_box.setSpacing(2)
        hdr_lbl = QLabel("Extensiones y módulos")
        hdr_lbl.setFont(QFont(UI_FONT, 12, QFont.Weight.DemiBold))
        hdr_lbl.setStyleSheet(f"color: {C.WHITE}; background: transparent;")
        title_box.addWidget(hdr_lbl)

        total_p = len(self._plugins)
        act_p = sum(1 for p in self._plugins if p.get("enabled", False))
        sub_lbl = QLabel(f"{total_p} módulos instalados  ·  {act_p} activos")
        sub_lbl.setFont(QFont(UI_FONT, 8))
        sub_lbl.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent;")
        title_box.addWidget(sub_lbl)
        top_row.addLayout(title_box)
        top_row.addStretch(1)

        # Category Filter Tabs
        self._cat_btns: dict[str, QPushButton] = {}
        categories = ["TODOS", "SISTEMA", "PRODUCTIVIDAD", "RED & SEG", "MULTIMEDIA"]
        cat_row = QHBoxLayout(); cat_row.setSpacing(4)
        for cat in categories:
            b = QPushButton(cat.capitalize())
            b.setCheckable(True)
            b.setFixedHeight(26)
            b.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _, c=cat: self._set_category(c))
            self._cat_btns[cat] = b
            cat_row.addWidget(b)
        top_row.addLayout(cat_row)
        root.addLayout(top_row)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {C.BORDER}; margin: 2px 0;")
        root.addWidget(sep)

        # ── BODY: Master-Detail Two Column Split ─────────────────────────────
        body = QHBoxLayout(); body.setSpacing(12)

        # --- LEFT PANE (Compact, Clean List) ---
        left_pane = QWidget(); left_pane.setFixedWidth(310)
        left_pane.setStyleSheet("background: transparent;")
        l_lay = QVBoxLayout(left_pane)
        l_lay.setContentsMargins(0, 0, 0, 0)
        l_lay.setSpacing(6)

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("Filtrar extensiones…")
        self._search_input.setFont(QFont(UI_FONT, 9))
        self._search_input.setFixedHeight(28)
        self._search_input.setStyleSheet(self._fs)
        self._search_input.textChanged.connect(self._filter_list)
        l_lay.addWidget(self._search_input)

        scroll_left = QScrollArea()
        scroll_left.setWidgetResizable(True)
        scroll_left.setFrameShape(QFrame.Shape.NoFrame)
        scroll_left.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_left.setStyleSheet(f"""
            QScrollArea {{ background: {C.DARK}; border: 1px solid {C.BORDER}; border-radius: 8px; }}
            QScrollBar:vertical {{ background: {C.DARK}; width: 5px; margin: 0; }}
            QScrollBar::handle:vertical {{ background: {C.BORDER_B}; border-radius: 3px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        """)

        left_inner = QWidget(); left_inner.setStyleSheet("background: transparent;")
        self._list_layout = QVBoxLayout(left_inner)
        self._list_layout.setContentsMargins(6, 6, 6, 6)
        self._list_layout.setSpacing(4)

        for p in self._plugins:
            row_w = self._build_list_row(p)
            self._list_item_widgets[p["name"]] = row_w
            self._list_layout.addWidget(row_w)

        self._list_layout.addStretch(1)
        scroll_left.setWidget(left_inner)
        l_lay.addWidget(scroll_left, stretch=1)
        body.addWidget(left_pane)

        # --- RIGHT PANE (Plugin Detail & Inspector) ---
        self._right_pane = QWidget()
        self._right_pane.setObjectName("RightPane")
        self._right_pane.setStyleSheet(f"""
            QWidget#RightPane {{
                background: {C.DARK};
                border: 1px solid {C.BORDER};
                border-radius: 10px;
            }}
        """)
        self._r_lay = QVBoxLayout(self._right_pane)
        self._r_lay.setContentsMargins(16, 14, 16, 14)
        self._r_lay.setSpacing(8)

        body.addWidget(self._right_pane, stretch=1)
        root.addLayout(body, stretch=1)

        # ── BOTTOM BAR ───────────────────────────────────────────────────────
        bot_row = QHBoxLayout(); bot_row.setSpacing(8)
        open_folder_btn = QPushButton("Abrir carpeta de plugins")
        open_folder_btn.setFixedHeight(30)
        open_folder_btn.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        open_folder_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_folder_btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {C.TEXT_MED}; border: 1px solid {C.BORDER}; border-radius: 8px; padding: 0 12px; }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
        """)
        open_folder_btn.clicked.connect(self._open_plugins_folder)
        bot_row.addWidget(open_folder_btn)

        bot_row.addStretch(1)

        self._save_feedback = QLabel("")
        self._save_feedback.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        self._save_feedback.setStyleSheet(f"color: {C.GREEN}; background: transparent;")
        bot_row.addWidget(self._save_feedback)

        save_btn = QPushButton("Guardar ajustes")
        save_btn.setFixedHeight(32)
        save_btn.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet(f"""
            QPushButton {{ background: {C.PRI}; color: {C.WHITE}; border: none; border-radius: 8px; padding: 0 16px; }}
            QPushButton:hover {{ background: {C.PRI_DIM}; }}
        """)
        save_btn.clicked.connect(self._save_all)
        bot_row.addWidget(save_btn)

        close_btn = QPushButton("Cerrar")
        close_btn.setFixedHeight(32)
        close_btn.setFixedWidth(80)
        close_btn.setFont(QFont(UI_FONT, 9))
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {C.TEXT_MED}; border: 1px solid {C.BORDER}; border-radius: 8px; }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
        """)
        close_btn.clicked.connect(self.hide)
        bot_row.addWidget(close_btn)
        root.addLayout(bot_row)

        self._update_cat_buttons()

        if self._plugins:
            self._select_plugin(self._plugins[0]["name"])

    def _open_plugins_folder(self):
        try:
            folder = Path(__file__).resolve().parent / "plugins"
            if folder.exists():
                os.startfile(str(folder))
        except Exception:
            pass

    def _set_category(self, cat: str):
        self._active_category = cat
        self._update_cat_buttons()
        self._filter_list()

    def _update_cat_buttons(self):
        for c, btn in self._cat_btns.items():
            active = (c == self._active_category)
            btn.setChecked(active)
            if active:
                btn.setStyleSheet(f"QPushButton {{ background: {C.PRI_GHO}; color: {C.PRI}; border: 1px solid {C.PRI}; border-radius: 7px; padding: 0 10px; }}")
            else:
                btn.setStyleSheet(f"QPushButton {{ background: transparent; color: {C.TEXT_DIM}; border: 1px solid {C.BORDER}; border-radius: 7px; padding: 0 10px; }}")

    def _build_list_row(self, p: dict) -> QFrame:
        row = QFrame()
        row.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        name = p.get("name", "plugin")
        enabled = p.get("enabled", True)
        cat = get_plugin_category(name)

        row.setFixedHeight(34)
        row.setCursor(Qt.CursorShape.PointingHandCursor)
        self._style_row(row, is_selected=False)

        lay = QHBoxLayout(row)
        lay.setContentsMargins(8, 2, 8, 2)
        lay.setSpacing(6)

        dot = QLabel("●")
        dot.setFont(QFont(UI_FONT, 8))
        dot.setStyleSheet(f"color: {C.GREEN if enabled else C.TEXT_DIM}; background: transparent;")
        lay.addWidget(dot)

        lbl = QLabel(name)
        lbl.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        lbl.setStyleSheet(f"color: {C.TEXT}; background: transparent;")
        lbl.setToolTip(f"{name} [{cat}]")
        lay.addWidget(lbl, stretch=1)

        tog = QPushButton("ON" if enabled else "OFF")
        tog.setFixedSize(38, 20)
        tog.setFont(QFont(UI_FONT, 7, QFont.Weight.DemiBold))
        tog.setCursor(Qt.CursorShape.PointingHandCursor)
        self._style_mini_toggle(tog, enabled)
        tog.clicked.connect(lambda _, n=name, b=tog, d=dot: self._toggle_plugin_state(n, b, d))
        lay.addWidget(tog)

        row.mousePressEvent = lambda e, n=name: self._select_plugin(n)
        return row

    def _style_row(self, row: QFrame, is_selected: bool):
        if is_selected:
            row.setStyleSheet(f"""
                QFrame {{
                    background: {C.PRI_GHO};
                    border: 1px solid {C.PRI};
                    border-radius: 6px;
                }}
            """)
        else:
            row.setStyleSheet(f"""
                QFrame {{
                    background: {C.PANEL};
                    border: 1px solid {C.BORDER};
                    border-radius: 6px;
                }}
                QFrame:hover {{
                    border: 1px solid {C.BORDER_B};
                }}
            """)

    def _style_mini_toggle(self, btn: QPushButton, enabled: bool):
        if enabled:
            btn.setText("ON")
            btn.setStyleSheet(f"QPushButton {{ background: {_rgba(C.GREEN, 0.14)}; color: {C.GREEN}; border: 1px solid {_rgba(C.GREEN, 0.4)}; border-radius: 5px; }}")
        else:
            btn.setText("OFF")
            btn.setStyleSheet(f"QPushButton {{ background: transparent; color: {C.TEXT_DIM}; border: 1px solid {C.BORDER}; border-radius: 5px; }}")

    def _toggle_plugin_state(self, name: str, btn: QPushButton, dot: QLabel):
        from memory.config_manager import get_plugin_enabled, save_plugin_enabled
        new_val = not get_plugin_enabled(name)
        save_plugin_enabled(name, new_val)
        self._style_mini_toggle(btn, new_val)
        dot.setStyleSheet(f"color: {C.GREEN if new_val else C.TEXT_DIM}; background: transparent;")
        for p in self._plugins:
            if p["name"] == name:
                p["enabled"] = new_val
                break
        if self._selected_plugin_name == name:
            self._render_detail_pane(name)

    def _filter_list(self):
        q = self._search_input.text().strip().lower()
        first_visible = None
        for p in self._plugins:
            name = p.get("name", "")
            desc = p.get("description", "")
            cat = get_plugin_category(name)
            card = self._list_item_widgets.get(name)

            cat_match = (self._active_category == "TODOS") or (cat == self._active_category)
            search_match = (not q) or (q in name.lower()) or (q in desc.lower())
            visible = cat_match and search_match

            if card:
                card.setVisible(visible)
            if visible and first_visible is None:
                first_visible = name

        cur_row = self._list_item_widgets.get(self._selected_plugin_name or "")
        if cur_row and not cur_row.isVisible() and first_visible:
            self._select_plugin(first_visible)

    def _select_plugin(self, name: str):
        self._selected_plugin_name = name
        for n, row in self._list_item_widgets.items():
            self._style_row(row, is_selected=(n == name))
        self._render_detail_pane(name)

    def _render_detail_pane(self, name: str):
        while self._r_lay.count():
            item = self._r_lay.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
            l = item.layout()
            if l:
                while l.count():
                    li = l.takeAt(0)
                    if li.widget():
                        li.widget().deleteLater()

        p = next((x for x in self._plugins if x["name"] == name), None)
        if not p:
            empty = QLabel("Selecciona un módulo de la lista izquierda para ver sus detalles.")
            empty.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent;")
            self._r_lay.addWidget(empty)
            return

        enabled = p.get("enabled", True)
        valid = p.get("valid", True)
        desc = p.get("description", "Sin descripción.")
        fpath = p.get("file", f"{name}.py")
        cat = get_plugin_category(name)

        # ── Header of Selected Plugin ─────────────────────────────────────────
        hdr_row = QHBoxLayout(); hdr_row.setSpacing(8)
        t_lbl = QLabel(name)
        t_lbl.setFont(QFont(UI_FONT, 12, QFont.Weight.DemiBold))
        t_lbl.setStyleSheet(f"color: {C.WHITE}; background: transparent;")
        hdr_row.addWidget(t_lbl, stretch=1)

        cat_badge = QLabel(f"  {cat}  ")
        cat_badge.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        cat_badge.setStyleSheet(f"background: {C.PRI_GHO}; color: {C.PRI}; border: 1px solid {C.PRI_DIM}; border-radius: 6px;")
        hdr_row.addWidget(cat_badge)

        open_file_btn = QPushButton("Abrir archivo")
        open_file_btn.setFixedHeight(24)
        open_file_btn.setFont(QFont(UI_FONT, 8))
        open_file_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_file_btn.setStyleSheet(f"""
            QPushButton {{ background: transparent; color: {C.TEXT_MED}; border: 1px solid {C.BORDER}; border-radius: 6px; padding: 0 8px; }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
        """)
        open_file_btn.clicked.connect(lambda _, fp=fpath: self._open_plugin_file(fp))
        hdr_row.addWidget(open_file_btn)
        self._r_lay.addLayout(hdr_row)

        sub_info = QLabel(f"Ruta: plugins/{fpath}  ·  Estado: {'Activo' if enabled else 'Inactivo'}")
        sub_info.setFont(QFont(UI_FONT, 8))
        sub_info.setStyleSheet(f"color: {C.GREEN if enabled else C.TEXT_DIM}; background: transparent;")
        self._r_lay.addWidget(sub_info)

        line = QFrame(); line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"color: {C.BORDER}; margin: 2px 0;")
        self._r_lay.addWidget(line)

        # ── Scroll Area for Plugin Details, Settings & Testing ────────────────
        det_scroll = QScrollArea()
        det_scroll.setWidgetResizable(True)
        det_scroll.setFrameShape(QFrame.Shape.NoFrame)
        det_scroll.setStyleSheet(f"""
            QScrollArea {{ background: transparent; border: none; }}
            QScrollBar:vertical {{ background: {C.DARK}; width: 5px; margin: 0; }}
            QScrollBar::handle:vertical {{ background: {C.BORDER_B}; border-radius: 3px; }}
        """)

        inner = QWidget(); inner.setStyleSheet("background: transparent;")
        in_lay = QVBoxLayout(inner)
        in_lay.setContentsMargins(0, 0, 4, 0)
        in_lay.setSpacing(8)

        # Description Box
        desc_box = QFrame()
        desc_box.setStyleSheet(f"background: {C.PANEL}; border: 1px solid {C.BORDER}; border-radius: 8px;")
        d_lay = QVBoxLayout(desc_box)
        d_lay.setContentsMargins(12, 10, 12, 10)
        d_title = QLabel("Descripción y uso")
        d_title.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        d_title.setStyleSheet(f"color: {C.TEXT}; background: transparent; border: none;")
        d_lay.addWidget(d_title)
        d_txt = QLabel(desc)
        d_txt.setFont(QFont(UI_FONT, 9))
        d_txt.setWordWrap(True)
        d_txt.setStyleSheet(f"color: {C.TEXT_MED}; background: transparent; border: none;")
        d_lay.addWidget(d_txt)
        in_lay.addWidget(desc_box)

        # Execution & Test Console
        test_box = QFrame()
        test_box.setStyleSheet(f"background: {C.PANEL}; border: 1px solid {C.BORDER}; border-radius: 8px;")
        t_lay = QVBoxLayout(test_box)
        t_lay.setContentsMargins(12, 10, 12, 10)
        t_lay.setSpacing(6)

        t_row = QHBoxLayout()
        t_title = QLabel("Ejecución directa")
        t_title.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        t_title.setStyleSheet(f"color: {C.TEXT}; background: transparent; border: none;")
        t_row.addWidget(t_title, stretch=1)

        run_btn = QPushButton("Probar módulo")
        run_btn.setFixedHeight(26)
        run_btn.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        run_btn.setStyleSheet(f"""
            QPushButton {{ background: {C.PANEL2}; color: {C.PRI}; border: 1px solid {C.BORDER_B}; border-radius: 6px; padding: 0 10px; }}
            QPushButton:hover {{ background: {C.PRI_GHO}; border-color: {C.PRI}; }}
        """)
        run_btn.clicked.connect(lambda _, n=name: self._test_plugin(n))
        t_row.addWidget(run_btn)
        t_lay.addLayout(t_row)

        out_lbl = QLabel(self._test_output_text.get(name, "Haz clic en 'Probar módulo' para ejecutarlo en vivo."))
        out_lbl.setFont(QFont(UI_FONT, 8))
        out_lbl.setWordWrap(True)
        out_lbl.setStyleSheet(f"color: {C.PRI if name in self._test_output_text else C.TEXT_DIM}; background: transparent; border: none;")
        t_lay.addWidget(out_lbl)
        self._status_labels[name] = out_lbl
        in_lay.addWidget(test_box)

        # Embedded Configuration form if fields exist
        sec = next((s for s in self._sections if (s.get("plugin") == name or s.get("namespace") == name)), None)
        if sec and sec.get("fields"):
            cfg_box = QFrame()
            cfg_box.setStyleSheet(f"background: {C.PANEL}; border: 1px solid {C.BORDER}; border-radius: 8px;")
            c_lay = QVBoxLayout(cfg_box)
            c_lay.setContentsMargins(12, 10, 12, 10)
            c_lay.setSpacing(6)

            c_title = QLabel("Parámetros del módulo")
            c_title.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
            c_title.setStyleSheet(f"color: {C.TEXT}; background: transparent; border: none;")
            c_lay.addWidget(c_title)

            ns = sec.get("namespace") or name
            fields = sec.get("fields", [])
            values = sec.get("values", {})

            for field in fields:
                if not isinstance(field, dict) or not field.get("key"):
                    continue
                k = field["key"]
                ftype = (field.get("type") or "text").lower()
                flabel = field.get("label") or k
                fdef = field.get("default")
                stored = values.get(k, fdef)

                frow = QHBoxLayout(); frow.setSpacing(8)
                lbl = QLabel(flabel)
                lbl.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
                lbl.setStyleSheet(f"color: {C.TEXT_MED}; background: transparent; border: none;")
                frow.addWidget(lbl, stretch=1)

                if ftype == "choice":
                    cw = QComboBox()
                    cw.addItems([str(o) for o in field.get("options", [])])
                    cw.setFont(QFont(UI_FONT, 8))
                    cw.setFixedHeight(26)
                    cw.setStyleSheet(f"QComboBox {{ background: {C.DARK}; color: {C.TEXT}; border: 1px solid {C.BORDER}; border-radius: 6px; padding: 0 6px; }}")
                    if stored is not None:
                        cw.setCurrentText(str(stored))
                    inp_w = cw
                elif ftype == "toggle":
                    tw = QPushButton()
                    tw.setCheckable(True)
                    tw.setChecked(bool(stored))
                    tw.setFixedSize(50, 22)
                    tw.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
                    self._style_mini_toggle(tw, bool(stored))
                    tw.toggled.connect(lambda on, b=tw: self._style_mini_toggle(b, on))
                    inp_w = tw
                else:
                    lw = QLineEdit("" if stored is None else str(stored))
                    lw.setFont(QFont(UI_FONT, 8))
                    lw.setFixedHeight(26)
                    lw.setStyleSheet(self._fs)
                    if field.get("placeholder"):
                        lw.setPlaceholderText(str(field["placeholder"]))
                    inp_w = lw

                self._widgets[(ns, k)] = inp_w
                self._types[(ns, k)] = ftype
                frow.addWidget(inp_w)
                c_lay.addLayout(frow)

            in_lay.addWidget(cfg_box)
        else:
            no_cfg = QLabel("✓ Este módulo funciona automáticamente por comandos de voz sin parámetros adicionales.")
            no_cfg.setFont(QFont(UI_FONT, 8))
            no_cfg.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent; padding: 4px;")
            in_lay.addWidget(no_cfg)

        in_lay.addStretch(1)
        det_scroll.setWidget(inner)
        self._r_lay.addWidget(det_scroll, stretch=1)

    def _has_settings(self, name: str) -> bool:
        return any((s.get("plugin") == name or s.get("namespace") == name) for s in self._sections)

    def _open_plugin_file(self, fpath: str):
        try:
            folder = Path(__file__).resolve().parent / "plugins"
            file_p = folder / fpath
            if file_p.exists():
                os.startfile(str(file_p))
        except Exception:
            pass

    def _test_plugin(self, name: str):
        lbl = self._status_labels.get(name)
        if lbl:
            lbl.setText(f"⏳ Ejecutando '{name}'...")

        def worker():
            res_str = ""
            try:
                if callable(self._runner):
                    res_str = str(self._runner(name, {}) or "Completado.")
                else:
                    import importlib
                    mod = importlib.import_module(f"plugins.{name}")
                    if hasattr(mod, "run"):
                        res_str = str(mod.run({}) or "Completado.")
            except Exception as e:
                res_str = f"Error: {e}"
            self._run_done.emit(name, res_str)

        threading.Thread(target=worker, daemon=True).start()

    def _on_run_done(self, name: str, text: str):
        clean = " ".join(text.split()[:40])
        self._test_output_text[name] = f"✓ Resultado: {clean}"
        lbl = self._status_labels.get(name)
        if lbl:
            lbl.setText(self._test_output_text[name])
            lbl.setStyleSheet(f"color: {C.PRI}; background: transparent;")

    def _gather(self, ns: str) -> dict:
        out = {}
        for (n, key), w in self._widgets.items():
            if n != ns:
                continue
            t = self._types.get((n, key), "text")
            if t == "choice":
                out[key] = w.currentText()
            elif t == "toggle":
                out[key] = w.isChecked()
            else:
                out[key] = w.text().strip()
        return out

    def _save_ns(self, ns: str):
        from memory.config_manager import save_plugin_config
        save_plugin_config(ns, self._gather(ns))

    def _save_all(self):
        saved_any = False
        for sec in self._sections:
            ns = sec.get("namespace") or sec.get("plugin")
            if ns:
                self._save_ns(ns)
                saved_any = True
        self._save_feedback.setText("Ajustes guardados ✓" if saved_any else "Guardado ✓")
        QTimer.singleShot(2500, lambda: self._save_feedback.setText(""))

    def _on_test_done(self, ns: str, ok: bool, msg: str):
        lbl = self._status_labels.get(ns)
        if lbl:
            lbl.setText(msg)
            color = C.PRI if ok else C.RED
            lbl.setStyleSheet(f"color: {color}; background: transparent;")

    def hideEvent(self, e):
        super().hideEvent(e)
        self.closed.emit()

    def closeEvent(self, e):
        super().closeEvent(e)
        self.closed.emit()


class RemoteKeyOverlay(_HudOverlay):
    """Floating overlay — QR code for instant phone pairing + manual key fallback."""

    closed = pyqtSignal()

    _OW, _OH = 420, 500

    def __init__(self, url: str, key: str, auto_login_url: str = "",
                 manual_url: str = "", expiry_secs: int = 600, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            RemoteKeyOverlay {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER_B};
                border-radius: 14px;
            }}
        """)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(32)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 6)
        self.setGraphicsEffect(shadow)

        self._expiry          = time.time() + expiry_secs
        self._on_new_key      = None
        self._auto_login_url  = auto_login_url
        self._manual_url      = manual_url or url

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 18, 24, 18)
        lay.setSpacing(6)

        def _lbl(txt, fs=9, bold=False, color=C.WHITE,
                 align=Qt.AlignmentFlag.AlignCenter):
            w = QLabel(txt)
            w.setAlignment(align)
            w.setFont(QFont(UI_FONT, int(round(fs)),
                            QFont.Weight.DemiBold if bold else QFont.Weight.Normal))
            w.setStyleSheet(f"color: {color}; background: transparent;")
            w.setWordWrap(True)
            return w

        lay.addWidget(_lbl("Control remoto móvil", 12, True))
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {C.BORDER}; margin: 1px 0;")
        lay.addWidget(sep)

        # ── QR code ───────────────────────────────────────────────────────────
        self._qr_label = QLabel()
        self._qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._qr_label.setFixedSize(176, 176)
        self._qr_label.setStyleSheet(
            "background: white; border-radius: 10px; padding: 4px;"
        )
        qr_row = QHBoxLayout()
        qr_row.addStretch()
        qr_row.addWidget(self._qr_label)
        qr_row.addStretch()
        lay.addLayout(qr_row)

        self._update_qr(auto_login_url)

        lay.addWidget(_lbl("Escanea con tu móvil para vincular al instante", 8, color=C.TEXT_DIM))

        sep2 = QFrame(); sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet(f"color: {C.BORDER}; margin: 1px 0;")
        lay.addWidget(sep2)

        lay.addWidget(_lbl("O ingresa manualmente desde el navegador:", 8, color=C.TEXT_DIM,
                           align=Qt.AlignmentFlag.AlignLeft))

        self._url_lbl = QLabel(self._manual_url)
        self._url_lbl.setFont(QFont(UI_FONT, 9))
        self._url_lbl.setStyleSheet(f"color: {C.PRI}; background: transparent;")
        self._url_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._url_lbl.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse)
        lay.addWidget(self._url_lbl)

        self._key_lbl = QLabel(key)
        self._key_lbl.setFont(QFont(UI_FONT, 24, QFont.Weight.Bold))
        self._key_lbl.setStyleSheet(f"""
            color: {C.WHITE};
            background: {C.DARK};
            border: 1px solid {C.BORDER_B};
            border-radius: 8px;
            padding: 6px 4px;
            letter-spacing: 10px;
        """)
        self._key_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self._key_lbl)

        self._timer_lbl = QLabel()
        self._timer_lbl.setFont(QFont(UI_FONT, 8))
        self._timer_lbl.setStyleSheet(f"color: {C.TEXT_MED}; background: transparent;")
        self._timer_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self._timer_lbl)

        btn_row = QHBoxLayout(); btn_row.setSpacing(8)
        new_btn = QPushButton("Generar nueva clave")
        new_btn.setFixedHeight(34)
        new_btn.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        new_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        new_btn.setStyleSheet(f"""
            QPushButton {{
                background: {C.PRI}; color: {C.WHITE};
                border: none; border-radius: 8px;
            }}
            QPushButton:hover {{ background: {C.PRI_DIM}; }}
        """)
        new_btn.clicked.connect(self._refresh_key)
        btn_row.addWidget(new_btn)

        close_btn = QPushButton("Cerrar")
        close_btn.setFixedHeight(34)
        close_btn.setFont(QFont(UI_FONT, 9))
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {C.TEXT_MED};
                border: 1px solid {C.BORDER}; border-radius: 8px;
            }}
            QPushButton:hover {{ color: {C.TEXT}; border: 1px solid {C.BORDER_B}; }}
        """)
        close_btn.clicked.connect(self._do_close)
        btn_row.addWidget(close_btn)
        lay.addLayout(btn_row)

        self._ctimer = QTimer(self)
        self._ctimer.timeout.connect(self._tick)
        self._ctimer.start(1000)
        self._tick()

    def set_new_key_callback(self, fn) -> None:
        self._on_new_key = fn

    def _update_qr(self, url: str) -> None:
        if not url:
            self._qr_label.setText("—")
            return
        try:
            import qrcode as _qrmod
            from io import BytesIO
            qr = _qrmod.QRCode(
                box_size=5, border=2,
                error_correction=_qrmod.constants.ERROR_CORRECT_M,
            )
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buf = BytesIO()
            img.save(buf, format="PNG")
            px = QPixmap()
            px.loadFromData(buf.getvalue())
            self._qr_label.setPixmap(
                px.scaled(170, 170,
                          Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation)
            )
        except ImportError:
            self._qr_label.setText("pip install\nqrcode[pil]")
            self._qr_label.setFont(QFont(UI_FONT, 8))
            self._qr_label.setStyleSheet(
                "color: #888; background: white; border-radius: 10px; padding: 4px;"
            )
        except Exception:
            self._qr_label.setText(url[:28])
            self._qr_label.setFont(QFont(UI_FONT, 8))
            self._qr_label.setStyleSheet(
                f"color: {C.PRI}; background: white; border-radius: 10px; padding: 4px;"
            )

    def _tick(self):
        remaining = max(0, int(self._expiry - time.time()))
        m, s = divmod(remaining, 60)
        self._timer_lbl.setText(f"Expira en  {m:02d}:{s:02d}")
        if remaining == 0:
            self._do_close()

    def mark_connected(self) -> None:
        """Call from any thread when a phone successfully connects."""
        self._ctimer.stop()
        self._key_lbl.setText("VINCULADO")
        self._key_lbl.setStyleSheet(f"""
            color: {C.GREEN};
            background: {_rgba(C.GREEN, 0.12)};
            border: 1px solid {_rgba(C.GREEN, 0.40)};
            border-radius: 8px;
            padding: 6px 4px;
            letter-spacing: 4px;
        """)
        self._qr_label.setText("✓")
        self._qr_label.setFont(QFont(UI_FONT, 54, QFont.Weight.Bold))
        self._qr_label.setStyleSheet(
            f"color: {C.GREEN}; background: {_rgba(C.GREEN, 0.14)}; border-radius: 10px;"
        )
        _asst = (_read_full_config().get("assistant_name") or "Viernes").strip()
        self._timer_lbl.setText(f"Móvil vinculado — {_asst} lista")
        self._timer_lbl.setStyleSheet(f"color: {C.GREEN}; background: transparent;")

    def _refresh_key(self):
        if self._on_new_key:
            result = self._on_new_key()
            if result:
                url    = result[0]
                key    = result[1]
                auto   = result[2] if len(result) >= 3 else ""
                manual = result[3] if len(result) >= 4 else url
                self._manual_url     = manual or url
                self._url_lbl.setText(self._manual_url)
                self._key_lbl.setText(key)
                self._auto_login_url = auto
                self._update_qr(auto or url)
                self._expiry = time.time() + 600
                self._key_lbl.setStyleSheet(f"""
                    color: {C.WHITE};
                    background: {C.DARK};
                    border: 1px solid {C.BORDER_B};
                    border-radius: 8px;
                    padding: 6px 4px;
                    letter-spacing: 10px;
                """)
                self._timer_lbl.setStyleSheet(
                    f"color: {C.TEXT_MED}; background: transparent;"
                )
                self._ctimer.start(1000)
                self._tick()

    def _do_close(self):
        self._ctimer.stop()
        self.hide()
        self.closed.emit()

    def hideEvent(self, e):
        self._ctimer.stop()
        super().hideEvent(e)
        self.closed.emit()

    def closeEvent(self, e):
        self._ctimer.stop()
        super().closeEvent(e)
        self.closed.emit()


class MainWindow(QMainWindow):
    _log_sig        = pyqtSignal(str)
    _state_sig      = pyqtSignal(str)
    _content_sig    = pyqtSignal(str, str)   # (title, text) — thread-safe content display
    _reconfig_sig   = pyqtSignal()           # trigger setup overlay from any thread
    _camera_sig     = pyqtSignal(bytes)      # show camera frame preview (small overlay)
    _cam_stream_sig = pyqtSignal(bool)       # True=start live stream, False=stop
    _cam_frame_sig  = pyqtSignal(bytes)      # live camera frame → HUD area
    _video_open_sig  = pyqtSignal(str, str, bool, str)  # video, title, muted, audio
    _sports_open_sig = pyqtSignal(str, str, str, str, bool, object, int)  # url, frame_src, title, frame_host, muted, options, selected_option
    _radio_open_sig  = pyqtSignal(str, str, str, bool)  # url, title, subtitle, muted
    _cleanyourtv_sig = pyqtSignal(str)  # optional initial TV IP
    _wake_btns_sig   = pyqtSignal()          # wake state resolved off-thread
    _video_close_sig = pyqtSignal()
    _video_mute_sig  = pyqtSignal(bool)
    _video_fs_sig    = pyqtSignal(bool)
    _clipboard_sig  = pyqtSignal(str)        # clipboard text changed (thread-safe)
    _confirm_sig    = pyqtSignal(str, str)   # (title, detail) — irreversible-action gate
    _confirm_hide_sig = pyqtSignal()
    _wake_dl_sig    = pyqtSignal(bool, str)  # wake-word install finished (ok, message)
    _quiz_sig       = pyqtSignal(str, object, object)  # (topic, questions, grader)
    _quiz_hide_sig  = pyqtSignal()
    _review_sig     = pyqtSignal(str, str, object, object)  # document review payload
    _research_sig   = pyqtSignal(object)                     # deep research report payload
    _emotion_sig    = pyqtSignal(str, float, float)          # (name, intensity, duration)
    _action_sig     = pyqtSignal(str)                        # action name
    _semantic_intent_sig = pyqtSignal(str, object)           # (intent, metadata)
    _gesture_sig    = pyqtSignal(str, float, float)          # (name, duration, intensity)
    _interrupt_gestures_sig = pyqtSignal()
    _float_mode_sig = pyqtSignal(str)                        # float mode
    _visual_card_sig = pyqtSignal(object)                    # contextual visual card payload
    _visual_hide_sig = pyqtSignal()
    _gods_eye_sig    = pyqtSignal(str, str, str)             # (command, arg1, arg2)
    _external_file_sig = pyqtSignal(str)                     # file uploaded from mobile Remote Control
    _mute_sig             = pyqtSignal(bool, str)            # (muted, note) - thread-safe mic mute control

    def __init__(self, face_path: str):
        super().__init__()
        self.setAcceptDrops(True)
        self._face_path = face_path

        # Load customization from config
        _cfg = _read_full_config()
        self._assistant_name: str = (_cfg.get("assistant_name") or "Viernes").strip()
        _display = self._assistant_name.upper()

        # Apply saved HUD Studio theme BEFORE panels/stylesheets are built
        from core.hud_theme import load_hud_config, get_theme_palette
        self._hud_cfg = load_hud_config()
        apply_full_palette(
            get_theme_palette(
                self._hud_cfg.get("theme_id", "obsidian_pro"),
                self._hud_cfg.get("accent_override", ""),
            )
        )
        _ui_color = (_cfg.get("ui_color") or "").strip()
        _legacy_scifi = {"#ff9900", "#00d4ff", "#00ff88", "#a855f7", "#ff3366", "#00f0ff"}
        if _ui_color.lower() in _legacy_scifi:
            _ui_color = ""
        if _ui_color and not self._hud_cfg.get("accent_override"):
            apply_ui_accent(_ui_color)

        self.setWindowTitle(f"{_display} — {APP_VERSION}")
        self.setMinimumSize(_MIN_W, _MIN_H)
        self.resize(_DEFAULT_W, _DEFAULT_H)

        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            (screen.width()  - _DEFAULT_W) // 2,
            (screen.height() - _DEFAULT_H) // 2,
        )

        self.on_text_command   = None
        self.on_remote_clicked = None   # callable: () -> (url, key) | None
        self.on_interrupt      = None   # callable: () -> None — stop VIERNES mid-speech
        self.on_voice_change   = None   # callable: () -> None — rebuild session with new voice
        self.on_audio_device_change = None  # callable: () -> None — reopen audio streams
        self._confirm_overlay  = None   # live ConfirmBanner, if one is on screen
        self.get_plugins       = None   # callable: () -> list[dict], set by ViernesLive
        self.get_plugin_settings = None # callable: () -> list[dict] settings schemas, set by ViernesLive
        self.on_wake_toggle    = None   # callable: (enable: bool) -> str, set by ViernesLive
        self.on_wake_manual    = None   # callable: () -> None — manual sleep/wake
        self.on_push_to_talk   = None   # callable: (enable: bool) -> str scope
        self.ptt_hold          = None   # callable: (held: bool) -> None — windowed chord
        self.wake_get_state    = None   # callable: () -> dict {enabled, awake, ready}
        self._muted            = False
        self._current_file: str | None = None
        self._remote_overlay: RemoteKeyOverlay | None = None
        self._customize_overlay: CustomizeOverlay | None = None
        self._hud_studio_overlay = None
        self._cleanyourtv_overlay = None
        self._donation_overlay = None

        self._central_w = QWidget()
        self._central_w.setStyleSheet(f"background: {C.BG};")
        self.setCentralWidget(self._central_w)

        root = QVBoxLayout(self._central_w)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        self._header_widget = self._build_header()
        root.addWidget(self._header_widget)

        QApplication.instance().setStyleSheet(_APP_SS)
        body = QHBoxLayout()
        body.setContentsMargins(14, 14, 14, 14)
        body.setSpacing(14)
        self._body_layout = body

        self._left_panel = self._build_left_panel()
        body.addWidget(self._left_panel, stretch=0)

        # Center column: HUD + resizable content panel via QSplitter
        self.hud = HudCanvas(face_path, _display)
        self.hud.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._content_panel = self._build_content_panel()
        self._quiz_panel = self._build_quiz_panel()

        # Live camera container — replaces HUD when camera stream is active
        _cam_cont = QWidget()
        _cam_cont.setStyleSheet(f"background: {C.DARK}; border: 1px solid {C.BORDER}; border-radius: 12px;")
        _cam_v = QVBoxLayout(_cam_cont)
        _cam_v.setContentsMargins(0, 0, 0, 0)
        _cam_v.setSpacing(0)
        _cam_hdr = QHBoxLayout()
        _cam_hdr.setContentsMargins(12, 8, 12, 8)
        _cam_title = QLabel("●  Percepción visual en tiempo real")
        _cam_title.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        _cam_title.setStyleSheet(f"color: {C.TEXT}; background: transparent; border: none;")
        _cam_hdr.addWidget(_cam_title)
        _cam_hdr.addStretch()
        _cam_x = QPushButton("Cerrar  ✕")
        _cam_x.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        _cam_x.setCursor(Qt.CursorShape.PointingHandCursor)
        _cam_x.setStyleSheet(f"""
            QPushButton {{
                color: {C.TEXT_MED}; background: transparent;
                border: 1px solid {C.BORDER}; border-radius: 6px; padding: 2px 8px;
            }}
            QPushButton:hover {{ color: {C.WHITE}; border-color: {C.BORDER_B}; }}
        """)
        _cam_x.clicked.connect(self.stop_camera_stream)
        _cam_hdr.addWidget(_cam_x)
        _cam_v.addLayout(_cam_hdr)
        self._cam_live_lbl = QLabel()
        self._cam_live_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._cam_live_lbl.setStyleSheet("background: transparent; border: none;")
        self._cam_live_lbl.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        _cam_v.addWidget(self._cam_live_lbl, stretch=1)

        # ── Video surface ────────────────────────────────────────────────
        self._video_split = False
        self._video_auto_muted = False
        self._video_on = False
        self._video_cont = QWidget()
        self._video_cont.setStyleSheet(f"background: {C.DARK}; border: 1px solid {C.BORDER}; border-radius: 12px;")
        _vid_v = QVBoxLayout(self._video_cont)
        _vid_v.setContentsMargins(10, 8, 10, 10)
        _vid_v.setSpacing(6)

        _vid_hdr = QHBoxLayout()
        self._video_title = QLabel("▶  Reproducción de video")
        self._video_title.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        self._video_title.setStyleSheet(f"color: {C.WHITE}; background: transparent; border: none;")
        _vid_hdr.addWidget(self._video_title)
        _vid_hdr.addStretch()

        def _vid_btn(text: str) -> QPushButton:
            b = QPushButton(text)
            b.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setStyleSheet(f"""
                QPushButton {{
                    color: {C.TEXT_MED}; background: transparent;
                    border: 1px solid {C.BORDER}; border-radius: 6px; padding: 2px 8px;
                }}
                QPushButton:hover {{ color: {C.WHITE}; border-color: {C.BORDER_B}; }}
            """)
            return b

        self._video_opt_combo = QComboBox()
        self._video_opt_combo.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        self._video_opt_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self._video_opt_combo.setStyleSheet(
            f"QComboBox {{ background:{C.PANEL}; color:{C.TEXT_MED}; "
            f"border:1px solid {C.BORDER}; border-radius:6px; padding:2px 8px; }}"
            f"QComboBox:hover {{ color:{C.WHITE}; border-color:{C.BORDER_B}; }}"
            f"QComboBox QAbstractItemView {{ background:{C.PANEL}; color:{C.WHITE}; "
            f"selection-background-color:{C.BORDER_B}; }}"
        )
        self._video_opt_combo.currentIndexChanged.connect(self._on_sports_option_changed)
        self._video_opt_combo.hide()
        _vid_hdr.addWidget(self._video_opt_combo)

        self._video_reload_btn = _vid_btn("↻  Recargar")
        self._video_reload_btn.clicked.connect(self._reload_sports_channel)
        self._video_reload_btn.hide()
        _vid_hdr.addWidget(self._video_reload_btn)

        self._video_mute_btn = _vid_btn("🔇  Sin sonido")
        self._video_mute_btn.clicked.connect(self._toggle_video_mute)
        _vid_hdr.addWidget(self._video_mute_btn)

        self._video_fullscreen = False
        self._video_fs_btn = _vid_btn("⛶  Pantalla completa")
        self._video_fs_btn.clicked.connect(self._toggle_video_fullscreen)
        _vid_hdr.addWidget(self._video_fs_btn)

        _vid_x = _vid_btn("Cerrar  ✕")
        _vid_x.clicked.connect(self.stop_video)
        _vid_hdr.addWidget(_vid_x)
        _vid_v.addLayout(_vid_hdr)

        self._sports_web_view = None
        self._sports_web_mode = False
        self._radio_visualizer = None
        self._video_inner_stack = QStackedWidget()
        _vid_v.addWidget(self._video_inner_stack, stretch=1)

        if HAVE_VIDEO:
            # A GRAPHICS ITEM, NOT A QVideoWidget.
            #
            # QVideoWidget gets a native window of its own, and a native window
            # is painted by the compositor above every ordinary widget that
            # shares the screen with it — so the settings drawer opened
            # *underneath* the video and raise_() could not help, because the
            # two are not in the same painting order at all. A video item drawn
            # into a QGraphicsView goes through Qt's own painter like any other
            # widget, and anything laid over it stays over it.
            self._video_scene = QGraphicsScene(self)
            self._video_item = QGraphicsVideoItem()
            self._video_scene.addItem(self._video_item)
            self._video_widget = QGraphicsView(self._video_scene)
            self._video_widget.setStyleSheet("background: #000; border: none;")
            self._video_widget.setFrameShape(QGraphicsView.Shape.NoFrame)
            self._video_widget.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self._video_widget.setVerticalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self._video_widget.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            self._video_inner_stack.addWidget(self._video_widget)
            self._video_widget.viewport().installEventFilter(self)

            self._video_audio = QAudioOutput()
            self._video_audio.setMuted(True)
            self._video_player = QMediaPlayer()
            self._video_player.setVideoOutput(self._video_item)
            # Keep the picture filling the view as the window is resized.
            self._video_item.nativeSizeChanged.connect(self._fit_video)
            self._video_player.setAudioOutput(self._video_audio)
            self._video_player.errorOccurred.connect(self._on_video_error)

            # A SECOND player, for sound that arrives separately.
            #
            # YouTube no longer serves a single stream carrying both picture and
            # sound — not for new uploads and not for old ones; checked against
            # three videos including the oldest on the site, and every one of
            # them offered zero combined formats. Picture and sound are two
            # URLs, so they are two players, started together and nudged back
            # into line by the timer below.
            #
            # A local file or a direct video URL still uses the first player
            # alone: one stream, one player, nothing to synchronise.
            self._video_sound = QMediaPlayer()
            self._video_sound_out = QAudioOutput()
            self._video_sound_out.setMuted(True)
            self._video_sound.setAudioOutput(self._video_sound_out)

            self._video_sync = QTimer(self)
            self._video_sync.setInterval(1000)
            self._video_sync.timeout.connect(self._sync_video_sound)
        else:
            self._video_scene = None
            self._video_item = None
            self._video_widget = None
            self._video_player = None
            self._video_audio = None
            self._video_sound = None
            self._video_sound_out = None
            self._video_sync = None
            _miss = QLabel("Video playback is not available in this Qt install.")
            _miss.setAlignment(Qt.AlignmentFlag.AlignCenter)
            _miss.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent;")
            _vid_v.addWidget(_miss, stretch=1)

        # Stack: 0 = animated HUD, 1 = live camera, 2 = video, 3 = God's Eye View
        # Stack: 0 = animated HUD, 1 = live camera, 2 = video
        self._hud_cam_stack = QStackedWidget()
        self._hud_cam_stack.addWidget(self.hud)
        self._hud_cam_stack.addWidget(_cam_cont)
        self._hud_cam_stack.addWidget(self._video_cont)

        self._center_split = QSplitter(Qt.Orientation.Vertical)
        self._center_split.setStyleSheet(f"""
            QSplitter::handle {{
                background: rgba(255, 255, 255, 0.05);
                height: 2px;
                margin: 4px 0;
            }}
            QSplitter::handle:hover {{
                background: {C.PRI};
            }}
        """)
        self._center_split.addWidget(self._hud_cam_stack)
        self._center_split.addWidget(self._content_panel)
        self._center_split.addWidget(self._quiz_panel)
        self._center_split.setStretchFactor(0, 3)
        self._center_split.setStretchFactor(1, 1)
        self._center_split.setCollapsible(0, False)
        body.addWidget(self._center_split, stretch=5)

        self._right_panel = self._build_right_panel()
        body.addWidget(self._right_panel, stretch=0)

        root.addLayout(body, stretch=1)
        self._footer_widget = self._build_footer()
        root.addWidget(self._footer_widget)

        # Floating overlay drawers (built after central widget layout is done)
        from core.avatar_control_drawer import AvatarControlDrawer
        self._avatar_drawer = AvatarControlDrawer(self)
        self._quick_drawer = self._build_quick_drawer()
        self._ctrl_drawer = self._build_controls_drawer()
        self._warm_wake_state()
        self._update_autostart_btn(self._check_autostart())
        from memory.config_manager import get_brief_enabled as _gbe
        self._update_brief_btn(_gbe())

        self._clock_tmr = QTimer(self)
        self._clock_tmr.timeout.connect(self._tick_clock)
        self._clock_tmr.start(1000)

        # Apply saved HUD Studio layout, module visibility, density & effects
        self._apply_hud_config(self._hud_cfg, persist=False)
        self._tick_clock()

        # Metric update timer
        self._metric_tmr = QTimer(self)
        self._metric_tmr.timeout.connect(self._update_metrics)
        self._metric_tmr.start(2000)
        self._update_metrics()

        # Autonomous periodic expressive avatar animation timer
        from memory.config_manager import get_auto_animations_enabled
        self._auto_animations_enabled = get_auto_animations_enabled()
        self._auto_anim_timer = QTimer(self)
        self._auto_anim_timer.setSingleShot(True)
        self._auto_anim_timer.timeout.connect(self._on_auto_anim_tick)
        if self._auto_animations_enabled:
            self._schedule_next_auto_animation(initial=True)

        self._log_sig.connect(self._log.append_log)
        self._log_sig.connect(self._on_log_received)
        self._state_sig.connect(self._apply_state)
        self._content_sig.connect(self._show_content)
        self._reconfig_sig.connect(self._show_setup)
        self._camera_sig.connect(self._show_camera_frame)
        self._confirm_sig.connect(self._show_confirm_banner)
        self._confirm_hide_sig.connect(self._hide_confirm_banner)
        self._cam_stream_sig.connect(self._on_cam_stream)
        self._cam_frame_sig.connect(self._on_cam_frame)
        self._wake_btns_sig.connect(self._refresh_wake_btns)
        self._video_open_sig.connect(self._on_video_open)
        self._sports_open_sig.connect(self._on_sports_open)
        self._radio_open_sig.connect(self._on_radio_open)
        self._cleanyourtv_sig.connect(self._open_cleanyourtv)
        self._video_close_sig.connect(self._on_video_close)
        self._video_mute_sig.connect(self._on_video_mute)
        self._video_fs_sig.connect(self._set_video_fullscreen)
        self._mute_sig.connect(lambda m, n: self._set_muted(m, n, force=True))
        self._clipboard_sig.connect(self._show_clipboard_panel)
        self._wake_dl_sig.connect(self._on_wake_install_done)
        self._quiz_sig.connect(self._show_quiz)
        self._quiz_hide_sig.connect(self._hide_quiz)
        self._review_sig.connect(self._show_review)
        self._emotion_sig.connect(self._on_emotion_sig)
        self._action_sig.connect(self._on_action_sig)
        self._semantic_intent_sig.connect(self._on_semantic_intent_sig)
        self._gesture_sig.connect(self._on_gesture_sig)
        self._interrupt_gestures_sig.connect(self._on_interrupt_gestures_sig)
        self._float_mode_sig.connect(self._on_float_mode_sig)
        self._visual_card_sig.connect(self._on_visual_card_sig)
        self._visual_hide_sig.connect(self._on_visual_hide_sig)
        self._external_file_sig.connect(self._on_external_file_sig)
        self._cam_stop = threading.Event()

        # Camera preview overlay (child of central widget, positioned in resizeEvent)
        self._cam_preview = _CameraPreview(self.centralWidget())

        # Clipboard panel (child of central widget, bottom-center)
        self._clipboard_panel = ClipboardPanel(self.centralWidget())
        self._clipboard_panel.action_requested.connect(self._on_clipboard_action)
        QApplication.clipboard().dataChanged.connect(self._on_clipboard_changed)

        self._overlay: SetupOverlay | None = None
        self._research_overlay = None
        self._research_sig.connect(self._show_research)
        self._ready = self._check_config()
        if not self._ready:
            self._show_setup()

        # Inbound communications listener (WhatsApp & Gmail)
        try:
            from system_monitor.communication_monitor import comm_monitor
            def _on_ui_comm_alert(alert):
                txt = alert.get("spoken_text", "")
                icon = "💬" if alert.get("type", "").startswith("whatsapp") else "✉️"
                self._log_sig.emit(f"{icon} {txt}")
            comm_monitor.register_alert_listener(_on_ui_comm_alert)
        except Exception as e:
            print(f"[UI] CommMonitor hook error: {e}")

        sc_mute = QShortcut(QKeySequence("F4"), self)
        sc_mute.activated.connect(self._toggle_mute)
        sc_api_keys = QShortcut(QKeySequence("F6"), self)
        sc_api_keys.activated.connect(self._open_api_keys_dialog)
        sc_books = QShortcut(QKeySequence("F7"), self)
        sc_books.activated.connect(self._open_books_library)
        sc_integrations = QShortcut(QKeySequence("F8"), self)
        sc_integrations.activated.connect(self._show_integrations_overlay)
        sc_research = QShortcut(QKeySequence("F9"), self)
        sc_research.activated.connect(self._toggle_research_panel)
        sc_zen = QShortcut(QKeySequence("F10"), self)
        sc_zen.activated.connect(self._toggle_avatar_only)
        sc_full = QShortcut(QKeySequence("F11"), self)
        sc_full.activated.connect(self._toggle_fullscreen)
        sc_intr = QShortcut(QKeySequence("Escape"), self)
        sc_intr.activated.connect(self._do_interrupt)

    def mousePressEvent(self, event):
        pos = event.pos()
        if hasattr(self, "_avatar_drawer") and self._avatar_drawer.isVisible():
            drawer_rect = self._avatar_drawer.geometry()
            btn_rect = self._avatar_hdr_btn.geometry() if hasattr(self, "_avatar_hdr_btn") else QRect()
            hdr_pos = self._header_widget.mapFrom(self, pos) if hasattr(self, "_header_widget") else pos
            if not drawer_rect.contains(pos) and not btn_rect.contains(hdr_pos):
                self._close_avatar()
        if hasattr(self, "_quick_drawer") and self._quick_drawer.isVisible():
            drawer_rect = self._quick_drawer.geometry()
            btn_rect = self._drawer_btn.geometry() if hasattr(self, "_drawer_btn") else QRect()
            hdr_pos = self._header_widget.mapFrom(self, pos) if hasattr(self, "_header_widget") else pos
            if not drawer_rect.contains(pos) and not btn_rect.contains(hdr_pos):
                self._close_setup()
        if hasattr(self, "_ctrl_drawer") and self._ctrl_drawer.isVisible():
            drawer_rect = self._ctrl_drawer.geometry()
            btn_rect = self._ctrl_btn.geometry() if hasattr(self, "_ctrl_btn") else QRect()
            hdr_pos = self._header_widget.mapFrom(self, pos) if hasattr(self, "_header_widget") else pos
            if not drawer_rect.contains(pos) and not btn_rect.contains(hdr_pos):
                self._close_controls()
        super().mousePressEvent(event)

    def _open_api_keys_dialog(self):
        """Open the unified Claves API General dialog (F6 / Menu)."""
        try:
            if hasattr(self, "hud") and self.hud is not None:
                self.hud.set_overlay_active(True)
            from core.api_keys_overlay import ApiKeysGeneralDialog
            dlg = ApiKeysGeneralDialog(self)
            if hasattr(dlg, "keys_saved"):
                dlg.keys_saved.connect(self._on_api_keys_updated)
            elif hasattr(dlg, "credentials_updated"):
                dlg.credentials_updated.connect(lambda: self._on_api_keys_updated({}))
            dlg.exec()
        except Exception as e:
            print(f"[UI] Error opening ApiKeysGeneralDialog: {e}")
        finally:
            if hasattr(self, "hud") and self.hud is not None:
                self.hud.set_overlay_active(False)

    def _on_api_keys_updated(self, keys: dict):
        """Handle hot-reload notification when API keys are saved."""
        try:
            self._log_sig.emit("🔑 Claves API actualizadas exitosamente.")
            if keys.get("gemini"):
                self.system_status.emit("● Motor Gemini Configurado")
        except Exception as e:
            print(f"[UI] Error in _on_api_keys_updated: {e}")

    def _open_device_control(self):
        """Open Viernes Device Control Center."""
        try:
            if hasattr(self, "hud") and self.hud is not None:
                self.hud.set_overlay_active(True)
            from core.device_control_overlay import DeviceControlCenterDialog
            dlg = DeviceControlCenterDialog(self)
            dlg.exec()
        except Exception as e:
            print(f"[UI] Error opening DeviceControlCenterDialog: {e}")
        finally:
            if hasattr(self, "hud") and self.hud is not None:
                self.hud.set_overlay_active(False)

    def _show_integrations_overlay(self):
        """Open the unified Integrations Hub overlay dialog."""
        try:
            if hasattr(self, "hud") and self.hud is not None:
                self.hud.set_overlay_active(True)
            from core.integrations_overlay import IntegrationsHubOverlay
            ov = IntegrationsHubOverlay(self)
            ov.exec()
        except Exception as e:
            print(f"[UI] Error opening Integrations Hub: {e}")
        finally:
            if hasattr(self, "hud") and self.hud is not None:
                self.hud.set_overlay_active(False)

    def _position_cam_preview(self) -> None:
        """Position camera preview overlay at bottom-right corner of central area."""
        if not hasattr(self, "_cam_preview") or self._cam_preview is None:
            return
        cw = self.centralWidget()
        if cw is None:
            return
        pw = getattr(_CameraPreview, "_W", 260)
        ph = self._cam_preview.height() or getattr(_CameraPreview, "_H", 180)
        right_w = _RIGHT_W if "_RIGHT_W" in globals() else 340
        self._cam_preview.setGeometry(
            max(10, cw.width() - right_w - pw - 12),
            max(10, cw.height() - ph - 28),
            pw, ph,
        )

    def _show_camera_frame(self, img_bytes: bytes):
        """Slot — display camera preview overlay (main thread)."""
        if hasattr(self, "_cam_preview") and self._cam_preview:
            self._cam_preview.show_frame(img_bytes)
            self._position_cam_preview()

    # --- Live camera stream in HUD / PiP area ------------------------------
    def _on_cam_stream(self, start: bool) -> None:
        if start:
            if hasattr(self, "_cam_preview"):
                self._cam_preview._user_closed = False
            try:
                from core.opencv_vision import get_opencv_vision
                p_mode = get_opencv_vision().get_config().get("preview_mode", "pip")
            except Exception:
                p_mode = "pip"

            if p_mode == "hud":
                self._hud_cam_stack.setCurrentIndex(1)
                if hasattr(self, "_cam_preview"):
                    self._cam_preview.hide()
            else:
                self._hud_cam_stack.setCurrentIndex(0)
                if hasattr(self, "_cam_preview"):
                    self._cam_preview.show()
                    self._position_cam_preview()
        else:
            self._hud_cam_stack.setCurrentIndex(0)
            self._cam_live_lbl.clear()
            if hasattr(self, "_cam_preview"):
                self._cam_preview._timer.stop()
                self._cam_preview.hide()

    def _on_cam_frame(self, data: bytes) -> None:
        try:
            px = QPixmap()
            px.loadFromData(data)
            if px.isNull():
                return
            if self._hud_cam_stack.currentIndex() == 1:
                w, h = self._cam_live_lbl.width(), self._cam_live_lbl.height()
                if w > 1 and h > 1:
                    self._cam_live_lbl.setPixmap(
                        px.scaled(w, h,
                                  Qt.AspectRatioMode.KeepAspectRatio,
                                  Qt.TransformationMode.SmoothTransformation)
                    )
            elif hasattr(self, "_cam_preview"):
                self._cam_preview.show_frame(data, continuous=True)
        except Exception:
            pass

    def start_camera_stream(self) -> None:
        if hasattr(self, "_vision_hdr_btn"):
            self._vision_hdr_btn.setChecked(True)
            self._vision_hdr_btn.setText("📷  OpenCV: ON")

        try:
            from core.opencv_vision import get_opencv_vision
            coord = get_opencv_vision()
            coord.main_window_ref = self
            coord.ui_ref = getattr(self.hud, "_live2d_widget", None)
            coord.register_frame_subscriber(self._on_coordinator_frame)
            if not coord.is_active():
                coord.start_continuous_vision()
            self._cam_stream_sig.emit(True)
        except Exception as e:
            print(f"[OpenCV] Stream start error: {e}")

    def _on_coordinator_frame(self, data: bytes) -> None:
        self._cam_frame_sig.emit(data)

    def stop_camera_stream(self) -> None:
        if hasattr(self, "_vision_hdr_btn"):
            self._vision_hdr_btn.setChecked(False)
            self._vision_hdr_btn.setText("📷  OpenCV")

        try:
            from core.opencv_vision import get_opencv_vision
            coord = get_opencv_vision()
            coord.unregister_frame_subscriber(self._on_coordinator_frame)
            coord.stop_continuous_vision()
        except Exception as e:
            pass
        self._cam_stream_sig.emit(False)

    # --- Video in the HUD area ---------------------------------------------
    #
    # Everything below runs on the Qt thread. Plugins and the assistant reach it
    # through the signals above, the same way every other panel is driven, so a
    # background thread never touches a widget.
    def _on_video_open(self, source: str, title: str, muted: bool,
                       audio_source: str = "") -> None:
        if not HAVE_VIDEO or not self._video_player:
            self.write_log("SYS: Video playback is not available in this Qt "
                           "install.")
            return
        # A video and the live camera cannot share the centre of the HUD.
        self._cam_stop.set()

        if self._sports_web_view is not None:
            self._sports_web_view.stop_channel()
        if self._radio_visualizer is not None:
            self._radio_visualizer.stop()
        self._sports_web_mode = False
        self._video_reload_btn.hide()
        self._video_opt_combo.hide()
        if self._video_widget is not None:
            self._video_inner_stack.setCurrentWidget(self._video_widget)

        self._video_title.setText(f"▶  {(title or 'VIDEO')[:44].upper()}")
        self._video_split = bool(audio_source)
        self._set_video_muted(bool(muted))

        url = (QUrl.fromLocalFile(source) if Path(source).exists()
               else QUrl(source))
        self._video_player.setSource(url)
        if self._video_split:
            self._video_sound.setSource(QUrl(audio_source))
        self._hud_cam_stack.setCurrentIndex(2)
        self._video_on = True
        # Re-run now that the video counts as playing: _set_video_muted ran
        # before this line and saw no video, so its mic check was a no-op.
        self._sync_mic_for_video()
        self._video_player.play()
        if self._video_split:
            self._video_sound.play()
            self._video_sync.start()
        QTimer.singleShot(0, self._fit_video)
        QTimer.singleShot(100, self._fit_video)

    def _on_sports_open(
        self,
        url: str,
        frame_src: str,
        title: str,
        frame_host: str,
        muted: bool,
        options: object = None,
        selected_option: int = 1,
    ) -> None:
        self._cam_stop.set()
        if self._video_sync:
            self._video_sync.stop()
        for p in (self._video_player, self._video_sound):
            if p:
                p.stop()
                p.setSource(QUrl())
        if self._radio_visualizer is not None:
            self._radio_visualizer.stop()
        self._video_split = False

        if self._sports_web_view is None:
            try:
                from core.sports_web_view import SportsWebPlayer
                self._sports_web_view = SportsWebPlayer(self._video_cont)
                self._sports_web_view.stream_detected.connect(self._on_sports_stream_detected)
                self._video_inner_stack.addWidget(self._sports_web_view)
            except Exception as exc:
                self.write_log(f"ERR: No se pudo iniciar el reproductor web deportivo: {exc}")
                return

        opts_list = list(options) if isinstance(options, (list, tuple)) else []
        self._video_opt_combo.blockSignals(True)
        self._video_opt_combo.clear()
        if len(opts_list) > 1:
            for i, opt in enumerate(opts_list, start=1):
                lbl = str((opt or {}).get("label") or f"Opción {i}")
                u = str((opt or {}).get("url") or "")
                self._video_opt_combo.addItem(lbl, u)
            sel_idx = max(0, min(int(selected_option or 1) - 1, len(opts_list) - 1))
            self._video_opt_combo.setCurrentIndex(sel_idx)
            self._video_opt_combo.show()
        else:
            self._video_opt_combo.hide()
        self._video_opt_combo.blockSignals(False)

        self._sports_last_args = (url, frame_src, frame_host)
        self._sports_web_mode = True
        self._video_reload_btn.show()
        self._video_title.setText(f"📺  {(title or 'EN VIVO')[:44].upper()}")
        self._video_inner_stack.setCurrentWidget(self._sports_web_view)
        self._hud_cam_stack.setCurrentIndex(2)
        self._video_on = True
        self._sports_web_view.load_channel(url, frame_src=frame_src, frame_host=frame_host, muted=bool(muted))
        self._set_video_muted(bool(muted))

    def _on_sports_option_changed(self, idx: int) -> None:
        if idx < 0 or not self._sports_web_mode or self._sports_web_view is None:
            return
        opt_url = str(self._video_opt_combo.itemData(idx) or "").strip()
        if not opt_url:
            return
        from urllib.parse import urlparse
        page_url = (getattr(self, "_sports_last_args", None) or ("", "", ""))[0] or opt_url
        host = urlparse(opt_url).netloc
        self._sports_last_args = (page_url, opt_url, host)
        for p in (self._video_player, self._video_sound):
            if p:
                p.stop()
                p.setSource(QUrl())
        muted = self._video_audio.isMuted() if self._video_audio else _load_video_muted()
        self._video_inner_stack.setCurrentWidget(self._sports_web_view)
        self._sports_web_view.load_channel(page_url, frame_src=opt_url, frame_host=host, muted=bool(muted))

    def _on_sports_stream_detected(self, proxy_url: str) -> None:
        if not (HAVE_VIDEO and self._video_player and self._video_widget and self._sports_web_mode):
            return
        muted = self._sports_web_view.is_muted() if self._sports_web_view is not None else _load_video_muted()
        self._video_inner_stack.setCurrentWidget(self._video_widget)
        self._video_player.setSource(QUrl(proxy_url))
        self._set_video_muted(bool(muted))
        self._sync_mic_for_video()
        self._video_player.play()
        QTimer.singleShot(0, self._fit_video)
        QTimer.singleShot(100, self._fit_video)

    def _reload_sports_channel(self) -> None:
        if self._sports_web_mode and self._sports_web_view is not None:
            args = getattr(self, "_sports_last_args", None)
            if args:
                for p in (self._video_player, self._video_sound):
                    if p:
                        p.stop()
                        p.setSource(QUrl())
                muted = self._video_audio.isMuted() if self._video_audio else _load_video_muted()
                self._video_inner_stack.setCurrentWidget(self._sports_web_view)
                self._sports_web_view.load_channel(
                    args[0], frame_src=args[1], frame_host=args[2], muted=bool(muted)
                )
            else:
                self._sports_web_view.reload_channel()

    def _fit_video(self, *_a) -> None:
        """Size the picture to the panel, keeping its shape."""
        if not (self._video_item and self._video_widget):
            return
        try:
            native = self._video_item.nativeSize()
            if native.isEmpty():
                return
            view = self._video_widget.viewport().size()
            scale = min(view.width() / native.width(),
                        view.height() / native.height())
            w, h = native.width() * scale, native.height() * scale
            self._video_item.setSize(QSizeF(w, h))
            self._video_scene.setSceneRect(0, 0, w, h)
            self._video_widget.centerOn(self._video_item)
        except Exception:
            pass

    def _on_radio_open(self, url: str, title: str, subtitle: str, muted: bool) -> None:
        if not HAVE_VIDEO or not self._video_player:
            self.write_log("SYS: audio/video unavailable — check PyQt6-Multimedia install.")
            return
        self._cam_stop.set()
        if self._video_sync:
            self._video_sync.stop()
        if self._sports_web_view is not None:
            self._sports_web_view.stop_channel()
        self._sports_web_mode = False
        self._video_reload_btn.hide()
        self._video_opt_combo.hide()
        for p in (self._video_player, self._video_sound):
            if p:
                p.stop()
                p.setSource(QUrl())
        self._video_split = False

        if self._radio_visualizer is None:
            from core.radio_visualizer import RadioVisualizerWidget
            self._radio_visualizer = RadioVisualizerWidget(
                self._video_cont,
                on_random=self._on_radio_random_clicked,
                on_stop=self.stop_video,
            )
            self._video_inner_stack.addWidget(self._radio_visualizer)

        self._video_title.setText(f"📻  {(title or 'RADIO')[:44].upper()}")
        self._radio_visualizer.set_station(title or "Viernes Radio", subtitle or "", muted=bool(muted))
        self._video_inner_stack.setCurrentWidget(self._radio_visualizer)

        self._set_video_muted(bool(muted))
        self._video_player.setSource(QUrl(url))
        self._hud_cam_stack.setCurrentIndex(2)
        self._video_on = True
        self._sync_mic_for_video()
        self._video_player.play()

    def _on_radio_random_clicked(self) -> None:
        def _worker():
            try:
                from core.radio_engine import get_radio_manager
                res = get_radio_manager().random_spanish_station()
                if res.get("ok"):
                    st = res["station"]
                    sub = " · ".join([x for x in [st.get("group"), st.get("country"), st.get("source")] if x])
                    self._radio_open_sig.emit(
                        res["url"],
                        st.get("name") or "Radio en Español",
                        sub,
                        _load_video_muted(),
                    )
                else:
                    self.write_log(f"SYS: {res.get('reason', 'No se encontró radio aleatoria en español.')}")
            except Exception as exc:
                self.write_log(f"ERR: Error cambiando a radio aleatoria: {exc}")

        threading.Thread(target=_worker, daemon=True).start()

    def _on_video_close(self) -> None:
        if getattr(self, "_video_fullscreen", False):
            self._toggle_video_fullscreen()
        if self._video_sync:
            self._video_sync.stop()
        for p in (self._video_player, self._video_sound):
            if p:
                p.stop()
                p.setSource(QUrl())
        if self._sports_web_view is not None:
            self._sports_web_view.stop_channel()
        if self._radio_visualizer is not None:
            self._radio_visualizer.stop()
        self._sports_web_mode = False
        self._video_reload_btn.hide()
        self._video_opt_combo.hide()
        self._video_split = False
        self._video_on = False
        self._hud_cam_stack.setCurrentIndex(0)
        self._sync_mic_for_video()      # gives the microphone back

    def toggle_gods_eye(self) -> None:
        pass

    def open_gods_eye(self, location: str = "", sensor: str = "") -> None:
        pass

    def close_gods_eye(self) -> None:
        pass

    def _on_gods_eye_sig(self, cmd: str, arg1: str, arg2: str) -> None:
        pass

    def _set_video_muted(self, muted: bool) -> None:
        """Silence whichever output is carrying the sound for this video."""
        muted = bool(muted)
        if self._sports_web_mode and self._sports_web_view is not None:
            self._sports_web_view.set_muted(muted)
        if self._radio_visualizer is not None:
            self._radio_visualizer.set_muted(muted)
        if self._video_audio:
            self._video_audio.setMuted(muted)
        if self._video_sound_out:
            self._video_sound_out.setMuted(muted)
        self._sync_video_mute_btn()
        self._sync_mic_for_video()

    def _on_video_mute(self, muted: bool) -> None:
        _save_video_muted(bool(muted))
        self._set_video_muted(bool(muted))

    def _sync_mic_for_video(self) -> None:
        """Close the microphone while the video is making sound.

        VIERNES subtracts its OWN output from the microphone — that is what
        core/echo.py does — but a video plays through a different output
        entirely, so the guard has never heard of it and the assistant answers
        the film. There is no arrangement in which an open microphone and a
        loudspeaker in the same room do not do that.

        So the microphone closes for exactly as long as the sound is on, and
        opens again by itself the moment it goes off or the video is closed.
        Only if VIERNES closed it: a microphone the user muted themselves stays
        muted, and pressing the mute key during a video hands the decision back
        to them for good.
        """
        if self._sports_web_mode and self._sports_web_view is not None:
            sound_on = bool(self._video_on and not self._sports_web_view.is_muted())
        else:
            out = self._video_sound_out if self._video_split else self._video_audio
            sound_on = bool(self._video_on and out and not out.isMuted())
        if sound_on and not self._muted:
            self._video_auto_muted = True
            self._set_muted(True, "The video's sound is on — silence it, close "
                                  "it, or press F4 to talk. Typing still works.")
        elif not sound_on and self._video_auto_muted:
            self._video_auto_muted = False
            self._set_muted(False, "The video is quiet again.")

    def _sync_video_sound(self) -> None:
        """Keep the separate soundtrack in step with the picture.

        Two players started at the same moment do not stay together: they buffer
        independently, and measured on a real stream they were about half a
        second apart after nine seconds. So the sound is nudged back to the
        picture whenever it drifts far enough to hear — and only then, because
        correcting a smaller gap is itself audible.
        """
        if not (self._video_split and self._video_sound and self._video_player):
            return
        try:
            if self._video_player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
                return
            drift = self._video_sound.position() - self._video_player.position()
            if abs(drift) > 300:
                self._video_sound.setPosition(self._video_player.position())
        except Exception:
            pass

    def _sync_video_mute_btn(self) -> None:
        if self._sports_web_mode and self._sports_web_view is not None:
            muted = self._sports_web_view.is_muted()
        else:
            out = self._video_sound_out if self._video_split else self._video_audio
            muted = bool(out and out.isMuted())
        self._video_mute_btn.setText("🔇  SOUND OFF" if muted else "🔊  SOUND ON")

    def _toggle_video_mute(self) -> None:
        if self._sports_web_mode and self._sports_web_view is not None:
            new_muted = not self._sports_web_view.is_muted()
            _save_video_muted(new_muted)
            self._set_video_muted(new_muted)
            return
        out = self._video_sound_out if self._video_split else self._video_audio
        if out:
            new_muted = not out.isMuted()
            _save_video_muted(new_muted)
            self._set_video_muted(new_muted)

    def _on_video_error(self, *_a) -> None:
        err = ""
        try:
            err = self._video_player.errorString()
        except Exception:
            pass
        self.write_log(f"SYS: The video could not be played{(' — ' + err) if err else ''}.")
        self._on_video_close()

    def stop_video(self) -> None:
        self._video_close_sig.emit()

    def video_is_playing(self) -> bool:
        return bool(self._video_on)

    # ------------------------------------------------------------------
    # Icon generation — arc-reactor style, rendered with Pillow
    # ------------------------------------------------------------------
    @staticmethod
    def _build_viernes_icon(out_path: Path) -> bool:
        """
        Render a VIERNES arc-reactor icon at 4× resolution and downsample
        for crisp results at all sizes. Saves a multi-res .ico to out_path.
        Returns True on success.
        """
        try:
            import math
            import PIL.Image
            import PIL.ImageDraw
            import PIL.ImageFilter
        except ImportError:
            return False

        CYAN   = (0, 212, 255)
        DIM    = (0, 100, 140)
        DARK   = (0, 6, 10)
        GLOW   = (0, 160, 200)
        WHITE  = (220, 240, 255)

        def _render(sz: int) -> PIL.Image.Image:
            S  = sz * 4                     # draw at 4× then downscale
            img = PIL.Image.new("RGBA", (S, S), (0, 0, 0, 0))
            d   = PIL.ImageDraw.Draw(img)
            cx = cy = S // 2

            # ── filled background circle ──────────────────────────────────
            R = S // 2 - 2
            d.ellipse([cx-R, cy-R, cx+R, cy+R], fill=(*DARK, 255))

            # ── outer border ring ─────────────────────────────────────────
            lw = max(2, S // 40)
            d.ellipse([cx-R, cy-R, cx+R, cy+R],
                      outline=(*CYAN, 220), width=lw)

            # ── mid decorative ring ───────────────────────────────────────
            R2 = int(R * 0.72)
            d.ellipse([cx-R2, cy-R2, cx+R2, cy+R2],
                      outline=(*DIM, 180), width=max(1, lw // 2))

            # ── 6 radial spokes (hex bolt) ────────────────────────────────
            R_inner = int(R * 0.30)
            R_outer = int(R * 0.62)
            spoke_w = max(1, S // 80)
            for i in range(6):
                angle = math.radians(i * 60 - 30)
                x1 = cx + int(R_inner * math.cos(angle))
                y1 = cy + int(R_inner * math.sin(angle))
                x2 = cx + int(R_outer * math.cos(angle))
                y2 = cy + int(R_outer * math.sin(angle))
                d.line([x1, y1, x2, y2], fill=(*GLOW, 200), width=spoke_w)

            # ── 6 tick marks on outer ring ────────────────────────────────
            for i in range(6):
                angle = math.radians(i * 60)
                for dr in range(lw * 2):
                    rx = (R - lw - dr)
                    d.point(
                        [cx + int(rx * math.cos(angle)),
                         cy + int(rx * math.sin(angle))],
                        fill=(*WHITE, 220),
                    )

            # ── inner glowing ring ────────────────────────────────────────
            Ri = int(R * 0.26)
            d.ellipse([cx-Ri, cy-Ri, cx+Ri, cy+Ri],
                      outline=(*CYAN, 255), width=max(2, lw))

            # ── bright glow soft blur applied before core ─────────────────
            # (draw a slightly larger cyan circle on a separate layer)
            glow_layer = PIL.Image.new("RGBA", (S, S), (0, 0, 0, 0))
            gd = PIL.ImageDraw.Draw(glow_layer)
            Rc = int(R * 0.13)
            gd.ellipse([cx-Rc*2, cy-Rc*2, cx+Rc*2, cy+Rc*2],
                       fill=(*CYAN, 110))
            glow_layer = glow_layer.filter(PIL.ImageFilter.GaussianBlur(S // 14))
            img = PIL.Image.alpha_composite(img, glow_layer)
            d   = PIL.ImageDraw.Draw(img)

            # ── core dot ──────────────────────────────────────────────────
            d.ellipse([cx-Rc, cy-Rc, cx+Rc, cy+Rc], fill=(*WHITE, 255))

            # ── downscale to target size ──────────────────────────────────
            return img.resize((sz, sz), PIL.Image.LANCZOS)

        try:
            sizes  = [256, 128, 64, 48, 32, 16]
            frames = [_render(s) for s in sizes]
            frames[0].save(
                out_path,
                format="ICO",
                append_images=frames[1:],
                sizes=[(s, s) for s in sizes],
            )
            return True
        except Exception as e:
            print(f"[Shortcut] ⚠️  Icon generation failed: {e}")
            return False

    @staticmethod
    def _create_lnk_windows(lnk: str, target: str, args: str,
                             work_dir: str, icon_loc: str,
                             description: str = "VIERNES AI Assistant") -> None:
        """
        Create a Windows .lnk shortcut WITHOUT launching PowerShell or cmd.
        Tries win32com (pywin32) first; falls back to wscript.exe + VBScript.
        wscript.exe is a GUI-mode host — it never opens a console window.
        """
        # ── Option 1: pywin32 (pure Python COM, zero subprocess) ──────────
        try:
            from win32com.client import Dispatch   # type: ignore
            sh = Dispatch("WScript.Shell")
            sc = sh.CreateShortCut(lnk)
            sc.TargetPath       = target
            sc.Arguments        = f'"{args}"'
            sc.WorkingDirectory = work_dir
            sc.Description      = description
            sc.IconLocation     = icon_loc
            sc.save()
            return
        except ImportError:
            pass

        # ── Option 2: wscript.exe + VBScript (always available on Windows,
        #    GUI-mode executable — never opens a console window) ────────────
        vbs = "\n".join([
            'Set ws = CreateObject("WScript.Shell")',
            f'Set sc = ws.CreateShortcut("{lnk}")',
            f'sc.TargetPath = "{target}"',
            f'sc.Arguments = Chr(34) & "{args}" & Chr(34)',
            f'sc.WorkingDirectory = "{work_dir}"',
            f'sc.Description = "{description}"',
            f'sc.IconLocation = "{icon_loc}"',
            'sc.Save',
        ])
        import tempfile
        fd, tmp = tempfile.mkstemp(suffix=".vbs")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(vbs)
            proc = subprocess.Popen(
                ["wscript.exe", "/nologo", tmp],
                creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW,
            )
            proc.wait(timeout=10)
        finally:
            try:
                os.unlink(tmp)
            except Exception:
                pass

    @staticmethod
    def _get_desktop_dir() -> Path:
        """
        Resolve the user's REAL desktop directory instead of assuming
        ~/Desktop, which breaks when:
          • OneDrive "Known Folder Move" relocates the desktop
            (C:/Users/x/OneDrive/Desktop) — very common on Win 10/11;
          • the XDG desktop is localized on Linux (~/Masaüstü,
            ~/Schreibtisch, ~/Bureau, …).
        Falls back to ~/Desktop only as a last resort.
        """
        home = Path.home()
        _os = platform.system()

        if _os == "Windows":
            # ── 1) SHGetKnownFolderPath(FOLDERID_Desktop) — the canonical
            #       answer; follows OneDrive redirection. No dependencies. ──
            try:
                import ctypes
                from ctypes import wintypes

                class _GUID(ctypes.Structure):
                    _fields_ = [("Data1", wintypes.DWORD),
                                ("Data2", wintypes.WORD),
                                ("Data3", wintypes.WORD),
                                ("Data4", ctypes.c_ubyte * 8)]

                # FOLDERID_Desktop {B4BFCC3A-DB2C-424C-B029-7FE99A87C641}
                fid = _GUID(0xB4BFCC3A, 0xDB2C, 0x424C,
                            (ctypes.c_ubyte * 8)(0xB0, 0x29, 0x7F, 0xE9,
                                                 0x9A, 0x87, 0xC6, 0x41))
                buf = ctypes.c_wchar_p()
                if ctypes.windll.shell32.SHGetKnownFolderPath(
                        ctypes.byref(fid), 0, None, ctypes.byref(buf)) == 0:
                    p = Path(buf.value)
                    ctypes.windll.ole32.CoTaskMemFree(buf)
                    if p.is_dir():
                        return p
            except Exception:
                pass

            # ── 2) Registry: User Shell Folders (may contain %VARS%) ──────
            try:
                import winreg
                with winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER,
                        r"Software\Microsoft\Windows\CurrentVersion"
                        r"\Explorer\User Shell Folders") as key:
                    val, _t = winreg.QueryValueEx(key, "Desktop")
                p = Path(os.path.expandvars(val))
                if p.is_dir():
                    return p
            except Exception:
                pass

        elif _os == "Linux":
            # ── xdg-user-dir honours localized names (~/Masaüstü, …) ──────
            try:
                out = subprocess.run(["xdg-user-dir", "DESKTOP"],
                                     capture_output=True, text=True, timeout=5)
                p = Path(out.stdout.strip())
                if out.stdout.strip() and p != home and p.is_dir():
                    return p
            except Exception:
                pass
            try:
                cfg = home / ".config" / "user-dirs.dirs"
                for line in cfg.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line.startswith("XDG_DESKTOP_DIR"):
                        val = line.split("=", 1)[1].strip().strip('"')
                        p = Path(val.replace("$HOME", str(home)))
                        if p != home and p.is_dir():
                            return p
            except Exception:
                pass

        # macOS: ~/Desktop is always the real path (localization is
        # display-only). Everything else lands here as a last resort.
        return home / "Desktop"

    def _create_desktop_shortcut(self):
        """
        Create a desktop shortcut on Windows / macOS / Linux.
        Never opens a terminal, console, or PowerShell window on any platform.
        """
        import stat as _stat
        script  = Path(__file__).resolve().parent / "main.py"
        python  = Path(sys.executable)
        desktop = self._get_desktop_dir()

        asst_name = (getattr(self, "_assistant_name", None) or "Viernes").strip()
        asst_display = asst_name.upper()

        # Arc-reactor icon (.ico — also exported as .png for Linux/macOS)
        ico_path = Path(__file__).resolve().parent / "config" / "viernes.ico"
        if not ico_path.exists():
            self._build_viernes_icon(ico_path)

        try:
            _os = platform.system()

            # ── Windows ───────────────────────────────────────────────────────
            if _os == "Windows":
                pythonw  = python.parent / "pythonw.exe"
                target   = str(pythonw if pythonw.exists() else python)
                lnk_name = f"{asst_display}.lnk"
                lnk      = str(desktop / lnk_name)
                icon_loc = str(ico_path) if ico_path.exists() else f"{target},0"
                self._create_lnk_windows(lnk, target, str(script),
                                         str(script.parent), icon_loc,
                                         description=f"{asst_display} AI Assistant")
                # Remove obsolete J.A.R.V.I.S.lnk / JARVIS.lnk if it exists on desktop
                for old_name in ("J.A.R.V.I.S.lnk", "JARVIS.lnk", "Jarvis.lnk"):
                    old_lnk = desktop / old_name
                    if old_lnk.exists() and old_lnk.resolve() != Path(lnk).resolve():
                        try:
                            old_lnk.unlink()
                        except Exception:
                            pass

            # ── macOS — proper .app bundle (no Terminal window) ───────────────
            elif _os == "Darwin":
                app     = desktop / f"{asst_display}.app"
                mac_dir = app / "Contents" / "MacOS"
                res_dir = app / "Contents" / "Resources"
                mac_dir.mkdir(parents=True, exist_ok=True)
                res_dir.mkdir(exist_ok=True)

                # Launcher executable (bash — runs as background process,
                # macOS does NOT open Terminal for executables inside .app bundles)
                launcher = mac_dir / asst_display
                launcher.write_text(
                    "#!/usr/bin/env bash\n"
                    f'cd "{script.parent}"\n'
                    f'exec "{python}" "{script}"\n'
                )
                launcher.chmod(launcher.stat().st_mode
                               | _stat.S_IEXEC | _stat.S_IXGRP | _stat.S_IXOTH)

                # Minimal Info.plist (required for .app recognition)
                (app / "Contents" / "Info.plist").write_text(
                    '<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
                    '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
                    f'<plist version="1.0"><dict>\n'
                    f'  <key>CFBundleExecutable</key><string>{asst_display}</string>\n'
                    f'  <key>CFBundleIdentifier</key>'
                    f'<string>com.viernes.assistant</string>\n'
                    f'  <key>CFBundleName</key><string>{asst_display}</string>\n'
                    f'  <key>CFBundlePackageType</key><string>APPL</string>\n'
                    f'  <key>CFBundleVersion</key><string>1.0</string>\n'
                    f'</dict></plist>\n'
                )

                # Optional: copy icon as .icns (skip silently if Pillow is missing)
                try:
                    import PIL.Image
                    icns = res_dir / "AppIcon.icns"
                    PIL.Image.open(ico_path).save(icns, format="ICNS")
                    # Inject icon reference into plist
                    plist = app / "Contents" / "Info.plist"
                    txt = plist.read_text()
                    plist.write_text(
                        txt.replace(
                            '</dict></plist>',
                            '  <key>CFBundleIconFile</key>'
                            '<string>AppIcon</string>\n</dict></plist>\n',
                        )
                    )
                except Exception:
                    pass  # icon is optional

            # ── Linux — .desktop file (Terminal=false, no console) ────────────
            else:
                # Export .ico → .png for better desktop integration
                png_path = ico_path.with_suffix(".png")
                if not png_path.exists() and ico_path.exists():
                    try:
                        import PIL.Image
                        PIL.Image.open(ico_path).resize(
                            (256, 256), PIL.Image.LANCZOS
                        ).save(png_path, format="PNG")
                    except Exception:
                        png_path = ico_path  # fallback to .ico

                icon_line = f"Icon={png_path}\n" if png_path.exists() else ""
                desk = desktop / f"{asst_display}.desktop"
                desk.write_text(
                    "[Desktop Entry]\n"
                    f"Name={asst_display}\n"
                    f"Exec={python} {script}\n"
                    f"Path={script.parent}\n"
                    "Type=Application\n"
                    "Terminal=false\n"
                    "Categories=Utility;\n"
                    + icon_line
                )
                desk.chmod(desk.stat().st_mode | 0o755)

            self._log.append_log(f"SYS: Acceso directo de {asst_display} creado en el escritorio.")
        except Exception as e:
            self._log.append_log(f"ERR: Shortcut failed — {e}")

    def _toggle_fullscreen(self):
        if getattr(self, "_video_fullscreen", False):
            self._toggle_video_fullscreen()
            return
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
        self._update_fs_ui()
        QTimer.singleShot(0, self._fit_video)
        QTimer.singleShot(80, self._fit_video)

    def _toggle_video_fullscreen(self):
        entering = not getattr(self, "_video_fullscreen", False)
        self._video_fullscreen = entering
        if entering:
            self._video_fs_was_win_fs = self.isFullScreen()
            self._video_fs_saved_sizes = self._center_split.sizes()
            self._close_setup()
            self._close_controls()
            for attr in ("_header_widget", "_footer_widget", "_left_panel", "_right_panel", "_content_panel", "_quiz_panel"):
                w = getattr(self, attr, None)
                if w is not None:
                    w.hide()
            if not self.isFullScreen():
                self.showFullScreen()
        else:
            for attr in ("_header_widget", "_footer_widget", "_left_panel", "_right_panel", "_content_panel"):
                w = getattr(self, attr, None)
                if w is not None:
                    w.show()
            saved = getattr(self, "_video_fs_saved_sizes", None)
            if saved:
                self._center_split.setSizes(saved)
            if not getattr(self, "_video_fs_was_win_fs", False) and self.isFullScreen():
                self.showNormal()
        self._update_fs_ui()
        QTimer.singleShot(0, self._fit_video)
        QTimer.singleShot(80, self._fit_video)

    def _set_video_fullscreen(self, enabled: bool):
        want = bool(enabled)
        if bool(getattr(self, "_video_fullscreen", False)) != want:
            self._toggle_video_fullscreen()

    def _update_fs_ui(self):
        is_fs = self.isFullScreen()
        is_vfs = getattr(self, "_video_fullscreen", False)
        if hasattr(self, "_fs_hdr_btn"):
            self._fs_hdr_btn.setText("🗗" if is_fs else "⛶")
            self._fs_hdr_btn.setToolTip("Salir de Pantalla Completa [F11]" if is_fs else "Pantalla Completa [F11]")
        if hasattr(self, "_video_fs_btn"):
            self._video_fs_btn.setText("🗗  Salir pantalla completa" if is_vfs else "⛶  Pantalla completa")
        if hasattr(self, "hud") and hasattr(self.hud, "_btn_zen_fs"):
            self.hud._btn_zen_fs.setText("🗗 VENTANA [F11]" if is_fs else "⛶ PANTALLA COMPLETA [F11]")

    def _toggle_avatar_only(self):
        self._avatar_only = not getattr(self, "_avatar_only", False)
        is_zen = self._avatar_only

        if is_zen:
            self._saved_splitter_sizes = self._center_split.sizes()
            self._close_setup()
            self._close_controls()
            if hasattr(self, "_header_widget"):
                self._header_widget.hide()
            if hasattr(self, "_footer_widget"):
                self._footer_widget.hide()
            if hasattr(self, "_left_panel"):
                self._left_panel.hide()
            if hasattr(self, "_right_panel"):
                self._right_panel.hide()
            if hasattr(self, "_content_panel"):
                self._content_panel.hide()
            if hasattr(self, "_quiz_panel"):
                self._quiz_panel.hide()
            self.hud.set_zen_mode(True)
        else:
            if hasattr(self, "_header_widget"):
                self._header_widget.show()
            if hasattr(self, "_footer_widget"):
                self._footer_widget.show()
            if hasattr(self, "_left_panel"):
                self._left_panel.show()
            if hasattr(self, "_right_panel"):
                self._right_panel.show()
            if hasattr(self, "_content_panel"):
                self._content_panel.show()
            if hasattr(self, "_saved_splitter_sizes") and self._saved_splitter_sizes:
                self._center_split.setSizes(self._saved_splitter_sizes)
            self.hud.set_zen_mode(False)

        if hasattr(self, "_zen_hdr_btn"):
            self._zen_hdr_btn.setChecked(is_zen)
        if hasattr(self, "_zen_drawer_btn"):
            self._zen_drawer_btn.setText("🌸   Salir de modo avatar  ·  F10" if is_zen else "🌸   Modo avatar  ·  F10")

        self._update_fs_ui()

    def eventFilter(self, obj, event):
        if getattr(self, "_video_widget", None) is not None and obj is self._video_widget.viewport():
            if event.type() == QEvent.Type.Resize:
                QTimer.singleShot(0, self._fit_video)
        return super().eventFilter(obj, event)

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.Type.WindowStateChange:
            self._update_fs_ui()
            QTimer.singleShot(0, self._fit_video)
            QTimer.singleShot(80, self._fit_video)
            minimized = self.isMinimized()
            if minimized:
                _metrics.pause()
                self._metric_tmr.setInterval(10000)
                if hasattr(self, "hud") and self.hud is not None:
                    self.hud.pause()
            else:
                _metrics.resume()
                is_sleeping = getattr(self.hud, "state", "") == "SLEEPING"
                self._metric_tmr.setInterval(8000 if is_sleeping else 2000)
                if hasattr(self, "hud") and self.hud is not None:
                    self.hud.resume()

    def _cycle_background_mode(self):
        new_mode = self.hud.cycle_bg_mode()
        names = {
            "auto": "☀ AUTO (HORA REAL)",
            "morning": "🌅 MAÑANA",
            "day": "☀️ DÍA",
            "sunset": "🌇 ATARDECER",
            "night": "🌙 NOCHE",
        }
        lbl = names.get(new_mode, "☀ AUTO")
        if hasattr(self, "_bg_tod_btn"):
            self._bg_tod_btn.setText(f"🌅   Fondo: {lbl}")
        self._log.append_log(f"SYS: Fondo cambiado a {lbl}.")

    def _schedule_next_auto_animation(self, initial: bool = False):
        if not getattr(self, "_auto_animations_enabled", True):
            return
        # Initial action starts in 4-7 seconds; subsequent ones every 16-28 seconds
        delay_ms = random.randint(4500, 7500) if initial else random.randint(16000, 28000)
        if hasattr(self, "_auto_anim_timer"):
            self._auto_anim_timer.stop()
            self._auto_anim_timer.start(delay_ms)

    def _on_auto_anim_tick(self):
        if not getattr(self, "_auto_animations_enabled", True):
            return
        try:
            hud = getattr(self, "hud", None)
            if hud is not None:
                if getattr(hud, "_overlay_active", False):
                    self._schedule_next_auto_animation()
                    return
                if getattr(hud, "speaking", False) or getattr(hud, "state", "") in ("SLEEPING", "MUTED"):
                    self._schedule_next_auto_animation()
                    return
            if self.isMinimized() or self.isHidden() or getattr(self, "_muted", False):
                self._schedule_next_auto_animation()
                return

            self._trigger_random_avatar_action(log_action=False)
        except Exception:
            pass
        self._schedule_next_auto_animation()

    def _refresh_action_drawer_btn(self):
        enabled = getattr(self, "_auto_animations_enabled", True)
        if hasattr(self, "_action_drawer_btn") and self._action_drawer_btn:
            if enabled:
                self._action_drawer_btn.setText("✨   Animaciones automáticas: Sí")
                self._action_drawer_btn.setStyleSheet(_ss_row(on=True))
            else:
                self._action_drawer_btn.setText("✨   Animaciones automáticas: No")
                self._action_drawer_btn.setStyleSheet(_ss_row(on=False))

        if hasattr(self, "_anim_hdr_btn") and self._anim_hdr_btn:
            self._anim_hdr_btn.blockSignals(True)
            self._anim_hdr_btn.setChecked(enabled)
            self._anim_hdr_btn.setText("✨  Animación: ON" if enabled else "✨  Animación: OFF")
            self._anim_hdr_btn.blockSignals(False)

    def _toggle_auto_animations(self):
        cur = getattr(self, "_auto_animations_enabled", True)
        new_val = not cur
        self.set_auto_animations(new_val)
        if new_val:
            self._trigger_random_avatar_action(log_action=True)
            self._log.append_log("SYS: Animaciones automáticas activadas. Viernes se moverá periódicamente en reposo.")
        else:
            self._log.append_log("SYS: Animaciones automáticas desactivadas.")

    def set_auto_animations(self, enabled: bool):
        self._auto_animations_enabled = bool(enabled)
        try:
            from memory.config_manager import save_auto_animations_enabled
            save_auto_animations_enabled(self._auto_animations_enabled)
        except Exception:
            pass
        self._refresh_action_drawer_btn()
        if self._auto_animations_enabled:
            self._schedule_next_auto_animation(initial=False)
        else:
            if hasattr(self, "_auto_anim_timer"):
                self._auto_anim_timer.stop()

    def _trigger_random_avatar_action(self, log_action: bool = True):
        style = getattr(self.hud, "hud_style", "edith_live2d")
        act_desc = ""

        # 1. Edith Live2D Pro (Cubism 4)
        if (style == "edith_live2d" or getattr(self.hud, "_live2d_widget", None)) and getattr(self.hud, "_live2d_widget", None):
            edith_actions = [
                ("ELEGANT_BOW", "Reverencia distinguida", "polite"),
                ("THINKING_DEEP", "Reflexión estratégica", "thinking"),
                ("AGREE_WARM_NOD", "Asentimiento cálido", "cheerful"),
                ("EXPLAIN_POINT", "Explicación elocuente", "neutral"),
                ("ATTENTIVE_LEAN", "Escucha atenta y cercana", "curious"),
                ("CALM_BREATHE", "Respiración serena", "calm"),
                ("HAIR_ADJUST", "Acomodar flequillo", "cheerful"),
                ("CONFIDENT_CROSS", "Seguridad y compostura", "proud_smug"),
                ("WELCOME_PRESENT", "Presentación de cortesía", "happy"),
                ("GENTLE_SMILE_SWAY", "Balanceo sereno", "calm"),
                ("ENCOURAGE_CLAP", "Aplauso refinado", "happy"),
                ("GREETING_WAVE", "Saludo cortés", "happy"),
                ("HEAD_TILT_CURIOUS", "Curiosidad analítica", "curious"),
                ("LOOK_AROUND", "Observar el entorno", "neutral"),
                ("FIDGET_SWAY", "Balanceo rítmico", "calm"),
                ("STRETCH", "Estiramiento pausado", "relieved"),
                ("WINK_HAPPY", "Guiño sutil", "cheerful"),
                ("SHY_HIDE", "Modestia reservada", "shy"),
                ("BOB_DANCE", "Cadencia rítmica", "happy"),
            ]
            act_key, act_desc, act_emo = random.choice(edith_actions)
            self.hud.trigger_action(act_key)
            self.hud.set_emotion(act_emo, intensity=1.0, duration=3.8)

        # 2. Viernes 2D (Morphing)
        elif hasattr(self.hud, "_avatar") and self.hud._avatar is not None and hasattr(self.hud._avatar, "play_action"):
            actions = [
                "greeting_wave", "blush_shy", "giggle", "excited_sparkle",
                "proud_smug", "happy_cheer", "curious", "pout", "nod_yes", "wink_left", "wink_right"
            ]
            act_key = random.choice(actions)
            self.hud._avatar.play_action(act_key, duration=3.0)
            self.hud.update()
            act_desc = act_key

        # 3. Reactor Core
        else:
            if hasattr(self.hud, "energy"):
                self.hud.energy = 1.0
            self.hud.update()
            act_desc = "Pulso de energía del núcleo"

        if act_desc and log_action:
            self._log.append_log(f"SYS: Animación ejecutada ({act_desc}).")

    def _cycle_theme_preset(self):
        from memory.config_manager import load_api_keys
        cfg = _read_full_config()
        cur_clr = cfg.get("ui_color") or DEFAULT_UI_COLOR
        k, name, new_hex = cycle_ui_theme(cur_clr)
        old_pal = current_palette()
        if apply_ui_accent(new_hex):
            retheme_all_widgets(old_pal, current_palette())
            self.hud.update()
            if hasattr(self, "_theme_cycle_btn"):
                self._theme_cycle_btn.setText(f"🎨   Tema: {name}")
            data = load_api_keys()
            data["ui_color"] = new_hex
            API_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")
            self._log.append_log(f"SYS: Tema visual cambiado a {name} ({new_hex}).")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cw = self.centralWidget()
        if self._overlay and self._overlay.isVisible():
            ow, oh = 460, 390
            self._overlay.setGeometry(
                (cw.width()  - ow) // 2,
                (cw.height() - oh) // 2,
                ow, oh,
            )
        if self._remote_overlay and self._remote_overlay.isVisible():
            ow, oh = RemoteKeyOverlay._OW, RemoteKeyOverlay._OH
            self._remote_overlay.setGeometry(
                (cw.width()  - ow) // 2,
                (cw.height() - oh) // 2,
                ow, oh,
            )
        if self._customize_overlay and self._customize_overlay.isVisible():
            ow, oh = CustomizeOverlay._OW, CustomizeOverlay._OH
            self._customize_overlay.setGeometry(
                (cw.width()  - ow) // 2,
                (cw.height() - oh) // 2,
                ow, oh,
            )
        if hasattr(self, "_research_overlay") and self._research_overlay and self._research_overlay.isVisible():
            rw = min(960, int(cw.width() * 0.92))
            rh = min(700, int(cw.height() * 0.90))
            self._research_overlay.setGeometry(
                (cw.width() - rw) // 2,
                (cw.height() - rh) // 2,
                rw, rh,
            )
        if hasattr(self, "_plugin_settings_overlay") and self._plugin_settings_overlay and self._plugin_settings_overlay.isVisible():
            ow = min(PluginSettingsOverlay._OW, cw.width() - 20)
            oh = min(580, max(460, cw.height() - 24))
            self._plugin_settings_overlay.setGeometry(
                (cw.width()  - ow) // 2,
                (cw.height() - oh) // 2,
                ow, oh,
            )
        # Camera preview — bottom-right corner of the center/HUD area
        if hasattr(self, '_cam_preview') and self._cam_preview.isVisible():
            self._position_cam_preview()
        # Clipboard panel — bottom-center
        if hasattr(self, '_clipboard_panel') and self._clipboard_panel.isVisible():
            self._position_clipboard_panel()
        # Quick drawer — reposition if open
        if hasattr(self, '_avatar_drawer') and self._avatar_drawer.isVisible():
            self._position_avatar_drawer()
            if hasattr(self, "hud") and hasattr(self.hud, "_update_vrm_geometry"):
                self.hud._update_vrm_geometry()
        if hasattr(self, '_quick_drawer') and self._quick_drawer.isVisible():
            self._position_quick_drawer()
        if hasattr(self, '_ctrl_drawer') and self._ctrl_drawer.isVisible():
            self._position_ctrl_drawer()
        self._fit_video()

    def _update_metrics(self):
        snap = _metrics.snapshot()

        # CPU
        cpu = snap["cpu"]
        self._bar_cpu.set_value(cpu, f"{cpu:.0f}%")

        # MEM
        mem = snap["mem"]
        self._bar_mem.set_value(mem, f"{mem:.0f}%")

        # NET
        net = snap["net"]
        if net < 1.0:
            net_str = f"{net*1024:.0f}KB/s"
        else:
            net_str = f"{net:.1f}MB/s"
        net_pct = min(100, net * 10)  # 10 MB/s = %100
        self._bar_net.set_value(net_pct, net_str)

        # GPU
        gpu = snap["gpu"]
        if gpu >= 0:
            self._bar_gpu.set_value(gpu, f"{gpu:.0f}%")
        else:
            self._bar_gpu.set_value(0, "N/A")

        # TMP
        tmp = snap["tmp"]
        if tmp >= 0:
            tmp_pct = min(100, (tmp / 100) * 100)
            self._bar_tmp.set_value(tmp_pct, f"{tmp:.0f}°C")
        else:
            self._bar_tmp.set_value(0, "N/A")

        try:
            boot_t  = psutil.boot_time()
            elapsed = time.time() - boot_t
            h = int(elapsed // 3600)
            m = int((elapsed % 3600) // 60)
            self._uptime_lbl.setText(f"{h}h {m:02d}m")
        except Exception:
            self._uptime_lbl.setText("--")

        try:
            proc_count = len(psutil.pids())
            self._proc_lbl.setText(f"{proc_count}")
        except Exception:
            self._proc_lbl.setText("--")


    def _build_header(self) -> QWidget:
        w = QWidget()
        w.setObjectName("Header")
        w.setFixedHeight(_HEADER_H)
        w.setStyleSheet(f"""
            QWidget#Header {{
                background: {C.BG};
                border-bottom: 1px solid {C.BORDER};
            }}
        """)
        lay = QHBoxLayout(w)
        lay.setContentsMargins(20, 0, 18, 0)
        lay.setSpacing(12)

        # Brand — Editorial Studio Monogram + Wordmark + Status Badge
        brand_box = QHBoxLayout()
        brand_box.setSpacing(10)

        self._brand_logo = QLabel((self._assistant_name[:1] or "V").upper())
        self._brand_logo.setFixedSize(30, 30)
        self._brand_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._brand_logo.setFont(QFont(UI_FONT, 11, QFont.Weight.Bold))
        self._brand_logo.setStyleSheet(f"""
            QLabel {{
                color: {C.WHITE};
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {C.PRI}, stop:1 {C.PRI_DIM});
                border: 1px solid {_rgba(C.WHITE, 0.16)};
                border-radius: 8px;
            }}
        """)
        self._logo_lbl = self._brand_logo
        brand_box.addWidget(self._brand_logo)

        title_col = QVBoxLayout()
        title_col.setContentsMargins(0, 0, 0, 0)
        title_col.setSpacing(0)
        self._title_lbl = QLabel(self._assistant_name)
        tf = QFont(UI_FONT, 11, QFont.Weight.DemiBold)
        tf.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0.2)
        self._title_lbl.setFont(tf)
        self._title_lbl.setStyleSheet(f"color: {C.WHITE}; background: transparent;")
        title_col.addWidget(self._title_lbl)

        self._sub_lbl = QLabel("Estudio personal")
        self._sub_lbl.setFont(QFont(UI_FONT, 8))
        self._sub_lbl.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent;")
        title_col.addWidget(self._sub_lbl)
        brand_box.addLayout(title_col)

        brand_box.addSpacing(4)
        self._status_pill = QLabel("●  En línea")
        self._status_pill.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        self._status_pill.setStyleSheet(f"""
            QLabel {{
                color: {C.GREEN};
                background: {_rgba(C.GREEN, 0.10)};
                border: 1px solid {_rgba(C.GREEN, 0.25)};
                border-radius: 11px;
                padding: 3px 10px;
            }}
        """)
        brand_box.addWidget(self._status_pill)

        lay.addLayout(brand_box)
        lay.addStretch()

        # Centre — Segmented workspace switcher (Linear / Raycast inspired)
        bar = QFrame(); bar.setObjectName("ToolBar")
        bar.setStyleSheet(f"""
            QFrame#ToolBar {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER};
                border-radius: 10px;
            }}
        """)
        bl = QHBoxLayout(bar); bl.setContentsMargins(4, 4, 4, 4); bl.setSpacing(3)

        def _tool(text, tip, slot, checkable=True, width=None):
            b = QPushButton(text)
            b.setFixedHeight(32)
            if width:
                b.setFixedWidth(width)
            b.setFont(QFont(UI_FONT, 9, QFont.Weight.Medium))
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setToolTip(tip)
            b.setCheckable(checkable)
            b.setStyleSheet(_ss_tool())
            b.clicked.connect(slot)
            bl.addWidget(b)
            return b

        self._avatar_hdr_btn = _tool("Presencia  ▾", "Ajustes de presencia y avatar interactivo  [F10]", self._toggle_avatar_drawer)
        self._integrations_hdr_btn = _tool("Integraciones", "Centro de integraciones y servicios conectados  [F8]",
                                           self._show_integrations_overlay, checkable=False)
        self._research_hdr_btn = _tool("Investigar", "Estación de investigación documental y web  [F9]",
                                       self._toggle_research_panel, checkable=False)
        self._vision_hdr_btn = _tool("📷  OpenCV", "Visión por computadora en tiempo real con OpenCV",
                                     self._toggle_realtime_vision, checkable=True)
        self._hud_studio_hdr_btn = _tool("✦  HUD Studio", "Personalizar diseño, tema, módulos y layout del HUD",
                                         self._open_hud_studio, checkable=False)
        self._focus_hdr_btn = _tool("◧", "Alternar paneles laterales (Modo Enfoque)",
                                    self._toggle_focus_panels, checkable=False, width=36)
        self._fs_hdr_btn = _tool("⛶", "Pantalla completa  [F11]", self._toggle_fullscreen,
                                 checkable=False, width=36)

        # Backward compatibility pointers
        self._zen_hdr_btn = self._avatar_hdr_btn
        self._anim_hdr_btn = None
        self._api_keys_hdr_btn = None
        lay.addWidget(bar)
        lay.addStretch()

        # Right — Editorial Clock + Quick Drawers
        clock = QVBoxLayout(); clock.setSpacing(0)
        self._clock_lbl = QLabel("00:00")
        cf = QFont(UI_FONT, 13, QFont.Weight.DemiBold)
        cf.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0.5)
        self._clock_lbl.setFont(cf)
        self._clock_lbl.setStyleSheet(f"color: {C.WHITE}; background: transparent;")
        self._clock_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        clock.addWidget(self._clock_lbl)
        self._date_lbl = QLabel("")
        df = QFont(UI_FONT, 8)
        self._date_lbl.setFont(df)
        self._date_lbl.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent;")
        self._date_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        clock.addWidget(self._date_lbl)
        lay.addLayout(clock)
        lay.addSpacing(10)

        def _icon(glyph, tip, slot):
            b = QPushButton(glyph)
            b.setFixedSize(34, 34)
            b.setFont(QFont(UI_FONT, 11))
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setToolTip(tip)
            b.setCheckable(True)
            b.setStyleSheet(_ss_icon())
            b.clicked.connect(slot)
            lay.addWidget(b)
            return b

        self._ctrl_btn = _icon("🎛", "Controles rápidos de sesión", self._toggle_controls)
        self._drawer_btn = _icon("⚙", "Configuración general", self._toggle_drawer)
        return w

    def _update_status_pill(self, state: str) -> None:
        if not hasattr(self, "_status_pill") or not self._status_pill.isVisible():
            return
        label, col = {
            "LISTENING":  ("Escuchando", C.GREEN),
            "SPEAKING":   ("Hablando", C.ACC),
            "THINKING":   ("Razonando…", C.ACC2),
            "PROCESSING": ("Procesando…", C.ACC2),
            "MUTED":      ("Silenciado", C.MUTED_C),
            "SLEEPING":   ("En reposo", C.TEXT_DIM),
        }.get((state or "").upper(), ("En línea", C.GREEN))
        self._status_pill.setText(f"●  {label}")
        self._status_pill.setStyleSheet(f"""
            QLabel {{
                color: {col};
                background: {_rgba(col, 0.10)};
                border: 1px solid {_rgba(col, 0.25)};
                border-radius: 11px;
                padding: 3px 10px;
            }}
        """)

    def _tick_clock(self):
        _d = ("Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom")
        _m = ("ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic")
        t = time.localtime()
        self._clock_lbl.setText(time.strftime("%H:%M", t))
        self._date_lbl.setText(f"{_d[t.tm_wday]}, {t.tm_mday} {_m[t.tm_mon - 1]}")

    def _card(self, title: str | None = None, margins=(14, 12, 14, 14)):
        """Elevated architectural surface container with subtle gradient & border."""
        rad = int(getattr(self, "_hud_cfg", {}).get("card_radius", 12))
        f = QFrame(); f.setObjectName("Card")
        f.setStyleSheet(f"""
            QFrame#Card {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {C.PANEL2}, stop:0.18 {C.PANEL}, stop:1 {C.PANEL});
                border: 1px solid {C.BORDER};
                border-top: 1px solid {C.BORDER_B};
                border-radius: {rad}px;
            }}
            QFrame#Card QLabel {{
                background: transparent;
                border: none;
            }}
        """)
        l = QVBoxLayout(f); l.setContentsMargins(*margins); l.setSpacing(8)
        if title:
            l.addWidget(self._section_lbl(title))
        return f, l

    @staticmethod
    def _section_lbl(text: str) -> QLabel:
        l = QLabel(text)
        f = QFont(UI_FONT, 9, QFont.Weight.DemiBold)
        f.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 0.3)
        l.setFont(f)
        l.setStyleSheet(f"color: {C.TEXT_MED}; background: transparent; border: none; padding-bottom: 1px;")
        return l

    @staticmethod
    def _hline() -> QFrame:
        ln = QFrame(); ln.setFixedHeight(1)
        ln.setStyleSheet(f"background: {C.BORDER_A}; border: none;")
        return ln

    def _build_left_panel(self) -> QWidget:
        w = QWidget(); w.setObjectName("LeftPanel")
        w.setFixedWidth(_LEFT_W)
        w.setStyleSheet("QWidget#LeftPanel { background: transparent; }")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        # 1. Canal de Voz y Presencia
        vcard, vl = self._card("Voz y presencia", (12, 10, 12, 10))
        self._vcard = vcard
        self._voice_monitor = VoiceVisualizerWidget()
        vl.addWidget(self._voice_monitor)
        lay.addWidget(vcard)

        # 2. Contexto climático local
        wcard, wl = self._card("Clima local", (12, 10, 12, 10))
        self._wcard = wcard
        self._weather_widget = WeatherWidget()
        wl.addWidget(self._weather_widget)
        lay.addWidget(wcard)

        # 3. Diagnóstico del equipo (compacto y colapsable)
        card, cl = self._card(None, (12, 10, 12, 10))
        self._syscard = card
        cl.setSpacing(5)

        sys_hdr = QHBoxLayout()
        sys_hdr.setContentsMargins(0, 0, 0, 0)
        sys_hdr.addWidget(self._section_lbl("Diagnóstico del equipo"))
        sys_hdr.addStretch()
        self._sys_toggle_btn = QPushButton("▾")
        self._sys_toggle_btn.setFixedSize(22, 20)
        self._sys_toggle_btn.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        self._sys_toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._sys_toggle_btn.setToolTip("Mostrar / ocultar métricas del sistema")
        self._sys_toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {C.TEXT_DIM};
                border: none; border-radius: 4px;
            }}
            QPushButton:hover {{ color: {C.TEXT}; background: {C.PANEL2}; }}
        """)
        sys_hdr.addWidget(self._sys_toggle_btn)
        cl.addLayout(sys_hdr)

        self._sys_body = QWidget()
        self._sys_body.setStyleSheet("background: transparent;")
        sbl = QVBoxLayout(self._sys_body)
        sbl.setContentsMargins(0, 2, 0, 0)
        sbl.setSpacing(4)

        self._bar_cpu = MetricBar("Procesador", C.PRI)
        self._bar_mem = MetricBar("Memoria", "#8B87F8")
        self._bar_net = MetricBar("Red", C.GREEN)
        self._bar_gpu = MetricBar("Gráficos", "#60A5FA")
        self._bar_tmp = MetricBar("Temperatura", C.ACC)
        for bar in (self._bar_cpu, self._bar_mem, self._bar_net, self._bar_gpu, self._bar_tmp):
            sbl.addWidget(bar)
        sbl.addSpacing(2)
        sbl.addWidget(self._hline())
        sbl.addSpacing(1)

        def _kv(key: str, val: QLabel):
            row = QHBoxLayout(); row.setSpacing(6)
            k = QLabel(key)
            k.setFont(QFont(UI_FONT, 8))
            k.setStyleSheet(f"color: {C.TEXT_DIM};")
            val.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
            val.setStyleSheet(f"color: {C.TEXT_MED};")
            val.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            row.addWidget(k); row.addStretch(); row.addWidget(val)
            sbl.addLayout(row)

        self._uptime_lbl = QLabel("--")
        self._proc_lbl = QLabel("--")
        os_name = {"Windows": "Windows 11", "Darwin": "macOS", "Linux": "Linux"}.get(_OS, _OS)
        _kv("Sesión activa", self._uptime_lbl)
        _kv("Procesos", self._proc_lbl)
        _kv("Entorno", QLabel(os_name))
        cl.addWidget(self._sys_body)

        def _toggle_sys():
            vis = not self._sys_body.isVisible()
            self._sys_body.setVisible(vis)
            self._sys_toggle_btn.setText("▾" if vis else "▸")

        self._sys_toggle_btn.clicked.connect(_toggle_sys)
        lay.addWidget(card)

        lay.addStretch()
        return w

    def _build_right_panel(self) -> QWidget:
        w = QWidget(); w.setObjectName("RightPanel")
        w.setFixedWidth(_RIGHT_W)
        w.setStyleSheet("QWidget#RightPanel { background: transparent; }")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        # Conversation Stream
        conv, cl = self._card(None, (14, 12, 10, 10))
        hdr = QHBoxLayout()
        hdr.addWidget(self._section_lbl("Conversación"))
        hdr.addStretch()
        clr = QPushButton("Limpiar")
        clr.setFont(QFont(UI_FONT, 8, QFont.Weight.Medium))
        clr.setFixedHeight(24)
        clr.setCursor(Qt.CursorShape.PointingHandCursor)
        clr.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {C.TEXT_DIM};
                border: 1px solid {C.BORDER};
                border-radius: 6px;
                padding: 0 9px;
            }}
            QPushButton:hover {{
                background: {C.PANEL2};
                color: {C.TEXT};
                border-color: {C.BORDER_B};
            }}
        """)
        hdr.addWidget(clr)
        cl.addLayout(hdr)
        self._log = LogWidget()
        self._log._ai_name_lc = self._assistant_name.lower()
        clr.clicked.connect(self._log.clear)
        cl.addWidget(self._log, stretch=1)
        lay.addWidget(conv, stretch=1)

        # Compact Attachment Tray
        files, fl = self._card(None, (12, 8, 12, 8))
        self._attach_card = files
        fl.setSpacing(5)
        f_hdr = QHBoxLayout(); f_hdr.setContentsMargins(0, 0, 0, 0); f_hdr.setSpacing(6)
        f_hdr.addWidget(self._section_lbl("Contexto adjunto"))
        f_hdr.addStretch()
        browse_btn = QPushButton("Explorar…")
        browse_btn.setFixedHeight(22)
        browse_btn.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {C.TEXT_MED};
                border: 1px solid {C.BORDER};
                border-radius: 6px;
                padding: 0 8px;
            }}
            QPushButton:hover {{
                background: {C.PANEL2};
                color: {C.WHITE};
                border-color: {C.BORDER_B};
            }}
        """)
        f_hdr.addWidget(browse_btn)
        fl.addLayout(f_hdr)

        self._drop_zone = FileDropZone()
        self._drop_zone.file_selected.connect(self._on_file_selected)
        self._drop_zone.file_cleared.connect(self._on_file_cleared)
        browse_btn.clicked.connect(self._drop_zone._browse)
        fl.addWidget(self._drop_zone)

        self._file_hint = QLabel("Sin archivos adjuntos")
        self._file_hint.setFont(QFont(UI_FONT, 8))
        self._file_hint.setStyleSheet(f"color: {C.TEXT_DIM};")
        self._file_hint.setWordWrap(True)
        fl.addWidget(self._file_hint)
        lay.addWidget(files)

        # Command & Voice Composer
        comp, ml = self._card(None, (10, 10, 10, 10))
        ml.setSpacing(8)
        ml.addLayout(self._build_input_row())
        acts = QHBoxLayout(); acts.setSpacing(6)
        self._mute_btn = QPushButton()
        self._mute_btn.setFixedHeight(34)
        self._mute_btn.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        self._mute_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._mute_btn.setToolTip("Activar / silenciar micrófono  [F4]")
        self._mute_btn.clicked.connect(self._toggle_mute)
        self._style_mute_btn()
        acts.addWidget(self._mute_btn, stretch=1)

        self._wake_act_btn = QPushButton("🎙️  Palabra de activación")
        self._wake_act_btn.setFixedHeight(34)
        self._wake_act_btn.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        self._wake_act_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._wake_act_btn.setToolTip("Activar / desactivar palabra de activación")
        self._wake_act_btn.clicked.connect(self._toggle_wake_word)
        acts.addWidget(self._wake_act_btn, stretch=1)

        self._interrupt_btn = QPushButton("Detener")
        self._interrupt_btn.setFixedSize(68, 34)
        self._interrupt_btn.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        self._interrupt_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._interrupt_btn.setToolTip("Interrumpir respuesta actual  [Esc]")
        self._interrupt_btn.setStyleSheet(_ss_soft_btn(C.RED))
        self._interrupt_btn.clicked.connect(self._do_interrupt)
        acts.addWidget(self._interrupt_btn)
        ml.addLayout(acts)
        lay.addWidget(comp)
        return w

    def _drawer_title(self, text: str) -> QLabel:
        l = QLabel(text)
        f = QFont(UI_FONT, 10, QFont.Weight.DemiBold)
        l.setFont(f)
        l.setStyleSheet(f"color: {C.WHITE}; background: transparent; padding: 2px 12px 6px 12px;")
        return l

    def _drawer_section(self, text: str) -> QWidget:
        box = QWidget(); box.setStyleSheet("background: transparent;")
        bl = QVBoxLayout(box); bl.setContentsMargins(12, 8, 12, 2)
        bl.addWidget(self._section_lbl(text))
        return box

    def _build_quick_drawer(self) -> QWidget:
        """Floating setup panel shown when the ⚙ header button is toggled."""
        self._BTN_PRI, self._BTN_DIM = _ss_row(accent=True), _ss_row()
        w = QWidget(self.centralWidget())
        w.setObjectName("QuickDrawer")
        w.setStyleSheet(_ss_drawer())
        w.hide()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(8, 12, 8, 8)
        lay.setSpacing(2)
        lay.addWidget(self._drawer_title("Configuración"))

        def _row(text, slot=None, style=None):
            b = QPushButton(text)
            b.setFixedHeight(32)
            b.setFont(QFont(UI_FONT, 9))
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setStyleSheet(style or self._BTN_DIM)
            if slot:
                def _make_slot(s):
                    return lambda: (self._close_setup(), s())
                b.clicked.connect(_make_slot(slot))
            lay.addWidget(b)
            return b

        lay.addWidget(self._drawer_section("Asistente"))
        _row("✦   HUD Studio (Diseño y Layout)", self._open_hud_studio, self._BTN_PRI)
        _row("🎨   Personalizar asistente y voz", self._open_customize, self._BTN_PRI)
        _row("🔑   Claves API y proveedores", self._open_api_keys_dialog, self._BTN_PRI)
        _row("🎧   Dispositivos de audio", self._open_audio_devices)
        _row("🧠   Memoria personal", self._open_memory_panel)
        _row("📚   Biblioteca cognitiva (PDF)", self._open_books_library)
        lay.addWidget(self._drawer_section("Extensiones"))
        _row("🧩   Gestor de extensiones", self._open_plugin_manager)
        _row("⚙   Parámetros de módulos", self._open_plugin_settings)
        lay.addWidget(self._drawer_section("Sistema"))
        _row("🧹   Clean Your TV (Limpiar TV)", lambda: self._open_cleanyourtv(""))
        _row("📱   Control remoto móvil", self._open_remote)
        _row("🖥   Crear acceso directo", self._create_desktop_shortcut)
        self._autostart_btn = _row("⏻   Inicio automático", self._toggle_autostart)
        w.adjustSize()
        return w

    def _build_controls_drawer(self) -> QWidget:
        """The switches that get flicked every day, in their own panel."""
        w = QWidget(self.centralWidget())
        w.setObjectName("QuickDrawer")
        w.setStyleSheet(_ss_drawer())
        w.hide()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(8, 12, 8, 8)
        lay.setSpacing(2)
        lay.addWidget(self._drawer_title("Controles rápidos"))

        def _row(button, style=None, height=32):
            button.setFixedHeight(height)
            button.setFont(QFont(UI_FONT, 9))
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            if style:
                button.setStyleSheet(style)
            lay.addWidget(button)
            return button

        lay.addWidget(self._drawer_section("Voz y escucha"))
        self._wake_btn = _row(QPushButton())
        self._wake_btn.clicked.connect(self._toggle_wake_word)
        self._wake_sleep_btn = _row(QPushButton())
        self._wake_sleep_btn.clicked.connect(self._tap_wake_manual)
        self._wake_btn.setText("🎙   Palabra de activación")
        self._wake_btn.setStyleSheet(self._BTN_DIM)
        self._wake_sleep_btn.hide()
        self._brief_btn = _row(QPushButton())
        self._brief_btn.clicked.connect(self._toggle_brief)
        self._ptt_btn = _row(QPushButton())
        self._ptt_btn.clicked.connect(self._toggle_ptt)
        self._refresh_talk_btns()

        lay.addWidget(self._drawer_section("Entorno visual"))
        fs_btn = _row(QPushButton("⛶   Pantalla completa  ·  F11"), self._BTN_DIM)
        fs_btn.clicked.connect(self._toggle_fullscreen)
        self._zen_drawer_btn = _row(QPushButton("🌸   Modo enfoque  ·  F10"), self._BTN_DIM)
        self._zen_drawer_btn.clicked.connect(self._toggle_avatar_only)
        self._bg_tod_btn = _row(QPushButton("🌅   Ambiente: Automático"), self._BTN_DIM)
        self._bg_tod_btn.clicked.connect(self._cycle_background_mode)
        cur_clr = (_read_full_config().get("ui_color") or DEFAULT_UI_COLOR).lower()
        self._theme_cycle_btn = _row(QPushButton(f"🎨   Tema: {get_theme_label(cur_clr)}"), self._BTN_DIM)
        self._theme_cycle_btn.clicked.connect(self._cycle_theme_preset)

        lay.addWidget(self._drawer_section("Capacidades activas"))
        avatar_hub_btn = _row(QPushButton("🎭   Presencia y avatar  ▾"), self._BTN_PRI)
        avatar_hub_btn.clicked.connect(lambda: (self._close_controls(), self._toggle_avatar_drawer(True)))
        self._vision_drawer_btn = _row(QPushButton("📷   OpenCV (Cámara y detección)"), self._BTN_DIM)
        self._vision_drawer_btn.clicked.connect(self._toggle_realtime_vision)
        self._device_ctrl_drawer_btn = _row(QPushButton("🖥   Device Control (Red y TVs)"), self._BTN_DIM)
        self._device_ctrl_drawer_btn.clicked.connect(lambda: (self._close_controls(), self._open_device_control()))
        self._local_ai_drawer_btn = _row(QPushButton("🧠   IA Local y Visión (Ollama)"), self._BTN_DIM)
        self._local_ai_drawer_btn.clicked.connect(self._show_local_ai_status)
        self._sports_drawer_btn = _row(QPushButton("⚽   TV Deportiva y AdBlock"), self._BTN_DIM)
        self._sports_drawer_btn.clicked.connect(lambda: (self._close_controls(), self._open_sports_settings()))

        # Retain hidden widgets for backwards compatibility with dynamic updaters
        self._hud_btn = QPushButton(); self._hud_btn.hide()
        self._skin_btn = QPushButton(); self._skin_btn.hide()
        self._edith_btn = QPushButton(); self._edith_btn.hide()
        self._action_drawer_btn = QPushButton(); self._action_drawer_btn.hide()
        self._research_drawer_btn = QPushButton(); self._research_drawer_btn.hide()
        self._integrations_drawer_btn = QPushButton(); self._integrations_drawer_btn.hide()
        self._api_keys_drawer_btn = QPushButton(); self._api_keys_drawer_btn.hide()
        self._books_drawer_btn = QPushButton(); self._books_drawer_btn.hide()

        w.adjustSize()
        return w

    def _warm_wake_state(self) -> None:
        """Work out the wake-word state off the UI thread, once."""
        def work():
            try:
                self._wake_state()
            except Exception:
                pass
            try:
                self._wake_btns_sig.emit()
            except Exception:
                pass
        threading.Thread(target=work, daemon=True, name="wake-state-warm").start()

    def _toggle_avatar_drawer(self, checked: bool | None = None):
        if not hasattr(self, "_avatar_drawer"):
            return
        is_open = self._avatar_drawer.isVisible()
        show = not is_open if checked is None else bool(checked)
        if show:
            self._close_setup()
            self._close_controls()
            self._position_avatar_drawer()
            self._avatar_drawer.refresh_state()
            self._avatar_drawer.show()
            self._avatar_drawer.raise_()
            if hasattr(self, "_avatar_hdr_btn"):
                self._avatar_hdr_btn.setChecked(True)
            if hasattr(self, "hud") and hasattr(self.hud, "_update_vrm_geometry"):
                self.hud._update_vrm_geometry()
            if hasattr(self, "hud") and hasattr(self.hud, "_live2d_widget") and self.hud._live2d_widget:
                try:
                    self.hud._live2d_widget.glance(-0.35, -0.05, 3.5)
                except Exception:
                    pass
        else:
            self._close_avatar()

    def _close_avatar(self):
        if hasattr(self, "_avatar_drawer"):
            self._avatar_drawer.hide()
        if hasattr(self, "_avatar_hdr_btn"):
            self._avatar_hdr_btn.setChecked(False)
        if hasattr(self, "hud") and hasattr(self.hud, "_update_vrm_geometry"):
            self.hud._update_vrm_geometry()

    def _position_avatar_drawer(self):
        if not hasattr(self, "_avatar_drawer"):
            return
        cw = self.centralWidget()
        _W = getattr(self._avatar_drawer, "_WIDTH", 340)
        if hasattr(self, "hud") and self.hud is not None:
            try:
                hud_pt = cw.mapFromGlobal(self.hud.mapToGlobal(QPoint(12, 12)))
                left = hud_pt.x()
                top = hud_pt.y()
            except Exception:
                top = _HEADER_H + 16
                left = _LEFT_W + 28
            max_h = max(340, min(560, self.hud.height() - 24))
        else:
            top = _HEADER_H + 16
            left = _LEFT_W + 28
            max_h = max(340, min(560, cw.height() - top - 32))
        self._avatar_drawer.setFixedWidth(_W)
        self._avatar_drawer.setFixedHeight(max_h)
        self._avatar_drawer.move(left, top)
        self._avatar_drawer.raise_()

    def _toggle_drawer(self, checked: bool):
        if checked:
            self._close_controls()
            self._close_avatar()
            self._position_quick_drawer()
            self._quick_drawer.show()
            self._quick_drawer.raise_()
        else:
            self._quick_drawer.hide()

    def _toggle_controls(self, checked: bool):
        if checked:
            self._close_setup()
            self._close_avatar()
            self._refresh_wake_btns()
            self._position_ctrl_drawer()
            self._ctrl_drawer.show()
            self._ctrl_drawer.raise_()
        else:
            self._ctrl_drawer.hide()

    def _close_setup(self):
        if hasattr(self, "_quick_drawer"):
            self._quick_drawer.hide()
        if hasattr(self, "_drawer_btn"):
            self._drawer_btn.setChecked(False)

    def _close_controls(self):
        if hasattr(self, "_ctrl_drawer"):
            self._ctrl_drawer.hide()
        if hasattr(self, "_ctrl_btn"):
            self._ctrl_btn.setChecked(False)

    def _place_drawer(self, drawer, anchor=None, width=None):
        """Drop a drawer just under its header button, intelligently positioned."""
        _W = width or getattr(drawer, "_WIDTH", 268)
        cw = self.centralWidget()
        drawer.setFixedWidth(_W)
        drawer.adjustSize()
        left, top = cw.width() - _W - 12, _HEADER_H + 6
        if anchor is not None:
            try:
                g_orig = anchor.mapToGlobal(QPoint(0, anchor.height()))
                anchor_origin = cw.mapFromGlobal(g_orig)
                if anchor_origin.x() < cw.width() // 2:
                    left, top = anchor_origin.x(), anchor_origin.y() + 8
                else:
                    g_pt = anchor.mapToGlobal(QPoint(anchor.width(), anchor.height()))
                    pt = cw.mapFromGlobal(g_pt)
                    left, top = pt.x() - _W, pt.y() + 8
            except Exception:
                pass
        left = max(12, min(left, cw.width() - _W - 12))
        drawer.setGeometry(left, top, _W, drawer.sizeHint().height())

    def _position_quick_drawer(self):
        if hasattr(self, "_quick_drawer"):
            self._place_drawer(self._quick_drawer, getattr(self, "_drawer_btn", None))

    def _position_ctrl_drawer(self):
        if hasattr(self, "_ctrl_drawer"):
            self._place_drawer(self._ctrl_drawer, getattr(self, "_ctrl_btn", None))

    def _build_input_row(self) -> QHBoxLayout:
        row = QHBoxLayout(); row.setSpacing(8)
        self._input = QLineEdit()
        self._input.setPlaceholderText(f"Escribe un mensaje o instrucción para {self._assistant_name}…")
        self._input.setFont(QFont(UI_FONT, 10))
        self._input.setFixedHeight(40)
        self._input.setStyleSheet(f"""
            QLineEdit {{
                background: {C.DARK};
                color: {C.WHITE};
                border: 1px solid {C.BORDER_B};
                border-radius: 10px;
                padding: 0 14px;
                selection-background-color: {C.PRI_GHO};
            }}
            QLineEdit:focus {{
                border: 1px solid {C.PRI};
                background: {C.DARK};
            }}
        """)
        self._input.returnPressed.connect(self._send)
        row.addWidget(self._input)

        send = QPushButton("↑")
        send.setFixedSize(40, 40)
        send.setFont(QFont(UI_FONT, 13, QFont.Weight.DemiBold))
        send.setCursor(Qt.CursorShape.PointingHandCursor)
        send.setToolTip("Enviar mensaje  [Enter]")
        send.setStyleSheet(f"""
            QPushButton {{
                background: {C.PRI};
                color: {C.WHITE};
                border: none;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background: {C.PRI_DIM};
            }}
            QPushButton:pressed {{
                background: {C.PRI_DIM};
            }}
        """)
        send.clicked.connect(self._send)
        row.addWidget(send)
        return row

    def _build_content_panel(self) -> QWidget:
        """
        Collapsible panel below the HUD — shows search results, news, briefings.
        Hidden by default; appears when show_content() is called.
        """
        w = QWidget()
        w.setObjectName("ContentPanel")
        w.setStyleSheet(f"""
            QWidget#ContentPanel {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER};
                border-radius: 12px;
            }}
        """)
        w.hide()

        lay = QVBoxLayout(w)
        lay.setContentsMargins(14, 10, 14, 10)
        lay.setSpacing(6)

        # ── header row ───────────────────────────────────────────────────────
        hdr = QHBoxLayout(); hdr.setSpacing(6)

        self._content_title_lbl = QLabel("Notas y contexto")
        self._content_title_lbl.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        self._content_title_lbl.setStyleSheet(
            f"color: {C.WHITE}; background: transparent;"
        )
        hdr.addWidget(self._content_title_lbl)
        hdr.addStretch()

        self._content_ts_lbl = QLabel("")
        self._content_ts_lbl.setFont(QFont(UI_FONT, 8))
        self._content_ts_lbl.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent;")
        hdr.addWidget(self._content_ts_lbl)

        self._content_dismiss_btn = QPushButton("Cerrar  ✕")
        self._content_dismiss_btn.setFont(QFont(UI_FONT, 8))
        self._content_dismiss_btn.setFixedHeight(22)
        self._content_dismiss_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._content_dismiss_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {C.TEXT_DIM};
                border: 1px solid {C.BORDER}; border-radius: 6px; padding: 0 8px;
            }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
        """)
        self._content_dismiss_btn.clicked.connect(self._hide_content_panel)
        hdr.addWidget(self._content_dismiss_btn)
        lay.addLayout(hdr)

        self._content_dismiss_timer = QTimer(self)
        self._content_dismiss_timer.setInterval(1000)
        self._content_dismiss_timer.timeout.connect(self._on_content_dismiss_tick)
        self._content_dismiss_remaining: int = 40
        self._content_dismiss_paused: bool = False

        orig_content_enter = w.enterEvent
        orig_content_leave = w.leaveEvent
        def _on_content_enter(ev):
            if hasattr(self, "_content_dismiss_timer") and self._content_dismiss_timer.isActive():
                self._content_dismiss_paused = True
                self._content_dismiss_timer.stop()
                if hasattr(self, "_content_dismiss_btn"):
                    self._content_dismiss_btn.setText(f"Cerrar (pausado {self._content_dismiss_remaining}s)  ✕")
            if orig_content_enter:
                orig_content_enter(ev)

        def _on_content_leave(ev):
            if getattr(self, "_content_dismiss_paused", False) and getattr(self, "_content_dismiss_remaining", 0) > 0:
                self._content_dismiss_paused = False
                if hasattr(self, "_content_dismiss_timer") and hasattr(self, "_content_panel") and self._content_panel.isVisible():
                    self._content_dismiss_timer.start(1000)
                    if hasattr(self, "_content_dismiss_btn"):
                        self._content_dismiss_btn.setText(f"Cerrar ({self._content_dismiss_remaining}s)  ✕")
            if orig_content_leave:
                orig_content_leave(ev)

        w.enterEvent = _on_content_enter
        w.leaveEvent = _on_content_leave

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {C.BORDER};"); lay.addWidget(sep)

        self._content_display = QTextEdit()
        self._content_display.setReadOnly(True)
        self._content_display.setFont(QFont(UI_FONT, 9))
        self._content_display.setMinimumHeight(60)
        self._content_display.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self._content_display.setStyleSheet(f"""
            QTextEdit {{
                background: {C.DARK};
                color: {C.TEXT};
                border: 1px solid {C.BORDER};
                border-radius: 8px;
                padding: 8px 10px;
                selection-background-color: {C.PRI_GHO};
            }}
            QScrollBar:vertical {{
                background: {C.DARK}; width: 6px; border: none;
            }}
            QScrollBar::handle:vertical {{
                background: {C.BORDER_B}; border-radius: 3px; min-height: 16px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0; border: none;
            }}
        """)
        lay.addWidget(self._content_display)

        return w

    def _start_content_dismiss_countdown(self, seconds: int = 40):
        """Starts 40s auto-dismiss countdown on search/briefing content panel."""
        self._content_dismiss_remaining = seconds
        self._content_dismiss_paused = False
        if hasattr(self, "_content_dismiss_btn"):
            self._content_dismiss_btn.setText(f"Cerrar ({self._content_dismiss_remaining}s)  ✕")
        if hasattr(self, "_content_dismiss_timer"):
            self._content_dismiss_timer.stop()
            self._content_dismiss_timer.start(1000)

    def _on_content_dismiss_tick(self):
        """Content panel auto-dismiss tick handler."""
        if not hasattr(self, "_content_panel") or not self._content_panel.isVisible():
            if hasattr(self, "_content_dismiss_timer"):
                self._content_dismiss_timer.stop()
            return
        self._content_dismiss_remaining -= 1
        if self._content_dismiss_remaining > 0:
            if hasattr(self, "_content_dismiss_btn"):
                self._content_dismiss_btn.setText(f"Cerrar ({self._content_dismiss_remaining}s)  ✕")
        else:
            self._hide_content_panel()

    def _hide_content_panel(self):
        """Immediately stops dismiss timer and hides content panel."""
        if hasattr(self, "_content_dismiss_timer"):
            self._content_dismiss_timer.stop()
        if hasattr(self, "_content_panel"):
            self._content_panel.hide()

    def _show_content(self, title: str, text: str):
        """Slot — runs on Qt main thread. Updates and shows the content panel."""
        import time as _time
        self.hud.glance(0.0, -0.85, hold=1.3)
        self._content_title_lbl.setText((title or "Notas")[:48])
        self._content_ts_lbl.setText(_time.strftime("%H:%M:%S"))
        self._content_display.setPlainText(text)
        self._content_display.moveCursor(
            self._content_display.textCursor().MoveOperation.Start
        )
        first_show = not self._content_panel.isVisible()
        self._content_panel.show()
        if first_show:
            total = self._center_split.height()
            self._center_split.setSizes([max(total - 220, 120), 220])
        self._start_content_dismiss_countdown(40)

    _REVIEW_MARKS = {"serious": ("RED", "▲"), "caution": ("ACC2", "●"), "note": ("PRI_DIM", "·")}

    @staticmethod
    def _esc(s) -> str:
        return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace("\n", "<br>"))

    def _show_review(self, title: str, summary: str, findings, unclear):
        """Slot — Qt main thread. Lays a document review into the content panel."""
        e = self._esc
        parts = [f'<div style="color:{C.TEXT}; font-family:\'{UI_FONT}\';">']

        if summary:
            parts.append(
                f'<div style="color:{C.WHITE}; border-left:2px solid {C.PRI};'
                f' padding-left:8px; margin-bottom:10px;">{e(summary)}</div>')

        for f in (findings or []):
            key, mark = self._REVIEW_MARKS.get(f.get("severity"), ("PRI_DIM", "·"))
            colour = getattr(C, key)
            parts.append(f'<div style="margin-bottom:11px;">')
            parts.append(
                f'<span style="color:{colour}; font-weight:bold;">{mark}</span> '
                f'<span style="color:{C.WHITE}; font-weight:bold;">'
                f'{e(f.get("heading"))}</span>')
            if f.get("detail"):
                parts.append(f'<div style="margin-left:12px;">{e(f["detail"])}</div>')
            if f.get("quote"):
                parts.append(
                    f'<div style="margin-left:12px; color:{C.TEXT_DIM};'
                    f' border-left:1px solid {C.BORDER}; padding-left:7px;">'
                    f'&ldquo;{e(f["quote"])}&rdquo;</div>')
            if f.get("suggestion"):
                parts.append(
                    f'<div style="margin-left:12px; color:{C.PRI};">'
                    f'&rarr; {e(f["suggestion"])}</div>')
            parts.append('</div>')

        if unclear:
            parts.append(
                f'<div style="margin-top:6px; border-top:1px solid {C.BORDER};'
                f' padding-top:7px; color:{C.TEXT_MED};">'
                'Puntos abiertos del documento:</div>')
            for u in unclear:
                parts.append(
                    f'<div style="margin-left:12px; color:{C.TEXT_MED};">'
                    f'&middot; {e(u)}</div>')
        parts.append('</div>')

        import time as _time
        self.hud.glance(0.0, -0.85, hold=1.3)
        self._content_title_lbl.setText((title or "Revisión documental")[:48])
        self._content_ts_lbl.setText(_time.strftime("%H:%M:%S"))
        self._content_display.setHtml("".join(parts))
        self._content_display.moveCursor(
            self._content_display.textCursor().MoveOperation.Start)
        first_show = not self._content_panel.isVisible()
        self._content_panel.show()
        if first_show:
            total = self._center_split.height()
            self._center_split.setSizes([max(total - 260, 120), 260, 0])
        self._start_content_dismiss_countdown(40)

    def _quiz_btn(self, text: str, primary: bool = False) -> QPushButton:
        b = QPushButton(text)
        b.setFont(QFont(UI_FONT, 9))
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        b.setMinimumHeight(26)
        edge = C.BORDER_B if primary else C.BORDER
        col = C.PRI if primary else C.TEXT_MED
        b.setStyleSheet(f"""
            QPushButton {{
                background: {C.PANEL2}; color: {col};
                border: 1px solid {edge}; border-radius: 8px;
                padding: 4px 10px; text-align: left;
            }}
            QPushButton:hover {{ color: {C.WHITE}; border-color: {C.PRI_DIM}; }}
            QPushButton:disabled {{ color: {C.TEXT_DIM}; border-color: {C.BORDER}; }}
        """)
        return b

    def _build_quiz_panel(self) -> QWidget:
        w = QWidget()
        w.setObjectName("QuizPanel")
        w.setStyleSheet(f"""
            QWidget#QuizPanel {{
                background: {C.PANEL};
                border: 1px solid {C.BORDER};
                border-radius: 12px;
            }}
        """)
        w.hide()

        lay = QVBoxLayout(w)
        lay.setContentsMargins(14, 10, 14, 10)
        lay.setSpacing(6)

        hdr = QHBoxLayout(); hdr.setSpacing(6)
        self._quiz_title_lbl = QLabel("Cuestionario")
        self._quiz_title_lbl.setFont(QFont(UI_FONT, 9, QFont.Weight.DemiBold))
        self._quiz_title_lbl.setStyleSheet(
            f"color: {C.WHITE}; background: transparent;")
        hdr.addWidget(self._quiz_title_lbl)
        hdr.addStretch()

        self._quiz_count_lbl = QLabel("")
        self._quiz_count_lbl.setFont(QFont(UI_FONT, 8))
        self._quiz_count_lbl.setStyleSheet(f"color: {C.TEXT_DIM}; background: transparent;")
        hdr.addWidget(self._quiz_count_lbl)

        quit_btn = QPushButton("Cerrar  ✕")
        quit_btn.setFont(QFont(UI_FONT, 8))
        quit_btn.setFixedHeight(22)
        quit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        quit_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; color: {C.TEXT_DIM};
                border: 1px solid {C.BORDER}; border-radius: 6px; padding: 0 8px;
            }}
            QPushButton:hover {{ color: {C.TEXT}; border-color: {C.BORDER_B}; }}
        """)
        quit_btn.clicked.connect(self._hide_quiz)
        hdr.addWidget(quit_btn)
        lay.addLayout(hdr)

        rule = QFrame(); rule.setFixedHeight(1)
        rule.setStyleSheet(f"background: {C.BORDER};")
        lay.addWidget(rule)

        self._quiz_q_lbl = QLabel("")
        self._quiz_q_lbl.setWordWrap(True)
        self._quiz_q_lbl.setFont(QFont(UI_FONT, 10))
        self._quiz_q_lbl.setStyleSheet(f"color: {C.WHITE}; background: transparent;")
        lay.addWidget(self._quiz_q_lbl)

        self._quiz_answers = QWidget()
        self._quiz_answers.setStyleSheet("background: transparent;")
        self._quiz_answers_lay = QVBoxLayout(self._quiz_answers)
        self._quiz_answers_lay.setContentsMargins(0, 2, 0, 0)
        self._quiz_answers_lay.setSpacing(4)
        lay.addWidget(self._quiz_answers)

        self._quiz_note_lbl = QLabel("")
        self._quiz_note_lbl.setWordWrap(True)
        self._quiz_note_lbl.setFont(QFont(UI_FONT, 9))
        self._quiz_note_lbl.setStyleSheet(f"color: {C.TEXT_MED}; background: transparent;")
        self._quiz_note_lbl.hide()
        lay.addWidget(self._quiz_note_lbl)

        foot = QHBoxLayout()
        foot.addStretch()
        self._quiz_next_btn = self._quiz_btn("Siguiente  →", primary=True)
        self._quiz_next_btn.setFixedWidth(110)
        self._quiz_next_btn.clicked.connect(self._quiz_next)
        self._quiz_next_btn.hide()
        foot.addWidget(self._quiz_next_btn)
        lay.addLayout(foot)

        self._quiz = None
        return w

    def _show_quiz(self, topic: str, questions, grader=None):
        """Slot — Qt main thread. Puts a fresh quiz on the board."""
        if not questions:
            return
        self._quiz = {
            "topic": topic or "",
            "questions": list(questions),
            "grader": grader,
            "i": 0,
            "results": [],
            "answered": False,
        }
        self._quiz_title_lbl.setText((topic or "Cuestionario")[:48])
        self.hud.glance(0.0, -0.85, hold=1.3)
        first_show = not self._quiz_panel.isVisible()
        self._quiz_panel.show()
        if first_show:
            total = self._center_split.height()
            self._center_split.setSizes([max(total - 250, 120), 0, 250])
        self._quiz_render()

    def _hide_quiz(self):
        self._quiz = None
        self._quiz_panel.hide()

    def _quiz_clear_answers(self):
        while self._quiz_answers_lay.count():
            item = self._quiz_answers_lay.takeAt(0)
            child = item.widget()
            if child is not None:
                child.setParent(None)
                child.deleteLater()

    def _quiz_render(self):
        q = self._quiz["questions"][self._quiz["i"]]
        n, total = self._quiz["i"] + 1, len(self._quiz["questions"])
        self._quiz_count_lbl.setText(f"{n} / {total}")
        self._quiz_q_lbl.setText(q.get("question", ""))
        self._quiz_note_lbl.hide()
        self._quiz_next_btn.hide()
        self._quiz["answered"] = False
        self._quiz_clear_answers()

        opts = q.get("options") or []
        if opts:
            for text in opts:
                b = self._quiz_btn("   " + text)
                b.clicked.connect(lambda _=False, t=text: self._quiz_submit(t))
                self._quiz_answers_lay.addWidget(b)
        else:
            row = QWidget(); row.setStyleSheet("background: transparent;")
            h = QHBoxLayout(row); h.setContentsMargins(0, 0, 0, 0); h.setSpacing(6)
            field = QLineEdit()
            field.setFont(QFont(UI_FONT, 9))
            field.setPlaceholderText("Escribe tu respuesta…")
            field.setStyleSheet(f"""
                QLineEdit {{
                    background: {C.DARK}; color: {C.WHITE};
                    border: 1px solid {C.BORDER}; border-radius: 8px; padding: 4px 10px;
                }}
                QLineEdit:focus {{ border-color: {C.PRI}; }}
            """)
            send = self._quiz_btn("Responder", primary=True)
            send.setFixedWidth(96)
            field.returnPressed.connect(lambda: self._quiz_submit(field.text()))
            send.clicked.connect(lambda: self._quiz_submit(field.text()))
            h.addWidget(field, stretch=1)
            h.addWidget(send)
            self._quiz_answers_lay.addWidget(row)
            field.setFocus()

    def _quiz_submit(self, given: str):
        if self._quiz is None or self._quiz["answered"]:
            return
        self._quiz["answered"] = True
        q = self._quiz["questions"][self._quiz["i"]]
        grader = self._quiz.get("grader")
        verdict = None
        if callable(grader):
            try:
                verdict = grader(q, given)
            except Exception:
                verdict = None
        self._quiz["results"].append({
            "question": q.get("question", ""),
            "type": q.get("type", ""),
            "given": str(given or "").strip(),
            "answer": q.get("answer", ""),
            "correct": verdict,
        })

        for i in range(self._quiz_answers_lay.count()):
            wdg = self._quiz_answers_lay.itemAt(i).widget()
            if wdg is not None:
                wdg.setEnabled(False)

        if verdict is True:
            mark, colour = "✓  Correcto", C.GREEN
        elif verdict is False:
            mark, colour = "✕  " + str(q.get("answer", "")), C.RED
        else:
            mark, colour = "…  Registrado — lo revisaremos al finalizar", C.ACC2
        note = q.get("note") or ""
        self._quiz_note_lbl.setText(mark + (("\n" + note) if note else ""))
        self._quiz_note_lbl.setStyleSheet(f"color: {colour}; background: transparent;")
        self._quiz_note_lbl.show()

        last = self._quiz["i"] >= len(self._quiz["questions"]) - 1
        self._quiz_next_btn.setText("Finalizar  →" if last else "Siguiente  →")
        self._quiz_next_btn.show()
        self._quiz_next_btn.setFocus()

    def _quiz_next(self):
        if self._quiz is None:
            return
        if self._quiz["i"] >= len(self._quiz["questions"]) - 1:
            self._quiz_finish()
        else:
            self._quiz["i"] += 1
            self._quiz_render()

    def _quiz_finish(self):
        if self._quiz is None:
            return
        topic = self._quiz["topic"]
        results = self._quiz["results"]
        right = sum(1 for r in results if r["correct"] is True)
        unsure = sum(1 for r in results if r["correct"] is None)
        total = len(results)
        self._quiz_panel.hide()
        self._quiz = None

        self._log.append_log(f"QUIZ: {topic or 'quiz'} — {right}/{total} correct")

        lines = [f"[QUIZ_DONE] topic={topic or 'general'} | "
                 f"auto-marked {right}/{total} correct"
                 + (f", {unsure} still need your marking" if unsure else "")]
        for i, r in enumerate(results, 1):
            state = ("correct" if r["correct"] is True
                     else "wrong" if r["correct"] is False else "NEEDS MARKING")
            lines.append(
                f"{i}. [{r['type']}] {r['question']} | they answered: "
                f"{r['given'] or '(blank)'} | expected: {r['answer']} | {state}")
        lines.append(
            "Mark every question flagged NEEDS MARKING yourself — accept an answer "
            "that means the same thing. Then tell them how they did in their own "
            "language: the score, what they got wrong and why, in a couple of "
            "sentences. Offer another round only if it fits. "
            "Remember something only if it would still matter next week — that they "
            "are working through a subject, or keep missing the same thing. A score "
            "from one session is not worth a memory, and a memory per quiz would "
            "bury the things that are.")
        msg = "\n".join(lines)
        if self.on_text_command:
            threading.Thread(target=self.on_text_command, args=(msg,), daemon=True).start()

    def _build_footer(self) -> QWidget:
        w = QWidget(); w.setObjectName("Footer")
        w.setFixedHeight(30)
        w.setStyleSheet(f"""
            QWidget#Footer {{
                background: {C.BG};
                border-top: 1px solid {C.BORDER};
            }}
        """)
        lay = QHBoxLayout(w); lay.setContentsMargins(20, 0, 20, 0); lay.setSpacing(12)

        def _key(k, label):
            l = QLabel(
                f'<span style="color:{C.TEXT_MED}; background:{C.PANEL2}; border:1px solid {C.BORDER}; '
                f'border-radius:4px; padding:1px 5px; font-weight:600; font-size:7pt;">{k}</span> '
                f'<span style="color:{C.TEXT_DIM}; font-size:7.5pt;">{label}</span>')
            l.setFont(QFont(UI_FONT, 8))
            l.setStyleSheet("background: transparent;")
            lay.addWidget(l)

        for k, label in (("F4", "Micrófono"), ("F8", "Integraciones"), ("F9", "Investigar"),
                         ("F10", "Presencia"), ("F11", "Pantalla completa"), ("Esc", "Detener")):
            _key(k, label)

        lay.addStretch()
        cr = QLabel(
            f'<span style="color:{C.GREEN};">●</span> '
            f'<span style="color:{C.TEXT_MED}; font-weight:600;">Asistente activo</span> '
            f'<span style="color:{C.TEXT_DIM};">·  {APP_VERSION}</span>'
        )
        cr.setFont(QFont(UI_FONT, 8))
        cr.setStyleSheet("background: transparent;")
        lay.addWidget(cr)

        donate_btn = QPushButton("💛  Donar · PayPal")
        donate_btn.setFixedHeight(22)
        donate_btn.setFont(QFont(UI_FONT, 8, QFont.Weight.DemiBold))
        donate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        donate_btn.setToolTip("Apoya el desarrollo gratuito de Viernes (Groovi Developer) vía PayPal")
        donate_btn.setStyleSheet(
            f"QPushButton {{ background: rgba(251,191,36,0.12); color: #FBBF24; "
            f"border: 1px solid rgba(251,191,36,0.38); border-radius: 6px; padding: 0 10px; }}"
            f"QPushButton:hover {{ background: rgba(251,191,36,0.22); color: #FDE68A; }}"
        )
        donate_btn.clicked.connect(self._open_donation_modal)
        lay.addWidget(donate_btn)
        return w

    def dragEnterEvent(self, e: QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent):
        urls = e.mimeData().urls()
        if urls:
            e.acceptProposedAction()
            path = urls[0].toLocalFile()
            if path and Path(path).is_file():
                self._drop_zone._set_file(path)

    def _on_file_cleared(self):
        self._current_file = None
        self._file_hint.setText("Ningún archivo cargado")
        self._log.append_log("SYS: Archivo descargado de la bandeja.")

    def _on_external_file_sig(self, path: str):
        """Display a file uploaded from the mobile Remote Control in the Desktop UI."""
        if not path or not Path(path).is_file():
            return
        self._current_file = path
        self._drop_zone.set_file_silent(path)
        p    = Path(path)
        cat  = _file_category(p)
        icon, _ = _FILE_ICONS.get(cat, _FILE_ICONS["unknown"])
        size = _fmt_size(p.stat().st_size)
        self._file_hint.setText(f"{icon}  {p.name}  ·  {size}  —  recibido desde Control Remoto")

    def _on_file_selected(self, path: str):
        self._current_file = path
        p    = Path(path)
        cat  = _file_category(p)
        icon, _ = _FILE_ICONS.get(cat, _FILE_ICONS["unknown"])
        size = _fmt_size(p.stat().st_size)
        self._file_hint.setText(f"{icon}  {p.name}  ·  {size}  —  dile a {self._assistant_name} qué hacer con él")
        self._log.append_log(f"FILE: {p.name} ({size}) cargado y listo")
        if self.on_text_command:
            msg = (
                f"[FILE_UPLOADED] path={path} | name={p.name} | "
                f"type={p.suffix.lstrip('.')} | size={size} | "
                f"El usuario acaba de cargar el archivo '{p.name}' ({size}). "
                f"Confirma brevemente en español que ya ves el archivo '{p.name}' y pregúntale qué desea hacer con él."
            )
            threading.Thread(target=self.on_text_command, args=(msg,), daemon=True).start()

    def notify_phone_connected(self) -> None:
        if self._remote_overlay and self._remote_overlay.isVisible():
            self._remote_overlay.mark_connected()

    def _open_remote(self):
        self._close_setup()
        self._close_controls()
        if not self.on_remote_clicked:
            self._log.append_log("SYS: Dashboard not running — remote unavailable.")
            return
        result = self.on_remote_clicked()
        if not result:
            self._log.append_log("SYS: Could not generate remote key.")
            return
        url    = result[0]
        key    = result[1]
        auto   = result[2] if len(result) >= 3 else ""
        manual = result[3] if len(result) >= 4 else url
        if self._remote_overlay:
            self._remote_overlay._do_close()
        cw  = self.centralWidget()
        ow, oh = RemoteKeyOverlay._OW, RemoteKeyOverlay._OH
        ov  = RemoteKeyOverlay(url, key, auto_login_url=auto, manual_url=manual,
                               expiry_secs=600, parent=cw)
        ov.set_new_key_callback(self.on_remote_clicked)
        ov.setGeometry(
            (cw.width()  - ow) // 2,
            (cw.height() - oh) // 2,
            ow, oh,
        )
        ov.closed.connect(lambda: setattr(self, '_remote_overlay', None))
        if hasattr(self, "hud") and self.hud is not None:
            self.hud.register_overlay(ov)
        ov.show()
        ov.raise_()
        self._remote_overlay = ov
        self._log.append_log(f"SYS: Remote key generated — manual: {manual or url}")

    # ── Auto-start ──────────────────────────────────────────────────────────────

    def _check_autostart(self) -> bool:
        """Returns True if auto-start is currently registered on this OS."""
        try:
            if _OS == "Windows":
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
                try:
                    winreg.QueryValueEx(key, "VIERNES_AI")
                    return True
                except FileNotFoundError:
                    return False
                finally:
                    winreg.CloseKey(key)
            elif _OS == "Darwin":
                return (Path.home() / "Library" / "LaunchAgents"
                        / "com.viernes.assistant.plist").exists()
            else:
                return (Path.home() / ".config" / "autostart" / "viernes.desktop").exists()
        except Exception:
            return False

    def _toggle_autostart(self):
        currently_on = self._check_autostart()
        try:
            script = str(Path(__file__).resolve().parent / "main.py")
            if _OS == "Windows":
                import winreg
                reg = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
                if currently_on:
                    winreg.DeleteValue(reg, "VIERNES_AI")
                else:
                    pythonw = Path(sys.executable).parent / "pythonw.exe"
                    exe = str(pythonw if pythonw.exists() else sys.executable)
                    winreg.SetValueEx(reg, "VIERNES_AI", 0, winreg.REG_SZ,
                                      f'"{exe}" "{script}"')
                winreg.CloseKey(reg)
            elif _OS == "Darwin":
                plist_dir = Path.home() / "Library" / "LaunchAgents"
                plist_dir.mkdir(parents=True, exist_ok=True)
                plist = plist_dir / "com.viernes.assistant.plist"
                if currently_on:
                    plist.unlink(missing_ok=True)
                else:
                    plist.write_text(
                        '<?xml version="1.0" encoding="UTF-8"?>\n'
                        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
                        '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
                        '<plist version="1.0"><dict>\n'
                        '  <key>Label</key><string>com.viernes.assistant</string>\n'
                        '  <key>ProgramArguments</key><array>\n'
                        f'    <string>{sys.executable}</string>\n'
                        f'    <string>{script}</string>\n'
                        '  </array>\n'
                        '  <key>RunAtLoad</key><true/>\n'
                        '</dict></plist>\n'
                    )
            else:
                desk_dir = Path.home() / ".config" / "autostart"
                desk_dir.mkdir(parents=True, exist_ok=True)
                desk = desk_dir / "viernes.desktop"
                if currently_on:
                    desk.unlink(missing_ok=True)
                else:
                    desk.write_text(
                        "[Desktop Entry]\n"
                        f"Name={self._assistant_name}\n"
                        f"Exec={sys.executable} {script}\n"
                        "Type=Application\nTerminal=false\n"
                        "X-GNOME-Autostart-enabled=true\n"
                    )
            enabled = not currently_on
            self._update_autostart_btn(enabled)
            self._log.append_log(
                f"SYS: Auto-start {'enabled' if enabled else 'disabled'}.")
        except Exception as e:
            self._log.append_log(f"ERR: Auto-start failed — {e}")

    def _update_autostart_btn(self, enabled: bool):
        if not hasattr(self, '_autostart_btn'):
            return
        self._autostart_btn.setText(f"⏻   Inicio automático: {'Sí' if enabled else 'No'}")
        self._autostart_btn.setStyleSheet(_ss_row(on=enabled))

    def _toggle_brief(self):
        from memory.config_manager import get_brief_enabled, save_brief_enabled
        new_val = not get_brief_enabled()
        save_brief_enabled(new_val)
        self._update_brief_btn(new_val)

    # ── Wake word settings ───────────────────────────────────────────────────

    def _wake_state(self) -> dict:
        """Combined state for the two wake-word buttons. Readiness is a cheap,
        deterministic on-disk check now (see core.wake_word.is_ready), so there
        is nothing to cache — the button never flickers to a stale value."""
        if self.wake_get_state:
            try:
                s = self.wake_get_state()
                return {"ready": bool(s.get("ready")),
                        "enabled": bool(s.get("enabled")),
                        "awake": bool(s.get("awake"))}
            except Exception:
                pass
        # Before ViernesLive has wired its callback (drawer built at startup).
        ready, enabled = False, False
        try:
            from core.wake_word import is_ready
            from memory.config_manager import get_wake_word_enabled
            ready, enabled = is_ready(), get_wake_word_enabled()
        except Exception:
            pass
        return {"ready": ready, "enabled": enabled, "awake": True}

    def _refresh_wake_btns(self):
        st = self._wake_state()
        if hasattr(self, '_wake_btn'):
            self._wake_btn.setEnabled(True)
            if st["enabled"]:
                self._wake_btn.setText("🎙   Palabra de activación: Sí")
                self._wake_btn.setStyleSheet(_ss_row(on=True))
                self._wake_sleep_btn.show()
                is_awake = bool(st.get("awake", True) and getattr(self.hud, "state", "") != "SLEEPING")
                self._wake_sleep_btn.setText("😴   Dormir ahora" if is_awake else "👂   Despertar ahora")
                self._wake_sleep_btn.setStyleSheet(_ss_row())
            else:
                self._wake_btn.setText("🎙   Palabra de activación: No")
                self._wake_btn.setStyleSheet(_ss_row())
                self._wake_sleep_btn.hide()

        if hasattr(self, '_wake_act_btn'):
            self._wake_act_btn.setEnabled(True)
            if st["enabled"]:
                self._wake_act_btn.setText("🎙️  Palabra de activación: Sí")
                self._wake_act_btn.setStyleSheet(_ss_soft_btn(C.PRI))
                self._wake_act_btn.setToolTip("Palabra de activación activada — clic para desactivar")
            else:
                self._wake_act_btn.setText("🎙️  Palabra de activación: No")
                self._wake_act_btn.setStyleSheet(_ss_soft_btn(C.TEXT_DIM))
                self._wake_act_btn.setToolTip("Palabra de activación desactivada — clic para activar")

    def _refresh_talk_btns(self):
        """Repaint the push-to-talk row from the saved setting."""
        if not hasattr(self, "_ptt_btn"):
            return
        from core.hotkey import chord_label
        from memory.config_manager import get_push_to_talk_enabled
        ptt = get_push_to_talk_enabled()
        self._ptt_btn.setText(f"🎚   Pulsar para hablar: {chord_label()}" if ptt
                              else "🎚   Pulsar para hablar: No")
        self._ptt_btn.setStyleSheet(_ss_row(on=ptt))
        self._ptt_btn.setToolTip(
            "El micrófono permanece cerrado hasta que mantienes la tecla pulsada." if ptt
            else "Mantén una tecla para hablar en lugar de transmitir el micrófono siempre.")

    def _refresh_hud_btn(self):
        from memory.config_manager import get_hud_style
        st = get_hud_style()
        style = _ss_row(accent=True)
        if st == "edith_live2d":
            self._hud_btn.setText("✨  HUD: EDITH (LIVE2D PRO)")
            self._hud_btn.setToolTip("Avatar Edith Live2D Cubism oficial en tiempo real con física avanzada y seguimiento ocular. Clic para cambiar a Viernes 2D.")
        elif st == "face":
            self._hud_btn.setText("🌸  HUD: VIERNES 2D (LIVE2D)")
            self._hud_btn.setToolTip("Avatar 2D con morphing de expresiones y fonemas. Clic para cambiar al reactor core.")
        else:
            self._hud_btn.setText("◉  HUD: REACTOR CORE (HOLO)")
            self._hud_btn.setToolTip("Reactor holográfico reactivo. Clic para cambiar a Edith Live2D.")
        self._hud_btn.setStyleSheet(style)
        if hasattr(self, "_refresh_edith_btn"):
            self._refresh_edith_btn()
        if hasattr(self, "_refresh_skin_btn"):
            self._refresh_skin_btn()

    def _refresh_skin_btn(self):
        if not hasattr(self, "_skin_btn"):
            return
        from memory.config_manager import get_hud_style, get_live2d_skin
        if get_hud_style() != "edith_live2d":
            self._skin_btn.hide()
            return
        self._skin_btn.show()
        current_skin = get_live2d_skin()
        self._skin_btn.setText(f"🎭   Personaje: {current_skin}  ▾")
        self._skin_btn.setToolTip(f"Personaje Live2D actual: {current_skin}. Clic para seleccionar o abrir la carpeta de skins.")
        self._skin_btn.setStyleSheet(_ss_row(accent=True))

    def _show_skin_menu(self):
        try:
            from core.live2d.skin_manager import discover_live2d_skins, open_skins_folder
            from memory.config_manager import get_live2d_skin

            skins = discover_live2d_skins()
            current_skin = get_live2d_skin()

            menu = QMenu(self)
            menu.setStyleSheet(f"""
                QMenu {{
                    background-color: {C.PANEL};
                    color: {C.TEXT};
                    border: 1px solid {C.BORDER_A};
                    border-radius: 8px;
                    padding: 6px;
                    font-family: {UI_FONT};
                    font-size: 12px;
                }}
                QMenu::item {{
                    padding: 6px 24px 6px 20px;
                    border-radius: 4px;
                }}
                QMenu::item:selected {{
                    background-color: {C.PANEL2};
                    color: {C.PRI};
                }}
                QMenu::separator {{
                    height: 1px;
                    background: {C.BORDER_A};
                    margin: 4px 8px;
                }}
            """)

            hdr = menu.addAction("🎭 PERSONAJES LIVE2D DISPONIBLES")
            hdr.setEnabled(False)
            menu.addSeparator()

            for s_name, s_data in skins.items():
                is_active = (s_name.lower() == current_skin.lower())
                label = f"✓  {s_name}" if is_active else f"    {s_name}"
                act = menu.addAction(label)
                def _make_handler(name=s_name, url=s_data["model_url"]):
                    return lambda: self._apply_live2d_skin(name, url)
                act.triggered.connect(_make_handler())

            menu.addSeparator()
            open_act = menu.addAction("📂  Abrir carpeta de personajes (live2d_models)...")
            open_act.triggered.connect(open_skins_folder)

            ref_act = menu.addAction("🔄  Actualizar lista")
            ref_act.triggered.connect(self._refresh_skin_btn)

            pos = self._skin_btn.mapToGlobal(QPoint(0, self._skin_btn.height() + 2))
            menu.exec(pos)
        except Exception as e:
            print(f"[Live2DSkinSelector] Error showing skin menu: {e}")

    def _apply_live2d_skin(self, name: str, url: str):
        try:
            from memory.config_manager import save_live2d_skin
            save_live2d_skin(name)
            if hasattr(self.hud, "_live2d_widget") and self.hud._live2d_widget is not None:
                self.hud._live2d_widget.load_model(url)
            self._refresh_skin_btn()
            self._log.append_log(f"SYS: Personaje Live2D cambiado a '{name}'.")
        except Exception as e:
            print(f"[Live2DSkinSelector] Error applying skin {name}: {e}")

    def _refresh_edith_btn(self):
        if not hasattr(self, "_edith_btn"):
            return
        from memory.config_manager import (
            get_hud_style,
            get_edith_autonomy_enabled,
            get_edith_spontaneity_level
        )
        if get_hud_style() != "edith_live2d":
            self._edith_btn.hide()
            return
        self._edith_btn.show()

        auto = get_edith_autonomy_enabled()
        level = get_edith_spontaneity_level()

        style = _ss_row(accent=True)

        if not auto:
            self._edith_btn.setText("💤  EDITH: AUTONOMÍA OFF")
            self._edith_btn.setToolTip("Edith en modo estático sin acciones espontáneas. Clic para activar modo tranquilo.")
        elif level <= 0.6:
            self._edith_btn.setText("🌸  EDITH: TRANQUILA (0.5x)")
            self._edith_btn.setToolTip("Movimientos sutiles de reposo y baja frecuencia de acciones. Clic para cambiar a modo natural.")
        elif level <= 1.1:
            self._edith_btn.setText("✨  EDITH: NATURAL (1.0x)")
            self._edith_btn.setToolTip("Autonomía equilibrada, curiosidad orgánica y bailes ocasionales. Clic para cambiar a modo expresivo.")
        else:
            self._edith_btn.setText("🎉  EDITH: EXPRESIVA (1.5x)")
            self._edith_btn.setToolTip("Alta frecuencia de expresiones, bailes y gestos espontáneos. Clic para desactivar autonomía.")
        self._edith_btn.setStyleSheet(style)

    def _toggle_edith_autonomy(self):
        from memory.config_manager import (
            get_edith_autonomy_enabled,
            save_edith_autonomy_enabled,
            get_edith_spontaneity_level,
            save_edith_spontaneity_level
        )
        auto = get_edith_autonomy_enabled()
        level = get_edith_spontaneity_level()

        if not auto:
            # Off -> Tranquilo
            save_edith_autonomy_enabled(True)
            save_edith_spontaneity_level(0.5)
            new_auto, new_level = True, 0.5
            msg = "Edith: Modo Tranquilo activado (0.5x)."
        elif level <= 0.6:
            # Tranquilo -> Normal
            save_edith_spontaneity_level(1.0)
            new_auto, new_level = True, 1.0
            msg = "Edith: Modo Natural activado (1.0x)."
        elif level <= 1.1:
            # Normal -> Expresivo
            save_edith_spontaneity_level(1.5)
            new_auto, new_level = True, 1.5
            msg = "Edith: Modo Expresivo activado (1.5x)."
        else:
            # Expresivo -> Desactivado
            save_edith_autonomy_enabled(False)
            new_auto, new_level = False, 0.0
            msg = "Edith: Autonomía corporal desactivada."

        if hasattr(self.hud, "_live2d_widget") and self.hud._live2d_widget is not None:
            self.hud._live2d_widget.set_autonomy_enabled(new_auto)
            self.hud._live2d_widget.set_spontaneity_level(new_level)

        self._refresh_edith_btn()
        self._log.append_log(f"SYS: {msg}")

    def _on_emotion_sig(self, name: str, intensity: float, duration: float) -> None:
        if hasattr(self, "hud") and hasattr(self.hud, "set_emotion"):
            self.hud.set_emotion(name, intensity, duration)

    def _on_action_sig(self, name: str) -> None:
        if hasattr(self, "hud") and hasattr(self.hud, "trigger_action"):
            self.hud.trigger_action(name)

    def _on_semantic_intent_sig(self, intent: str, metadata: dict) -> None:
        if hasattr(self, "hud") and hasattr(self.hud, "set_semantic_intent"):
            self.hud.set_semantic_intent(intent, metadata)

    def _on_gesture_sig(self, name: str, duration: float, intensity: float) -> None:
        if hasattr(self, "hud") and hasattr(self.hud, "trigger_gesture"):
            self.hud.trigger_gesture(name, duration, intensity)

    def _on_interrupt_gestures_sig(self) -> None:
        if hasattr(self, "hud") and hasattr(self.hud, "interrupt_gestures"):
            self.hud.interrupt_gestures()

    def _on_float_mode_sig(self, mode: str) -> None:
        if hasattr(self, "hud") and hasattr(self.hud, "set_float_mode"):
            self.hud.set_float_mode(mode)

    def _on_visual_card_sig(self, card_data: object) -> None:
        if hasattr(self, "hud") and hasattr(self.hud, "show_visual_card"):
            self.hud.show_visual_card(card_data)

    def _on_visual_hide_sig(self) -> None:
        if hasattr(self, "hud") and hasattr(self.hud, "hide_visual_card"):
            self.hud.hide_visual_card()

    def _on_log_received(self, text: str):
        tl = (text or "").lower()
        if tl.startswith("err:") and hasattr(self, "hud") and hasattr(self.hud, "notify_task_error"):
            self.hud.notify_task_error(text)

    def _toggle_hud_style(self):
        """Toggle between Edith Live2D and Holograma Core."""
        from memory.config_manager import get_hud_style, save_hud_style
        curr = get_hud_style()
        want = "core" if curr == "edith_live2d" else "edith_live2d"
        save_hud_style(want)
        try:
            self.hud.set_hud_style(want)
        except Exception:
            pass
        self._refresh_hud_btn()
        if want == "edith_live2d":
            self._log.append_log("SYS: HUD cambiado a Edith Live2D (física en tiempo real).")
        else:
            self._log.append_log("SYS: HUD cambiado a Holograma Core.")

    def _toggle_ptt(self):
        from memory.config_manager import (get_push_to_talk_enabled,
                                           save_push_to_talk_enabled)
        want = not get_push_to_talk_enabled()
        save_push_to_talk_enabled(want)
        scope = None
        if self.on_push_to_talk:
            try:
                scope = self.on_push_to_talk(want)
            except Exception as e:
                self._log.append_log(f"ERR: Push-to-talk failed — {e}")
                save_push_to_talk_enabled(False)
                want = False
        self._apply_ptt_shortcut(want and scope != "global")
        self._refresh_talk_btns()

    def _apply_ptt_shortcut(self, needed: bool):
        """Bind the chord inside the window when no global hook is available.

        On macOS and Linux there is no dependency-free way to read global key
        state, so the chord is at least live whenever this window has focus.
        Qt gives no key-release for a QShortcut, so a press latches the mic open
        and a short timer closes it; held down, auto-repeat keeps pushing that
        timer out, which behaves like holding a key.
        """
        from PyQt6.QtGui import QKeySequence, QShortcut
        from core.hotkey import qt_sequence

        if not needed:
            sc = getattr(self, "_ptt_sc", None)
            if sc is not None:
                sc.setEnabled(False)
                self._ptt_sc = None
            self._ptt_hold(False)
            return
        if getattr(self, "_ptt_sc", None) is not None:
            return

        self._ptt_release = QTimer(self)
        self._ptt_release.setSingleShot(True)
        self._ptt_release.setInterval(420)
        self._ptt_release.timeout.connect(lambda: self._ptt_hold(False))

        def _press():
            self._ptt_hold(True)
            self._ptt_release.start()

        self._ptt_sc = QShortcut(QKeySequence(qt_sequence()), self)
        self._ptt_sc.setAutoRepeat(True)
        self._ptt_sc.activated.connect(_press)

    def _ptt_hold(self, held: bool):
        """Report a windowed press/release to whoever owns the microphone."""
        cb = getattr(self, "ptt_hold", None)
        if cb:
            try:
                cb(bool(held))
            except Exception:
                pass

    def _toggle_wake_word(self):
        st = self._wake_state()
        want_enable = not st["enabled"]
        if self.on_wake_toggle:
            try:
                self.on_wake_toggle(want_enable)
            except Exception:
                pass
        else:
            try:
                from memory.config_manager import save_wake_word_enabled
                save_wake_word_enabled(want_enable)
            except Exception:
                pass
            if want_enable:
                self._apply_state("SLEEPING")
            else:
                self._apply_state("LISTENING")
        self._refresh_wake_btns()

    def _on_wake_install_done(self, ok: bool, msg: str):
        self._log_sig.emit(f"SYS: {'Wake word ready.' if ok else 'Wake word setup failed: ' + msg}")
        self._refresh_wake_btns()

    def _tap_wake_manual(self):
        if self.on_wake_manual:
            try:
                self.on_wake_manual()
            except Exception:
                pass
        else:
            if getattr(self.hud, "state", "") == "SLEEPING":
                self._apply_state("LISTENING")
            else:
                self._apply_state("SLEEPING")
        self._refresh_wake_btns()

    def _update_brief_btn(self, enabled: bool):
        if not hasattr(self, '_brief_btn'):
            return
        self._brief_btn.setText(f"☀   Resumen matutino: {'Sí' if enabled else 'No'}")
        self._brief_btn.setStyleSheet(_ss_row(on=enabled))

    def _open_donation_modal(self):
        from core.donation_ui import DonationOverlay
        if self._donation_overlay is not None:
            try:
                self._donation_overlay.hide()
                self._donation_overlay.deleteLater()
            except Exception:
                pass
            self._donation_overlay = None

        cw = self.centralWidget()
        ov = DonationOverlay(parent=cw)
        ow = min(DonationOverlay._OW, cw.width() - 24)
        oh = min(DonationOverlay._OH, cw.height() - 24)
        ov.setGeometry(
            (cw.width() - ow) // 2,
            (cw.height() - oh) // 2,
            ow, oh,
        )
        if hasattr(self, "hud") and self.hud is not None:
            self.hud.register_overlay(ov)
        ov.show()
        ov.raise_()
        self._donation_overlay = ov

    def _open_cleanyourtv(self, ip: str = ""):
        from core.cleanyourtv_ui import CleanYourTvOverlay
        if self._cleanyourtv_overlay is not None:
            try:
                self._cleanyourtv_overlay.hide()
                self._cleanyourtv_overlay.deleteLater()
            except Exception:
                pass
            self._cleanyourtv_overlay = None

        cw = self.centralWidget()
        ov = CleanYourTvOverlay(initial_ip=ip, parent=cw)
        ow = min(CleanYourTvOverlay._OW, cw.width() - 24)
        oh = min(CleanYourTvOverlay._OH, cw.height() - 24)
        ov.setGeometry(
            (cw.width() - ow) // 2,
            (cw.height() - oh) // 2,
            ow, oh,
        )
        ov.closed.connect(ov.hide)
        if hasattr(self, "hud") and self.hud is not None:
            self.hud.register_overlay(ov)
        ov.show()
        ov.raise_()
        self._cleanyourtv_overlay = ov

    # ── HUD Studio & Live Customization ─────────────────────────────────────────

    def _open_hud_studio(self):
        from core.hud_studio_ui import HudStudioOverlay
        if self._hud_studio_overlay is not None:
            try:
                self._hud_studio_overlay.hide()
                self._hud_studio_overlay.deleteLater()
            except Exception:
                pass
            self._hud_studio_overlay = None

        cw = self.centralWidget()
        ov = HudStudioOverlay(self._hud_cfg, parent=cw)
        ow = min(HudStudioOverlay._OW, cw.width() - 24)
        oh = min(HudStudioOverlay._OH, cw.height() - 24)
        ov.setGeometry(
            (cw.width() - ow) // 2,
            (cw.height() - oh) // 2,
            ow, oh,
        )
        ov.config_changed.connect(self._apply_hud_config)
        ov.closed.connect(ov.hide)
        if hasattr(self, "hud") and self.hud is not None:
            self.hud.register_overlay(ov)
        ov.show()
        ov.raise_()
        self._hud_studio_overlay = ov

    def _toggle_focus_panels(self):
        cfg = dict(self._hud_cfg)
        both_hidden = not cfg.get("show_left_panel", True) and not cfg.get("show_right_panel", True)
        if both_hidden:
            cfg["show_left_panel"] = True
            cfg["show_right_panel"] = True
            cfg["layout_preset"] = "studio"
        elif cfg.get("show_left_panel", True):
            cfg["show_left_panel"] = False
            cfg["show_right_panel"] = True
            cfg["layout_preset"] = "focus"
        else:
            cfg["show_left_panel"] = False
            cfg["show_right_panel"] = False
            cfg["layout_preset"] = "cinematic"
        self._apply_hud_config(cfg, persist=True)

    def _apply_hud_config(self, cfg: dict, persist: bool = False) -> None:
        from core.hud_theme import get_theme_palette, save_hud_config

        self._hud_cfg = dict(cfg)
        if persist:
            self._hud_cfg = save_hud_config(self._hud_cfg)

        # 1. Theme palette live swap across all widgets
        old_pal = full_palette_snapshot()
        new_pal = get_theme_palette(
            self._hud_cfg.get("theme_id", "obsidian_pro"),
            self._hud_cfg.get("accent_override", ""),
        )
        apply_full_palette(new_pal)
        retheme_all_widgets(old_pal, new_pal)

        # 2. Panel visibility & column widths
        show_left = bool(self._hud_cfg.get("show_left_panel", True))
        show_right = bool(self._hud_cfg.get("show_right_panel", True))
        if getattr(self, "_left_panel", None) is not None:
            self._left_panel.setFixedWidth(int(self._hud_cfg.get("left_width", 266)))
            self._left_panel.setVisible(show_left)
        if getattr(self, "_right_panel", None) is not None:
            self._right_panel.setFixedWidth(int(self._hud_cfg.get("right_width", 356)))
            self._right_panel.setVisible(show_right)

        # 3. Individual module visibility
        widgets = self._hud_cfg.get("widgets", {})
        if getattr(self, "_vcard", None) is not None:
            self._vcard.setVisible(bool(widgets.get("voice_monitor", True)))
        if getattr(self, "_wcard", None) is not None:
            self._wcard.setVisible(bool(widgets.get("weather", True)))
        if getattr(self, "_syscard", None) is not None:
            self._syscard.setVisible(bool(widgets.get("system_metrics", True)))
        if getattr(self, "_attach_card", None) is not None:
            self._attach_card.setVisible(bool(widgets.get("attachments", True)))
        if getattr(self, "_content_panel", None) is not None:
            if not widgets.get("news_panel", True) and not getattr(self, "_content_has_user_output", False):
                self._content_panel.hide()
            elif widgets.get("news_panel", True):
                self._content_panel.show()

        # 4. Visual density & card border radius
        density = self._hud_cfg.get("density", "balanced")
        pad_map = {"compact": (8, 8), "balanced": (14, 14), "spacious": (20, 18)}
        margin, spacing = pad_map.get(density, (14, 14))
        if getattr(self, "_body_layout", None) is not None:
            self._body_layout.setContentsMargins(margin, margin, margin, margin)
            self._body_layout.setSpacing(spacing)

        rad = int(self._hud_cfg.get("card_radius", 12))
        card_ss = (
            f"QFrame#Card {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {C.PANEL2}, stop:0.18 {C.PANEL}, stop:1 {C.PANEL}); "
            f"border: 1px solid {C.BORDER}; border-top: 1px solid {C.BORDER_B}; border-radius: {rad}px; }}"
            f"QFrame#Card QLabel {{ background: transparent; border: none; }}"
        )
        for card_w in self.findChildren(QFrame, "Card"):
            card_w.setStyleSheet(card_ss)

        # 5. Central HUD canvas effects & backdrop
        if getattr(self, "hud", None) is not None:
            self.hud._show_grid = bool(self._hud_cfg.get("hud_grid", True))
            self.hud._glass_glow = bool(self._hud_cfg.get("glass_glow", True))
            self.hud.set_custom_bg_path(self._hud_cfg.get("bg_custom_path", ""))
            self.hud.set_backdrop_params(
                self._hud_cfg.get("bg_dim", 0.42),
                self._hud_cfg.get("bg_glow", 0.65),
            )
            self.hud.set_bg_mode(self._hud_cfg.get("bg_mode", "aurora_atmos"))
            self.hud._grid_cache = None
            self.hud.update()

    # ── Customization ────────────────────────────────────────────────────────────

    def _open_customize(self):
        cfg = _read_full_config()
        if self._customize_overlay:
            self._customize_overlay.hide()
        cw = self.centralWidget()
        ov = CustomizeOverlay(
            cfg.get("assistant_name", "Viernes") or "Viernes",
            cfg.get("user_name", ""),
            cfg.get("ui_color", "") or DEFAULT_UI_COLOR,
            cfg.get("voice_name", ""),
            tts_engine=cfg.get("tts_engine", "gemini"),
            el_key=cfg.get("elevenlabs_api_key", ""),
            el_voice=cfg.get("elevenlabs_voice_id", "21m00Tcm4TlvDq8ikWAM"),
            parent=cw,
        )
        ow, oh = CustomizeOverlay._OW, CustomizeOverlay._OH
        oh = min(oh, cw.height() - 16)
        ov.setGeometry(
            (cw.width()  - ow) // 2,
            (cw.height() - oh) // 2,
            ow, oh,
        )
        ov.on_preview = self._preview_ui_color
        ov.saved.connect(self._apply_name_update)
        if hasattr(self, "hud") and self.hud is not None:
            self.hud.register_overlay(ov)
        ov.show()
        ov.raise_()
        self._customize_overlay = ov

    def _toggle_research_panel(self):
        """Toggle the intelligent Web Research workstation overlay."""
        if not hasattr(self, "_research_overlay") or self._research_overlay is None:
            from core.research.ui_panel import ResearchOverlay
            self._research_overlay = ResearchOverlay(self.centralWidget())
            self._research_overlay.close_requested.connect(self._research_overlay.hide)
        if self._research_overlay.isVisible():
            self._research_overlay.hide()
            if hasattr(self, "hud") and self.hud is not None:
                self.hud.unregister_overlay(self._research_overlay)
        else:
            cw = self.centralWidget()
            rw = min(960, int(cw.width() * 0.92))
            rh = min(700, int(cw.height() * 0.90))
            self._research_overlay.setGeometry(
                (cw.width() - rw) // 2,
                (cw.height() - rh) // 2,
                rw, rh,
            )
            if hasattr(self, "hud") and self.hud is not None:
                self.hud.register_overlay(self._research_overlay)
            self._research_overlay.show()
            self._research_overlay.raise_()

    def _show_research(self, report_dict: dict):
        """Slot: display an externally generated research report (e.g. from web_research tool)."""
        if not hasattr(self, "_research_overlay") or self._research_overlay is None:
            from core.research.ui_panel import ResearchOverlay
            self._research_overlay = ResearchOverlay(self.centralWidget())
            self._research_overlay.close_requested.connect(self._research_overlay.hide)
        cw = self.centralWidget()
        rw = min(960, int(cw.width() * 0.92))
        rh = min(700, int(cw.height() * 0.90))
        self._research_overlay.setGeometry(
            (cw.width() - rw) // 2,
            (cw.height() - rh) // 2,
            rw, rh,
        )
        if hasattr(self, "hud") and self.hud is not None:
            self.hud.register_overlay(self._research_overlay)
        self._research_overlay.display_report(report_dict)
        self._research_overlay.show()
        self._research_overlay.raise_()

    def _preview_ui_color(self, hex_color: str):
        """Live preview — paints the whole interface the new colour (does NOT write to config)."""
        old = current_palette()
        if apply_ui_accent(hex_color):
            retheme_all_widgets(old, current_palette())

    def _apply_name_update(self, name: str, user_name: str, ui_color: str = "",
                           voice: str = "", tts_engine: str = "gemini",
                           el_key: str = "", el_voice: str = ""):
        """Update all name/theme-dependent UI elements and persist to config."""
        self._assistant_name = name.strip() or "Viernes"
        display = self._assistant_name.upper()
        self.setWindowTitle(f"{display} — {APP_VERSION}")
        self._title_lbl.setText(self._assistant_name)
        self._sub_lbl.setText(f"Asistente personal  ·  {APP_VERSION}")
        if hasattr(self, "_brand_logo"):
            self._brand_logo.setText((self._assistant_name[:1] or "V").upper())
        self._log._ai_name_lc = self._assistant_name.lower()
        self.hud._assistant_name = display

        color_changed = False
        if ui_color:
            old = current_palette()
            if apply_ui_accent(ui_color):
                # Live-paint the whole interface (panels, buttons, borders, HUD)
                retheme_all_widgets(old, current_palette())
                color_changed = old["PRI"] != C.PRI

        voice_changed = False
        if voice:
            from memory.config_manager import get_voice, save_voice
            if voice != get_voice():
                save_voice(voice)
                voice_changed = True

        engine_changed = False
        from memory.config_manager import get_tts_engine, save_tts_engine, save_elevenlabs_config
        old_engine = get_tts_engine()
        if tts_engine != old_engine:
            save_tts_engine(tts_engine)
            engine_changed = True
        save_elevenlabs_config(el_key, el_voice)

        try:
            data = _read_full_config()
            data["assistant_name"] = self._assistant_name
            data["user_name"] = user_name.strip()
            data["tts_engine"] = tts_engine
            data["elevenlabs_api_key"] = el_key.strip()
            data["elevenlabs_voice_id"] = el_voice.strip() or "21m00Tcm4TlvDq8ikWAM"
            if ui_color:
                data["ui_color"] = ui_color.strip().lower()
            API_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")
            self._log.append_log(f"SYS: Identity updated — {display}")
            if color_changed:
                self._log.append_log(f"SYS: UI colour applied — {ui_color}")
            if engine_changed:
                self._log.append_log(f"SYS: Voice engine set — {tts_engine.upper()}")
            if voice_changed and tts_engine == "gemini":
                self._log.append_log(f"SYS: Voice set — {voice}")
        except Exception as e:
            self._log.append_log(f"ERR: Config save failed — {e}")

        if (voice_changed or engine_changed) and self.on_voice_change:
            self.on_voice_change()

    def _centre_overlay(self, ov) -> None:
        """Place a floating overlay in the middle of the HUD and show it."""
        cw = self.centralWidget()
        ov.adjustSize()
        ov.setGeometry(
            max(0, (cw.width()  - ov.width())  // 2),
            max(0, (cw.height() - ov.height()) // 2),
            ov.width(), ov.height(),
        )
        if hasattr(self, "hud") and self.hud is not None:
            self.hud.register_overlay(ov)
        ov.show()
        ov.raise_()

    # ── Audio devices ────────────────────────────────────────────────────────

    def _open_audio_devices(self):
        ov = AudioDeviceOverlay(parent=self.centralWidget())
        ov.picked.connect(self._on_audio_devices_applied)
        self._centre_overlay(ov)
        self._audio_overlay = ov            # keep a reference so it isn't GC'd

    def _on_audio_devices_applied(self):
        self._log.append_log("SYS: Audio devices updated.")
        if self.on_audio_device_change:
            self.on_audio_device_change()

    # ── Memory panel ─────────────────────────────────────────────────────────

    def _open_memory_panel(self):
        ov = MemoryOverlay(parent=self.centralWidget())
        self._centre_overlay(ov)
        self._memory_overlay = ov

    def _open_books_library(self):
        ov = getattr(self, "_books_overlay", None)
        if ov is not None:
            ov.hide()
            ov.deleteLater()
            self._books_overlay = None
        ov = BooksLibraryOverlay(parent=self.centralWidget(), main_window=self)
        self._centre_overlay(ov)
        self._books_overlay = ov
        if hasattr(self, "hud") and self.hud is not None:
            self.hud.register_overlay(ov)
        ov.show()

    def _toggle_realtime_vision(self):
        try:
            from core.opencv_vision import get_opencv_vision
            coord = get_opencv_vision()
            is_active = coord.toggle_opencv_vision()
            if is_active:
                self.start_camera_stream()
                if hasattr(self, "_log") and self._log:
                    self._log.append_log("SYS: OpenCV ACTIVADO (detección de rostros, movimiento y QR en tiempo real).")
            else:
                self.stop_camera_stream()
                if hasattr(self, "_log") and self._log:
                    self._log.append_log("SYS: OpenCV en reposo.")
        except Exception as e:
            if hasattr(self, "_log") and self._log:
                self._log.append_log(f"ERR: Error en OpenCV: {e}")

    def _open_personality_settings(self):
        try:
            from core.personality_dialog import PersonalitySettingsDialog
            dlg = PersonalitySettingsDialog(self)
            dlg.exec()
            if hasattr(self, "_avatar_drawer") and self._avatar_drawer is not None:
                self._avatar_drawer.refresh_state()
        except Exception as e:
            if hasattr(self, "_log") and self._log:
                self._log.append_log(f"ERR: Error abriendo configuración de personalidad: {e}")

    def _open_vision_settings(self):
        try:
            from core.vision_settings_dialog import VisionSettingsDialog
            dlg = VisionSettingsDialog(self)
            dlg.exec()
        except Exception as e:
            if hasattr(self, "_log") and self._log:
                self._log.append_log(f"ERR: Error abriendo configuración de visión e IA: {e}")

    def _show_local_ai_status(self):
        self._open_vision_settings()

    def _open_sports_settings(self):
        try:
            from core.sports_settings_dialog import SportsSettingsDialog
            dlg = SportsSettingsDialog(self)
            dlg.exec()
        except Exception as e:
            if hasattr(self, "_log") and self._log:
                self._log.append_log(f"ERR: Error abriendo configuración de TV Deportiva: {e}")

    # ── Irreversible-action confirmation ─────────────────────────────────────

    def _show_confirm_banner(self, title: str, detail: str):
        self._hide_confirm_banner()
        ov = ConfirmBanner(title, detail, parent=self.centralWidget())
        ov.answered.connect(self._on_confirm_answered)
        self._centre_overlay(ov)
        self._confirm_overlay = ov

    def _hide_confirm_banner(self):
        ov = getattr(self, "_confirm_overlay", None)
        if ov is not None:
            ov.hide()
            ov.deleteLater()
            self._confirm_overlay = None

    def _on_confirm_answered(self, accepted: bool):
        # Tear the banner down first: core.confirm.resolve() may be about to
        # shut the machine down, and a live widget mid-callback is not where you
        # want to be when that happens.
        self._hide_confirm_banner()
        try:
            from core.confirm import resolve
            resolve(bool(accepted))
        except Exception as e:
            self._log.append_log(f"ERR: Confirmation failed — {e}")

    def _open_plugin_manager(self):
        self._open_plugin_settings()

    def _open_plugin_settings(self):
        sections = self.get_plugin_settings() if self.get_plugin_settings else []
        plugins = self.get_plugins() if self.get_plugins else []
        cw = self.centralWidget()
        ov = PluginSettingsOverlay(sections, plugins=plugins, parent=cw, runner=getattr(self, "run_plugin", None))
        ow = min(PluginSettingsOverlay._OW, cw.width() - 20)
        oh = min(580, max(460, cw.height() - 24))
        ov.setGeometry(
            (cw.width()  - ow) // 2,
            (cw.height() - oh) // 2,
            ow, oh,
        )
        if hasattr(self, "hud") and self.hud is not None:
            self.hud.register_overlay(ov)
        ov.show()
        ov.raise_()
        self._plugin_settings_overlay = ov

    # ── Clipboard intelligence ───────────────────────────────────────────────────

    def _on_clipboard_changed(self):
        try:
            text = QApplication.clipboard().text().strip()
            if len(text) >= 10:
                self._clipboard_sig.emit(text)
        except Exception:
            pass

    def _show_clipboard_panel(self, text: str):
        self._clipboard_panel.show_clipboard(text)
        self._position_clipboard_panel()

    def _position_clipboard_panel(self):
        cw = self.centralWidget()
        pw = ClipboardPanel._W
        ph = self._clipboard_panel.sizeHint().height() or ClipboardPanel._H
        x = (cw.width() - pw) // 2
        y = cw.height() - ph - 6
        self._clipboard_panel.setGeometry(x, y, pw, ph)
        self._clipboard_panel.raise_()

    def _on_clipboard_action(self, cmd: str):
        if self.on_text_command:
            threading.Thread(target=self.on_text_command, args=(cmd,), daemon=True).start()

    # ────────────────────────────────────────────────────────────────────────────

    def _do_interrupt(self):
        if getattr(self, "_video_fullscreen", False):
            self._toggle_video_fullscreen()
            return
        if getattr(self, "_avatar_only", False):
            self._toggle_avatar_only()
            return
        if self.isFullScreen():
            self.showNormal()
            self._update_fs_ui()
            return
        if self.on_interrupt:
            self.on_interrupt()

    def _toggle_mute(self):
        # A deliberate press settles the question: whatever the video did, or is
        # about to do, the user has now said what they want.
        self._video_auto_muted = False
        self._set_muted(not self._muted)

    def _set_muted(self, muted: bool, note: str = "", force: bool = False):
        muted = bool(muted)
        if muted == self._muted and not force:
            return
        self._muted = muted
        self.hud.muted = muted
        if hasattr(self, "_voice_monitor") and self._voice_monitor is not None:
            self._voice_monitor.set_muted(muted)
        self._style_mute_btn()
        if muted:
            self._apply_state("MUTED")
            self._log.append_log("SYS: Micrófono apagado." + (f" {note}" if note else ""))
        else:
            self._apply_state("LISTENING")
            self._log.append_log("SYS: Micrófono activo." + (f" {note}" if note else ""))

    def _style_mute_btn(self):
        if self._muted:
            self._mute_btn.setText("🔇  Silenciado")
            self._mute_btn.setStyleSheet(_ss_soft_btn(C.MUTED_C))
        else:
            self._mute_btn.setText("🎙  Micrófono")
            self._mute_btn.setStyleSheet(_ss_soft_btn(C.GREEN))

    def _send(self):
        txt = self._input.text().strip()
        if not txt: return
        self._input.clear()
        self._log.append_log(f"You: {txt}")
        if self.on_text_command:
            threading.Thread(target=self.on_text_command, args=(txt,), daemon=True).start()

    def _apply_state(self, state: str):
        prev = getattr(self.hud, "state", "")
        was_speaking = (prev == "SPEAKING") or getattr(self.hud, "speaking", False) or getattr(self, "speaking", False)
        is_speaking = (state == "SPEAKING")
        self.hud.state    = state
        self.hud.speaking = is_speaking
        self.speaking     = is_speaking
        if hasattr(self.hud, "_live2d_widget") and self.hud._live2d_widget is not None:
            self.hud._live2d_widget.set_state(state)
            self.hud._live2d_widget.set_speaking(is_speaking)
            if state == "SLEEPING":
                self.hud._live2d_widget.sleep()
            elif prev == "SLEEPING" and state != "SLEEPING":
                self.hud._live2d_widget.wake()
        if hasattr(self.hud, "_vrm_widget") and self.hud._vrm_widget is not None:
            self.hud._vrm_widget.set_state(state)
            self.hud._vrm_widget.set_speaking(is_speaking)
            if state == "SLEEPING":
                self.hud._vrm_widget.sleep()
            elif prev == "SLEEPING" and state != "SLEEPING":
                self.hud._vrm_widget.wake()
        if was_speaking and not is_speaking:
            if hasattr(self.hud, "notify_speech_finished"):
                self.hud.notify_speech_finished()
        if hasattr(self.hud, "_avatar") and self.hud._avatar is not None:
            if state == "SLEEPING" and not getattr(self.hud._avatar, "is_sleeping", False):
                self.hud._avatar.sleep()
            elif state != "SLEEPING" and getattr(self.hud._avatar, "is_sleeping", False):
                self.hud._avatar.wake()
        self._refresh_wake_btns()
        self._update_status_pill(state)
        if hasattr(self, "_voice_monitor") and self._voice_monitor is not None:
            self._voice_monitor.set_state(state)

        # Modulate power consumption based on active/sleeping state
        if state == "SLEEPING":
            _metrics.set_low_power(True)
            self._metric_tmr.setInterval(10000)
            if hasattr(self, "hud") and self.hud is not None:
                self.hud.set_low_power(True)
        else:
            _metrics.set_low_power(False)
            if not self.isMinimized():
                self._metric_tmr.setInterval(3000)
            if hasattr(self, "hud") and self.hud is not None:
                self.hud.set_low_power(False)

    def _check_config(self) -> bool:
        if not API_FILE.exists(): return False
        try:
            d = json.loads(API_FILE.read_text(encoding="utf-8"))
            return bool(d.get("gemini_api_key")) and bool(d.get("os_system"))
        except Exception:
            return False

    def _show_setup(self):
        ov = SetupOverlay(self.centralWidget())
        cw = self.centralWidget()
        ow, oh = 460, 390
        ov.setGeometry(
            (cw.width()  - ow) // 2,
            (cw.height() - oh) // 2,
            ow, oh,
        )
        ov.done.connect(self._on_setup_done)
        if hasattr(self, "hud") and self.hud is not None:
            self.hud.register_overlay(ov)
        ov.show()
        ov.raise_()
        self._overlay = ov

    def _on_setup_done(self, key: str, os_name: str):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        API_FILE.write_text(
            json.dumps({"gemini_api_key": key, "os_system": os_name}, indent=4),
            encoding="utf-8",
        )
        self._ready = True
        if self._overlay:
            self._overlay.hide()
            self._overlay = None
        self._apply_state("LISTENING")
        self._assistant_name = _read_full_config().get("assistant_name", "Viernes") or "Viernes"
        self._log.append_log(f"SYS: Initialised. OS={os_name.upper()}. {self._assistant_name} online.")


class _RootShim:
    def __init__(self, app: QApplication):
        self._app = app
    def mainloop(self):
        self._app.exec()
    def protocol(self, *_):
        pass


class ViernesUI:
    def __init__(self, face_path: str, size=None):
        self._app = QApplication.instance() or QApplication(sys.argv)
        self._app.setStyle("Fusion")
        self._win = MainWindow(face_path)
        self.root = _RootShim(self._app)
        self._win.show()

    @property
    def muted(self) -> bool:
        return self._win._muted

    @muted.setter
    def muted(self, v: bool):
        self.set_muted(bool(v))

    def set_muted(self, muted: bool, note: str = "") -> None:
        """Thread-safe: immediately update mic mute state and notify Qt main thread."""
        m = bool(muted)
        self._win._video_auto_muted = False
        self._win._muted = m
        self._win.hud.muted = m
        self._win._mute_sig.emit(m, str(note or ""))

    @property
    def current_file(self) -> str | None:
        return self._win._drop_zone.current_file() or self._win._current_file

    def set_uploaded_file(self, path: str) -> None:
        """Thread-safe: set the active file in the Desktop UI (e.g. when uploaded from phone)."""
        self._win._external_file_sig.emit(str(path or ""))

    @property
    def on_text_command(self):
        return self._win.on_text_command

    @on_text_command.setter
    def on_text_command(self, cb):
        self._win.on_text_command = cb

    @property
    def on_remote_clicked(self):
        return self._win.on_remote_clicked

    @on_remote_clicked.setter
    def on_remote_clicked(self, cb):
        self._win.on_remote_clicked = cb

    @property
    def on_interrupt(self):
        return self._win.on_interrupt

    @on_interrupt.setter
    def on_interrupt(self, cb):
        self._win.on_interrupt = cb

    @property
    def on_voice_change(self):
        return self._win.on_voice_change

    @on_voice_change.setter
    def on_voice_change(self, cb):
        self._win.on_voice_change = cb

    @property
    def on_audio_device_change(self):
        return self._win.on_audio_device_change

    @on_audio_device_change.setter
    def on_audio_device_change(self, cb):
        self._win.on_audio_device_change = cb

    def show_confirm(self, title: str, detail: str) -> None:
        """Thread-safe: raise the irreversible-action gate. Called from action
        handlers running in executor threads, so it goes through a signal."""
        self._win._confirm_sig.emit(str(title)[:120], str(detail)[:300])

    def hide_confirm(self) -> None:
        """Thread-safe: take the gate down."""
        self._win._confirm_hide_sig.emit()

    @property
    def get_plugins(self):
        return self._win.get_plugins

    @get_plugins.setter
    def get_plugins(self, cb):
        self._win.get_plugins = cb

    @property
    def get_plugin_settings(self):
        return self._win.get_plugin_settings

    @get_plugin_settings.setter
    def get_plugin_settings(self, cb):
        self._win.get_plugin_settings = cb

    @property
    def on_wake_toggle(self):
        return self._win.on_wake_toggle

    @on_wake_toggle.setter
    def on_wake_toggle(self, cb):
        self._win.on_wake_toggle = cb

    @property
    def on_wake_manual(self):
        return self._win.on_wake_manual

    @on_wake_manual.setter
    def on_wake_manual(self, cb):
        self._win.on_wake_manual = cb

    @property
    def wake_get_state(self):
        return self._win.wake_get_state

    @wake_get_state.setter
    def wake_get_state(self, cb):
        self._win.wake_get_state = cb

    def set_audio_level(self, level: float) -> None:
        """Thread-safe: feed a 0.0–1.0 live audio level to the HUD waveform.
        Called from the audio threads; a plain float store is atomic under the
        GIL, so no signal/lock is needed for this cosmetic value."""
        try:
            self._win.hud.set_audio_level(level)
        except Exception:
            pass

    def glance(self, dx: float, dy: float, hold: float = 1.1) -> None:
        """Ask the avatar to look somewhere for a moment (see HoloAvatar.glance)."""
        try:
            if self._avatar is not None:
                self._avatar.glance(dx, dy, hold)
        except Exception:
            pass

    @property
    def ptt_hold(self):
        return self._win.ptt_hold

    @ptt_hold.setter
    def ptt_hold(self, cb):
        self._win.ptt_hold = cb

    @property
    def on_push_to_talk(self):
        return self._win.on_push_to_talk

    @on_push_to_talk.setter
    def on_push_to_talk(self, cb):
        self._win.on_push_to_talk = cb

    def push_visemes(self, frames, hop: float, at: float) -> None:
        """Thread-safe: post a schedule of (level, openness, width) mouth frames
        for VIERNES's own speech. `at` is the wall-clock time the batch begins to
        sound, not the time of the call. See HudCanvas.push_visemes()."""
        try:
            self._win.hud.push_visemes(frames, hop, at)
        except Exception:
            pass

    def notify_phone_connected(self) -> None:
        self._win.notify_phone_connected()

    def set_state(self, state: str):
        self._win._state_sig.emit(state)

    def write_log(self, text: str):
        self._win._log_sig.emit(text)

    def wait_for_api_key(self):
        while not self._win._ready:
            time.sleep(0.1)

    def show_content(self, title: str, text: str):
        """Thread-safe: display content in the panel below the HUD."""
        self._win._content_sig.emit(title[:48], text[:4000])

    def show_research(self, report_dict: dict):
        """Thread-safe: open the research panel and display the full investigation report and sources."""
        self._win._research_sig.emit(report_dict)

    def show_quiz(self, topic: str, questions, grade=None) -> None:
        """Thread-safe: put an interactive quiz on the board.

        `grade(question, given)` decides each answer — the plugin supplies it so
        the marking rules live with the questions rather than being duplicated
        here. Returning None from it means "VIERNES should judge this one", which
        is how open answers and near-miss gap-fills are handled.

        Returns immediately: the user answers at their own pace and the finished
        result is delivered back through on_text_command.
        """
        self._win._quiz_sig.emit(str(topic or ""), list(questions or []), grade)

    def hide_quiz(self) -> None:
        """Thread-safe: clear any quiz currently on the board."""
        self._win._quiz_hide_sig.emit()

    def show_review(self, title: str, summary: str, findings, unclear=None) -> None:
        """Thread-safe: lay a document review into the panel below the HUD.

        `findings` is a list of {heading, detail, severity, quote, suggestion};
        severity is one of 'serious' / 'caution' / 'note' and decides colour and
        order here, so the caller supplies no styling of its own.
        """
        self._win._review_sig.emit(str(title or ""), str(summary or ""),
                                   list(findings or []), list(unclear or []))

    def prompt_reconfig(self):
        """Thread-safe: show the API key setup overlay (e.g. after an auth error)."""
        self._win._ready = False
        self._win._reconfig_sig.emit()

    def show_camera_frame(self, img_bytes: bytes):
        """Thread-safe: show a webcam frame in the small overlay (screen captures)."""
        self._win._camera_sig.emit(img_bytes)

    def show_video(self, source: str, title: str = "", muted: bool | None = None,
                   audio_source: str = "") -> None:
        """Thread-safe: play a video where the avatar normally is.

        `source` is a local path or a direct media URL. `audio_source` is for
        the case where the sound arrives as its own stream — YouTube serves no
        combined format any more — and when it is given the two are played
        together and kept in step.

        When `muted` is None (the default), uses the user's persisted mute
        preference from config/video_settings.json (default False so audio
        plays automatically unless the user toggled mute ON).
        """
        resolved_muted = _load_video_muted() if muted is None else bool(muted)
        self._win._video_open_sig.emit(str(source or ""), str(title or ""),
                                       resolved_muted, str(audio_source or ""))

    def show_sports_channel(self, url: str, title: str = "", frame_src: str = "",
                            frame_host: str = "", muted: bool | None = None,
                            options: list | None = None, selected_option: int = 1) -> None:
        """Thread-safe: open an ad-blocked direct iframe embed for a sports/TV channel in the HUD."""
        resolved_muted = _load_video_muted() if muted is None else bool(muted)
        self._win._sports_open_sig.emit(
            str(url or ""), str(frame_src or ""), str(title or ""), str(frame_host or ""),
            resolved_muted, list(options or []), int(selected_option or 1),
        )

    def show_radio(self, url: str, title: str = "", subtitle: str = "",
                   muted: bool | None = None) -> None:
        """Thread-safe: open an audio radio stream with visual spectrum in the HUD."""
        resolved_muted = _load_video_muted() if muted is None else bool(muted)
        self._win._radio_open_sig.emit(
            str(url or ""), str(title or ""), str(subtitle or ""), resolved_muted,
        )

    def open_cleanyourtv(self, ip: str = "") -> None:
        """Thread-safe: open the Clean Your TV 3-step visual wizard in the HUD."""
        self._win._cleanyourtv_sig.emit(str(ip or ""))

    def stop_video(self) -> None:
        """Thread-safe: close the video and give the HUD back to the avatar."""
        self._win._video_close_sig.emit()

    def set_video_muted(self, muted: bool) -> None:
        """Thread-safe: silence or unsilence whatever is playing."""
        self._win._video_mute_sig.emit(bool(muted))

    def set_video_fullscreen(self, fullscreen: bool = True) -> None:
        """Thread-safe: enter or exit video fullscreen mode."""
        self._win._video_fs_sig.emit(bool(fullscreen))

    def video_is_playing(self) -> bool:
        return bool(self._win.video_is_playing())

    def start_camera_stream(self) -> None:
        """Thread-safe: start live camera feed in the full HUD area."""
        self._win.start_camera_stream()

    def stop_camera_stream(self) -> None:
        """Thread-safe: stop the live camera feed."""
        self._win.stop_camera_stream()

    @property
    def assistant_name(self) -> str:
        return self._win._assistant_name

    def start_speaking(self):
        self.set_state("SPEAKING")

    def stop_speaking(self):
        if not self.muted:
            self.set_state("LISTENING")

    def set_emotion(self, name: str, intensity: float = 1.0, duration: float = 0.0) -> None:
        """Thread-safe: trigger an emotional reaction for Edith / Avatar."""
        self._win._emotion_sig.emit(str(name), float(intensity), float(duration))

    def trigger_action(self, name: str) -> None:
        """Thread-safe: trigger an autonomous action (dance, stretch, yawn, etc.)."""
        self._win._action_sig.emit(str(name))

    def set_semantic_intent(self, intent: str, metadata: dict | None = None) -> None:
        """Thread-safe: trigger semantic expressive behavior (explain, emphasize, present, confirm, etc.)."""
        self._win._semantic_intent_sig.emit(str(intent), metadata or {})

    def trigger_gesture(self, name: str, duration: float = 0.0, intensity: float = 1.0) -> None:
        """Thread-safe: trigger explicit arm/body gesture from GestureLibrary."""
        self._win._gesture_sig.emit(str(name), float(duration), float(intensity))

    def holo_start(self, tool: str, detail: str = "") -> None:
        """Thread-safe: show the holographic floating screens for a running tool."""
        ov = getattr(self._win.hud, "_holo_overlay", None)
        if ov is not None:
            ov.start_sig.emit(str(tool), str(detail))

    def holo_stop(self) -> None:
        """Thread-safe: fade the holographic screens out."""
        ov = getattr(self._win.hud, "_holo_overlay", None)
        if ov is not None:
            ov.stop_sig.emit()

    def interrupt_gestures(self) -> None:
        """Thread-safe: smoothly recover and abort active gestures."""
        self._win._interrupt_gestures_sig.emit()

    def set_float_mode(self, mode: str) -> None:
        """Thread-safe: set holographic floating mode."""
        self._win._float_mode_sig.emit(str(mode))

    def notify_task_completed(self) -> None:
        """Thread-safe: announce successful completion of a task."""
        self.set_emotion("proud", 0.9, 3.5)
        self.trigger_action("ENCOURAGE_CLAP")

    def notify_task_error(self, error_msg: str = "") -> None:
        """Thread-safe: announce an error or unexpected condition."""
        self.set_emotion("confused", 0.8, 3.0)

    def show_visual_card(self, card_data: object) -> None:
        """Thread-safe: display a dynamic, contextual visual panel to Edith's right."""
        self._win._visual_card_sig.emit(card_data)

    def hide_visual_card(self) -> None:
        """Thread-safe: smoothly hide the visual panel."""
        self._win._visual_hide_sig.emit()

    def open_gods_eye(self, location: str = "", sensor: str = "") -> None:
        pass

    def close_gods_eye(self) -> None:
        pass

    def gods_eye_fly_to(self, location: str) -> None:
        pass

    def gods_eye_set_sensor(self, mode: str) -> None:
        pass

    def gods_eye_track(self, target: str) -> None:
        pass


# Backward-compatible alias
ViernesUI = ViernesUI
