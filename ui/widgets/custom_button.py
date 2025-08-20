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
				background-color: rgba(0, 3, 0, 0.5);
				color: white;
				border: none;
				border-radius: 10px;
				padding: 5px;
				text-align: center;
				font-size: 14px;
			}
			QPushButton:hover {
				background-color: rgba(0, 0, 20, 0.6);
			}
			QPushButton:pressed {
				background-color: rgba(80, 84, 92, 0.9);
			}
			"""
        )
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
