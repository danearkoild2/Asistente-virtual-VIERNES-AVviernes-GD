from __future__ import annotations

import concurrent.futures
import ipaddress
import json
import os
import re
import shutil
import socket
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BASE_DIR / "config" / "cleanyourtv_cache"
PROFILES_INDEX_FILE = CACHE_DIR / "profiles_index.json"
BACKUPS_DIR = BASE_DIR / "config" / "cleanyourtv_backups"

GITHUB_EXAMPLES_API = "https://api.github.com/repos/Gathin23/cleanyourtv/contents/examples"
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/Gathin23/cleanyourtv/main/examples"
UA = "Viernes-CleanYourTV/1.0"

# Packages that must NEVER be disabled to keep Android TV / Google TV bootable & controllable
_NEVER_DISABLE: set[str] = {
    "android",
    "com.android.systemui",
    "com.android.settings",
    "com.android.tv.settings",
    "com.android.providers.settings",
    "com.android.vending",
    "com.google.android.gms",
    "com.google.android.gsf",
    "com.android.bluetooth",
    "com.android.networkstack",
    "com.android.wifi.resources",
    "com.google.android.webview",
    "com.android.webview",
    "com.android.inputmethod.latin",
    "com.google.android.inputmethod.latin",
    "com.android.packageinstaller",
    "com.google.android.packageinstaller",
    "com.android.permissioncontroller",
    "com.google.android.permissioncontroller",
    "com.android.shell",
}

# Universal Android TV / Google TV safe debloat rules (used alongside brand profile from Gathin23/cleanyourtv)
_UNIVERSAL_RULES: list[tuple[str, str, str]] = [
    # (package, category, description)
    ("com.google.android.tungsten.setupwraith", "Telemetría y Setup", "Asistente residual post-configuración"),
    ("com.google.android.tvrecommendations", "Anuncios y Recomendaciones", "Carrusel de recomendaciones y promos en inicio"),
    ("com.google.android.backdrop", "Extras / Salvapantallas", "Salvapantallas ambiental de Google"),
    ("com.google.android.videos", "Bloatware Google", "Google TV / Películas preinstalado"),
    ("com.google.android.music", "Bloatware Google", "Servicio legado Google Play Music"),
    ("com.google.android.apps.tachyon", "Bloatware Google", "Google Meet / Duo preinstalado"),
    ("com.google.android.feedback", "Telemetría y Rastreo", "Envío de reportes e informes de uso"),
    ("com.google.android.partnersetup", "Telemetría y Rastreo", "Configuración comercial de socios"),
    ("com.google.android.syncadapters.calendar", "Bloatware Google", "Sincronización de calendario innecesaria en TV"),
    ("com.google.android.syncadapters.contacts", "Bloatware Google", "Sincronización de contactos innecesaria en TV"),
    ("com.android.providers.calendar", "Bloatware Sistema", "Proveedor de calendario"),
    ("com.android.providers.contacts", "Bloatware Sistema", "Proveedor de contactos"),
    ("com.android.dreams.basic", "Extras / Salvapantallas", "Salvapantallas básico"),
    ("com.android.printspooler", "Bloatware Sistema", "Cola de impresión"),
    ("com.android.bips", "Bloatware Sistema", "Servicio de impresión integrado"),
    ("com.google.android.marvin.talkback", "Accesibilidad opcional", "Lector de pantalla TalkBack (si no se usa)"),
    ("com.netflix.ninja", "Apps Preinstaladas", "Netflix preinstalado (solo si no lo usas)"),
    ("com.amazon.amazonvideo.livingroom", "Apps Preinstaladas", "Prime Video preinstalado (solo si no lo usas)"),
]


def find_adb() -> Optional[str]:
    """Locate adb.exe on PATH or standard Android SDK platform-tools locations."""
    found = shutil.which("adb")
    if found:
        return found
    candidates = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Android" / "Sdk" / "platform-tools" / "adb.exe",
        Path("C:/platform-tools/adb.exe"),
        Path("C:/Android/platform-tools/adb.exe"),
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return None


def _run_adb(args: list[str], timeout: float = 12.0) -> tuple[int, str, str]:
    adb = find_adb()
    if not adb:
        return -1, "", "No se encontró adb.exe en el equipo (instala Android Platform Tools)."
    try:
        proc = subprocess.run(
            [adb, *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return proc.returncode, (proc.stdout or "").strip(), (proc.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return -2, "", f"Tiempo de espera agotado ejecutando adb {' '.join(args[:3])}."
    except Exception as exc:
        return -3, "", str(exc)


def _local_subnet() -> Optional[ipaddress.IPv4Network]:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return ipaddress.ip_network(f"{local_ip}/24", strict=False)
    except Exception:
        return None


def _probe_port_5555(ip: str, timeout: float = 0.35) -> Optional[str]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((ip, 5555)) == 0:
                return ip
    except Exception:
        pass
    return None


def discover_android_tvs() -> list[dict[str, Any]]:
    """Find Android TVs with ADB network debugging open (port 5555) or already connected in ADB."""
    found: dict[str, dict[str, Any]] = {}

    # 1. Existing ADB devices
    rc, out, _ = _run_adb(["devices", "-l"], timeout=5.0)
    if rc == 0:
        for line in out.splitlines()[1:]:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            serial = parts[0]
            state = parts[1] if len(parts) > 1 else "unknown"
            ip = serial.split(":")[0] if ":" in serial else serial
            model = ""
            for p in parts[2:]:
                if p.startswith("model:"):
                    model = p.split(":", 1)[1].replace("_", " ")
            found[serial] = {"serial": serial, "ip": ip, "state": state, "model": model or "Android TV"}

    # 2. Fast parallel scan of local /24 subnet on ADB port 5555
    net = _local_subnet()
    if net is not None:
        hosts = [str(h) for h in net.hosts()]
        with concurrent.futures.ThreadPoolExecutor(max_workers=48) as ex:
            for res in ex.map(_probe_port_5555, hosts):
                if res:
                    serial = f"{res}:5555"
                    if serial not in found:
                        found[serial] = {
                            "serial": serial,
                            "ip": res,
                            "state": "port_5555_open",
                            "model": "Android TV (ADB listo)",
                        }
    return list(found.values())


def get_remote_instructions(stage: str = "enable_adb") -> str:
    """Return clear step-by-step remote control instructions for the user."""
    if stage == "authorize":
        return (
            "Mira la pantalla de tu televisor: debe aparecer un aviso que dice "
            "'¿Permitir depuración USB?' (Allow USB debugging). Con tu control remoto, "
            "marca la casilla 'Permitir siempre desde esta computadora' y selecciona Aceptar / OK. "
            "Cuando lo hayas aceptado, avísame para continuar con el análisis."
        )
    return (
        "Para conectar Viernes a tu Android TV / Google TV con el control remoto:\n"
        "1. Abre Configuración (⚙) en tu televisor.\n"
        "2. Ve a Sistema → Acerca de (o Preferencias del dispositivo → Información).\n"
        "3. Baja hasta 'Compilación' (Build) y presiona OK 7 veces seguidas hasta que diga 'Ya eres desarrollador'.\n"
        "4. Regresa un paso, entra a 'Opciones de desarrollador' y activa 'Depuración USB' / 'Depuración de red'.\n"
        "5. Asegúrate de que el televisor y esta PC estén en el mismo Wi-Fi y dime la IP del TV (o pídeme escanear la red)."
    )


def connect_tv(ip: str) -> dict[str, Any]:
    """Step 1: Connect to Android TV over ADB Wi-Fi (port 5555) and inspect authorization state."""
    target = ip.strip()
    if not target:
        return {"ok": False, "state": "no_ip", "message": "Indica la IP del televisor o escanea la red primero."}
    serial = target if ":" in target else f"{target}:5555"

    rc, out, err = _run_adb(["connect", serial], timeout=8.0)
    if rc < 0:
        return {"ok": False, "state": "no_adb", "message": err or out}

    # Check exact state in `adb devices`
    _, dev_out, _ = _run_adb(["devices"], timeout=5.0)
    state = "offline"
    for line in dev_out.splitlines()[1:]:
        parts = line.strip().split()
        if parts and parts[0] == serial:
            state = parts[1] if len(parts) > 1 else "unknown"
            break

    if state == "unauthorized":
        return {
            "ok": False,
            "state": "unauthorized",
            "serial": serial,
            "message": get_remote_instructions("authorize"),
        }
    if state != "device":
        return {
            "ok": False,
            "state": "refused",
            "serial": serial,
            "message": (
                f"No pude conectar con {serial} ({out or err or state}).\n"
                + get_remote_instructions("enable_adb")
            ),
        }

    info = get_tv_info(serial)
    return {
        "ok": True,
        "state": "connected",
        "serial": serial,
        "info": info,
        "message": (
            f"Conectado a {info.get('manufacturer', '')} {info.get('model', 'Android TV')} "
            f"(Android {info.get('android_version', '?')}) en {serial}."
        ).strip(),
    }


def get_tv_info(serial: str) -> dict[str, str]:
    def _prop(name: str) -> str:
        rc, out, _ = _run_adb(["-s", serial, "shell", "getprop", name], timeout=5.0)
        return out.strip() if rc == 0 else ""

    return {
        "serial": serial,
        "manufacturer": _prop("ro.product.manufacturer") or _prop("ro.product.brand") or "Android TV",
        "model": _prop("ro.product.model") or _prop("ro.product.device") or "TV",
        "device": _prop("ro.product.device"),
        "android_version": _prop("ro.build.version.release"),
        "sdk": _prop("ro.build.version.sdk"),
    }


def _fetch_community_profiles(force: bool = False) -> list[str]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if not force and PROFILES_INDEX_FILE.exists():
        age_h = (time.time() - PROFILES_INDEX_FILE.stat().st_mtime) / 3600.0
        if age_h < 24.0:
            try:
                return json.loads(PROFILES_INDEX_FILE.read_text(encoding="utf-8")).get("profiles", [])
            except Exception:
                pass
    try:
        r = requests.get(GITHUB_EXAMPLES_API, headers={"User-Agent": UA}, timeout=10)
        if r.status_code == 200:
            names = [item["name"] for item in r.json() if item.get("type") == "dir"]
            PROFILES_INDEX_FILE.write_text(
                json.dumps({"ts": time.time(), "profiles": names}, ensure_ascii=False),
                encoding="utf-8",
            )
            return names
    except Exception:
        pass
    if PROFILES_INDEX_FILE.exists():
        try:
            return json.loads(PROFILES_INDEX_FILE.read_text(encoding="utf-8")).get("profiles", [])
        except Exception:
            pass
    return []


def _parse_debloat_txt(text: str) -> list[tuple[str, str, str]]:
    """Parse Gathin23/cleanyourtv debloat.txt format into (package, group, note)."""
    items: list[tuple[str, str, str]] = []
    current_group = "Bloatware de Marca"
    pending_comments: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            pending_comments.clear()
            continue
        if line.startswith("#"):
            c = line.lstrip("#").strip()
            # Commented-out package line (# com.foo.bar) means "kept by owner", skip
            if re.match(r"^[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+", c):
                continue
            if c:
                pending_comments.append(c)
            continue
        if pending_comments:
            current_group = pending_comments[0][:60]
            pending_comments.clear()
        pkg_part, _, note = line.partition("#")
        pkg = pkg_part.strip()
        if re.match(r"^[a-zA-Z0-9_]+(\.[a-zA-Z0-9_-]+)+$", pkg):
            items.append((pkg, current_group, note.strip()))
    return items


def _find_best_profile_rules(info: dict[str, str]) -> tuple[str, list[tuple[str, str, str]]]:
    brand = re.sub(r"[^a-z0-9]+", "-", (info.get("manufacturer") or "").lower()).strip("-")
    model = re.sub(r"[^a-z0-9]+", "-", (info.get("model") or "").lower()).strip("-")
    device = re.sub(r"[^a-z0-9]+", "-", (info.get("device") or "").lower()).strip("-")

    profiles = _fetch_community_profiles()
    matched_name = ""
    best_score = 0
    for p in profiles:
        pl = p.lower()
        score = 0
        if brand and brand in pl:
            score += 2
        if model and model in pl:
            score += 4
        if device and device in pl:
            score += 3
        if score > best_score:
            best_score = score
            matched_name = p

    rules = list(_UNIVERSAL_RULES)
    if matched_name and best_score >= 2:
        cache_file = CACHE_DIR / f"{matched_name}.txt"
        txt = ""
        if cache_file.exists():
            txt = cache_file.read_text(encoding="utf-8", errors="replace")
        else:
            try:
                r = requests.get(f"{GITHUB_RAW_BASE}/{matched_name}/debloat.txt", headers={"User-Agent": UA}, timeout=10)
                if r.status_code == 200:
                    txt = r.text
                    CACHE_DIR.mkdir(parents=True, exist_ok=True)
                    cache_file.write_text(txt, encoding="utf-8")
            except Exception:
                pass
        if txt:
            existing = {pkg for pkg, _, _ in rules}
            for pkg, grp, note in _parse_debloat_txt(txt):
                if pkg not in existing:
                    rules.append((pkg, grp, note or f"Perfil {matched_name}"))
                    existing.add(pkg)

    return matched_name or "Universal Android TV", rules


def analyze_tv(ip: str) -> dict[str, Any]:
    """Step 2: Read enabled packages on the TV and classify ads, tracking & bloatware without changing anything."""
    conn = connect_tv(ip)
    if not conn.get("ok"):
        return conn

    serial = conn["serial"]
    info = conn["info"]
    rc, out, err = _run_adb(["-s", serial, "shell", "pm", "list", "packages", "-e"], timeout=15.0)
    if rc != 0:
        return {"ok": False, "state": "error", "message": f"No se pudieron leer los paquetes del TV: {err or out}"}

    enabled_pkgs = {
        line.replace("package:", "").strip()
        for line in out.splitlines()
        if line.strip().startswith("package:")
    }

    profile_name, rules = _find_best_profile_rules(info)
    candidates: list[dict[str, str]] = []
    for pkg, category, desc in rules:
        if pkg in _NEVER_DISABLE:
            continue
        if pkg in enabled_pkgs:
            candidates.append({
                "package": pkg,
                "category": category,
                "description": desc or category,
            })

    return {
        "ok": True,
        "state": "analyzed",
        "serial": serial,
        "info": info,
        "profile_matched": profile_name,
        "total_enabled": len(enabled_pkgs),
        "candidates": candidates,
        "message": (
            f"Análisis completado en {info.get('manufacturer')} {info.get('model')} "
            f"(perfil: {profile_name}). Se encontraron {len(candidates)} paquetes seguros para desactivar "
            f"(de {len(enabled_pkgs)} activos). Nada ha sido modificado aún."
        ),
    }


def clean_tv(ip: str, packages: Optional[list[str]] = None) -> dict[str, Any]:
    """Step 3: Save a restore point and safely disable approved packages with `pm disable-user --user 0`."""
    analysis = analyze_tv(ip)
    if not analysis.get("ok"):
        return analysis

    serial = analysis["serial"]
    info = analysis["info"]
    candidate_map = {c["package"]: c for c in analysis.get("candidates", [])}

    if packages is None:
        target_pkgs = list(candidate_map.keys())
    else:
        target_pkgs = [p.strip() for p in packages if p.strip() and p.strip() not in _NEVER_DISABLE]

    if not target_pkgs:
        return {
            "ok": True,
            "state": "nothing_to_clean",
            "serial": serial,
            "disabled": [],
            "failed": [],
            "message": "Tu televisor ya está limpio; no hay paquetes pendientes por desactivar.",
        }

    # Create restore point BEFORE modifying anything
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_model = re.sub(r"[^a-zA-Z0-9_-]+", "_", info.get("model") or "tv")
    backup_path = BACKUPS_DIR / f"{safe_model}_{ts}.json"
    backup_payload = {
        "created_at": datetime.now().isoformat(),
        "serial": serial,
        "info": info,
        "profile_matched": analysis.get("profile_matched"),
        "packages": target_pkgs,
    }
    backup_path.write_text(json.dumps(backup_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    disabled: list[str] = []
    failed: list[dict[str, str]] = []
    for pkg in target_pkgs:
        rc, out, err = _run_adb(
            ["-s", serial, "shell", "pm", "disable-user", "--user", "0", pkg],
            timeout=8.0,
        )
        if rc == 0 and ("disabled" in out.lower() or "new state" in out.lower() or not err):
            disabled.append(pkg)
        else:
            failed.append({"package": pkg, "error": err or out or f"rc={rc}"})

    return {
        "ok": True,
        "state": "cleaned",
        "serial": serial,
        "info": info,
        "backup_file": str(backup_path),
        "disabled": disabled,
        "failed": failed,
        "message": (
            f"Limpieza completada: {len(disabled)} paquetes desactivados de forma segura y reversible "
            f"({len(failed)} omitidos). Punto de restauración guardado en {backup_path.name}."
        ),
    }


def list_backups() -> list[dict[str, Any]]:
    if not BACKUPS_DIR.exists():
        return []
    out: list[dict[str, Any]] = []
    for f in sorted(BACKUPS_DIR.glob("*.json"), reverse=True):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            d["file"] = str(f)
            d["filename"] = f.name
            out.append(d)
        except Exception:
            pass
    return out


def restore_tv(ip: str, backup_file: str = "", packages: Optional[list[str]] = None) -> dict[str, Any]:
    """Restore previously disabled packages using `pm enable`."""
    conn = connect_tv(ip)
    if not conn.get("ok"):
        return conn
    serial = conn["serial"]

    target_pkgs: list[str] = []
    if packages:
        target_pkgs = [p.strip() for p in packages if p.strip()]
    else:
        backups = list_backups()
        chosen = None
        if backup_file:
            for b in backups:
                if b["filename"] == backup_file or b["file"] == backup_file:
                    chosen = b
                    break
        elif backups:
            chosen = backups[0]
        if chosen:
            target_pkgs = list(chosen.get("packages") or [])

    if not target_pkgs:
        return {"ok": False, "state": "no_backup", "message": "No hay paquetes o punto de restauración para revertir."}

    restored: list[str] = []
    failed: list[dict[str, str]] = []
    for pkg in target_pkgs:
        rc, out, err = _run_adb(["-s", serial, "shell", "pm", "enable", pkg], timeout=8.0)
        if rc == 0:
            restored.append(pkg)
        else:
            failed.append({"package": pkg, "error": err or out})

    return {
        "ok": True,
        "state": "restored",
        "serial": serial,
        "restored": restored,
        "failed": failed,
        "message": f"Restauración completada: {len(restored)} paquetes reactivados en el televisor.",
    }
