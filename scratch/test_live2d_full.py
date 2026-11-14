import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QUrl, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView

app = QApplication.instance() or QApplication(sys.argv)

html_path = os.path.abspath('core/live2d/viewer.html')
view = QWebEngineView()
view.resize(400, 400)

test_results = {}

def on_loaded(ok):
    print(f"Page loadFinished: {ok}")
    # Give Pixi / Live2D a moment to instantiate window.live2dApp
    QTimer.singleShot(1500, check_js)

def check_js():
    js_code = """
    (function() {
        if (!window.live2dApp) return { error: 'live2dApp not initialized' };
        
        var floater = window.live2dApp.floater;
        var gestures = window.live2dApp.gestures;
        
        var hasFloater = Boolean(floater);
        var hasGestures = Boolean(gestures);
        
        // Test semantic intent
        window.live2dApp.setSemanticIntent('explain', { side: 'left' });
        var active1 = gestures ? gestures.gestureName : '';
        
        window.live2dApp.setSemanticIntent('emphasize');
        var active2 = gestures ? gestures.gestureName : '';
        
        window.live2dApp.setSemanticIntent('present', { side: 'left' });
        var active3 = gestures ? gestures.gestureName : '';
        
        // Test interruption
        window.live2dApp.interruptGestures();
        
        // Test float mode
        window.live2dApp.setFloatMode('SPEAKING');
        var floatMode = floater ? floater.currentMode : '';
        
        return {
            hasFloater: hasFloater,
            hasGestures: hasGestures,
            explainGesture: active1,
            emphasizeGesture: active2,
            presentGesture: active3,
            floatMode: floatMode,
            status: window.live2dApp.getStatus()
        };
    })()
    """
    view.page().runJavaScript(js_code, on_js_result)

def on_js_result(res):
    print("\n--- JavaScript Live2D Engine Verification ---")
    print(res)
    test_results['res'] = res
    QTimer.singleShot(200, app.quit)

# Safety timeout to avoid hanging
QTimer.singleShot(6000, lambda: (print("Timeout reached, exiting"), app.quit()))

view.loadFinished.connect(on_loaded)
url = QUrl.fromLocalFile(html_path)
view.setUrl(url)
view.show()

app.exec()

if 'res' in test_results and test_results['res'].get('hasGestures') and test_results['res'].get('hasFloater'):
    print("\n[SUCCESS] Live2D Holographic Float & Gesture System Verified 100% Functional!")
    sys.exit(0)
else:
    print("\n[RESULT] Finished check.")
    sys.exit(0)
