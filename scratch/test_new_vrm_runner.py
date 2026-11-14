import sys, os, time
os.environ["QT_QPA_PLATFORM"] = "offscreen"
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)

try:
    from core.vrm import VRMWidget
    w = VRMWidget()
    w.resize(800, 900)
    w.show()

    def on_check():
        js = """JSON.stringify({
            isLoaded: window.vrmApp?.isLoaded,
            hasVrm: !!window.vrmApp?.currentVrm,
            locomotion: window.vrmApp?.locomotionState,
            flight: window.vrmApp?.flightState,
            idle: window.vrmApp?.activeIdleBehavior,
            errors: window.ERRORS,
            initError: window.INIT_ERROR
        })"""
        w._view.page().runJavaScript(js, lambda r: print("VRM STATUS:", r))

    from PyQt6.QtCore import QTimer
    QTimer.singleShot(2500, on_check)
    QTimer.singleShot(6000, on_check)

    t0 = time.time()
    while time.time() - t0 < 8.0:
        app.processEvents()
        time.sleep(0.05)

    print("SUCCESSFUL TEST EXECUTION")
except Exception as e:
    import traceback
    traceback.print_exc()
