from __future__ import annotations

from PyQt6.QtCore import Qt, QUrl, pyqtSignal
from PyQt6.QtGui import QDesktopServices, QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

PAYPAL_CLIENT_ID = (
    "BAA3UkXdPH1d3xlBRLUDdl9mq0k1cmlMXROTWA4C25WlTYykNP0_j31RuQHN8HXD-TtWURZlPqfCIoarEg"
)
PAYPAL_HOSTED_BUTTON_ID = "NE56HM9KTAQRQ"

PAYPAL_HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #0B0D12;
      color: #F1F5F9;
      font-family: 'Segoe UI', system-ui, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 20px;
    }}
    .card {{
      width: 100%;
      max-width: 390px;
      background: #121620;
      border: 1px solid #242B3D;
      border-radius: 14px;
      padding: 20px;
      text-align: center;
      box-shadow: 0 18px 40px rgba(0,0,0,0.45);
    }}
    h3 {{ font-size: 15px; margin-bottom: 6px; color: #FFFFFF; }}
    p {{ font-size: 12px; color: #94A3B8; margin-bottom: 16px; line-height: 1.45; }}
    #paypal-container-{PAYPAL_HOSTED_BUTTON_ID} {{
      min-height: 90px;
    }}
  </style>
  <script
    src="https://www.paypal.com/sdk/js?client-id={PAYPAL_CLIENT_ID}&components=hosted-buttons&disable-funding=venmo&currency=USD">
  </script>
</head>
<body>
  <div class="card">
    <h3>Apoya el desarrollo de Viernes</h3>
    <p>Proyecto gratuito y open-source creado por <strong>Groovi Developer</strong>. Tu aporte impulsa nuevas funciones e integraciones.</p>
    <div id="paypal-container-{PAYPAL_HOSTED_BUTTON_ID}"></div>
  </div>
  <script>
    if (window.paypal && paypal.HostedButtons) {{
      paypal.HostedButtons({{
        hostedButtonId: "{PAYPAL_HOSTED_BUTTON_ID}",
      }}).render("#paypal-container-{PAYPAL_HOSTED_BUTTON_ID}");
    }}
  </script>
</body>
</html>
"""


class DonationOverlay(QWidget):
    """Floating modal rendering the official PayPal Hosted Button for Viernes."""

    closed = pyqtSignal()
    _OW, _OH = 460, 420

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(
            "DonationOverlay { background: #121620; border: 1px solid #36415C; border-radius: 14px; }"
        )
        self._web = None
        self._build_ui()

    def _build_ui(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(10)

        hdr = QHBoxLayout()
        lbl = QLabel("Apoyar a Viernes · Groovi Developer")
        lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lbl.setStyleSheet("color: #FFFFFF; background: transparent;")
        hdr.addWidget(lbl)
        hdr.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(26, 26)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(
            "QPushButton { background: transparent; color: #94A3B8; border: 1px solid #242B3D; border-radius: 6px; }"
            "QPushButton:hover { color: #FFFFFF; border-color: #36415C; }"
        )
        close_btn.clicked.connect(self._close)
        hdr.addWidget(close_btn)
        lay.addLayout(hdr)

        try:
            from PyQt6.QtWebEngineWidgets import QWebEngineView
            self._web = QWebEngineView(self)
            self._web.setHtml(PAYPAL_HTML, QUrl("https://www.paypal.com/"))
            lay.addWidget(self._web, stretch=1)
        except Exception:
            fallback = QLabel(
                "Haz clic abajo para abrir la pasarela oficial de PayPal en tu navegador."
            )
            fallback.setWordWrap(True)
            fallback.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback.setStyleSheet("color: #94A3B8; background: #0B0D12; border-radius: 10px; padding: 20px;")
            lay.addWidget(fallback, stretch=1)

        foot = QHBoxLayout()
        ext_btn = QPushButton("Abrir PayPal en navegador")
        ext_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ext_btn.setFixedHeight(30)
        ext_btn.setStyleSheet(
            "QPushButton { background: #191F2E; color: #FBBF24; border: 1px solid rgba(251,191,36,0.35); border-radius: 7px; padding: 0 12px; font-weight: 600; }"
            "QPushButton:hover { background: rgba(251,191,36,0.12); }"
        )
        ext_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl(f"https://www.paypal.com/ncp/payment/{PAYPAL_HOSTED_BUTTON_ID}")
            )
        )
        foot.addWidget(ext_btn)
        foot.addStretch()
        lay.addLayout(foot)

    def _close(self) -> None:
        if self._web is not None:
            try:
                self._web.setHtml("")
                self._web.deleteLater()
            except Exception:
                pass
            self._web = None
        self.hide()
        self.closed.emit()
