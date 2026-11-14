"""
Window Layout Manager Plugin for MARK LV / Viernes.
Organizes open windows on screen into productive split/centered presets via Windows user32.
"""
from __future__ import annotations
import ctypes
from ctypes import wintypes
import time
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "window_layout_manager",
    "description": (
        "Snaps and arranges application windows on screen (left split, right split, center, minimize all, maximize). "
        "Use when user asks 'acomoda mis ventanas', 'organiza la pantalla', 'modo dos columnas', "
        "or 'centra esta ventana'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "layout": {
                "type": "STRING",
                "description": "'left_half', 'right_half', 'center', 'maximize', 'minimize_others', or 'split_two'.",
            }
        },
        "required": ["layout"],
    },
}

PLUGIN_SETTINGS = {
    "title": "Organizador de Ventanas",
    "fields": [
        {
            "key": "snap_margins",
            "label": "Márgenes en Pantalla (px)",
            "type": "choice",
            "options": ["0", "6", "12", "20"],
            "default": "6",
        },
    ],
}

user32 = ctypes.windll.user32

def _get_active_window() -> int:
    return user32.GetForegroundWindow()

def _get_screen_workarea() -> tuple[int, int, int, int]:
    # SystemParametersInfoW SPI_GETWORKAREA = 0x0030
    rect = wintypes.RECT()
    user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(rect), 0)
    return rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top

def run(parameters: dict, player=None, session_memory=None) -> str:
    layout = str(parameters.get("layout", "split_two")).lower().strip()
    margin = int(get_plugin_setting("window_layout_manager", "snap_margins", 6))
    
    hwnd = _get_active_window()
    if not hwnd:
        return "No pude detectar una ventana activa en primer plano."

    sx, sy, sw, sh = _get_screen_workarea()

    SWP_NOZORDER = 0x0004
    SWP_SHOWWINDOW = 0x0040

    if layout in ("left_half", "izquierda", "left"):
        w = (sw // 2) - (margin * 2)
        h = sh - (margin * 2)
        x = sx + margin
        y = sy + margin
        user32.ShowWindow(hwnd, 9) # SW_RESTORE
        user32.SetWindowPos(hwnd, 0, x, y, w, h, SWP_NOZORDER | SWP_SHOWWINDOW)
        report = "Ventana anclada a la mitad izquierda de la pantalla."

    elif layout in ("right_half", "derecha", "right"):
        w = (sw // 2) - (margin * 2)
        h = sh - (margin * 2)
        x = sx + (sw // 2) + margin
        y = sy + margin
        user32.ShowWindow(hwnd, 9)
        user32.SetWindowPos(hwnd, 0, x, y, w, h, SWP_NOZORDER | SWP_SHOWWINDOW)
        report = "Ventana anclada a la mitad derecha de la pantalla."

    elif layout in ("center", "centrar"):
        w = int(sw * 0.72)
        h = int(sh * 0.82)
        x = sx + (sw - w) // 2
        y = sy + (sh - h) // 2
        user32.ShowWindow(hwnd, 9)
        user32.SetWindowPos(hwnd, 0, x, y, w, h, SWP_NOZORDER | SWP_SHOWWINDOW)
        report = "Ventana centrada con vista enfocada."

    elif layout in ("maximize", "maximizar"):
        user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
        report = "Ventana maximizada."

    else:
        # Default snap left
        w = (sw // 2) - (margin * 2)
        h = sh - (margin * 2)
        user32.ShowWindow(hwnd, 9)
        user32.SetWindowPos(hwnd, 0, sx + margin, sy + margin, w, h, SWP_NOZORDER | SWP_SHOWWINDOW)
        report = "Disposición de pantalla aplicada."

    if player:
        try:
            player.write_log(f"🪟 WINDOW MANAGER: {report}")
        except Exception:
            pass

    return f"Listo. {report}"
