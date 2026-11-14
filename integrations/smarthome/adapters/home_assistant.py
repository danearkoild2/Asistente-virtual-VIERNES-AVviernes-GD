"""
Home Assistant REST API Integration for VIERNES
================================================
Provides bi-directional connection with Home Assistant instances:
- Discovery of physical devices (lights, switches, climate, locks, media players)
- State synchronization
- Service calls (turn_on, turn_off, set_temperature, lock/unlock)
- Encrypted credential storage
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import requests

try:
    from homeassistant_api import Client as HomeAssistantAPIClient  # type: ignore
except Exception:
    HomeAssistantAPIClient = None  # type: ignore

from integrations.crypto import decrypt_secret, encrypt_secret

_CONFIG_FILE = Path(__file__).resolve().parent.parent.parent.parent / "config" / "home_assistant.enc"


class HomeAssistantClient:
    """Client for Home Assistant REST API."""

    def __init__(self):
        self.base_url: str = ""
        self.token: str = ""
        self._load_credentials()

    def _load_credentials(self):
        if _CONFIG_FILE.exists():
            try:
                enc = _CONFIG_FILE.read_text(encoding="utf-8")
                raw = decrypt_secret(enc)
                if raw:
                    data = json.loads(raw)
                    self.base_url = data.get("base_url", "").rstrip("/")
                    self.token = data.get("token", "").strip()
            except Exception as e:
                print(f"[HomeAssistantClient] Error loading credentials: {e}")
        if not self.base_url:
            self.base_url = (
                os.environ.get("HOME_ASSISTANT_URL")
                or os.environ.get("HA_URL")
                or ""
            ).strip().rstrip("/")
        if not self.token:
            self.token = (
                os.environ.get("HOME_ASSISTANT_TOKEN")
                or os.environ.get("HA_TOKEN")
                or ""
            ).strip()

    def save_credentials(self, base_url: str, token: str):
        self.base_url = base_url.strip().rstrip("/")
        self.token = token.strip()
        _CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps({"base_url": self.base_url, "token": self.token})
        _CONFIG_FILE.write_text(encrypt_secret(payload), encoding="utf-8")

    def disconnect(self):
        self.base_url = ""
        self.token = ""
        if _CONFIG_FILE.exists():
            try:
                _CONFIG_FILE.unlink()
            except Exception:
                pass

    def is_connected(self) -> bool:
        return bool(self.base_url and self.token)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def test_connection(self, base_url: Optional[str] = None, token: Optional[str] = None) -> Tuple[bool, str]:
        """Test API connectivity and authorization against Home Assistant."""
        url = (base_url or self.base_url).strip().rstrip("/")
        tok = (token or self.token).strip()

        if not url or not tok:
            return False, "Debes ingresar la URL base (ej: http://homeassistant.local:8123) y el Token de Acceso."

        try:
            api_url = f"{url}/api/"
            headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
            r = requests.get(api_url, headers=headers, timeout=6.0)

            if r.status_code == 200:
                msg = r.json().get("message", "API running.")
                return True, f"Conexión exitosa con Home Assistant ({msg})"
            elif r.status_code == 401:
                return False, "Error 401: Token de acceso no válido o revocado."
            elif r.status_code == 404:
                return False, "Error 404: Endpoint /api/ no encontrado. Revisa la URL."
            else:
                return False, f"Respuesta de Home Assistant HTTP {r.status_code}: {r.text[:120]}"
        except requests.exceptions.ConnectionError:
            return False, f"No se pudo conectar a {url}. Verifica que Home Assistant esté en línea y accesible."
        except requests.exceptions.Timeout:
            return False, "Tiempo de espera agotado al conectar con Home Assistant."
        except Exception as e:
            return False, f"Error de conexión: {e}"

    def get_states(self) -> List[Dict[str, Any]]:
        """Fetch all entity states from Home Assistant."""
        if not self.is_connected():
            return []

        try:
            url = f"{self.base_url}/api/states"
            r = requests.get(url, headers=self._get_headers(), timeout=8.0)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[HomeAssistantClient] Error fetching states: {e}")
        return []

    def call_service(self, domain: str, service: str, entity_id: Optional[str] = None, service_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """Call a Home Assistant service."""
        if not self.is_connected():
            return False, "Home Assistant no está conectado."

        payload = dict(service_data or {})
        if entity_id:
            payload["entity_id"] = entity_id

        try:
            url = f"{self.base_url}/api/services/{domain}/{service}"
            r = requests.post(url, headers=self._get_headers(), json=payload, timeout=8.0)
            if r.status_code in (200, 201):
                return True, f"Servicio {domain}.{service} ejecutado correctamente."
            return False, f"Home Assistant error HTTP {r.status_code}: {r.text[:100]}"
        except Exception as e:
            return False, f"Error al ejecutar servicio en Home Assistant: {e}"

    def get_state(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single entity state from Home Assistant."""
        if not self.is_connected() or not entity_id:
            return None
        try:
            r = requests.get(
                f"{self.base_url}/api/states/{entity_id}",
                headers=self._get_headers(),
                timeout=8.0,
            )
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[HomeAssistantClient] Error fetching state {entity_id}: {e}")
        return None

    def get_services(self) -> List[Dict[str, Any]]:
        """Fetch available Home Assistant service domains."""
        if not self.is_connected():
            return []
        try:
            r = requests.get(
                f"{self.base_url}/api/services",
                headers=self._get_headers(),
                timeout=8.0,
            )
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[HomeAssistantClient] Error fetching services: {e}")
        return []

    def fire_event(self, event_type: str, event_data: Optional[Dict[str, Any]] = None) -> Tuple[bool, str]:
        """Fire a custom event in Home Assistant."""
        if not self.is_connected():
            return False, "Home Assistant no está conectado."
        if not event_type:
            return False, "event_type es obligatorio."
        try:
            r = requests.post(
                f"{self.base_url}/api/events/{event_type}",
                headers=self._get_headers(),
                json=event_data or {},
                timeout=8.0,
            )
            if r.status_code in (200, 201):
                return True, f"Evento '{event_type}' disparado."
            return False, f"Home Assistant error HTTP {r.status_code}: {r.text[:100]}"
        except Exception as e:
            return False, f"Error al disparar evento: {e}"

    def render_template(self, template: str) -> Tuple[bool, str]:
        """Render a Jinja2 template via Home Assistant /api/template."""
        if not self.is_connected():
            return False, "Home Assistant no está conectado."
        if not template:
            return False, "template es obligatorio."
        try:
            r = requests.post(
                f"{self.base_url}/api/template",
                headers=self._get_headers(),
                json={"template": template},
                timeout=8.0,
            )
            if r.status_code == 200:
                return True, r.text
            return False, f"Home Assistant error HTTP {r.status_code}: {r.text[:100]}"
        except Exception as e:
            return False, f"Error al renderizar template: {e}"

    def get_config(self) -> Optional[Dict[str, Any]]:
        """Fetch Home Assistant core config (/api/config)."""
        if not self.is_connected():
            return None
        try:
            r = requests.get(
                f"{self.base_url}/api/config",
                headers=self._get_headers(),
                timeout=8.0,
            )
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[HomeAssistantClient] Error fetching config: {e}")
        return None

    def get_api_client(self):
        """Return an optional homeassistant_api.Client instance if installed and configured."""
        if HomeAssistantAPIClient is None or not self.is_connected():
            return None
        return HomeAssistantAPIClient(f"{self.base_url}/api", self.token)


# Singleton client
ha_client = HomeAssistantClient()
