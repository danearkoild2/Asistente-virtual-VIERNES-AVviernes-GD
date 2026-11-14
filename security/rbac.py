"""
Role-Based Access Control (RBAC) Subsystem for VIERNES
======================================================
Defines and enforces granular permission gates for users, voice identification,
and module access.
Roles: CREATOR, ADMIN, USER, GUEST.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from security.audit_logger import record_audit

_CONFIG_FILE = Path(__file__).resolve().parent.parent / "config" / "user_roles.json"

ROLE_CREATOR = "CREATOR"
ROLE_ADMIN   = "ADMIN"
ROLE_USER    = "USER"
ROLE_GUEST   = "GUEST"

PERMISSIONS: Dict[str, List[str]] = {
    # Full capabilities
    ROLE_CREATOR: [
        "gmail.read", "gmail.manage", "gmail.open",
        "finance.read", "finance.analyze", "finance.export",
        "smarthome.read", "smarthome.control", "smarthome.locks", "smarthome.scenes",
        "social.read", "social.publish", "social.analytics",
        "system.diagnostics", "system.monitor", "system.actions", "system.settings",
        "translation.live",
        "voice_id.manage", "security.audit",
    ],
    # High privileged delegate
    ROLE_ADMIN: [
        "gmail.read", "gmail.manage", "gmail.open",
        "smarthome.read", "smarthome.control", "smarthome.scenes",
        "social.read", "social.analytics",
        "system.diagnostics", "system.monitor",
        "translation.live",
    ],
    # Standard authorized household/office user
    ROLE_USER: [
        "smarthome.read", "smarthome.control_safe", "smarthome.scenes",
        "translation.live",
        "media.control", "queries.general",
    ],
    # Unknown speaker / Guest
    ROLE_GUEST: [
        "translation.live",
        "queries.general",
    ],
}

DEFAULT_USERS: Dict[str, Dict[str, Any]] = {
    "Jesús": {
        "role": ROLE_CREATOR,
        "is_creator": True,
        "voice_enrolled": True,
        "notes": "Primary Creator & Root Administrator",
    },
    "Invitado": {
        "role": ROLE_GUEST,
        "is_creator": False,
        "voice_enrolled": False,
        "notes": "Default guest profile for unrecognized voices",
    },
}


class RBACManager:
    def __init__(self):
        self._users: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self):
        if _CONFIG_FILE.exists():
            try:
                self._users = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
                return
            except Exception:
                pass
        self._users = dict(DEFAULT_USERS)
        self.save()

    def save(self):
        try:
            _CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            _CONFIG_FILE.write_text(json.dumps(self._users, indent=4, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"[RBAC] Error saving user roles: {e}")

    def get_users(self) -> Dict[str, Dict[str, Any]]:
        return dict(self._users)

    def get_user_role(self, user_name: str) -> str:
        u = self._users.get(user_name)
        if u:
            return u.get("role", ROLE_GUEST)
        return ROLE_GUEST

    def set_user_role(self, user_name: str, role: str) -> bool:
        if role not in PERMISSIONS:
            return False
        if user_name not in self._users:
            self._users[user_name] = {
                "role": role,
                "is_creator": False,
                "voice_enrolled": False,
                "notes": "Added user",
            }
        else:
            self._users[user_name]["role"] = role
        self.save()
        return True

    def check_permission(self, user_name: str, required_permission: str, target: str = "") -> bool:
        """
        Check if user has permission. Records audit event if denied.
        """
        role = self.get_user_role(user_name)
        allowed_perms = PERMISSIONS.get(role, [])

        has_perm = (required_permission in allowed_perms)

        if not has_perm:
            # Audit log security denial
            record_audit(
                action=f"ACCESS_{required_permission}",
                user=user_name,
                role=role,
                target=target or required_permission,
                result="DENIED",
                reason=f"Insufficient role permissions ({role} lacks {required_permission})",
            )
            return False

        return True


# Global RBAC singleton
rbac = RBACManager()
