"""
Duplicate File Finder Plugin for MARK LV / Viernes.
Finds identical duplicate files in folders using MD5 hashing to recover disk space.
"""
from __future__ import annotations
import hashlib
import os
from pathlib import Path
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "duplicate_file_finder",
    "description": (
        "Scans a folder (e.g. Downloads, Documents, Desktop) for identical duplicate files by content hash. "
        "Use when user asks 'busca archivos duplicados', 'encuentra duplicados en descargas', "
        "or 'tengo archivos repetidos'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "folder": {
                "type": "STRING",
                "description": "Folder path to scan. Defaults to user Downloads folder.",
            },
            "min_size_kb": {
                "type": "INTEGER",
                "description": "Minimum file size to inspect in KB. Defaults to 50.",
            }
        },
        "required": [],
    },
}

PLUGIN_SETTINGS = {
    "title": "Buscador de Duplicados",
    "fields": [
        {
            "key": "default_folder",
            "label": "Carpeta Predeterminada",
            "type": "choice",
            "options": ["Downloads", "Documents", "Desktop", "Pictures"],
            "default": "Downloads",
        },
        {
            "key": "min_size_kb",
            "label": "Tamaño Mínimo (KB)",
            "type": "text",
            "default": "50",
            "placeholder": "50",
        }
    ],
}

def _hash_file(filepath: Path, blocksize: int = 65536) -> str:
    hasher = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            buf = f.read(blocksize)
            while buf:
                hasher.update(buf)
                buf = f.read(blocksize)
        return hasher.hexdigest()
    except Exception:
        return ""

def run(parameters: dict, player=None, session_memory=None) -> str:
    user_home = Path(os.environ.get("USERPROFILE", "."))
    def_folder_name = get_plugin_setting("duplicate_file_finder", "default_folder", "Downloads")
    folder_param = parameters.get("folder")
    
    if folder_param:
        target_dir = Path(folder_param)
        if not target_dir.is_absolute():
            target_dir = user_home / folder_param
    else:
        target_dir = user_home / def_folder_name

    if not target_dir.exists() or not target_dir.is_dir():
        return f"Sir, la carpeta '{target_dir}' no existe o no es accesible."

    try:
        min_kb = int(parameters.get("min_size_kb") or get_plugin_setting("duplicate_file_finder", "min_size_kb", 50))
    except (TypeError, ValueError):
        min_kb = 50
    min_bytes = min_kb * 1024

    if player:
        try:
            player.write_log(f"🔍 DUPLICADOS: Escaneando carpeta {target_dir.name}...")
        except Exception:
            pass

    size_map: dict[int, list[Path]] = {}
    scanned_count = 0

    for root, _, files in os.walk(target_dir):
        for f in files:
            p = Path(root) / f
            try:
                sz = p.stat().st_size
                if sz >= min_bytes:
                    size_map.setdefault(sz, []).append(p)
                    scanned_count += 1
                if scanned_count > 1500:
                    break
            except Exception:
                continue

    # Hash files that share exact same size
    duplicates: list[tuple[Path, Path, int]] = []
    wasted_bytes = 0

    for sz, paths in size_map.items():
        if len(paths) < 2:
            continue
        hashes: dict[str, Path] = {}
        for p in paths:
            h = _hash_file(p)
            if not h:
                continue
            if h in hashes:
                duplicates.append((p, hashes[h], sz))
                wasted_bytes += sz
            else:
                hashes[h] = p

    wasted_mb = round(wasted_bytes / (1024 * 1024), 2)
    count_dups = len(duplicates)

    if count_dups == 0:
        res = f"Escaneo completado en {target_dir.name}. No se encontraron archivos idénticos duplicados."
    else:
        sample_names = ", ".join(f"'{d[0].name}'" for d in duplicates[:3])
        res = (f"Encontré {count_dups} archivos duplicados en {target_dir.name}, "
               f"ocupando aproximadamente {wasted_mb} MB de espacio innecesario. Ejemplos: {sample_names}.")

    if player:
        try:
            player.write_log(f"🔍 DUPLICADOS: {count_dups} encontrados (~{wasted_mb} MB recuperables)")
        except Exception:
            pass

    return res
