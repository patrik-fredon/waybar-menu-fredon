import os
import sys
import logging
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsBlurEffect, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtGui import QFontDatabase, QFont
from typing import Optional
from configparser import ConfigParser
from ..widgets.custom_button import CustomButton
from ..commands.command_executor import CommandExecutor
from ..constants import WINDOW_WIDTH, WINDOW_HEIGHT, BUTTON_SPACING
from main import Config, Category, MenuButton  # Data classes remain in main.py for now

logger = logging.getLogger(__name__)


class MainWindow(QWidget):
    """Main application window with category/submenu support"""

    def __init__(self):
        super().__init__()
        self.config = None
        self._layout = None
        self.initUI()

    def initUI(self) -> None:
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.centerWindow()
        self._layout = QVBoxLayout()
        self._layout.setSpacing(BUTTON_SPACING)
        self._layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self._layout)
        # Load JetBrains Mono NL Thin font
        font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets", "fonts", "JetBrainsMonoNL-Thin.ttf")
        self.jetbrains_font_id = QFontDatabase.addApplicationFont(font_path)
        if self.jetbrains_font_id == -1:
            logger.warning(f"Could not load JetBrains Mono NL Thin font from {font_path}")
            self.jetbrains_font_family = None
        else:
            families = QFontDatabase.applicationFontFamilies(self.jetbrains_font_id)
            self.jetbrains_font_family = families[0] if families else None
        try:
            self.config = Config.load()
        except Exception as e:
            logger.error(f"Failed to initialize UI: {e}")
            sys.exit(1)
        self.showMainMenu()
        background = QWidget(self)
        background.setObjectName("blurBackground")

        background.setGeometry(self.rect())
        blur = QGraphicsBlurEffect(background)
        blur.setBlurRadius(20)
        background.setGraphicsEffect(blur)
        background.lower()

    def centerWindow(self) -> None:
        screen = QApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.geometry()
            x = screen_geometry.x() + (screen_geometry.width() - self.width()) // 2
            y = screen_geometry.y() + (screen_geometry.height() - self.height()) // 2
            self.move(x, y)

    def clearLayout(self):
        layout = self._layout
        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget() if item else None
            if widget:
                widget.deleteLater()

    def showMainMenu(self):
        self.clearLayout()
        layout = self._layout
        if layout is None or not self.config:
            return
        # Get the script's directory (ui/windows/)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up two levels to project root, then into assets/icons/
        project_root = os.path.dirname(os.path.dirname(script_dir))
        svg_path = os.path.join(project_root, "assets", "icons", "favicon.svg")

        svg_widget = QSvgWidget(svg_path)
        # Set width to match button width, height to keep aspect ratio (e.g. 64x64 or 72x72)
        button_width = 200  # Adjust as needed or import from constants
        svg_widget.setFixedWidth(button_width)
        svg_widget.setFixedHeight(160)
        svg_widget.setStyleSheet("background: transparent;")
        layout.addWidget(svg_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

        categories = self.config.categories or []
        buttons = self.config.buttons if self.config.buttons else []
        category_map = {cat.name: cat for cat in categories}
        categorized = {cat.name: [] for cat in categories}
        uncategorized = []
        for btn in buttons:
            if btn.category and btn.category in category_map:
                categorized[btn.category].append(btn)
            else:
                uncategorized.append(btn)
        for cat in categories:
            btn = CustomButton(cat.name, cat.icon)
            btn.setToolTip(cat.description or "")
            btn.clicked.connect(self._make_show_submenu_callback(cat.name))
            if layout is not None:
                layout.addWidget(btn)
        for btn_cfg in uncategorized:
            btn = CustomButton(btn_cfg.name, btn_cfg.icon)
            btn.setToolTip(btn_cfg.description or "")
            btn.clicked.connect(self._make_command_callback(btn_cfg.command))
            if layout is not None:
                layout.addWidget(btn)

        # Add spacing above the quote for separation
        layout.addSpacerItem(QSpacerItem(10, 18, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))

        # Add the quote label centered below all buttons
        quote = 'Et in tenebris codicem inveni lucem'  # - Fredon
        quote_label = QLabel(f"{quote}  – Fredon")
        quote_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # Set JetBrains Mono NL Thin font if available
        if hasattr(self, "jetbrains_font_family") and self.jetbrains_font_family:
            font = QFont(self.jetbrains_font_family, 16)
            font.setWeight(QFont.Weight.Thin)
            quote_label.setFont(font)
        else:
            # Fallback to monospace thin
            font = QFont("monospace", 16)
            font.setWeight(QFont.Weight.Thin)
            quote_label.setFont(font)
        quote_label.setStyleSheet("color: #888; margin-top: 8px;")
        layout.addWidget(quote_label, alignment=Qt.AlignmentFlag.AlignHCenter)

    def _make_show_submenu_callback(self, category_name):
        return lambda checked=False, c=category_name: self.showSubMenu(c)

    def _make_command_callback(self, command):
        return lambda checked=False, cmd=command: self.executeCommand(cmd)

    def executeCommand(self, command: str) -> None:
        try:
            CommandExecutor.execute(command)
        except Exception as e:
            logger.error(f"Failed to execute command '{command}': {e}")
        self.close()

    def showSubMenu(self, category_name: str):
        self.clearLayout()
        layout = self._layout
        if layout is None or not self.config:
            return
        back_btn = CustomButton(" Back", "")
        back_btn.clicked.connect(self.showMainMenu)
        if layout is not None:
            layout.addWidget(back_btn)
        cat = next(
            (c for c in (self.config.categories or []) if c.name == category_name), None
        )
        if not cat:
            self.showMainMenu()
            return
        for btn_cfg in [b for b in self.config.buttons if b.category == category_name]:
            btn = CustomButton(btn_cfg.name, btn_cfg.icon)
            btn.setToolTip(btn_cfg.description or "")
            btn.clicked.connect(self._make_command_callback(btn_cfg.command))
            if layout is not None:
                layout.addWidget(btn)

    def mousePressEvent(self, a0):
        if a0 and not self.rect().contains(a0.pos()):
            layout = self._layout
            if layout and layout.count() > 0:
                first_item = layout.itemAt(0)
                first_widget = first_item.widget() if first_item else None
                if (
                    isinstance(first_widget, CustomButton)
                    and first_widget.text() == " Back"
                ):
                    self.showMainMenu()
                    return
            self.close()
