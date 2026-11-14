import os
import sys

# Test RHI and Chromium flags
backend = sys.argv[1] if len(sys.argv) > 1 else "default"
if backend != "default":
    os.environ["QT_RHI_BACKEND"] = backend

os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-gpu-rasterization --ignore-gpu-blocklist"

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView

app = QApplication([])
w = QWebEngineView()
print(f"Backend [{backend}] initialized cleanly!", flush=True)
os._exit(0)
