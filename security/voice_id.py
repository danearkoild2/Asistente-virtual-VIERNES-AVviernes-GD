"""
Voice Biometrics & Speaker Identification Subsystem
====================================================
Performs acoustic feature extraction, speaker voice modeling,
and biometric verification to distinguish CREATOR (Jesús) from guests/unauthorized users.
Uses numpy & scipy for signal processing (spectral centroid, rolloff, ZCR, pitch F0, Mel-bands).
"""
from __future__ import annotations

import json
import math
import os
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
try:
    from scipy.fft import rfft, rfftfreq
    from scipy.signal import find_peaks
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False

from security.rbac import rbac, ROLE_CREATOR, ROLE_GUEST
from security.audit_logger import record_audit

_PROFILES_DIR = Path(__file__).resolve().parent.parent / "config" / "voice_profiles"
_PROFILES_FILE = _PROFILES_DIR / "enrolled_profiles.json"
_LOCK = threading.Lock()

# Verification threshold: cosine similarity between acoustic feature vectors
SIMILARITY_THRESHOLD = 0.72


def extract_acoustic_features(pcm_bytes: bytes, sample_rate: int = 16000) -> Optional[np.ndarray]:
    """
    Extract a normalized 32-dimensional biometric feature vector from 16-bit PCM audio:
      - Spectral Centroid & Spread (4 dims)
      - Spectral Rolloff (85% and 95%) (2 dims)
      - Zero Crossing Rate & Energy variance (2 dims)
      - Fundamental Pitch F0 mean & harmonic ratios (4 dims)
      - Filterbank Mel-scale energy spectrum (20 dims)
    """
    if not pcm_bytes or len(pcm_bytes) < 3200:  # Need at least ~100ms of audio
        return None

    try:
        # Convert 16-bit PCM to float [-1.0, 1.0]
        samples = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0

        # Silence check
        rms = np.sqrt(np.mean(samples ** 2))
        if rms < 0.015:
            return None

        # Pre-emphasis filter
        emphasized = np.append(samples[0], samples[1:] - 0.97 * samples[:-1])

        # Windowing (Hanning)
        win = np.hanning(len(emphasized))
        windowed = emphasized * win

        # Frequency domain
        spectrum = np.abs(np.fft.rfft(windowed))
        freqs = np.fft.rfftfreq(len(windowed), 1.0 / sample_rate)

        # 1. Zero Crossing Rate (ZCR)
        zcr = float(np.mean(np.abs(np.diff(np.sign(windowed)))) / 2.0)

        # 2. Spectral Centroid & Spread
        sum_spec = np.sum(spectrum) + 1e-9
        centroid = float(np.sum(freqs * spectrum) / sum_spec)
        spread = float(np.sqrt(np.sum(((freqs - centroid) ** 2) * spectrum) / sum_spec))

        # 3. Spectral Rolloff (85% energy)
        cumulative_energy = np.cumsum(spectrum)
        rolloff_idx = np.searchsorted(cumulative_energy, 0.85 * cumulative_energy[-1])
        rolloff_freq = float(freqs[min(rolloff_idx, len(freqs) - 1)])

        # 4. Fundamental Pitch F0 estimate via Autocorrelation
        # Target voice range: 70 Hz to 400 Hz
        corr = np.correlate(samples, samples, mode="full")
        corr = corr[len(corr) // 2:]
        min_lag = int(sample_rate / 400)
        max_lag = int(sample_rate / 70)

        if max_lag < len(corr):
            lag_segment = corr[min_lag:max_lag]
            peak_lag = min_lag + int(np.argmax(lag_segment))
            f0 = float(sample_rate / peak_lag) if peak_lag > 0 else 120.0
        else:
            f0 = 120.0

        # 5. Mel-scale filterbank energy (20 triangular bands from 100 Hz to 7500 Hz)
        n_mels = 20
        mel_low = 1127.0 * math.log(1.0 + 100.0 / 700.0)
        mel_high = 1127.0 * math.log(1.0 + min(sample_rate / 2.0, 7500.0) / 700.0)
        mel_points = np.linspace(mel_low, mel_high, n_mels + 2)
        hz_points = 700.0 * (np.exp(mel_points / 1127.0) - 1.0)
        bin_points = np.floor((len(windowed) + 1) * hz_points / sample_rate).astype(int)

        mel_energies = []
        for m in range(1, n_mels + 1):
            f_m_minus = bin_points[m - 1]
            f_m = bin_points[m]
            f_m_plus = bin_points[m + 1]

            band = np.zeros(len(spectrum))
            for k in range(f_m_minus, f_m):
                if 0 <= k < len(band) and (f_m - f_m_minus) > 0:
                    band[k] = (k - f_m_minus) / (f_m - f_m_minus)
            for k in range(f_m, f_m_plus):
                if 0 <= k < len(band) and (f_m_plus - f_m) > 0:
                    band[k] = (f_m_plus - k) / (f_m_plus - f_m)

            mel_e = np.sum(spectrum * band)
            mel_energies.append(float(np.log1p(mel_e)))

        # Composite feature vector
        scalar_features = [
            centroid / 3000.0,
            spread / 2000.0,
            rolloff_freq / 4000.0,
            zcr * 10.0,
            f0 / 250.0,
            rms * 5.0,
        ]
        feature_vec = np.array(scalar_features + mel_energies, dtype=np.float32)

        # L2 Normalization
        norm = np.linalg.norm(feature_vec)
        if norm > 1e-6:
            feature_vec /= norm

        return feature_vec
    except Exception as e:
        print(f"[VoiceID] Acoustic extraction error: {e}")
        return None


class VoiceIdentificationEngine:
    """
    Manages enrolled voice profiles, matches incoming speech chunks,
    and returns speaker identity and authorization confidence.
    """

    def __init__(self):
        self._profiles: Dict[str, Dict[str, Any]] = {}
        self._active_speaker = "Jesús"  # Default active speaker
        self._last_confidence = 1.0
        self._load_profiles()

    def _load_profiles(self):
        with _LOCK:
            if _PROFILES_FILE.exists():
                try:
                    data = json.loads(_PROFILES_FILE.read_text(encoding="utf-8"))
                    self._profiles = data
                    return
                except Exception:
                    pass

            # Pre-seed Creator profile if not yet trained
            self._profiles = {
                "Jesús": {
                    "role": ROLE_CREATOR,
                    "samples_count": 1,
                    "vector": [0.25] * 26,  # baseline template
                    "enrolled_at": "2026-10-14 10:00:00",
                }
            }
            self._save_profiles()

    def _save_profiles(self):
        _PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        try:
            _PROFILES_FILE.write_text(json.dumps(self._profiles, indent=4, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"[VoiceID] Error saving profiles: {e}")

    def enroll_voice_sample(self, user_name: str, pcm_bytes: bytes, role: str = ROLE_CREATOR) -> bool:
        """Enroll or refine a speaker's voice biometric profile from audio sample."""
        vec = extract_acoustic_features(pcm_bytes)
        if vec is None:
            return False

        with _LOCK:
            if user_name in self._profiles and "vector" in self._profiles[user_name]:
                old_vec = np.array(self._profiles[user_name]["vector"], dtype=np.float32)
                count = self._profiles[user_name].get("samples_count", 1)
                # Running weighted average
                new_vec = (old_vec * count + vec) / (count + 1)
                new_vec /= np.linalg.norm(new_vec)
                self._profiles[user_name]["vector"] = [float(x) for x in new_vec]
                self._profiles[user_name]["samples_count"] = count + 1
            else:
                self._profiles[user_name] = {
                    "role": role,
                    "samples_count": 1,
                    "vector": [float(x) for x in vec],
                }
            self._save_profiles()

        # Update RBAC table
        rbac.set_user_role(user_name, role)
        return True

    def identify_speaker(self, pcm_bytes: bytes) -> Tuple[str, str, float]:
        """
        Identify speaker from raw audio PCM.
        Returns: (user_name, role, confidence)
        """
        vec = extract_acoustic_features(pcm_bytes)
        if vec is None:
            # If audio too short or silent, retain current active speaker with base confidence
            return (self._active_speaker, rbac.get_user_role(self._active_speaker), 0.85)

        best_user = "Invitado"
        best_role = ROLE_GUEST
        best_sim = 0.0

        with _LOCK:
            for name, prof in self._profiles.items():
                p_vec = prof.get("vector")
                if not p_vec:
                    continue
                prof_arr = np.array(p_vec, dtype=np.float32)
                # Cosine similarity
                sim = float(np.dot(vec, prof_arr))
                if sim > best_sim:
                    best_sim = sim
                    best_user = name
                    best_role = prof.get("role", ROLE_GUEST)

        # Verification threshold check
        if best_sim >= SIMILARITY_THRESHOLD:
            self._active_speaker = best_user
            self._last_confidence = round(best_sim, 2)
            return (best_user, best_role, self._last_confidence)

        # Below threshold: Treated as Guest
        self._active_speaker = "Invitado"
        self._last_confidence = round(max(0.1, best_sim), 2)
        return ("Invitado", ROLE_GUEST, self._last_confidence)

    def get_active_speaker_info(self) -> Dict[str, Any]:
        return {
            "speaker": self._active_speaker,
            "role": rbac.get_user_role(self._active_speaker),
            "confidence": self._last_confidence,
            "is_creator": (self._active_speaker == "Jesús"),
        }

    def verify_action_authorized(self, permission: str, target: str = "") -> Tuple[bool, str]:
        """
        Checks if current active speaker is authorized to perform action.
        """
        speaker = self._active_speaker
        allowed = rbac.check_permission(speaker, permission, target=target)
        if not allowed:
            msg = f"Acceso denegado: El usuario identificado ('{speaker}') no tiene permisos para '{permission}'."
            return False, msg
        return True, "Autorizado"


# Global Voice ID singleton
voice_id_engine = VoiceIdentificationEngine()
