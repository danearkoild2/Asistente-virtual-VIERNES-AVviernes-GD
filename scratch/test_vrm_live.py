"""
Verification script for Edith 3D VRM Engine.
Instantiates QApplication, VRMWidget, tests all method calls and signals.
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    print("[1] Verificando importaciones de VRM...")
    from core.vrm import VRMWidget
    from memory.config_manager import get_hud_style, save_hud_style, HUD_STYLES

    print(f"    HUD_STYLES disponibles: {HUD_STYLES}")
    print(f"    Estilo HUD actual: {get_hud_style()}")
    assert "vrm_3d" in HUD_STYLES, "vrm_3d debe estar en HUD_STYLES"

    print("[2] Inicializando QApplication en modo headless/offscreen...")
    os.environ["QT_QPA_PLATFORM"] = "offscreen"
    from PyQt6.QtWidgets import QApplication

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    print("[3] Creando instancia de VRMWidget...")
    w = VRMWidget()
    w.resize(800, 900)
    w.show()

    print("[4] Probando APIs y controladores...")
    w.set_state("LISTENING")
    w.set_speaking(True)
    w.set_level(0.75)
    w.glance(0.2, -0.1, 2.0)
    w.set_emotion("happy", 0.9, 3.0)
    w.trigger_gesture("WAVE_HELLO", 3.0)
    w.set_camera_preset("upper")
    w.set_semantic_intent("explain", {"topic": "3D engine"})
    w.set_autonomy_enabled(True)
    w.set_spontaneity_level(1.2)
    w.set_presentation_mode(True)
    w.set_presentation_mode(False)
    w.sleep()
    w.wake()

    print("[5] Procesando eventos de Qt por 1 segundo...")
    start = time.time()
    while time.time() - start < 1.0:
        app.processEvents()
        time.sleep(0.05)

    print("[6] Limpieza de recursos...")
    w.pause()
    w.close()
    print(">>> TODAS LAS PRUEBAS DE EDITH 3D VRM ENGINE FUERON EXITOSAS <<<")

if __name__ == "__main__":
    main()
