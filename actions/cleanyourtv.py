from __future__ import annotations

from typing import Any


def clean_your_tv_action(parameters: dict[str, Any] = None, player=None, **_) -> str:
    """Native Clean Your TV workflow: discover, connect, analyse, safely clean, and restore Android TVs."""
    params = parameters or {}
    action = str(params.get("action") or "start").strip().lower()
    ip = str(params.get("ip") or "").strip()
    backup_file = str(params.get("backup_file") or "").strip()
    packages_raw = params.get("packages")
    packages = (
        [str(p).strip() for p in packages_raw if str(p).strip()]
        if isinstance(packages_raw, list)
        else None
    )

    from core.cleanyourtv import (
        analyze_tv,
        clean_tv,
        connect_tv,
        discover_android_tvs,
        get_remote_instructions,
        list_backups,
        restore_tv,
    )

    if action == "guide":
        stage = str(params.get("stage") or "enable_adb").strip().lower()
        return get_remote_instructions(stage)

    if action in ("open_ui", "start"):
        if player is not None and hasattr(player, "open_cleanyourtv"):
            player.open_cleanyourtv(ip)
        if not ip:
            devs = discover_android_tvs()
            if not devs:
                return (
                    "Abrí el asistente visual de Clean Your TV en pantalla. "
                    "No detecté televisores con depuración de red activa aún.\n\n"
                    + get_remote_instructions("enable_adb")
                )
            lines = [f"- {d.get('model', 'Android TV')} ({d.get('ip')}) [{d.get('state')}]" for d in devs]
            return (
                "Abrí el asistente visual de Clean Your TV y detecté estos dispositivos en tu Wi-Fi:\n"
                + "\n".join(lines)
                + "\nDime la IP o a cuál quieres conectar para analizarlo paso a paso."
            )
        # If IP was given with start, connect & analyze right away
        action = "analyze"

    if action == "discover":
        devs = discover_android_tvs()
        if not devs:
            return (
                "No se encontraron Android TVs con el puerto ADB (5555) abierto en la red local.\n\n"
                + get_remote_instructions("enable_adb")
            )
        lines = [f"- {d.get('model', 'Android TV')} · IP: {d.get('ip')} · Estado: {d.get('state')}" for d in devs]
        return "Android TVs encontrados en tu red:\n" + "\n".join(lines)

    if action == "backups":
        bks = list_backups()
        if not bks:
            return "No hay puntos de restauración guardados todavía."
        lines = [
            f"- {b.get('filename')} | {b.get('info', {}).get('model', 'TV')} | {len(b.get('packages', []))} paquetes"
            for b in bks[:10]
        ]
        return "Puntos de restauración disponibles:\n" + "\n".join(lines)

    if not ip:
        devs = discover_android_tvs()
        if len(devs) == 1:
            ip = devs[0]["ip"]
        elif len(devs) > 1:
            lines = [f"- {d.get('model', 'Android TV')} ({d.get('ip')})" for d in devs]
            return "Encontré varios televisores. Dime cuál IP usar:\n" + "\n".join(lines)
        else:
            return (
                "Necesito la dirección IP de tu televisor (y que la depuración de red esté activada).\n\n"
                + get_remote_instructions("enable_adb")
            )

    if action == "connect":
        res = connect_tv(ip)
        return str(res.get("message") or "")

    if action == "analyze":
        res = analyze_tv(ip)
        if not res.get("ok"):
            return str(res.get("message") or "No se pudo analizar el televisor.")
        cands = res.get("candidates") or []
        summary = "\n".join(
            f"- [{c['category']}] {c['package']} ({c['description']})"
            for c in cands[:25]
        )
        extra = f"\n...y {len(cands) - 25} más." if len(cands) > 25 else ""
        return (
            f"{res['message']}\n\nPlan propuesto (nada modificado aún):\n{summary}{extra}\n\n"
            "Confírmame si quieres ejecutar la limpieza segura ahora."
        )

    if action == "clean":
        res = clean_tv(ip, packages=packages)
        return str(res.get("message") or "")

    if action == "restore":
        res = restore_tv(ip, backup_file=backup_file, packages=packages)
        return str(res.get("message") or "")

    return f"Acción '{action}' no reconocida para Clean Your TV."


TOOL = {
    "name": "clean_your_tv",
    "description": (
        "Asistente nativo 'Clean Your TV' (basado en udhaykumarbala/cleanyourtv-app y Gathin23/cleanyourtv) "
        "para limpiar anuncios, telemetría y bloatware en Android TV / Google TV vía ADB Wi-Fi de forma "
        "segura y 100% reversible (crea punto de restauración antes de desactivar paquetes). "
        "Úsalo siempre que el usuario diga que quiere hacerle un clean al TV, limpiar su televisor, "
        "quitarle anuncios/bloatware al TV, o restaurar apps desactivadas. Guía paso a paso con el control remoto."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "action": {
                "type": "STRING",
                "description": (
                    "Paso o acción: 'start' (abre el asistente visual y escanea la red), "
                    "'discover' (buscar Android TVs en Wi-Fi), 'guide' (instrucciones para el control remoto), "
                    "'connect' (conectar por ADB Wi-Fi), 'analyze' (Paso 2: leer paquetes y mostrar plan sin tocar nada), "
                    "'clean' (Paso 3: crear backup y desactivar bloatware), 'restore' (revertir cambios), "
                    "'backups' (listar puntos de restauración), 'open_ui'."
                ),
                "enum": ["start", "open_ui", "discover", "guide", "connect", "analyze", "clean", "restore", "backups"],
            },
            "ip": {
                "type": "STRING",
                "description": "IP local del Android TV (ej. '192.168.1.45'). Si se omite, intenta autodetectar.",
            },
            "stage": {
                "type": "STRING",
                "description": "Para action='guide': 'enable_adb' o 'authorize'.",
            },
            "packages": {
                "type": "ARRAY",
                "items": {"type": "STRING"},
                "description": "Lista opcional de paquetes específicos a limpiar o restaurar.",
            },
            "backup_file": {
                "type": "STRING",
                "description": "Nombre del archivo de punto de restauración para action='restore'.",
            },
        },
        "required": ["action"],
    },
    "handler": clean_your_tv_action,
}
