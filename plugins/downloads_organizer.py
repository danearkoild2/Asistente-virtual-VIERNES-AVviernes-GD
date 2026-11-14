"""
Downloads Auto-Organizer Plugin for MARK LV / Viernes.
Sorts cluttered files in Downloads folder into categorized directories.
"""
from __future__ import annotations
import shutil
from pathlib import Path

PLUGIN = {
    "name": "downloads_organizer",
    "description": (
        "Organizes the user's Downloads folder by categorizing files into Documents, Images, "
        "Videos, Audio, Archives, and Installers. "
        "Use when user asks 'organiza mis descargas', 'organize downloads folder', "
        "or 'limpia la carpeta descargas'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {},
        "required": [],
    },
}

CATEGORIES = {
    "Imágenes": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".ico", ".psd"],
    "Documentos": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv", ".epub"],
    "Instaladores": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
    "Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"],
    "Código": [".py", ".js", ".html", ".css", ".json", ".cpp", ".c", ".ts", ".java"],
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    downloads = Path.home() / "Downloads"
    if not downloads.exists():
        return "No se pudo encontrar la carpeta de Descargas del usuario."

    moved_count = 0
    cat_counts = {}

    for item in downloads.iterdir():
        if item.is_dir() or item.name.startswith("."):
            continue

        ext = item.suffix.lower()
        target_folder_name = "Otros"
        for cat_name, extensions in CATEGORIES.items():
            if ext in extensions:
                target_folder_name = cat_name
                break

        dest_dir = downloads / target_folder_name
        dest_dir.mkdir(exist_ok=True)
        dest_path = dest_dir / item.name

        # Avoid collision
        if dest_path.exists():
            dest_path = dest_dir / f"{item.stem}_{item.stat().st_mtime_ns}{item.suffix}"

        try:
            shutil.move(str(item), str(dest_path))
            moved_count += 1
            cat_counts[target_folder_name] = cat_counts.get(target_folder_name, 0) + 1
        except Exception:
            continue

    if moved_count == 0:
        msg = "La carpeta de Descargas ya está completamente ordenada. No hay archivos sueltos."
    else:
        details = ", ".join(f"{cnt} en {cat}" for cat, cnt in cat_counts.items())
        msg = f"Se organizaron {moved_count} archivos en Descargas ({details})."

    if player:
        try:
            player.write_log(f"SYS: {msg}")
        except Exception:
            pass

    return msg
