#!/usr/bin/env python3
"""Script Runner Dashboard - Main entry point."""

import sys
from PyQt6.QtWidgets import QApplication

from dashboard import ScriptRunnerDashboard


def main():
    """Initialize and run the Script Runner Dashboard application."""
    app = QApplication(sys.argv)
    window = ScriptRunnerDashboard()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
