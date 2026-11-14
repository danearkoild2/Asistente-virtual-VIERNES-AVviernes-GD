"""
Git Repository Voice Assistant Plugin for MARK LV / Viernes.
Checks status, creates commits and pushes branches using voice commands.
"""
from __future__ import annotations
import subprocess
from pathlib import Path

PLUGIN = {
    "name": "git_assistant",
    "description": (
        "Controls git repositories: checks git status, commits changes, or pushes code. "
        "Use when user asks 'estado del git', 'git status', 'haz commit de los cambios', "
        "or 'push a git'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "'status', 'commit', 'push', or 'log'.",
            },
            "commit_message": {
                "type": "STRING",
                "description": "Commit message if action is 'commit'.",
            }
        },
        "required": ["action"],
    },
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    action = parameters.get("action", "status").strip().lower()
    commit_msg = parameters.get("commit_message", "Update via Viernes Assistant")
    cwd = Path.cwd()

    try:
        if action == "status":
            res = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, cwd=cwd, timeout=5)
            if res.returncode != 0:
                return f"No se encontró un repositorio git activo en {cwd.name}."
            lines = res.stdout.strip().splitlines()
            if not lines:
                msg = f"El repositorio {cwd.name} está completamente limpio. Sin cambios pendientes."
            else:
                msg = f"Hay {len(lines)} archivos con modificaciones en {cwd.name}."
        elif action == "commit":
            subprocess.run(["git", "add", "."], capture_output=True, cwd=cwd, timeout=5)
            c_res = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True, cwd=cwd, timeout=8)
            if c_res.returncode == 0:
                msg = f"Commit realizado con éxito: '{commit_msg}'."
            else:
                msg = f"No había cambios para commitear o ocurrió un error: {c_res.stderr.strip()[:100]}"
        elif action == "push":
            p_res = subprocess.run(["git", "push"], capture_output=True, text=True, cwd=cwd, timeout=15)
            if p_res.returncode == 0:
                msg = "Cambios sincronizados y subidos al repositorio remoto con éxito."
            else:
                msg = f"Error al hacer git push: {p_res.stderr.strip()[:120]}"
        else:
            msg = f"Acción de git desconocida: {action}."
    except Exception as e:
        msg = f"Error al ejecutar comando de git: {e}"

    if player:
        try:
            player.write_log(f"SYS: {msg}")
        except Exception:
            pass

    return msg
