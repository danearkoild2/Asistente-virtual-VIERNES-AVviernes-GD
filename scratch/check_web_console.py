import sys, os, time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtCore import QUrl

app = QApplication(sys.argv)

class CustomPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, src):
        print(f"[CONSOLE {level}] {msg} ({src}:{line})")

view = QWebEngineView()
page = CustomPage(view)
settings = page.settings()
settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)

view.setPage(page)

def on_finished(ok):
    print(f"Page load finished: ok={ok}")
    def cb(res):
        print("RESULT:", res)
    js = """
    window.TEST_RES = 'pending';
    import('./lib/three.module.js')
      .then(m => { window.TEST_RES = 'THREE SUCCESS: ' + Object.keys(m).length; })
      .catch(err => { window.TEST_RES = 'THREE FAIL: ' + err.message + ' | ' + err.stack; });
    """
    page.runJavaScript(js)

    from PyQt6.QtCore import QTimer
    def check_res():
        page.runJavaScript("window.TEST_RES", print)
    QTimer.singleShot(1500, check_res)

view.loadFinished.connect(on_finished)

html_path = os.path.abspath("core/vrm/viewer.html")
url = QUrl.fromLocalFile(html_path)
url.setQuery("model=./models/edithof.vrm")
view.setUrl(url)
view.show()

t0 = time.time()
while time.time() - t0 < 6.0:
    app.processEvents()
    time.sleep(0.05)
