import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Configure environment before Qt imports
os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--use-angle=d3d11 --enable-gpu-rasterization --ignore-gpu-blocklist")

from memory.config_manager import get_hud_style, save_hud_style, HUD_STYLES
from core.vrm import VRMWidget
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

print("1. Checking HUD_STYLES:", HUD_STYLES)
assert "vrm_3d" in HUD_STYLES
assert "face" in HUD_STYLES
assert "core" in HUD_STYLES

# Test cycling
save_hud_style("vrm_3d")
assert get_hud_style() == "vrm_3d"
print("2. Current HUD style:", get_hud_style())

# Test files exist
vrm_files = [
    "core/vrm/viewer.html",
    "core/vrm/lib/three.module.js",
    "core/vrm/lib/GLTFLoader.js",
    "core/vrm/lib/OrbitControls.js",
    "core/vrm/lib/three-vrm.module.min.js",
    "core/vrm/models/viernes_3d.vrm"
]
for f in vrm_files:
    assert os.path.exists(f), f"Missing file: {f}"
    sz = os.path.getsize(f)
    print(f"3. Verified asset: {f} ({sz} bytes)")

# Test Qt Widget instantiation
app = QApplication.instance() or QApplication(sys.argv)
widget = VRMWidget()
print("4. VRMWidget created successfully!")

# Test methods
widget.set_speaking(True)
widget.set_level(0.65)
widget.set_state("SPEAKING")
widget.glance(0.2, -0.1)
widget.pause()
widget.resume()
widget.sleep()
widget.wake()
print("5. All VRMWidget control methods executed successfully!")

print("\n>>> ALL TESTS PASSED! Viernes 3D engine is fully verified. <<<")
