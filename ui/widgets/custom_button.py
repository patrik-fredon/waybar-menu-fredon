from PyQt6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor, QIcon
from typing import Optional
from PyQt6.QtWidgets import QWidget

BUTTON_HEIGHT = 50


class CustomButton(QPushButton):
    """Custom styled button for the menu"""

    def __init__(self, text: str, icon_path: str, parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setFixedHeight(BUTTON_HEIGHT)
        if icon_path:
            self.setIcon(QIcon(icon_path))
        self.setStyleSheet(
            """
			QPushButton {
				background-color: rgba(0, 3, 0, 0.6);
				color: white;
				border: 1px solid rgba(150, 150, 150, 0.5);
				border-radius: 10px;
				text-align: center;
				font-size: 16px;
                font-family: JetBrains Mono NL ExtraBold;
			}
			QPushButton:hover {
				background-color: rgba(0, 4, 2, 0.4);
                color: rgba(250, 0, 10, 0.5);
                border: 1px solid rgba(250, 0, 10, 0.3);
			}
			QPushButton:pressed {
                color: rgba(250, 0, 10, 0.5);
                border: 1px solid rgba(250, 0, 10, 0.3);
			}
			"""
        )
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(2, 4)
        self.setGraphicsEffect(shadow)
