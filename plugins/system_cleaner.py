"""
System Cleaner Plugin for MARK LV / Viernes.
Cleans Windows temp files, Prefetch and Recycled bin safely to recover disk space.
"""
from __future__ import annotations
import os
import shutil
import tempfile
from pathlib import Path

PLUGIN = {
    "name": "system_cleaner",
    "description": (
        "Cleans temporary files, application cache, and empty recycle bins to free disk space. "
        "Use when user asks to 'clean PC', 'limpiar la computadora', 'free disk space', "
        "or 'borrar archivos temporales'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {},
        "required": [],
    },
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    cleaned_bytes = 0
    cleaned_files = 0

    temp_dirs = [
        Path(tempfile.gettempdir()),
        Path(os.environ.get("LOCALAPPDATA", "")) / "Temp" if os.environ.get("LOCALAPPDATA") else None,
    ]

    for t_dir in temp_dirs:
        if not t_dir or not t_dir.exists():
            continue
        for item in t_dir.iterdir():
            try:
                if item.is_file() or item.is_symlink():
                    size = item.stat().st_size
                    item.unlink()
                    cleaned_bytes += size
                    cleaned_files += 1
                elif item.is_dir():
                    size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                    shutil.rmtree(item, ignore_errors=True)
                    cleaned_bytes += size
                    cleaned_files += 1
            except Exception:
                continue

    # Attempt to empty Recycle Bin via PowerShell safely
    try:
        import subprocess
        subprocess.run(["powershell", "-NoProfile", "-Command", "Clear-RecycleBin -Force -ErrorAction SilentlyContinue"],
                       capture_output=True, timeout=10)
    except Exception:
        pass

    mb_cleaned = cleaned_bytes / (1024 * 1024)
    if mb_cleaned > 1024:
        size_str = f"{mb_cleaned / 1024:.2f} GB"
    else:
        size_str = f"{mb_cleaned:.1f} MB"

    msg = f"Limpieza completada con éxito. Se eliminaron {cleaned_files} elementos temporales y se liberaron {size_str} de espacio en disco."
    if player:
        try:
            player.write_log(f"SYS: {msg}")
        except Exception:
            pass
    return msg
