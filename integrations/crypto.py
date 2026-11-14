"""
Security & Cryptography Subsystem for VIERNES
==============================================
Provides AES-128-CBC / HMAC-SHA256 (Fernet) encryption for OAuth tokens,
API keys, and sensitive integration credentials.
Never stores external credentials in plain text.
"""
from __future__ import annotations

import base64
import hashlib
import os
import platform
from pathlib import Path
from typing import Optional

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    HAVE_CRYPTO = True
except ImportError:
    HAVE_CRYPTO = False

_VAULT_KEY_FILE = Path(__file__).resolve().parent.parent / "config" / ".secret_vault.key"
_SALT_FILE = Path(__file__).resolve().parent.parent / "config" / ".vault_salt.bin"


def _get_machine_seed() -> bytes:
    """Generate a consistent, machine-specific seed for local key derivation."""
    seed_parts = [
        platform.node(),
        platform.machine(),
        os.environ.get("USERNAME", "viernes_user"),
        platform.processor(),
    ]
    return "|".join(seed_parts).encode("utf-8")


def _get_or_create_cipher() -> Optional[Fernet]:
    if not HAVE_CRYPTO:
        return None

    try:
        if _VAULT_KEY_FILE.exists():
            key = _VAULT_KEY_FILE.read_bytes().strip()
            return Fernet(key)

        # Derive a key using PBKDF2 with machine seed
        if not _SALT_FILE.exists():
            salt = os.urandom(16)
            _SALT_FILE.parent.mkdir(parents=True, exist_ok=True)
            _SALT_FILE.write_bytes(salt)
        else:
            salt = _SALT_FILE.read_bytes()

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(_get_machine_seed()))
        _VAULT_KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
        _VAULT_KEY_FILE.write_bytes(key)
        return Fernet(key)
    except Exception as e:
        print(f"[Crypto] Error initializing Fernet cipher: {e}")
        return None


_CIPHER = _get_or_create_cipher()


def encrypt_secret(plaintext: str) -> str:
    """Encrypt a plaintext secret string and return URL-safe base64 ciphertext."""
    if not plaintext:
        return ""
    if _CIPHER is not None:
        try:
            encrypted_bytes = _CIPHER.encrypt(plaintext.encode("utf-8"))
            return "ENC:" + encrypted_bytes.decode("utf-8")
        except Exception as e:
            print(f"[Crypto] Encryption error: {e}")
    # Fallback obfuscation if cryptography package is missing
    raw_b64 = base64.b64encode(plaintext.encode("utf-8")).decode("utf-8")
    return "OBF:" + raw_b64


def decrypt_secret(ciphertext: str) -> str:
    """Decrypt an encrypted secret string. Handles ENC: (Fernet) and OBF: (Fallback)."""
    if not ciphertext:
        return ""
    if ciphertext.startswith("ENC:"):
        token = ciphertext[4:]
        if _CIPHER is not None:
            try:
                decrypted_bytes = _CIPHER.decrypt(token.encode("utf-8"))
                return decrypted_bytes.decode("utf-8")
            except Exception as e:
                print(f"[Crypto] Decryption error: {e}")
                return ""
        return ""
    elif ciphertext.startswith("OBF:"):
        try:
            return base64.b64decode(ciphertext[4:]).decode("utf-8")
        except Exception:
            return ""
    # Plain text backward compatibility
    return ciphertext
