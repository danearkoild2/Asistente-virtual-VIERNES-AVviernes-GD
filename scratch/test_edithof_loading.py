import sys, os, time, threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl, QTimer

class CORSHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    def log_message(self, format, *args):
        pass

vrm_dir = os.path.abspath("core/vrm")
server = ThreadingHTTPServer(("127.0.0.1", 0), lambda *a, **k: CORSHandler(*a, directory=vrm_dir, **k))
port = server.server_address[1]
threading.Thread(target=server.serve_forever, daemon=True).start()
print(f"Local server on http://127.0.0.1:{port}/")

app = QApplication(sys.argv)
view = QWebEngineView()
settings = view.page().settings()
settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)

url = QUrl(f"http://127.0.0.1:{port}/viewer.html?model=./models/edithof.vrm")
view.setUrl(url)

def on_finished(ok):
    print(f"Page loaded: {ok}")

view.loadFinished.connect(on_finished)
view.show()

t0 = time.time()
while time.time() - t0 < 15.0:
    app.processEvents()
    time.sleep(0.1)
    if int(time.time() - t0) % 2 == 0:
        view.page().runJavaScript(
            "JSON.stringify({ isLoaded: window.vrmApp?.isLoaded, hasVrm: !!window.vrmApp?.currentVrm, errors: window.ERRORS, text: document.getElementById('loading-text')?.innerText })",
            lambda res: print("STATUS:", res)
        )

server.shutdown()
