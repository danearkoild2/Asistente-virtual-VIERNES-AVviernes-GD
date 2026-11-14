"""
Quick Image Converter & Optimizer Plugin for MARK LV / Viernes.
Converts and compresses images (PNG, JPG, WebP) in Downloads/Desktop.
"""
from __future__ import annotations
from pathlib import Path
import os

PLUGIN = {
    "name": "image_optimizer",
    "description": (
        "Converts and compresses images (e.g. to PNG, JPG, or WebP). "
        "Use when user asks 'convierte esta imagen a png', 'convierte a webp', "
        "or 'comprime esta imagen'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "format": {
                "type": "STRING",
                "description": "Target format: 'png', 'jpg', 'webp'. Defaults to 'webp'.",
            },
            "filename": {
                "type": "STRING",
                "description": "Optional image name or path. If omitted, uses most recent image in Downloads.",
            }
        },
        "required": [],
    },
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    target_fmt = parameters.get("format", "webp").strip().lower().replace(".", "")
    custom_name = parameters.get("filename", "").strip()

    search_dirs = [Path.home() / "Downloads", Path.home() / "Desktop"]
    src_img = None

    if custom_name:
        for d in search_dirs:
            candidate = d / custom_name
            if candidate.exists():
                src_img = candidate
                break
    else:
        # Find newest image
        img_exts = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
        newest_time = 0
        for d in search_dirs:
            if not d.exists(): continue
            for f in d.iterdir():
                if f.suffix.lower() in img_exts and f.stat().st_mtime > newest_time:
                    newest_time = f.stat().st_mtime
                    src_img = f

    if not src_img or not src_img.exists():
        return "No se encontró ninguna imagen reciente en Descargas o Escritorio para procesar."

    try:
        from PIL import Image
        im = Image.open(src_img)
        dest_path = src_img.parent / f"{src_img.stem}_converted.{target_fmt}"
        if target_fmt in ("jpg", "jpeg") and im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        im.save(dest_path, target_fmt.upper(), optimize=True)
        orig_kb = src_img.stat().st_size / 1024
        new_kb = dest_path.stat().st_size / 1024
        msg = f"Imagen '{src_img.name}' convertida exitosamente a {target_fmt.upper()} ({new_kb:.1f} KB). Guardada en {dest_path.name}."
    except Exception as e:
        msg = f"No se pudo convertir la imagen: {e}"

    if player:
        try:
            player.write_log(f"SYS: {msg}")
        except Exception:
            pass

    return msg
