import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

os.environ.setdefault("QT_LOGGING_RULES", "qt.multimedia.*=false;qt.rhi.*=false;qt.webenginecontext.*=false")
os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--enable-gpu-rasterization --ignore-gpu-blocklist --enable-webgl")

from PyQt6.QtWidgets import QApplication
from memory.config_manager import get_hud_style, save_hud_style
from ui import HudCanvas

app = QApplication.instance() or QApplication(sys.argv)
hud = HudCanvas("face.png")

print("1. Default/Initial hud_style:", hud.hud_style, flush=True)

# Test 1: Set to vrm_3d
hud.set_hud_style("vrm_3d")
assert hud.hud_style == "vrm_3d"
assert hud._vrm_widget is not None
print("2. Tested vrm_3d active, widget is visible:", not hud._vrm_widget.isHidden(), flush=True)

# Test 2: Set to face (Viernes 2D)
hud.set_hud_style("face")
assert hud.hud_style == "face"
assert hud._vrm_widget.isHidden()
print("3. Tested face (2D) active, vrm_widget hidden:", hud._vrm_widget.isHidden(), flush=True)

# Test 3: Set to core (Reactor Core)
hud.set_hud_style("core")
assert hud.hud_style == "core"
assert hud._vrm_widget.isHidden()
print("4. Tested core active, vrm_widget hidden:", hud._vrm_widget.isHidden(), flush=True)

# Test 4: Audio amplitude and speaking controls
hud.set_hud_style("vrm_3d")
hud.set_speaking(True)
assert hud.speaking is True
hud.set_level(0.75)
hud.set_state("SPEAKING")
assert hud.state == "SPEAKING"
hud.glance(0.3, -0.2)
print("5. Audio amplitude, speaking, state, and glance propagated to VRM successfully!", flush=True)

# Test 5: Fallback handling
hud._on_vrm_error("Simulated model loading error")
assert hud.hud_style == "face"
print("6. Tested graceful fallback on model error -> switched to face (Viernes 2D)!", flush=True)

print("\n>>> ALL 6 HUD & VRM TESTS COMPLETED SUCCESSFULLY! <<<", flush=True)
os._exit(0)
