#!/usr/bin/env python3
"""
Modern Hyprland Menu Overlay Application
A visually stunning, Wayland-native menu overlay for Hyprland
"""

import json
import logging
import sys
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses_json import dataclass_json  # type: ignore

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QMouseEvent

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


DEFAULT_CONFIG_PATH = Path.home() / ".config" / "hypr" / "menu-config.json"
LOCAL_CONFIG_PATH = Path(__file__).parent / "config" / "menu-config.json"


@dataclass_json
@dataclass
class MenuButton:
    """Data class for menu button configuration"""

    name: str
    icon: str
    command: str
    description: Optional[str] = None
    category: Optional[str] = None


@dataclass_json
@dataclass
class Category:
    """Data class for menu category configuration"""

    name: str
    icon: str
    description: Optional[str] = None


@dataclass_json
@dataclass
class Config:
    """Data class for application configuration"""

    buttons: List[MenuButton]
    theme: Dict[str, Any]
    categories: Optional[List[Category]] = None

    @classmethod
    def load(cls) -> "Config":
        """Load configuration from JSON file"""
        try:
            if DEFAULT_CONFIG_PATH.exists():
                logger.info(f"Loading config from {DEFAULT_CONFIG_PATH}")
                config_data = json.loads(DEFAULT_CONFIG_PATH.read_text())
            elif LOCAL_CONFIG_PATH.exists():
                logger.info(f"Loading config from {LOCAL_CONFIG_PATH}")
                config_data = json.loads(LOCAL_CONFIG_PATH.read_text())
            else:
                raise FileNotFoundError(
                    f"Configuration file not found at {DEFAULT_CONFIG_PATH} "
                    f"or {LOCAL_CONFIG_PATH}"
                )

            # Parse categories if present
            categories = None
            if "categories" in config_data:
                categories = [Category(**cat) for cat in config_data["categories"]]
            # Parse buttons
            buttons = [MenuButton(**btn) for btn in config_data["buttons"]]
            theme = config_data.get("theme", {})
            return cls(buttons=buttons, theme=theme, categories=categories)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise


def main() -> None:
    """Main application entry point"""
    try:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")  # Use Fusion style for better Wayland compatibility

        # Set application-wide style
        app.setStyleSheet(
            """
            QWidget {
                font-family: 'Noto Sans', sans-serif;
            }
        """
        )

        from ui.windows.main_window import MainWindow

        window = MainWindow()
        window.show()

        sys.exit(app.exec())

    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
