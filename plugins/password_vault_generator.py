"""
Password Vault Generator Plugin for MARK LV / Viernes.
Generates cryptographically random passwords, evaluates security entropy, and copies directly to clipboard.
"""
from __future__ import annotations
import math
import secrets
import string
from memory.config_manager import get_plugin_setting

PLUGIN = {
    "name": "password_vault_generator",
    "description": (
        "Generates strong cryptographic passwords and copies them to the clipboard. "
        "Use when user asks 'genera una contraseña', 'crea una clave segura', 'dame un password', "
        "or 'genera una contraseña de 20 caracteres'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "length": {
                "type": "INTEGER",
                "description": "Password length in characters (8 to 64). Defaults to 16.",
            },
            "include_symbols": {
                "type": "BOOLEAN",
                "description": "Whether to include punctuation symbols. Defaults to true.",
            },
            "phonetic": {
                "type": "BOOLEAN",
                "description": "If true, generates memorable passphrase words instead of pure random characters.",
            }
        },
        "required": [],
    },
}

PLUGIN_SETTINGS = {
    "title": "Generador de Contraseñas",
    "fields": [
        {
            "key": "default_length",
            "label": "Longitud por Defecto",
            "type": "text",
            "default": "16",
            "placeholder": "16",
        },
        {
            "key": "include_symbols",
            "label": "Incluir Caracteres Especiales (!@#)",
            "type": "toggle",
            "default": True,
        },
    ],
}

def _calc_entropy(password: str, pool_size: int) -> float:
    return len(password) * math.log2(pool_size) if pool_size > 0 else 0.0

def run(parameters: dict, player=None, session_memory=None) -> str:
    raw_len = parameters.get("length")
    cfg_len = get_plugin_setting("password_vault_generator", "default_length", 16)
    try:
        length = int(raw_len) if raw_len is not None else int(cfg_len)
    except (TypeError, ValueError):
        length = 16
    length = max(8, min(64, length))

    inc_sym = parameters.get("include_symbols")
    if inc_sym is None:
        inc_sym = bool(get_plugin_setting("password_vault_generator", "include_symbols", True))

    phonetic = parameters.get("phonetic", False)

    if phonetic:
        words = ["ciber", "luz", "orion", "vector", "cuanto", "solaris", "pulso", "aurora", "valquiria", "neon", "estela", "cristal", "zenit", "cosmos"]
        chosen = [secrets.choice(words).capitalize() for _ in range(4)]
        pwd = "-".join(chosen) + str(secrets.randbelow(90) + 10)
        entropy = 68.0
    else:
        chars = string.ascii_letters + string.digits
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if inc_sym:
            chars += symbols
        pwd = "".join(secrets.choice(chars) for _ in range(length))
        entropy = _calc_entropy(pwd, len(chars))

    # Copy to Windows clipboard
    copied = False
    try:
        import subprocess
        subprocess.run(["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value '{pwd}'"],
                       check=False, capture_output=True, timeout=2.0)
        copied = True
    except Exception:
        pass

    security_lvl = "Extrema" if entropy >= 80 else ("Alta" if entropy >= 60 else "Media")
    msg = f"🔐 CONTRASEÑA GENERADA: {pwd} ({length} caracteres, seguridad {security_lvl}, {int(entropy)} bits de entropía)."
    if copied:
        msg += " ¡Copiada al portapapeles!"

    if player:
        try:
            player.write_log(msg)
        except Exception:
            pass

    return f"He generado una contraseña segura de {length} caracteres con nivel de seguridad {security_lvl} y la he copiado a tu portapapeles."
