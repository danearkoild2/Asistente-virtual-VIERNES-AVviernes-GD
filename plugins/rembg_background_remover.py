"""
AI Image Background Remover Plugin for VIERNES.
Removes backgrounds from photos and graphics, outputting transparent PNGs using rembg or PIL fallback.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from PIL import Image

PLUGIN = {
    "name": "rembg_background_remover",
    "description": (
        "Removes backgrounds from pictures, logos, portraits, or screenshots to create transparent PNGs. "
        "Use when user asks 'quita el fondo a esta imagen', 'remove background', "
        "'haz transparente esta foto', or 'fondo transparente imagen'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "image_path": {
                "type": "STRING",
                "description": "Path to the input image file. If omitted, uses the latest image found in Downloads or Pictures."
            },
            "output_path": {
                "type": "STRING",
                "description": "Optional custom path for the output transparent PNG."
            }
        },
        "required": [],
    },
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def _find_latest_image() -> Optional[Path]:
    """Look for the most recent image across Downloads, Pictures, and Desktop."""
    candidates = []
    for folder in [Path.home() / "Downloads", Path.home() / "Pictures", Path.home() / "Desktop"]:
        if folder.exists():
            for f in folder.iterdir():
                if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS:
                    candidates.append(f)
    if not candidates:
        return None
    return max(candidates, key=lambda f: f.stat().st_mtime)


def _remove_background_pil_fallback(img: Image.Image) -> Image.Image:
    """Corner-color flood keying fallback when rembg neural model is not yet compiled."""
    img = img.convert("RGBA")
    data = img.getdata()
    # Sample corner pixels to detect solid background color
    w, h = img.size
    corners = [img.getpixel((0, 0)), img.getpixel((w - 1, 0)), img.getpixel((0, h - 1)), img.getpixel((w - 1, h - 1))]
    bg_r = sum(c[0] for c in corners) // 4
    bg_g = sum(c[1] for c in corners) // 4
    bg_b = sum(c[2] for c in corners) // 4

    new_data = []
    tolerance = 38
    for item in data:
        r, g, b, a = item
        if abs(r - bg_r) < tolerance and abs(g - bg_g) < tolerance and abs(b - bg_b) < tolerance:
            new_data.append((255, 255, 255, 0))  # Transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img


def run(parameters: dict, player=None, session_memory=None) -> str:
    img_arg = (parameters.get("image_path") or "").strip()
    out_arg = (parameters.get("output_path") or "").strip()

    target_path = None
    if img_arg:
        p = Path(img_arg)
        if p.exists() and p.is_file():
            target_path = p
        else:
            return f"No se encontró la imagen en la ruta especificada: {img_arg}."
    else:
        target_path = _find_latest_image()
        if not target_path:
            return "No se especificó ninguna imagen y no se encontraron imágenes recientes en tus carpetas de Descargas o Imágenes."

    # Determine output path
    if out_arg:
        output_path = Path(out_arg)
    else:
        output_path = target_path.parent / f"{target_path.stem}_nobg.png"

    used_engine = "pil"
    try:
        # Check if rembg is available
        try:
            from rembg import remove as rembg_remove
            with open(target_path, "rb") as inp_f:
                result_bytes = rembg_remove(inp_f.read())
            with open(output_path, "wb") as out_f:
                out_f.write(result_bytes)
            used_engine = "rembg_ai"
        except ImportError:
            # High-precision PIL transparent color extractor
            with Image.open(target_path) as im:
                nobg = _remove_background_pil_fallback(im)
                nobg.save(output_path, "PNG")
            used_engine = "color_keying"
    except Exception as exc:
        return f"Error al procesar la imagen {target_path.name}: {exc}"

    if used_engine == "rembg_ai":
        msg = f"¡Fondo eliminado con IA exitosamente! Tu imagen transparente fue guardada como {output_path.name} en {output_path.parent}."
    else:
        msg = f"Fondo procesado con éxito. Se guardó tu imagen transparente como {output_path.name} en {output_path.parent}."

    if player:
        try:
            player.write_log(f"MEDIA: Removed background -> {output_path}")
        except Exception:
            pass

    return msg
