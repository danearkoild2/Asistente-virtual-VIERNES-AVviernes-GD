"""
actions/project_intelligence.py — Deep Project Intelligence & Proactive Context Engine.
Provides deep comprehension of user projects, tech stacks, git activities, code goals,
and suggests proactive engineering steps for DanearKoild / Groovi Dev.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
MEMORY_DIR = BASE_DIR / "memory"
PROJECTS_CONTEXT_FILE = MEMORY_DIR / "projects_context.json"

# Common workspaces to scan for Groovi Dev / DanearKoild
DEFAULT_SCAN_PATHS = [
    str(BASE_DIR),
    str(Path.home() / "Desktop"),
    str(Path.home() / "Documents"),
]

# File ignore patterns for scanning
IGNORED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".idea", ".vscode", "dist", "build", "target", "coverage",
    ".cache", "tmp", "temp", "vendor"
}


def _load_projects_store() -> Dict[str, Any]:
    """Loads the projects context store from disk."""
    if not PROJECTS_CONTEXT_FILE.exists():
        initial = {
            "version": "1.0",
            "active_project": "Viernes",
            "projects": {
                "Viernes": {
                    "path": str(BASE_DIR),
                    "organization": "Groovi Dev",
                    "description": "VIERNES personal assistant core",
                    "goals": [
                        {"id": 1, "task": "Integrar análisis de datos en tiempo real y predicciones", "status": "in_progress", "created": "2026-10-14"},
                        {"id": 2, "task": "Comprensión profunda de proyectos y contexto proactivo", "status": "in_progress", "created": "2026-10-14"}
                    ],
                    "notes": "Desarrollado para DanearKoild (CEO Groovi Dev)"
                }
            },
            "last_scan": datetime.now().isoformat()
        }
        _save_projects_store(initial)
        return initial

    try:
        with open(PROJECTS_CONTEXT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ProjectIntelligence] Warning: could not load context store: {e}")
        return {"version": "1.0", "active_project": "Viernes", "projects": {}, "last_scan": None}


def _save_projects_store(data: Dict[str, Any]) -> None:
    """Saves the projects context store to disk."""
    try:
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        with open(PROJECTS_CONTEXT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ProjectIntelligence] Error saving context store: {e}")


def _run_git_cmd(cwd: str, args: List[str]) -> Optional[str]:
    """Runs a git command in the target directory safely."""
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )
        if res.returncode == 0:
            return res.stdout.strip()
    except Exception:
        pass
    return None


def inspect_git(project_path: str) -> Dict[str, Any]:
    """Inspects git repository status, branch, recent commits, and dirty files."""
    p = Path(project_path)
    git_dir = p / ".git"
    if not git_dir.exists():
        return {"is_git": False}

    branch = _run_git_cmd(project_path, ["branch", "--show-current"]) or "detached"
    status_out = _run_git_cmd(project_path, ["status", "--porcelain"]) or ""
    log_out = _run_git_cmd(project_path, ["log", "-n", "3", "--pretty=format:%h - %s (%cr)"]) or ""

    dirty_files = []
    for line in status_out.splitlines():
        line = line.strip()
        if line:
            dirty_files.append(line)

    recent_commits = [c.strip() for c in log_out.splitlines() if c.strip()]

    return {
        "is_git": True,
        "branch": branch,
        "is_clean": len(dirty_files) == 0,
        "dirty_count": len(dirty_files),
        "dirty_files": dirty_files[:8],
        "recent_commits": recent_commits
    }


def detect_tech_stack(project_path: str) -> Dict[str, Any]:
    """Detects programming languages, frameworks, and tools in a project directory."""
    p = Path(project_path)
    stack = []
    frameworks = []

    # Python
    py_indicators = ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"]
    if any((p / f).exists() for f in py_indicators) or list(p.glob("*.py")):
        stack.append("Python")
        req_file = p / "requirements.txt"
        if req_file.exists():
            try:
                content = req_file.read_text(encoding="utf-8", errors="ignore").lower()
                for fw in ["fastapi", "flask", "django", "numpy", "scipy", "torch", "pandas", "google-genai", "websockets"]:
                    if fw in content:
                        frameworks.append(fw)
            except Exception:
                pass

    # Node / JS / TS
    pkg_file = p / "package.json"
    if pkg_file.exists():
        stack.append("Node.js / JavaScript")
        try:
            with open(pkg_file, "r", encoding="utf-8") as f:
                pkg = json.load(f)
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                if "typescript" in deps or (p / "tsconfig.json").exists():
                    stack.append("TypeScript")
                for key in ["react", "vue", "vite", "next", "electron", "tailwindcss", "express"]:
                    if key in deps:
                        frameworks.append(key)
        except Exception:
            pass

    # Rust
    if (p / "Cargo.toml").exists():
        stack.append("Rust")

    # Mobile / Flutter
    if (p / "pubspec.yaml").exists():
        stack.append("Flutter / Dart")

    # C / C++
    if (p / "CMakeLists.txt").exists() or list(p.glob("*.cpp")) or list(p.glob("*.h")):
        stack.append("C/C++")

    # Web HTML/CSS
    if list(p.glob("*.html")) and "Node.js / JavaScript" not in stack:
        stack.append("HTML5 / Frontend")

    return {
        "languages": list(set(stack)),
        "frameworks": list(set(frameworks))
    }


def find_todos(project_path: str, max_results: int = 6) -> List[Dict[str, Any]]:
    """Scans code files for open TODO, FIXME, or HACK comments."""
    p = Path(project_path)
    todos = []
    extensions = {".py", ".js", ".ts", ".html", ".css", ".json", ".rs", ".cpp", ".dart"}

    try:
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in extensions:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, project_path)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            for idx, line in enumerate(f, start=1):
                                match = re.search(r"\b(TODO|FIXME|HACK|OPTIMIZE)\b[:\s]*(.*)", line, re.IGNORECASE)
                                if match:
                                    tag = match.group(1).upper()
                                    desc = match.group(2).strip()[:100]
                                    todos.append({
                                        "file": rel_path,
                                        "line": idx,
                                        "tag": tag,
                                        "comment": desc or "(no details)"
                                    })
                                    if len(todos) >= max_results:
                                        return todos
                    except Exception:
                        continue
    except Exception:
        pass
    return todos


def get_active_project_summary() -> str:
    """
    Returns a high-density, context-rich summary for the ProactiveEngine prompt
    so VIERNES knows exactly what DanearKoild is working on.
    """
    store = _load_projects_store()
    active_name = store.get("active_project", "Viernes")
    proj_info = store.get("projects", {}).get(active_name, {})
    path = proj_info.get("path", str(BASE_DIR))

    git_info = inspect_git(path)
    tech = detect_tech_stack(path)
    goals = [g["task"] for g in proj_info.get("goals", []) if g.get("status") == "in_progress"]

    parts = [f"Proyecto activo: {active_name} (Ruta: {path})"]
    if tech.get("languages"):
        langs = ", ".join(tech["languages"])
        fws = f" con {', '.join(tech['frameworks'])}" if tech.get("frameworks") else ""
        parts.append(f"Stack: {langs}{fws}")

    if git_info.get("is_git"):
        branch = git_info.get("branch", "unknown")
        dirty = git_info.get("dirty_count", 0)
        status_txt = f"Limpio ({branch})" if git_info.get("is_clean") else f"{dirty} archivos modificados/pendientes ({branch})"
        parts.append(f"Estado Git: {status_txt}")
        if git_info.get("dirty_files"):
            parts.append(f"En desarrollo: {', '.join(git_info['dirty_files'][:4])}")

    if goals:
        parts.append(f"Objetivos actuales: {' | '.join(goals[:2])}")

    return " | ".join(parts)


# ── Action Execution Functions ────────────────────────────────────────────────

def scan_all_projects(roots: Optional[List[str]] = None) -> Dict[str, Any]:
    """Discovers projects across specified root folders."""
    roots = roots or DEFAULT_SCAN_PATHS
    store = _load_projects_store()
    discovered = {}

    for root_str in roots:
        root = Path(root_str)
        if not root.exists():
            continue

        # Check if the root itself is a project
        if (root / ".git").exists() or (root / "package.json").exists() or (root / "requirements.txt").exists():
            p_name = root.name
            discovered[p_name] = {
                "path": str(root),
                "git": inspect_git(str(root)),
                "stack": detect_tech_stack(str(root))
            }

        # Check immediate subdirectories
        try:
            for item in root.iterdir():
                if item.is_dir() and item.name not in IGNORED_DIRS and not item.name.startswith("."):
                    if (item / ".git").exists() or (item / "package.json").exists() or (item / "requirements.txt").exists():
                        discovered[item.name] = {
                            "path": str(item),
                            "git": inspect_git(str(item)),
                            "stack": detect_tech_stack(str(item))
                        }
        except Exception:
            continue

    # Merge into store
    for name, data in discovered.items():
        if name not in store["projects"]:
            store["projects"][name] = {
                "path": data["path"],
                "organization": "Groovi Dev",
                "description": f"Proyecto detectado en {data['path']}",
                "goals": [],
                "notes": ""
            }
        else:
            store["projects"][name]["path"] = data["path"]

    store["last_scan"] = datetime.now().isoformat()
    _save_projects_store(store)

    return {
        "status": "success",
        "total_projects": len(discovered),
        "projects": list(discovered.keys()),
        "details": discovered
    }


def get_project_context(project_name: Optional[str] = None) -> Dict[str, Any]:
    """Retrieves deep technical context and status for a project."""
    store = _load_projects_store()
    name = project_name or store.get("active_project", "Viernes")
    proj_info = store.get("projects", {}).get(name)

    if not proj_info:
        # Fallback to current BASE_DIR if name matches Viernes
        path = str(BASE_DIR)
        name = "Viernes"
    else:
        path = proj_info.get("path", str(BASE_DIR))

    git_info = inspect_git(path)
    stack_info = detect_tech_stack(path)
    todos = find_todos(path, max_results=8)
    goals = proj_info.get("goals", []) if proj_info else []

    return {
        "status": "success",
        "project": name,
        "path": path,
        "git": git_info,
        "tech_stack": stack_info,
        "goals": goals,
        "open_todos": todos,
        "notes": proj_info.get("notes", "") if proj_info else ""
    }


def add_project_goal(task: str, project_name: Optional[str] = None) -> Dict[str, Any]:
    """Adds a new engineering goal or milestone to a project."""
    store = _load_projects_store()
    name = project_name or store.get("active_project", "Viernes")

    if name not in store["projects"]:
        store["projects"][name] = {
            "path": str(BASE_DIR),
            "organization": "Groovi Dev",
            "goals": [],
            "notes": ""
        }

    proj = store["projects"][name]
    new_id = len(proj.get("goals", [])) + 1
    new_goal = {
        "id": new_id,
        "task": task,
        "status": "in_progress",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    proj.setdefault("goals", []).append(new_goal)
    _save_projects_store(store)

    return {
        "status": "success",
        "message": f"Objetivo #{new_id} agregado a {name}: '{task}'",
        "goal": new_goal
    }


def suggest_next_steps(project_name: Optional[str] = None) -> Dict[str, Any]:
    """Synthesizes git state, open TODOs, and active goals into actionable engineering suggestions."""
    ctx = get_project_context(project_name)
    suggestions = []

    git = ctx.get("git", {})
    if git.get("is_git"):
        if not git.get("is_clean"):
            dirty_count = git.get("dirty_count", 0)
            dirty_files = ", ".join(git.get("dirty_files", [])[:3])
            suggestions.append(
                f"Tienes {dirty_count} archivos con cambios sin guardar en Git ({dirty_files}). "
                "Sería ideal revisar las modificaciones y hacer commit una vez probadas."
            )
        else:
            suggestions.append("El repositorio Git está limpio y en orden en la rama actual.")

    # Incomplete goals
    pending_goals = [g for g in ctx.get("goals", []) if g.get("status") == "in_progress"]
    if pending_goals:
        next_goal = pending_goals[0]
        suggestions.append(f"Objetivo prioritario en curso: '{next_goal['task']}'.")

    # Open TODOs
    todos = ctx.get("open_todos", [])
    if todos:
        first_todo = todos[0]
        suggestions.append(f"Recordatorio de código ({first_todo['file']}:{first_todo['line']}): [{first_todo['tag']}] {first_todo['comment']}")

    if not suggestions:
        suggestions.append("Todos los objetivos y tareas inmediatas están al día. ¿Deseas planear el siguiente módulo para Groovi Dev?")

    return {
        "status": "success",
        "project": ctx.get("project"),
        "suggestions": suggestions,
        "summary": " | ".join(suggestions)
    }


# ── Action Dispatcher & Gemini Tool ───────────────────────────────────────────

def project_intelligence(
    action: str = "get_context",
    project_name: Optional[str] = None,
    task_goal: Optional[str] = None,
    scan_paths: Optional[List[str]] = None
) -> str:
    """Entrypoint dispatcher invoked by Gemini Live."""
    try:
        act = (action or "get_context").lower().strip()
        if act in ("scan", "scan_all", "discover"):
            res = scan_all_projects(scan_paths)
            projs = ", ".join(res.get("projects", []))
            return f"He escaneado el entorno y detecté {res['total_projects']} proyectos: {projs}."

        elif act in ("add_goal", "set_goal", "new_goal"):
            if not task_goal:
                return "Por favor indica la meta o tarea que deseas registrar para el proyecto."
            res = add_project_goal(task_goal, project_name)
            return res.get("message", "Meta guardada correctamente.")

        elif act in ("suggest", "next_steps", "proactive_advice"):
            res = suggest_next_steps(project_name)
            return f"Sugerencias para {res['project']}:\n" + "\n".join(f"- {s}" for s in res['suggestions'])

        else: # "get_context", "status", "info"
            ctx = get_project_context(project_name)
            proj = ctx["project"]
            langs = ", ".join(ctx["tech_stack"].get("languages", ["desconocido"]))
            git = ctx["git"]
            git_status = f"Git: rama '{git.get('branch', 'main')}', {'limpio' if git.get('is_clean') else f'{git.get('dirty_count')} cambios'}" if git.get("is_git") else "Sin control Git"
            goals = ctx.get("goals", [])
            goals_str = f"{len(goals)} metas registradas" if goals else "sin metas registradas"

            return (
                f"Contexto del proyecto '{proj}':\n"
                f"- Stack: {langs}\n"
                f"- Control de versiones: {git_status}\n"
                f"- Estado de metas: {goals_str}\n"
                f"- Ruta: {ctx['path']}"
            )
    except Exception as e:
        return f"Error al procesar la inteligencia de proyectos: {str(e)}"


def project_intelligence_action(
    parameters: dict = None,
    player=None,
    session_memory=None,
) -> str:
    """Action wrapper called by core.action_loader."""
    params = parameters or {}
    action = params.get("action", "get_context")
    project_name = params.get("project_name")
    task_goal = params.get("task_goal")
    scan_paths = params.get("scan_paths")

    res = project_intelligence(
        action=action,
        project_name=project_name,
        task_goal=task_goal,
        scan_paths=scan_paths
    )

    if player and hasattr(player, "write_log"):
        player.write_log(f"PROJ: {res[:80]}...")

    return res


TOOL: Dict[str, Any] = {
    "name": "project_intelligence",
    "description": (
        "Módulo de inteligencia y contexto profundo sobre los proyectos de desarrollo de DanearKoild / Groovi Dev. "
        "Permite analizar la arquitectura, stack tecnológico, estado de Git (ramas, archivos modificados, commits), "
        "gestionar metas/hitos de desarrollo y ofrecer recomendaciones técnicas proactivas sobre los siguientes pasos."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": "Operación a realizar: 'get_context' (ver estado y arquitectura), 'suggest' (sugerencias y siguientes pasos), 'scan' (descubrir proyectos en el sistema), 'add_goal' (registrar meta o tarea).",
            },
            "project_name": {
                "type": "STRING",
                "description": "Nombre del proyecto (por ejemplo 'Viernes' o el nombre de una carpeta de proyecto). Si se omite, usa el proyecto activo.",
            },
            "task_goal": {
                "type": "STRING",
                "description": "Texto del objetivo o hito de desarrollo a guardar cuando action='add_goal'.",
            }
        },
        "required": ["action"]
    },
    "handler": project_intelligence_action,
}
