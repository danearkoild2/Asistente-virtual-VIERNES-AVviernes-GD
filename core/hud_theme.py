from __future__ import annotations

import colorsys
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
HUD_CONFIG_FILE = BASE_DIR / "config" / "hud_studio.json"

HUD_THEMES: dict[str, dict[str, Any]] = {
    "obsidian_pro": {
        "name": "Obsidian Glass Pro",
        "subtitle": "Carbono profundo · Índigo & Cian",
        "palette": {
            "BG": "#0B0D12",
            "PANEL": "#121620",
            "PANEL2": "#191F2E",
            "BORDER": "#242B3D",
            "BORDER_B": "#36415C",
            "BORDER_A": "#1A2030",
            "PRI": "#6366F1",
            "PRI_DIM": "#4F46E5",
            "PRI_GHO": "#1C1F3B",
            "ACC": "#38BDF8",
            "ACC2": "#F59E0B",
            "GREEN": "#10B981",
            "GREEN_D": "#059669",
            "RED": "#F43F5E",
            "MUTED_C": "#F43F5E",
            "TEXT": "#F1F5F9",
            "TEXT_DIM": "#64748B",
            "TEXT_MED": "#94A3B8",
            "WHITE": "#FFFFFF",
            "DARK": "#07090D",
            "BAR_BG": "#1E2536",
        },
    },
    "midnight_cyan": {
        "name": "Midnight Telemetry",
        "subtitle": "Azul abisal · Cian eléctrico",
        "palette": {
            "BG": "#060A13",
            "PANEL": "#0C1322",
            "PANEL2": "#131D33",
            "BORDER": "#1D2B48",
            "BORDER_B": "#2B406B",
            "BORDER_A": "#141E33",
            "PRI": "#06B6D4",
            "PRI_DIM": "#0891B2",
            "PRI_GHO": "#102A3A",
            "ACC": "#3B82F6",
            "ACC2": "#FBBF24",
            "GREEN": "#22C55E",
            "GREEN_D": "#16A34A",
            "RED": "#FB7185",
            "MUTED_C": "#FB7185",
            "TEXT": "#E2E8F0",
            "TEXT_DIM": "#64748B",
            "TEXT_MED": "#94A3B8",
            "WHITE": "#F8FAFC",
            "DARK": "#04070E",
            "BAR_BG": "#16223B",
        },
    },
    "emerald_ops": {
        "name": "Emerald Ops",
        "subtitle": "Grafito táctico · Esmeralda",
        "palette": {
            "BG": "#080D0B",
            "PANEL": "#0F1814",
            "PANEL2": "#16241E",
            "BORDER": "#21362D",
            "BORDER_B": "#2F4F41",
            "BORDER_A": "#16251F",
            "PRI": "#10B981",
            "PRI_DIM": "#059669",
            "PRI_GHO": "#102E23",
            "ACC": "#38BDF8",
            "ACC2": "#EAB308",
            "GREEN": "#34D399",
            "GREEN_D": "#10B981",
            "RED": "#F87171",
            "MUTED_C": "#F87171",
            "TEXT": "#ECFDF5",
            "TEXT_DIM": "#6B8A7E",
            "TEXT_MED": "#9BB8AC",
            "WHITE": "#FFFFFF",
            "DARK": "#050907",
            "BAR_BG": "#1A2B24",
        },
    },
    "crimson_apex": {
        "name": "Apex Crimson",
        "subtitle": "Obsidiana · Carmesí & Coral",
        "palette": {
            "BG": "#0D090C",
            "PANEL": "#161015",
            "PANEL2": "#20171E",
            "BORDER": "#33232F",
            "BORDER_B": "#4D3446",
            "BORDER_A": "#221820",
            "PRI": "#F43F5E",
            "PRI_DIM": "#E11D48",
            "PRI_GHO": "#351520",
            "ACC": "#FB923C",
            "ACC2": "#FBBF24",
            "GREEN": "#34D399",
            "GREEN_D": "#10B981",
            "RED": "#FB7185",
            "MUTED_C": "#FB7185",
            "TEXT": "#F8FAFC",
            "TEXT_DIM": "#8A6D7E",
            "TEXT_MED": "#B89DAD",
            "WHITE": "#FFFFFF",
            "DARK": "#080507",
            "BAR_BG": "#291C26",
        },
    },
    "amber_studio": {
        "name": "Amber Studio",
        "subtitle": "Carbón cálido · Oro & Ámbar",
        "palette": {
            "BG": "#0F0D0A",
            "PANEL": "#18140F",
            "PANEL2": "#221D15",
            "BORDER": "#362E22",
            "BORDER_B": "#4F4331",
            "BORDER_A": "#241F17",
            "PRI": "#F59E0B",
            "PRI_DIM": "#D97706",
            "PRI_GHO": "#332610",
            "ACC": "#FB923C",
            "ACC2": "#FDE047",
            "GREEN": "#34D399",
            "GREEN_D": "#10B981",
            "RED": "#F87171",
            "MUTED_C": "#F87171",
            "TEXT": "#FAF7F2",
            "TEXT_DIM": "#8C8070",
            "TEXT_MED": "#B8AA98",
            "WHITE": "#FFFFFF",
            "DARK": "#090806",
            "BAR_BG": "#2B241A",
        },
    },
    "monochrome_stealth": {
        "name": "Stealth Monochrome",
        "subtitle": "Negro mate · Platino minimal",
        "palette": {
            "BG": "#09090B",
            "PANEL": "#121216",
            "PANEL2": "#1A1A20",
            "BORDER": "#27272F",
            "BORDER_B": "#3B3B47",
            "BORDER_A": "#1B1B22",
            "PRI": "#E4E4E7",
            "PRI_DIM": "#A1A1AA",
            "PRI_GHO": "#27272E",
            "ACC": "#38BDF8",
            "ACC2": "#FBBF24",
            "GREEN": "#34D399",
            "GREEN_D": "#10B981",
            "RED": "#F87171",
            "MUTED_C": "#F87171",
            "TEXT": "#FAFAFA",
            "TEXT_DIM": "#71717A",
            "TEXT_MED": "#A1A1AA",
            "WHITE": "#FFFFFF",
            "DARK": "#050507",
            "BAR_BG": "#22222A",
        },
    },
}

LAYOUT_PRESETS: dict[str, dict[str, Any]] = {
    "studio": {
        "label": "Estudio Completo",
        "desc": "3 columnas equilibradas con telemetría, HUD central y chat.",
        "show_left_panel": True,
        "show_right_panel": True,
        "left_width": 266,
        "right_width": 356,
        "widgets": {
            "voice_monitor": True,
            "weather": True,
            "system_metrics": True,
            "news_panel": True,
            "attachments": True,
        },
    },
    "focus": {
        "label": "Modo Enfoque",
        "desc": "Oculta la barra lateral izquierda y da prioridad al HUD y chat.",
        "show_left_panel": False,
        "show_right_panel": True,
        "left_width": 250,
        "right_width": 340,
        "widgets": {
            "voice_monitor": True,
            "weather": True,
            "system_metrics": True,
            "news_panel": False,
            "attachments": True,
        },
    },
    "cinematic": {
        "label": "Modo Cinema / HUD Puro",
        "desc": "Maximiza el lienzo central para el avatar, TV, video o radio.",
        "show_left_panel": False,
        "show_right_panel": False,
        "left_width": 250,
        "right_width": 340,
        "widgets": {
            "voice_monitor": False,
            "weather": False,
            "system_metrics": False,
            "news_panel": False,
            "attachments": False,
        },
    },
    "command": {
        "label": "Centro de Comando",
        "desc": "Telemetría ampliada y panel de conversación ancho.",
        "show_left_panel": True,
        "show_right_panel": True,
        "left_width": 295,
        "right_width": 400,
        "widgets": {
            "voice_monitor": True,
            "weather": True,
            "system_metrics": True,
            "news_panel": True,
            "attachments": True,
        },
    },
}

DEFAULT_HUD_CONFIG: dict[str, Any] = {
    "theme_id": "obsidian_pro",
    "accent_override": "",
    "layout_preset": "studio",
    "density": "balanced",  # compact | balanced | spacious
    "card_radius": 12,
    "show_left_panel": True,
    "show_right_panel": True,
    "left_width": 266,
    "right_width": 356,
    "glass_glow": True,
    "hud_grid": True,
    "bg_mode": "aurora_atmos",
    "bg_custom_path": "",
    "bg_dim": 0.42,
    "bg_glow": 0.65,
    "widgets": {
        "voice_monitor": True,
        "weather": True,
        "system_metrics": True,
        "news_panel": True,
        "attachments": True,
    },
}

HUD_BACKGROUNDS: dict[str, dict[str, str]] = {
    "aurora_atmos": {
        "name": "Aurora Atmosférica",
        "desc": "Ondas suaves de luz adaptadas al color de tu tema.",
        "kind": "procedural",
    },
    "studio_pro": {
        "name": "Estudio Arquitectónico",
        "desc": "Fondo limpio de estudio oscuro con iluminación cenital.",
        "kind": "procedural",
    },
    "orbital_horizon": {
        "name": "Horizonte Orbital",
        "desc": "Arco atmosférico y estrellas tenues de alta precisión.",
        "kind": "procedural",
    },
    "neural_mesh": {
        "name": "Malla Neural Táctica",
        "desc": "Red geométrica sutil que reacciona al ritmo de la voz.",
        "kind": "procedural",
    },
    "penthouse_night": {
        "name": "Penthouse Nocturno",
        "desc": "Estudio panorámico nocturno con ciudad bokeh.",
        "kind": "image",
        "file": "viernes/bg_penthouse.jpg",
    },
    "command_bridge": {
        "name": "Puente de Comando",
        "desc": "Arquitectura minimalista oscura de alta tecnología.",
        "kind": "image",
        "file": "viernes/bg_command.jpg",
    },
    "zen_loft": {
        "name": "Loft Arquitectónico",
        "desc": "Concreto oscuro, cristal ahumado e iluminación cálida.",
        "kind": "image",
        "file": "viernes/bg_loft.jpg",
    },
    "auto": {
        "name": "Ciclo Solar (Hora Real)",
        "desc": "Cambia automáticamente según mañana, día, tarde y noche.",
        "kind": "cycle",
    },
    "custom_image": {
        "name": "Imagen Personalizada",
        "desc": "Usa cualquier wallpaper o fotografía local de tu equipo.",
        "kind": "custom",
    },
}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_hud_config() -> dict[str, Any]:
    try:
        if HUD_CONFIG_FILE.exists():
            raw = json.loads(HUD_CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                cfg = _deep_merge(DEFAULT_HUD_CONFIG, raw)
                if cfg.get("theme_id") not in HUD_THEMES:
                    cfg["theme_id"] = "obsidian_pro"
                return cfg
    except Exception:
        pass
    return deepcopy(DEFAULT_HUD_CONFIG)


def save_hud_config(cfg: dict[str, Any]) -> dict[str, Any]:
    merged = _deep_merge(DEFAULT_HUD_CONFIG, cfg)
    try:
        HUD_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        HUD_CONFIG_FILE.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    return merged


def _hex_to_hsv(hex_str: str) -> tuple[float, float, float]:
    h = hex_str.strip().lstrip("#")
    r = int(h[0:2], 16) / 255.0
    g = int(h[2:4], 16) / 255.0
    b = int(h[4:6], 16) / 255.0
    return colorsys.rgb_to_hsv(r, g, b)


def _hsv_to_hex(h: float, s: float, v: float) -> str:
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, max(0.0, min(1.0, s)), max(0.0, min(1.0, v)))
    return "#{:02X}{:02X}{:02X}".format(int(r * 255 + 0.5), int(g * 255 + 0.5), int(b * 255 + 0.5))


def get_theme_palette(theme_id: str, accent_override: str = "") -> dict[str, str]:
    theme = HUD_THEMES.get(theme_id) or HUD_THEMES["obsidian_pro"]
    pal = dict(theme["palette"])
    acc = (accent_override or "").strip()
    if acc.startswith("#") and len(acc) == 7:
        try:
            int(acc[1:], 16)
            ah, asat, aval = _hex_to_hsv(acc)
            pal["PRI"] = acc.upper()
            pal["PRI_DIM"] = _hsv_to_hex(ah, min(1.0, asat * 1.05), max(0.25, aval * 0.78))
            pal["PRI_GHO"] = _hsv_to_hex(ah, max(0.15, asat * 0.55), 0.22)
        except Exception:
            pass
    return pal
