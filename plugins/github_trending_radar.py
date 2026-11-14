"""
GitHub Trending Radar Plugin for MARK LV / Viernes.
Fetches top trending repositories and popular AI/developer tools from GitHub API.
"""
from __future__ import annotations
from datetime import datetime, timedelta
import json
import urllib.request
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "github_trending_radar",
    "description": (
        "Discovers trending and newly popular open-source repositories and tools on GitHub. "
        "Use when user asks 'qué hay de nuevo en github', 'repositorios trending', 'tendencias de programación', "
        "or 'proyectos populares en python'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "language": {
                "type": "STRING",
                "description": "Programming language filter, e.g. 'python', 'typescript', 'rust', or empty for all.",
            },
            "topic": {
                "type": "STRING",
                "description": "Topic or keyword filter, e.g. 'ai', 'llm', 'vision', 'agent'.",
            }
        },
        "required": [],
    },
}

PLUGIN_SETTINGS = {
    "title": "Radar de Tendencias GitHub",
    "fields": [
        {
            "key": "default_language",
            "label": "Lenguaje Predeterminado",
            "type": "choice",
            "options": ["Cualquiera", "Python", "TypeScript", "Rust", "Go"],
            "default": "Python",
        },
    ],
}

def run(parameters: dict, player=None, session_memory=None) -> str:
    lang = parameters.get("language")
    if not lang:
        def_lang = get_plugin_setting("github_trending_radar", "default_language", "Python")
        if def_lang != "Cualquiera":
            lang = def_lang.lower()

    topic = parameters.get("topic", "")

    # Query repos created/updated recently with high stars
    since_date = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
    q = f"created:>{since_date}"
    if lang:
        q += f" language:{lang}"
    if topic:
        q += f" {topic}"

    url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&sort=stars&order=desc&per_page=4"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Viernes-Assistant"})
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        items = data.get("items", [])
        if not items:
            return "No se encontraron repositorios destacados con esos filtros en las últimas dos semanas."

        repos_summary = []
        for it in items[:3]:
            name = it.get("full_name")
            stars = it.get("stargazers_count", 0)
            desc = it.get("description") or "Sin descripción"
            desc_short = desc[:60] + "..." if len(desc) > 60 else desc
            repos_summary.append(f"⭐ {stars} | {name}: {desc_short}")

        summary_str = "\n• " + "\n• ".join(repos_summary)
        if player:
            try:
                player.write_log(f"🐙 GITHUB TRENDING:{summary_str}")
            except Exception:
                pass

        top_one = items[0].get("full_name")
        return f"Entre las tendencias más populares de GitHub destaca {top_one} con {items[0].get('stargazers_count')} estrellas: {items[0].get('description') or ''}."

    except Exception as e:
        return f"Sir, no pude consultar la API de GitHub en este momento: {e}"
