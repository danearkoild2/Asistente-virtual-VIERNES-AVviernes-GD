"""
Live2D Skin / Model Manager
===========================
Discovers, tracks, and manages Live2D Cubism characters and skins.
Scans the dedicated 'live2d_models' directory and 'edith' directory.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent.parent


BASE_DIR = _get_base_dir()
LIVE2D_DIR = BASE_DIR / "core" / "live2d"
MODELS_DIR = BASE_DIR / "live2d_models"
EDITH_DIR = BASE_DIR / "edith"


def ensure_models_dir() -> Path:
    """Ensure live2d_models folder exists with a helpful README."""
    if not MODELS_DIR.exists():
        try:
            MODELS_DIR.mkdir(parents=True, exist_ok=True)
            readme = MODELS_DIR / "README.txt"
            if not readme.exists():
                readme.write_text(
                    "=====================================================\n"
                    "CARPETA DE MODELOS / SKINS LIVE2D (MARK LV / VIERNES)\n"
                    "=====================================================\n\n"
                    "Para agregar un nuevo personaje o skin Live2D:\n"
                    "1. Crea una carpeta aqui con el nombre del personaje (ejemplo: 'Hiyori', 'Miku', 'Edith Maid', etc.).\n"
                    "2. Pega dentro de esa carpeta todos los archivos del modelo:\n"
                    "   - Archivo .model3.json\n"
                    "   - Archivo .moc3\n"
                    "   - Carpeta de texturas (textures/)\n"
                    "   - Archivos de fisica o expresiones (.physics3.json, etc.)\n\n"
                    "3. En el menu de Avatar (icono de controles en el header), aparecera automaticamente\n"
                    "   el selector de Personaje con tu nueva skin lista para usar con toda la fisica,\n"
                    "   sincronizacion de voz y seguimiento de mirada!\n",
                    encoding="utf-8"
                )
        except Exception as e:
            print(f"[Live2DSkins] Warning creating models dir: {e}")
    return MODELS_DIR


def discover_live2d_skins() -> dict[str, dict]:
    """
    Scan for all available Live2D models.
    Returns:
        dict mapping skin_name -> {
            'name': str,
            'folder': Path,
            'model_file': Path,
            'model_url': str,  # relative to core/live2d/viewer.html
            'is_default': bool,
        }
    """
    ensure_models_dir()
    skins: dict[str, dict] = {}

    # 1. Default Edith
    edith_model = EDITH_DIR / "edith.model3.json"
    if not edith_model.exists():
        edith_model = EDITH_DIR / "edith_hq.model3.json"

    if edith_model.exists():
        rel = os.path.relpath(edith_model, LIVE2D_DIR).replace("\\", "/")
        skins["Edith"] = {
            "name": "Edith",
            "folder": EDITH_DIR,
            "model_file": edith_model,
            "model_url": rel,
            "is_default": True,
        }

    # 2. Scan dedicated live2d_models/ folder
    if MODELS_DIR.exists():
        for item in sorted(MODELS_DIR.iterdir()):
            if item.is_dir() and not item.name.startswith("."):
                # Look for .model3.json or AI-generated .edith2d.json directly in folder or 1 level deep
                model_files = list(item.glob("*.model3.json")) + list(item.glob("*.edith2d.json"))
                if not model_files:
                    model_files = list(item.glob("*/*.model3.json")) + list(item.glob("*/*.edith2d.json"))
                if model_files:
                    model_file = model_files[0]
                    skin_name = item.name.replace("_", " ").strip()
                    rel = os.path.relpath(model_file, LIVE2D_DIR).replace("\\", "/")
                    skins[skin_name] = {
                        "name": skin_name,
                        "folder": item,
                        "model_file": model_file,
                        "model_url": rel,
                        "is_default": False,
                    }

    # 3. Check optional edith/skins folder
    edith_skins = EDITH_DIR / "skins"
    if edith_skins.exists():
        for item in sorted(edith_skins.iterdir()):
            if item.is_dir() and not item.name.startswith("."):
                model_files = list(item.glob("*.model3.json"))
                if model_files:
                    model_file = model_files[0]
                    skin_name = f"Edith ({item.name.replace('_', ' ').title()})"
                    rel = os.path.relpath(model_file, LIVE2D_DIR).replace("\\", "/")
                    if skin_name not in skins:
                        skins[skin_name] = {
                            "name": skin_name,
                            "folder": item,
                            "model_file": model_file,
                            "model_url": rel,
                            "is_default": False,
                        }

    return skins


def get_skin_model_url(skin_name: str) -> str:
    """Return relative model_url for given skin_name, or default to Edith."""
    skins = discover_live2d_skins()
    target = (skin_name or "").strip().lower()
    for name, data in skins.items():
        if name.lower() == target:
            return data["model_url"]
    # Fallback to Edith or first available skin
    if "Edith" in skins:
        return skins["Edith"]["model_url"]
    if skins:
        return next(iter(skins.values()))["model_url"]
    return "../../edith/edith.model3.json"


def open_skins_folder() -> None:
    """Open the live2d_models folder in the OS file manager."""
    ensure_models_dir()
    try:
        if sys.platform == "win32":
            os.startfile(str(MODELS_DIR))
        elif sys.platform == "darwin":
            import subprocess
            subprocess.Popen(["open", str(MODELS_DIR)])
        else:
            import subprocess
            subprocess.Popen(["xdg-open", str(MODELS_DIR)])
    except Exception as e:
        print(f"[Live2DSkins] Error opening folder: {e}")
