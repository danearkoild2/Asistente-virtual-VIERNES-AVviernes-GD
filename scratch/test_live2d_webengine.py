import os, sys
from pathlib import Path
os.environ["QT_LOGGING_RULES"] = "qt.multimedia.*=false;qt.rhi.*=false;qt.webenginecontext.*=false"
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--use-angle=d3d11 --disable-gpu-rasterization --ignore-gpu-blocklist"

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl, QTimer

app = QApplication(sys.argv)
viewer_path = Path(__file__).resolve().parent.parent / "core" / "live2d" / "viewer.html"

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
        js = "window.live2dApp ? ('live2dApp READY: ' + (window.live2dApp.model ? 'model loaded' : 'loading')) : 'no live2dApp'"
        view.page().runJavaScript(js, lambda res: print("Result:", res, flush=True))
    QTimer.singleShot(1500, check_app)

view.loadFinished.connect(on_load_finished)
view.setUrl(QUrl.fromLocalFile(str(viewer_path)))
view.resize(800, 600)
view.show()

QTimer.singleShot(3500, lambda: os._exit(0))
app.exec()
