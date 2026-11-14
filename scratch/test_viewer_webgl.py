import os
import sys
from pathlib import Path

os.environ["QT_LOGGING_RULES"] = "qt.multimedia.*=false;qt.rhi.*=false;qt.webenginecontext.*=false"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--use-angle=d3d11 --disable-gpu-rasterization --ignore-gpu-blocklist"

# Try different flags or no flags
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl, QTimer

app = QApplication.instance() or QApplication(sys.argv)
viewer_path = Path(__file__).resolve().parent.parent / "core" / "live2d" / "test_min.html"

class CustomPage(QWebEngineView().page().__class__):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"[JS {level}] {sourceID}:{lineNumber} -> {message}", flush=True)

view = QWebEngineView()
page = CustomPage(view)
view.setPage(page)

settings = view.settings()
settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)

def on_load_finished(ok):
    print("Page load finished:", ok, flush=True)
    def check_app():
        view.page().runJavaScript("window.vrmApp ? 'vrmApp READY: ' + (window.vrmApp.vrm ? 'model loaded' : 'loading') : 'no vrmApp'", lambda res: print("Result:", res, flush=True))
    QTimer.singleShot(1000, check_app)

view.loadFinished.connect(on_load_finished)
view.setUrl(QUrl.fromLocalFile(str(viewer_path)))
view.show()

QTimer.singleShot(2500, lambda: os._exit(0))
app.exec()
