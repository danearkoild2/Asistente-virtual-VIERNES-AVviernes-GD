import os
import sys

flags = sys.argv[1] if len(sys.argv) > 1 else ""
if flags:
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = flags

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, QTimer

app = QApplication.instance() or QApplication(sys.argv)
view = QWebEngineView()
html = """
<!DOCTYPE html>
<html>
<head><title>Test</title></head>
<body>
<canvas id="c"></canvas>
<script>
const c = document.getElementById('c');
const gl = c.getContext('webgl');
console.log('WebGL supported:', !!gl);
</script>
</body>
</html>
"""
view.setHtml(html)
view.show()
QTimer.singleShot(1000, app.quit)
app.exec()
print("FLAGS:", flags, "FINISHED OK", flush=True)
os._exit(0)
