"""
Text-to-Speech engines for MARK XL.

EdgeTTS     – free Microsoft TTS (internet required, no API key)
Kokoro      – fully offline neural TTS (~330 MB model)
ElevenLabs  – cloud API (API key required, best quality)
"""
from __future__ import annotations

import asyncio
import os
import queue as _queue
import threading
from typing import Callable, Optional

import numpy as np
import sounddevice as sd



# USE_TF=0 stops transformers from importing TensorFlow (saves 4-8 s startup).
# Do NOT set USE_TORCH or USE_JAX explicitly — forcing those values breaks
# transformers' lazy-loader on certain versions, causing AutoModel and other
# classes to vanish from the public namespace.  Auto-detection is reliable.
os.environ.setdefault("USE_TF",                 "0")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")


# ---------------------------------------------------------------------------
# Audio playback helpers
# ---------------------------------------------------------------------------

def _to_numpy(samples) -> np.ndarray:
    """Convert samples to float32 numpy array.

    Handles both numpy arrays and PyTorch tensors (Kokoro >= 0.9).

    PyTorch built against numpy 1.x raises RuntimeError('Numpy is not available')
    when numpy 2.x is installed.  The .tolist() fallback always works regardless
    of PyTorch / numpy version pairing.
    """
    if hasattr(samples, "detach"):                  # PyTorch tensor
        t = samples.detach().cpu().float()
        try:
            return t.numpy()                        # fast path (compatible versions)
        except RuntimeError:
            # PyTorch/numpy version mismatch — convert via Python list (always safe)
            return np.asarray(t.tolist(), dtype=np.float32)
    return np.asarray(samples, dtype=np.float32)


def _compress_silence(
    arr: np.ndarray,
    sample_rate: int    = 24_000,
    max_silence_ms: int = 500,    # cap punctuation pauses — keeps natural rhythm
    threshold: float    = 0.003,  # RMS below this = silence; lower = less clipping
) -> np.ndarray:
    """
    Shorten Kokoro's very long punctuation pauses (1-2 s → ≤500 ms).
    Conservative settings preserve natural prosody; only trims extreme pauses.
    """
    max_samp  = int(max_silence_ms * sample_rate / 1000)
    frame_len = 240                   # ~10 ms at 24 kHz
    out: list[np.ndarray] = []
    silent_acc = 0

    for i in range(0, len(arr), frame_len):
        chunk = arr[i : i + frame_len]
        if np.sqrt(np.mean(chunk ** 2) + 1e-12) < threshold:
            silent_acc += len(chunk)
            if silent_acc <= max_samp:
                out.append(chunk)
        else:
            silent_acc = 0
            out.append(chunk)

    return np.concatenate(out) if out else arr


def _play_np(samples, sample_rate: int) -> None:
    """Play float32 mono (or stereo) audio via sounddevice.
    Accepts numpy arrays or PyTorch tensors.
    """
    sd.play(_to_numpy(samples), sample_rate)
    sd.wait()


def _play_audio_bytes(audio_bytes: bytes) -> None:
    """Decode MP3/WAV/OGG bytes and play via sounddevice (uses miniaudio)."""
    import miniaudio
    decoded = miniaudio.decode(
        audio_bytes,
        output_format=miniaudio.SampleFormat.FLOAT32,
        nchannels=1,
    )
    samples = np.array(decoded.samples, dtype=np.float32)
    sd.play(samples, decoded.sample_rate)
    sd.wait()


# ---------------------------------------------------------------------------
# Engines
# ---------------------------------------------------------------------------

class EdgeTTSEngine:
    """Microsoft EdgeTTS – free, requires internet."""

    def __init__(self, voice: str = "es-MX-DaliaNeural"):
        self.voice = voice

    def speak(self, text: str) -> None:
        loop = asyncio.new_event_loop()
        try:
            audio_bytes = loop.run_until_complete(self._synth(text))
        finally:
            loop.close()
        if audio_bytes:
            _play_audio_bytes(audio_bytes)

    def synthesize_pcm(self, text: str, sample_rate: int = 24000) -> bytes:
        """Synthesize text using Edge Neural TTS and return 16-bit mono PCM at sample_rate."""
        import miniaudio
        loop = asyncio.new_event_loop()
        try:
            mp3_bytes = loop.run_until_complete(self._synth(text))
        finally:
            loop.close()
        if not mp3_bytes:
            return b""
        decoded = miniaudio.decode(
            mp3_bytes,
            output_format=miniaudio.SampleFormat.SIGNED16,
            nchannels=1,
            sample_rate=sample_rate,
        )
        return bytes(decoded.samples)

    async def _synth(self, text: str) -> bytes:
        import edge_tts
        comm = edge_tts.Communicate(text, self.voice)
        buf  = bytearray()
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                buf.extend(chunk["data"])
        return bytes(buf)


# ---------------------------------------------------------------------------
# Kokoro import helper — auto-upgrades on version-mismatch errors
# ---------------------------------------------------------------------------

# Errors that indicate the installed kokoro uses old transformers classes
# (AlbertModel, AutoModel) that are no longer exported at the top level.
_KOKORO_COMPAT_ERRORS = ("AlbertModel", "AutoModel", "cannot import name")


def _import_kokoro_pipeline():
    """Import KPipeline, auto-upgrading kokoro if a version mismatch is found.

    Old kokoro (<0.9) imports AlbertModel / AutoModel from transformers.
    Newer transformers versions no longer export these at the top level,
    causing an ImportError.  kokoro>=0.9 removed these dependencies.

    When the error is detected we:
      1. Upgrade kokoro to >=0.9 via pip (silent, background)
      2. Flush stale kokoro entries from sys.modules
      3. Re-import — this time it should succeed
    """
    import sys

    def _try_import():
        from kokoro import KPipeline  # noqa: PLC0415
        return KPipeline

    try:
        return _try_import()
    except Exception as first_err:
        err_msg = str(first_err)
        if not any(marker in err_msg for marker in _KOKORO_COMPAT_ERRORS):
            # Unrelated error (kokoro not installed, etc.)
            raise RuntimeError(
                f"Kokoro import failed: {first_err}\n"
                "Run: pip install kokoro>=0.9 soundfile"
            ) from first_err

        # ── Version mismatch: upgrade kokoro silently and retry ──────────
        print("[TTS] Kokoro/transformers version mismatch detected — upgrading kokoro…")
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "kokoro>=0.9",
             "--upgrade", "--quiet", "--disable-pip-version-check"],
            capture_output=True,
        )
        if result.returncode != 0:
            stderr = result.stderr.decode(errors="replace").strip()
            raise RuntimeError(
                f"Kokoro auto-upgrade failed: {stderr[:200]}\n"
                "Run manually: pip install kokoro>=0.9 soundfile"
            ) from first_err

        # Flush any stale kokoro submodules from the import cache
        stale = [k for k in sys.modules if k == "kokoro" or k.startswith("kokoro.")]
        for key in stale:
            del sys.modules[key]

        print("[TTS] Kokoro upgraded — retrying import…")
        try:
            return _try_import()
        except Exception as retry_err:
            raise RuntimeError(
                f"Kokoro still broken after upgrade: {retry_err}\n"
                "Run manually: pip install --upgrade kokoro transformers"
            ) from retry_err


# Kokoro voice prefix → KPipeline lang_code mapping
_KOKORO_LANG_CODES = {
    "a": "a",   # American English  (af_*, am_*)
    "b": "b",   # British English   (bf_*, bm_*)
    "j": "j",   # Japanese          (jf_*, jm_*)
    "z": "z",   # Mandarin Chinese  (zf_*, zm_*)
    "s": "s",   # Spanish           (sf_*, sm_*)
    "f": "f",   # French            (ff_*, fm_*)
    "h": "h",   # Hindi             (hf_*, hm_*)
    "i": "i",   # Italian           (if_*, im_*)
    "p": "p",   # Brazilian Portuguese
    "r": "r",   # Russian           (rf_*, rm_*)
    "e": "e",   # German            (ef_*, em_*)
}


class KokoroTTSEngine:
    """Fully offline Kokoro neural TTS.

    Model (~330 MB) is downloaded from HuggingFace on first use,
    then cached locally — subsequent starts load from disk.

    Warmup strategy: _init() runs synchronously in the background
    _do_tts() thread (not the UI thread).  After the pipeline loads,
    a dummy inference compiles the PyTorch JIT graph immediately so
    the first real speak() call has zero compilation overhead.
    """

    def __init__(self, voice: str = "af_heart", speed: float = 1.0):
        self.voice     = voice
        self.speed     = speed
        self._pipeline = None
        self._lock     = threading.Lock()
        self._init()   # blocking, but called from background thread

    @property
    def _lang_code(self) -> str:
        prefix = self.voice[0].lower() if self.voice else "a"
        return _KOKORO_LANG_CODES.get(prefix, "a")

    def _init(self) -> None:
        if self._pipeline is not None:
            return

        lang = self._lang_code

        # Prefer GPU — Kokoro on CUDA is ~10x faster than CPU.
        try:
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
            if device == "cpu":
                import os as _os
                n_threads = max(1, min(4, (_os.cpu_count() or 4) // 2))
                try:
                    torch.set_num_threads(n_threads)
                    torch.set_num_interop_threads(2)
                except RuntimeError:
                    pass
                print(
                    f"[TTS] Kokoro on CPU — for faster speech install CUDA PyTorch:\n"
                    "      pip install torch --index-url https://download.pytorch.org/whl/cu118"
                )
        except Exception:
            device = "cpu"

        print(f"[TTS] Kokoro — loading (lang='{lang}', device='{device}')…")

        KPipeline = _import_kokoro_pipeline()

        def _create_pipeline():
            try:
                return KPipeline(lang_code=lang, device=device)
            except TypeError:
                return KPipeline(lang_code=lang)   # older build — no device param

        try:
            self._pipeline = _create_pipeline()
        except Exception as _first_err:
            # Offline flag set but model not cached yet → clear flags and download once.
            # Keywords cover multiple huggingface_hub error message variants across versions.
            _e = str(_first_err).lower()
            _offline_keywords = (
                "offline", "not found", "cache", "localentry",
                "does not exist", "outgoing", "local_files_only",
            )
            if any(k in _e for k in _offline_keywords):
                print("[TTS] Kokoro model not in local cache — downloading (one-time, internet required)…")
                os.environ.pop("HF_HUB_OFFLINE",      None)
                os.environ.pop("TRANSFORMERS_OFFLINE", None)
                os.environ.pop("HF_DATASETS_OFFLINE",  None)
                try:
                    self._pipeline = _create_pipeline()
                except Exception as _dl_err:
                    raise RuntimeError(
                        f"Kokoro model download failed.\n"
                        f"Internet access is required the first time to download the voice model (~330 MB).\n"
                        f"After the first download it runs fully offline.\n"
                        f"Tip: Switch to EdgeTTS (free, no download) in the Configure panel if offline.\n"
                        f"Details: {_dl_err}"
                    ) from _dl_err
            else:
                raise

        print("[TTS] Kokoro compiling (first-time only)…")
        # Warmup: compiles PyTorch JIT graph so first real speak() call is instant.
        try:
            for _ in self._pipeline("hello", voice=self.voice, speed=self.speed):
                pass
            print("[TTS] Kokoro ready.")
        except Exception as e:
            print(f"[TTS] Kokoro warmup warning: {e}")

    def speak(self, text: str) -> None:
        with self._lock:
            if self._pipeline is None:
                self._init()

        # ── Concurrent synthesise + playback ────────────────────────────────
        # Kokoro generates audio chunks lazily.  Without threading, we:
        #   synthesise chunk N → play N → synthesise N+1 → play N+1 …
        # With a producer/consumer pair, chunk N+1 synthesises WHILE chunk N
        # plays, cutting perceived latency by the playback duration of all but
        # the last chunk (typically 1-3 s on multi-sentence responses).
        audio_q: "_queue.Queue[np.ndarray | None]" = _queue.Queue(maxsize=4)
        synth_error: list[Exception] = []

        def _synth():
            try:
                for _, _, audio in self._pipeline(text, voice=self.voice, speed=self.speed):
                    if audio is not None:
                        arr = _to_numpy(audio)
                        arr = _compress_silence(arr)
                        if arr.size > 0:
                            audio_q.put(arr)          # blocks if player is slow (backpressure)
            except Exception as exc:
                synth_error.append(exc)
            finally:
                audio_q.put(None)                     # sentinel → player exits

        synth_thread = threading.Thread(target=_synth, daemon=True)
        synth_thread.start()

        # Player runs in this thread so sd.wait() doesn't block the synth thread.
        while True:
            arr = audio_q.get()
            if arr is None:
                break
            _play_np(arr, 24000)

        synth_thread.join()

        if synth_error:
            raise synth_error[0]


_EL_SESSION = None
_EL_PCM_SUPPORTED: dict[str, bool] = {}  # api_key_prefix -> bool (whether tier allows raw pcm_24000)


def _get_el_session():
    global _EL_SESSION
    if _EL_SESSION is None:
        import requests
        _EL_SESSION = requests.Session()
    return _EL_SESSION


def fetch_elevenlabs_voices(api_key: str) -> list[tuple[str, str, str, str]]:
    """Fetch available voices from user's ElevenLabs account.
    Returns list of (voice_id, name, gender, description).
    """
    key = (api_key or "").strip()
    if not key:
        return []
    sess = _get_el_session()
    resp = sess.get(
        "https://api.elevenlabs.io/v1/voices",
        headers={"xi-api-key": key},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    out: list[tuple[str, str, str, str]] = []
    for v in data.get("voices", []):
        vid = v.get("voice_id", "")
        name = v.get("name", "Voz")
        labels = v.get("labels") or {}
        gender_raw = (labels.get("gender") or "").lower()
        gender = "Femenina" if "female" in gender_raw else ("Masculina" if "male" in gender_raw else "Personalizada")
        accent = labels.get("accent") or labels.get("use_case") or v.get("category") or "ElevenLabs"
        desc = labels.get("description") or str(accent).capitalize()
        if vid:
            out.append((vid, name, gender, desc))
    return out


class ElevenLabsTTSEngine:
    """ElevenLabs cloud TTS – Ultra-low latency Flash v2.5 streaming."""

    def __init__(self, api_key: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM"):
        self.api_key  = api_key.strip()
        self.voice_id = voice_id.strip() or "21m00Tcm4TlvDq8ikWAM"

    def stream_pcm_chunks(self, text: str, sample_rate: int = 24000, chunk_bytes: int = 2400):
        """Yield 24kHz 16-bit mono PCM chunks in real time using ElevenLabs Flash v2.5 streaming."""
        txt = (text or "").strip()
        if not txt:
            return
        sess = _get_el_session()
        key_tag = self.api_key[:10]
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "text": txt,
            "model_id": "eleven_flash_v2_5",
            "language_code": "es",
            "voice_settings": {
                "stability": 0.45,
                "similarity_boost": 0.78,
                "speed": 1.04,
            },
        }

        # 1. Try zero-decode raw PCM streaming first (fastest possible: ~150-220ms to first byte)
        if _EL_PCM_SUPPORTED.get(key_tag, True) and sample_rate == 24000:
            url_pcm = (
                f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
                f"?output_format=pcm_24000&optimize_streaming_latency=4"
            )
            try:
                with sess.post(url_pcm, json=payload, headers=headers, stream=True, timeout=15) as r:
                    if r.status_code == 200:
                        _EL_PCM_SUPPORTED[key_tag] = True
                        carry = b""
                        for raw in r.iter_content(chunk_size=chunk_bytes):
                            if not raw:
                                continue
                            buf = carry + raw
                            # Keep 16-bit sample alignment (even number of bytes)
                            even_len = (len(buf) // 2) * 2
                            if even_len > 0:
                                yield buf[:even_len]
                            carry = buf[even_len:]
                        return
                    elif r.status_code in (400, 401, 403):
                        # Free tier or unsupported language_code param -> fallback
                        _EL_PCM_SUPPORTED[key_tag] = False
            except Exception:
                pass

        # 2. Fast MP3 stream fallback (works on all tiers including Free tier)
        pcm_all = self.synthesize_pcm(txt, sample_rate=sample_rate)
        for i in range(0, len(pcm_all), chunk_bytes):
            yield pcm_all[i : i + chunk_bytes]

    def synthesize_pcm(self, text: str, sample_rate: int = 24000) -> bytes:
        """Synthesize text and return 16-bit mono signed PCM bytes at sample_rate."""
        import miniaudio
        sess = _get_el_session()
        headers = {
            "xi-api-key":   self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "text":     text,
            "model_id": "eleven_flash_v2_5",
            "voice_settings": {"stability": 0.45, "similarity_boost": 0.78},
        }
        url = (
            f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream"
            f"?output_format=mp3_22050_32&optimize_streaming_latency=4"
        )
        resp = sess.post(url, json=payload, headers=headers, timeout=18)
        if not resp.ok:
            payload["model_id"] = "eleven_multilingual_v2"
            resp = sess.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}",
                json=payload, headers=headers, timeout=22,
            )
        if not resp.ok:
            try:
                err_data = resp.json()
                msg = err_data.get("detail", {}).get("message") or str(err_data)
            except Exception:
                msg = resp.text[:200]
            raise RuntimeError(f"ElevenLabs error ({resp.status_code}): {msg}")
        decoded = miniaudio.decode(
            resp.content,
            output_format=miniaudio.SampleFormat.SIGNED16,
            nchannels=1,
            sample_rate=sample_rate,
        )
        return bytes(decoded.samples)

    def speak(self, text: str) -> None:
        sess = _get_el_session()
        headers = {
            "xi-api-key":   self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "text":     text,
            "model_id": "eleven_flash_v2_5",
            "voice_settings": {"stability": 0.45, "similarity_boost": 0.78},
        }
        resp = sess.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/stream?optimize_streaming_latency=4",
            json=payload, headers=headers, timeout=25,
        )
        resp.raise_for_status()
        _play_audio_bytes(resp.content)


_COQUI_MODEL = None
_COQUI_LOCK = threading.Lock()


def is_coqui_installed() -> bool:
    """Return True if idiap/coqui-ai-TTS (`TTS` package) is importable."""
    import importlib.util
    return importlib.util.find_spec("TTS") is not None


class CoquiXTTSEngine:
    """Local neural TTS & voice cloning via idiap/coqui-ai-TTS (XTTS-v2).

    Model weights (~1.8 GB) are lazy-loaded only on first synthesis so startup
    and idle memory remain untouched when another voice engine is active.
    """

    MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
    NATIVE_SR = 24000

    def __init__(
        self,
        speaker: str = "Ana Florence",
        speaker_wav: str = "",
        language: str = "es",
    ) -> None:
        self.speaker = (speaker or "Ana Florence").strip()
        self.speaker_wav = (speaker_wav or "").strip()
        self.language = (language or "es").strip() or "es"

    @classmethod
    def _get_model(cls):
        global _COQUI_MODEL
        if _COQUI_MODEL is not None:
            return _COQUI_MODEL
        with _COQUI_LOCK:
            if _COQUI_MODEL is not None:
                return _COQUI_MODEL
            try:
                import os
                os.environ.setdefault("COQUI_TOS_AGREED", "1")
                os.environ.setdefault("TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD", "1")
                import torch
                from TTS.api import TTS
            except ImportError as exc:
                raise RuntimeError(
                    "coqui-tts no está instalado. Instálalo con: pip install coqui-tts"
                ) from exc

            device = "cuda" if torch.cuda.is_available() else "cpu"
            _COQUI_MODEL = TTS(cls.MODEL_NAME).to(device)
            return _COQUI_MODEL

    def synthesize_pcm(self, text: str, sample_rate: int = 24000) -> bytes:
        """Synthesize text with XTTS-v2 and return 16-bit signed mono PCM bytes."""
        clean = (text or "").strip()
        if not clean:
            return b""

        tts = self._get_model()
        kwargs: dict = {"text": clean, "language": self.language}
        if self.speaker_wav and Path(self.speaker_wav).exists():
            kwargs["speaker_wav"] = self.speaker_wav
        else:
            kwargs["speaker"] = self.speaker

        wav = tts.tts(**kwargs)
        arr = np.asarray(wav, dtype=np.float32)
        if arr.ndim > 1:
            arr = arr.mean(axis=-1)

        if sample_rate != self.NATIVE_SR and len(arr) > 1:
            new_len = max(1, int(round(len(arr) * (sample_rate / self.NATIVE_SR))))
            x_old = np.linspace(0.0, 1.0, len(arr), endpoint=False)
            x_new = np.linspace(0.0, 1.0, new_len, endpoint=False)
            arr = np.interp(x_new, x_old, arr).astype(np.float32)

        arr = np.clip(arr, -1.0, 1.0)
        pcm = (arr * 32767.0).astype("<i2")
        return pcm.tobytes()

    def speak(self, text: str) -> None:
        pcm = self.synthesize_pcm(text, sample_rate=self.NATIVE_SR)
        if pcm:
            arr = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32767.0
            sd.play(arr, samplerate=self.NATIVE_SR, blocking=True)


# ---------------------------------------------------------------------------
# Thread-safe player wrapper
# ---------------------------------------------------------------------------

class TTSPlayer:
    """
    Wraps any *Engine. Exposes a blocking speak() method
    meant to be called from a dedicated background thread.
    """

    def __init__(self, engine):
        self._engine  = engine
        self._playing = False
        self._lock    = threading.Lock()

    @property
    def is_playing(self) -> bool:
        return self._playing

    def speak(
        self,
        text:     str,
        on_start: Optional[Callable] = None,
        on_done:  Optional[Callable] = None,
    ) -> None:
        """Synthesise and play text. BLOCKING – call from a dedicated thread."""
        try:
            with self._lock:
                self._playing = True
            if on_start:
                on_start()
            self._engine.speak(text)
        except Exception as e:
            print(f"[TTS] Error: {e}")
        finally:
            with self._lock:
                self._playing = False
            if on_done:
                on_done()

    def stop(self) -> None:
        sd.stop()
        with self._lock:
            self._playing = False


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def create_tts_player(config: dict) -> TTSPlayer:
    engine_name = config.get("tts_engine", "edgetts").lower()
    if engine_name == "kokoro":
        voice  = config.get("tts_voice", "af_heart")
        speed  = float(config.get("tts_speed", 1.0))
        engine = KokoroTTSEngine(voice=voice, speed=speed)
    elif engine_name == "elevenlabs":
        api_key  = config.get("elevenlabs_api_key", "")
        voice_id = config.get("tts_voice", "pNInz6obpgDQGcFmaJgB")
        engine   = ElevenLabsTTSEngine(api_key=api_key, voice_id=voice_id)
    elif engine_name == "coqui_xtts":
        engine = CoquiXTTSEngine(
            speaker=config.get("coqui_speaker", "Ana Florence"),
            speaker_wav=config.get("coqui_speaker_wav", ""),
            language=config.get("coqui_language", "es"),
        )
    else:   # edgetts (default)
        voice  = config.get("tts_voice", "en-US-GuyNeural")
        engine = EdgeTTSEngine(voice=voice)
    return TTSPlayer(engine)
