import sys, os, time, threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QTimer

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

vrm_dir = os.path.abspath("core/vrm")
server = ThreadingHTTPServer(("127.0.0.1", 0), lambda *a, **k: QuietHandler(*a, directory=vrm_dir, **k))
port = server.server_address[1]
threading.Thread(target=server.serve_forever, daemon=True).start()
print(f"Local server on http://127.0.0.1:{port}/")

app = QApplication(sys.argv)
view = QWebEngineView()
url = QUrl(f"http://127.0.0.1:{port}/viewer.html?model=./models/edithof.vrm")
view.setUrl(url)

def on_finished(ok):
    print(f"Page loaded: {ok}")
    def check():
        def cb1(res): print("vrmApp:", res)
        def cb2(err): print("INIT_ERROR:", err)
        def cb3(errs): print("window.ERRORS:", errs)
        def cb4(txt): print("loading-text:", txt)
        view.page().runJavaScript("window.vrmApp ? ('LOADED! isLoaded=' + window.vrmApp.isLoaded + ', vrm=' + !!window.vrmApp.currentVrm) : 'NULL'", cb1)
        view.page().runJavaScript("window.INIT_ERROR || 'NONE'", cb2)
        view.page().runJavaScript("window.ERRORS", cb3)
        view.page().runJavaScript("document.getElementById('loading-text').innerText", cb4)
    QTimer.singleShot(2500, check)

view.loadFinished.connect(on_finished)
view.show()

t0 = time.time()
while time.time() - t0 < 6.0:
    app.processEvents()
    time.sleep(0.05)

server.shutdown()
