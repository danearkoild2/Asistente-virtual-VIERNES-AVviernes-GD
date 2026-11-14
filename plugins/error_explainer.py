"""
Code Error Explainer Plugin for MARK LV / Viernes.
Inspects stack traces copied to the clipboard and gives instant concise fixes.
"""
from __future__ import annotations
import subprocess

PLUGIN = {
    "name": "error_explainer",
    "description": (
        "Analyzes programming errors, tracebacks, or exceptions copied in the clipboard and explains the solution. "
        "Use when user asks 'revisa este error', 'explain this error', 'por qué falla mi código', "
        "or 'analiza el error que copié'."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {},
        "required": [],
    },
}

def _get_clipboard_windows() -> str:
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                             capture_output=True, text=True, timeout=3)
        return res.stdout.strip()
    except Exception:
        return ""

def run(parameters: dict, player=None, session_memory=None) -> str:
    text = _get_clipboard_windows()
    if not text:
        return "No hay ningún error o texto copiado en el portapapeles para analizar."

    # Heuristic detection of common errors
    t_lower = text.lower()
    solution = ""

    if "modulenotfounderror" in t_lower or "no module named" in t_lower:
        missing = text.split("No module named")[-1].strip().strip("'\"").split()[0] if "No module named" in text else "la librería faltante"
        solution = f"Error de dependencia: falta instalar el paquete. Puedes solucionarlo ejecutando: pip install {missing}."
    elif "syntaxerror" in t_lower:
        solution = "Error de sintaxis: suele deberse a un paréntesis, comilla o dos puntos sin cerrar cerca de la línea señalada."
    elif "keyerror" in t_lower:
        solution = "KeyError: se intentó acceder a una clave de diccionario que no existe. Usa .get(clave) o valida antes con 'if clave in dict:'."
    elif "indexerror" in t_lower:
        solution = "IndexError: la lista está vacía o el índice excede la longitud actual de la colección."
    elif "attributeerror" in t_lower:
        solution = "AttributeError: el objeto recibido es probablemente None o de un tipo diferente al esperado. Verifica de dónde proviene la variable."
    elif "401" in t_lower or "unauthorized" in t_lower or "invalid_api_key" in t_lower:
        solution = "Error de autenticación: la API Key proporcionada es inválida o ha expirado. Revisa las credenciales en tu configuración."
    elif "connectionerror" in t_lower or "connection refused" in t_lower:
        solution = "Error de conexión: el servidor local o remoto no está encendido o el puerto está bloqueado."
    else:
        first_line = text.strip().splitlines()[-1][:120]
        solution = f"Error detectado: {first_line}. Revisa los parámetros pasados y el tipo de dato recibido."

    msg = f"Diagnóstico del error: {solution}"
    if player:
        try:
            player.write_log(f"ERR ANALYZER: {solution}")
        except Exception:
            pass

    return msg
