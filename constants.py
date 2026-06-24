"""Application constants and configuration."""

# Window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
WINDOW_TITLE = "Script Runner Dashboard"

# Colors - Dark Theme
COLOR_BACKGROUND = "#1e1e1e"
COLOR_SURFACE = "#2b2b2b"
COLOR_SURFACE_LIGHT = "#333333"
COLOR_SURFACE_DARKER = "#1a1a1a"

COLOR_TEXT_PRIMARY = "#ffffff"
COLOR_TEXT_SECONDARY = "#cccccc"
COLOR_TEXT_MUTED = "#aaaaaa"
COLOR_TEXT_DIM = "#888888"

# Status Colors
COLOR_STATUS_PENDING = "#888888"
COLOR_STATUS_RUNNING = "#0099ff"
COLOR_STATUS_SUCCESS = "#00cc66"
COLOR_STATUS_FAILED = "#ff4444"

# Button Colors
COLOR_BUTTON_PRIMARY = "#0066cc"
COLOR_BUTTON_PRIMARY_HOVER = "#0052a3"
COLOR_BUTTON_PRIMARY_PRESS = "#003d7a"

COLOR_BUTTON_SUCCESS = "#00aa44"
COLOR_BUTTON_SUCCESS_HOVER = "#009933"
COLOR_BUTTON_SUCCESS_PRESS = "#007722"

COLOR_BUTTON_WARNING = "#aa6600"
COLOR_BUTTON_WARNING_HOVER = "#995500"
COLOR_BUTTON_WARNING_PRESS = "#774400"

COLOR_BUTTON_SECONDARY = "#333333"
COLOR_BUTTON_SECONDARY_HOVER = "#444444"

COLOR_PROGRESS_BAR = "#0099ff"
COLOR_PROGRESS_BACKGROUND = "#2b2b2b"
COLOR_PROGRESS_BORDER = "#444444"

# Fonts
FONT_FAMILY_MONOSPACE = "Monaco"
FONT_SIZE_TITLE = 18
FONT_SIZE_LABEL = 11
FONT_SIZE_BUTTON = 10
FONT_SIZE_SCRIPT_NAME = 10
FONT_SIZE_SCRIPT_DESC = 9
FONT_SIZE_CONSOLE = 9
FONT_SIZE_STATUS_DOT = 14

# Spacing
PADDING_MAIN = 16
PADDING_ROW = 12
PADDING_HEADER = 8
PADDING_BUTTON = 8
MARGIN_ROW = 8

SPACING_HEADER = 16
SPACING_ROW = 12
SPACING_SECTION = 8

# Size
MIN_ROW_HEIGHT = 70
BUTTON_WIDTH_RUN = 70
BUTTON_WIDTH_ACTION = 100
TIME_LABEL_WIDTH = 40
STATUS_DOT_WIDTH = 30
CLEAR_BUTTON_WIDTH = 50
BORDER_RADIUS = 4
BORDER_RADIUS_LARGE = 6

# Script Configuration
SCRIPT_NAMES = [
    "load_data.py",
    "validate_input.py",
    "run_simulation.py",
    "process_results.py",
    "export_results.py",
]

SCRIPT_DESCRIPTIONS = {
    "load_data.py": "Load grid topology data",
    "validate_input.py": "Validate converter parameters",
    "run_simulation.py": "Run load flow simulation",
    "process_results.py": "Post-process results",
    "export_results.py": "Export simulation results",
}

TOTAL_SCRIPTS = len(SCRIPT_NAMES)

# Timers
PROGRESS_UPDATE_INTERVAL = 100  # milliseconds
ELAPSED_TIME_UPDATE_INTERVAL = 100  # milliseconds

# Console Header
CONSOLE_HEADER_RUNNING = "▶ {}"
CONSOLE_HEADER_READY = "Ready to run scripts"
CONSOLE_HEADER_SEPARATOR = "─" * 60

# Messages
MESSAGE_SCRIPT_STARTED = "\n{}\nRunning: {}\n{}\n"
MESSAGE_SCRIPT_SUCCESS = "\n✓ {} completed successfully\n"
MESSAGE_SCRIPT_FAILED = "\n✗ {} failed with exit code {}\n"
MESSAGE_RUN_ALL_STOPPED = "\n⚠ Run All sequence stopped due to failure\n"
MESSAGE_SCRIPT_NOT_FOUND = "Script not found: {}"
MESSAGE_SCRIPT_EXECUTION_ERROR = "Failed to execute script: {}"
