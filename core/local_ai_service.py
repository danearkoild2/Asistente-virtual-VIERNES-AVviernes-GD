"""
Local AI Service - Gestor e Inferencia de Inteligencia Artificial Local (Ollama & OpenAI Compatible)
===================================================================================================
Gestiona la conexión, descubrimiento de modelos, clasificación multimodal (texto vs visión),
inferencia conversacional y análisis visual 100% offline para VIERNES y Edith.
"""

from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Callable, Generator

import requests

def _get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

BASE_DIR = _get_base_dir()
CONFIG_PATH = BASE_DIR / "config" / "api_keys.json"

_VISION_PATTERNS = [
    r"vision",
    r"llava",
    r"moondream",
    r"minicpm-v",
    r"qwen.*-vl",
    r"bakllava",
    r"cogvlm",
    r"omni",
    r"mllama",
    r"internvl",
]


class LocalAIService:
    """Singleton service for local AI discovery, model management, and offline multimodal vision."""

    _instance: "LocalAIService | None" = None

    def __new__(cls) -> "LocalAIService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_service()
        return cls._instance

    def _init_service(self):
        self._last_check_time = 0.0
        self._is_available = False
        self._installed_models: list[dict] = []
        self._vision_models: list[str] = []
        self._text_models: list[str] = []

    def load_config(self) -> dict:
        try:
            if CONFIG_PATH.exists():
                return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[LocalAI] Error loading config: {e}")
        return {}

    def save_config(self, updates: dict) -> bool:
        try:
            cfg = self.load_config()
            cfg.update(updates)
            CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
            return True
        except Exception as e:
            print(f"[LocalAI] Error saving config: {e}")
            return False

    def get_settings(self) -> dict:
        cfg = self.load_config()
        provider = cfg.get("llm_provider", "ollama").strip().lower()
        if provider not in ("ollama", "openai"):
            provider = "openai" if provider in ("lmstudio", "localai", "jan", "llamacpp") else "ollama"

        url = cfg.get("llm_url", "http://localhost:11434" if provider == "ollama" else "http://localhost:1234").rstrip("/")
        model = cfg.get("llm_model", "llama3.2")
        vision_model = cfg.get("vision_model", "llama3.2-vision")
        prefer_local_vision = bool(cfg.get("prefer_local_vision", False))

        return {
            "provider": provider,
            "url": url,
            "current_model": model,
            "vision_model": vision_model,
            "prefer_local_vision": prefer_local_vision,
        }

    def check_connection(self, force_refresh: bool = False) -> dict:
        now = time.monotonic()
        if not force_refresh and (now - self._last_check_time) < 8.0:
            return {
                "connected": self._is_available,
                "installed_models": self._installed_models,
                "vision_models": self._vision_models,
                "text_models": self._text_models,
            }

        self._last_check_time = now
        st = self.get_settings()
        url = st["url"]
        provider = st["provider"]

        installed = []
        vision_models = []
        text_models = []
        connected = False

        if provider == "ollama":
            endpoint = f"{url}/api/tags"
            try:
                r = requests.get(endpoint, timeout=3.5)
                if r.status_code == 200:
                    connected = True
                    data = r.json()
                    for m in data.get("models", []):
                        name = m.get("name", "")
                        size_b = m.get("size", 0)
                        size_gb = round(size_b / (1024**3), 2)
                        mod_time = m.get("modified_at", "")[:10]

                        # Check if model has vision capabilities
                        is_vision = any(re.search(pat, name, re.IGNORECASE) for pat in _VISION_PATTERNS)
                        if is_vision:
                            vision_models.append(name)
                        else:
                            text_models.append(name)

                        installed.append({
                            "name": name,
                            "size_gb": size_gb,
                            "is_vision": is_vision,
                            "modified": mod_time,
                            "details": m.get("details", {}),
                        })
            except Exception:
                connected = False

        else:  # OpenAI compatible (LM Studio, LocalAI, Jan)
            endpoint = f"{url}/v1/models"
            try:
                r = requests.get(endpoint, timeout=3.5)
                if r.status_code == 200:
                    connected = True
                    data = r.json()
                    for m in data.get("data", []):
                        m_id = m.get("id", "")
                        is_vision = any(re.search(pat, m_id, re.IGNORECASE) for pat in _VISION_PATTERNS)
                        if is_vision:
                            vision_models.append(m_id)
                        else:
                            text_models.append(m_id)
                        installed.append({
                            "name": m_id,
                            "size_gb": 0.0,
                            "is_vision": is_vision,
                            "modified": "local",
                            "details": {},
                        })
            except Exception:
                connected = False

        self._is_available = connected
        self._installed_models = installed
        self._vision_models = vision_models
        self._text_models = text_models

        return {
            "connected": connected,
            "installed_models": installed,
            "vision_models": vision_models,
            "text_models": text_models,
        }

    def ensure_service_running(self) -> bool:
        """Ping local LLM server; auto-launch ollama if not running on Windows/Linux."""
        res = self.check_connection(force_refresh=True)
        if res["connected"]:
            return True

        st = self.get_settings()
        if st["provider"] == "ollama":
            print("[LocalAI] Intentando iniciar Ollama automáticamente...")
            try:
                kwargs = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
                if sys.platform == "win32":
                    kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
                subprocess.Popen(["ollama", "serve"], **kwargs)

                # Wait for startup up to 6 seconds
                for _ in range(6):
                    time.sleep(1.0)
                    if self.check_connection(force_refresh=True)["connected"]:
                        print("[LocalAI] Ollama iniciado y listo.")
                        return True
            except FileNotFoundError:
                print("[LocalAI] Comando 'ollama' no encontrado en el sistema.")
            except Exception as e:
                print(f"[LocalAI] Error lanzando Ollama: {e}")

        return False

    def analyze_image(
        self,
        image_bytes: bytes,
        prompt: str = "¿Qué observas en esta imagen? Describe objetos, personas y entorno con precisión.",
        model: str | None = None,
        system_prompt: str | None = None,
        timeout: int = 45,
    ) -> dict:
        """
        Analiza una imagen en memoria mediante el modelo de visión local disponible.
        Retorna: {"success": bool, "text": str, "model": str, "duration_s": float, "error": str}
        """
        self.check_connection()
        if not self._is_available:
            return {
                "success": False,
                "text": "",
                "model": "",
                "duration_s": 0.0,
                "error": "El servidor de IA local (Ollama) no está en ejecución.",
            }

        st = self.get_settings()
        target_model = model or st["vision_model"]

        # Si el modelo solicitado no está, intentar usar el primer modelo de visión instalado
        if target_model not in self._vision_models:
            if self._vision_models:
                target_model = self._vision_models[0]
            else:
                return {
                    "success": False,
                    "text": "",
                    "model": target_model,
                    "duration_s": 0.0,
                    "error": (
                        f"Ningún modelo de visión local detectado.\n"
                        f"Para analizar imágenes localmente sin internet, ejecuta en tu terminal:\n"
                        f"  ollama run llama3.2-vision\n"
                        f"o bien:\n"
                        f"  ollama run moondream"
                    ),
                }

        b64_image = base64.b64encode(image_bytes).decode("ascii")
        t_start = time.monotonic()

        sys_inst = system_prompt or (
            "Eres Edith, la asistente visual de VIERNES. "
            "Describe con naturalidad y precisión lo que estás viendo en la imagen. "
            "Sé concisa, profesional y útil. Si no distingues algo claramente, indícalo honestamente."
        )

        try:
            if st["provider"] == "ollama":
                url = f"{st['url']}/api/chat"
                payload = {
                    "model": target_model,
                    "messages": [
                        {"role": "system", "content": sys_inst},
                        {
                            "role": "user",
                            "content": prompt,
                            "images": [b64_image],
                        },
                    ],
                    "stream": False,
                    "keep_alive": "10m",
                    "options": {
                        "num_predict": 300,
                        "temperature": 0.35,
                    },
                }
                resp = requests.post(url, json=payload, timeout=timeout)
                resp.raise_for_status()
                data = resp.json()
                text = (data.get("message", {}).get("content") or "").strip()

            else:  # OpenAI Multimodal Vision
                url = f"{st['url']}/v1/chat/completions"
                payload = {
                    "model": target_model,
                    "messages": [
                        {"role": "system", "content": sys_inst},
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"},
                                },
                            ],
                        },
                    ],
                    "stream": False,
                    "max_tokens": 300,
                }
                resp = requests.post(url, json=payload, timeout=timeout)
                resp.raise_for_status()
                data = resp.json()
                choices = data.get("choices", [])
                text = (choices[0].get("message", {}).get("content") or "").strip() if choices else ""

            duration = round(time.monotonic() - t_start, 2)
            return {
                "success": True,
                "text": text,
                "model": target_model,
                "duration_s": duration,
                "error": "",
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "text": "",
                "model": target_model,
                "duration_s": round(time.monotonic() - t_start, 2),
                "error": f"Tiempo de espera agotado ({timeout}s) analizando imagen con {target_model}.",
            }
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "model": target_model,
                "duration_s": round(time.monotonic() - t_start, 2),
                "error": f"Error en inferencia visual local ({target_model}): {e}",
            }

    def chat_text(
        self,
        prompt: str,
        system_prompt: str | None = None,
        model: str | None = None,
        timeout: int = 60,
    ) -> str:
        """Llamada de texto sin herramientas."""
        st = self.get_settings()
        target_model = model or st["current_model"]
        url = f"{st['url']}/api/chat"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": target_model,
            "messages": messages,
            "stream": False,
            "keep_alive": -1,
            "options": {"num_predict": 450, "temperature": 0.7},
        }

        try:
            r = requests.post(url, json=payload, timeout=timeout)
            r.raise_for_status()
            return (r.json().get("message", {}).get("content") or "").strip()
        except Exception as e:
            raise RuntimeError(f"Error en chat local ({target_model}): {e}")

    def get_status_info(self) -> dict:
        conn = self.check_connection(force_refresh=True)
        st = self.get_settings()

        has_sapi = False
        if sys.platform == "win32":
            try:
                import win32com.client
                win32com.client.Dispatch("SAPI.SpVoice")
                has_sapi = True
            except Exception:
                has_sapi = False

        return {
            "is_available": conn["connected"],
            "provider": st["provider"],
            "url": st["url"],
            "current_model": st["current_model"],
            "vision_model_configured": st["vision_model"],
            "available_models": [m["name"] for m in conn["installed_models"]],
            "vision_models": conn["vision_models"],
            "text_models": conn["text_models"],
            "vision_model_available": bool(conn["vision_models"]),
            "prefer_local_vision": st["prefer_local_vision"],
            "has_offline_voice": has_sapi,
        }


def get_local_ai_service() -> LocalAIService:
    return LocalAIService()
