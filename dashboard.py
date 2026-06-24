"""Main dashboard window for Script Runner."""

from typing import Dict, List, Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QFrame, QScrollArea, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, QTime
from PyQt6.QtGui import QFont, QColor, QTextCursor

from models import ScriptState, ScriptStatus
from widgets import ScriptRow, ScriptListContainer
from runner import ScriptRunnerThread
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    COLOR_BACKGROUND,
    COLOR_SURFACE,
    COLOR_SURFACE_DARKER,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    COLOR_TEXT_DIM,
    COLOR_BUTTON_SUCCESS,
    COLOR_BUTTON_SUCCESS_HOVER,
    COLOR_BUTTON_SUCCESS_PRESS,
    COLOR_BUTTON_WARNING,
    COLOR_BUTTON_WARNING_HOVER,
    COLOR_BUTTON_WARNING_PRESS,
    COLOR_BUTTON_SECONDARY,
    COLOR_BUTTON_SECONDARY_HOVER,
    COLOR_PROGRESS_BAR,
    COLOR_PROGRESS_BACKGROUND,
    COLOR_PROGRESS_BORDER,
    COLOR_STATUS_FAILED,
    COLOR_STATUS_SUCCESS,
    FONT_FAMILY_MONOSPACE,
    FONT_SIZE_TITLE,
    FONT_SIZE_LABEL,
    FONT_SIZE_BUTTON,
    FONT_SIZE_CONSOLE,
    PADDING_MAIN,
    PADDING_HEADER,
    SPACING_HEADER,
    SPACING_SECTION,
    BUTTON_WIDTH_ACTION,
    CLEAR_BUTTON_WIDTH,
    TOTAL_SCRIPTS,
    SCRIPT_NAMES,
    SCRIPT_DESCRIPTIONS,
    PROGRESS_UPDATE_INTERVAL,
    CONSOLE_HEADER_RUNNING,
    CONSOLE_HEADER_READY,
    CONSOLE_HEADER_SEPARATOR,
    MESSAGE_SCRIPT_STARTED,
    MESSAGE_SCRIPT_SUCCESS,
    MESSAGE_SCRIPT_FAILED,
    MESSAGE_RUN_ALL_STOPPED,
)


class ScriptRunnerDashboard(QMainWindow):
    """Main application window for the Script Runner Dashboard."""

    def __init__(self):
        """Initialize the dashboard with script states and UI."""
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Initialize script states
        self.scripts: Dict[str, ScriptState] = {
            script_name: ScriptState(script_name, SCRIPT_DESCRIPTIONS[script_name])
            for script_name in SCRIPT_NAMES
        }

        self.script_rows: Dict[str, ScriptRow] = {}
        self.running_scripts: List[str] = list(self.scripts.keys())
        self.current_script: Optional[str] = None
        self.is_running_all = False
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_progress)

        self.run_all_button: Optional[QPushButton] = None
        self.progress_bar: Optional[QProgressBar] = None
        self.progress_text: Optional[QLabel] = None
        self.console: Optional[QTextEdit] = None
        self.console_header: Optional[QLabel] = None
        self.script_list_container: Optional[ScriptListContainer] = None

        self.setup_ui()
        self.apply_dark_theme()

    def setup_ui(self) -> None:
        """Build the complete UI layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(PADDING_MAIN, PADDING_MAIN, PADDING_MAIN, PADDING_MAIN)
        main_layout.setSpacing(SPACING_HEADER)

        # Header
        main_layout.addLayout(self._create_header_layout())

        # Script list
        main_layout.addWidget(QLabel("Scripts"))
        main_layout.addWidget(self._create_script_list(), 2)

        # Progress bar
        main_layout.addLayout(self._create_progress_layout())

        # Console
        main_layout.addWidget(QLabel("Output"))
        main_layout.addWidget(self._create_console_panel(), 1)

        central_widget.setLayout(main_layout)

    def _create_header_layout(self) -> QHBoxLayout:
        """Create the header layout with title and action buttons."""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING_HEADER)

        title_label = QLabel(WINDOW_TITLE)
        title_label.setFont(QFont(FONT_FAMILY_MONOSPACE, FONT_SIZE_TITLE, QFont.Weight.Bold))
        title_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY};")
        layout.addWidget(title_label, 1)

        self.run_all_button = self._create_action_button(
            "Run All",
            COLOR_BUTTON_SUCCESS,
            COLOR_BUTTON_SUCCESS_HOVER,
            COLOR_BUTTON_SUCCESS_PRESS,
            self.run_all_scripts
        )
        layout.addWidget(self.run_all_button, 0)

        reset_button = self._create_action_button(
            "Reset",
            COLOR_BUTTON_WARNING,
            COLOR_BUTTON_WARNING_HOVER,
            COLOR_BUTTON_WARNING_PRESS,
            self.reset_all
        )
        layout.addWidget(reset_button, 0)

        return layout

    def _create_action_button(
        self,
        text: str,
        bg_color: str,
        hover_color: str,
        press_color: str,
        callback
    ) -> QPushButton:
        """Create a styled action button."""
        button = QPushButton(text)
        button.setFont(QFont(FONT_FAMILY_MONOSPACE, FONT_SIZE_BUTTON, QFont.Weight.Bold))
        button.setMinimumWidth(BUTTON_WIDTH_ACTION)
        button.clicked.connect(callback)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                color: {COLOR_TEXT_PRIMARY};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 10pt;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {press_color};
            }}
        """)
        return button

    def _create_script_list(self) -> QScrollArea:
        """Create the scrollable script list widget with drag-and-drop reordering."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {COLOR_BACKGROUND};
                border: none;
            }}
            QScrollBar:vertical {{
                background-color: {COLOR_SURFACE};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background-color: #555555;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #666666;
            }}
        """)

        # Create the script list container with drag-and-drop support
        self.script_list_container = ScriptListContainer()
        self.script_list_container.order_changed.connect(self.on_script_order_changed)

        for script_name, script_state in self.scripts.items():
            row = ScriptRow(script_state)
            row.run_clicked.connect(self.run_single_script)
            self.script_rows[script_name] = row
            self.script_list_container.add_script_row(script_name, row)

        scroll_area.setWidget(self.script_list_container)

        return scroll_area

    def _create_progress_layout(self) -> QHBoxLayout:
        """Create the progress bar layout."""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        progress_label = QLabel("Overall Progress:")
        progress_label.setFont(QFont(FONT_FAMILY_MONOSPACE, FONT_SIZE_BUTTON))
        progress_label.setStyleSheet(f"color: {COLOR_TEXT_DIM};")
        layout.addWidget(progress_label, 0)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(TOTAL_SCRIPTS)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {COLOR_PROGRESS_BACKGROUND};
                border: 1px solid {COLOR_PROGRESS_BORDER};
                border-radius: 4px;
                height: 20px;
            }}
            QProgressBar::chunk {{
                background-color: {COLOR_PROGRESS_BAR};
                border-radius: 3px;
            }}
        """)
        layout.addWidget(self.progress_bar, 1)

        self.progress_text = QLabel("0/5")
        self.progress_text.setFont(QFont(FONT_FAMILY_MONOSPACE, FONT_SIZE_BUTTON))
        self.progress_text.setStyleSheet(f"color: {COLOR_TEXT_DIM};")
        self.progress_text.setMinimumWidth(40)
        layout.addWidget(self.progress_text, 0)

        return layout

    def _create_console_panel(self) -> QFrame:
        """Create the console output panel."""
        console_frame = QFrame()
        console_frame.setStyleSheet(f"background-color: {COLOR_SURFACE_DARKER}; border-radius: 4px;")
        console_layout = QVBoxLayout()
        console_layout.setContentsMargins(0, 0, 0, 0)
        console_layout.setSpacing(0)

        # Console header
        console_header_layout = QHBoxLayout()
        console_header_layout.setContentsMargins(12, PADDING_HEADER, 12, PADDING_HEADER)
        console_header_layout.setSpacing(0)

        self.console_header = QLabel(CONSOLE_HEADER_READY)
        self.console_header.setFont(QFont(FONT_FAMILY_MONOSPACE, FONT_SIZE_BUTTON - 1))
        self.console_header.setStyleSheet(f"color: {COLOR_TEXT_DIM};")
        console_header_layout.addWidget(self.console_header, 1)

        clear_button = QPushButton("Clear")
        clear_button.setFont(QFont(FONT_FAMILY_MONOSPACE, 8))
        clear_button.setMaximumWidth(CLEAR_BUTTON_WIDTH)
        clear_button.clicked.connect(self.clear_console)
        clear_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_BUTTON_SECONDARY};
                color: {COLOR_TEXT_DIM};
                border: none;
                border-radius: 3px;
                padding: 4px 8px;
            }}
            QPushButton:hover {{
                background-color: {COLOR_BUTTON_SECONDARY_HOVER};
            }}
        """)
        console_header_layout.addWidget(clear_button, 0)

        console_layout.addLayout(console_header_layout)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont(FONT_FAMILY_MONOSPACE, FONT_SIZE_CONSOLE))
        self.console.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLOR_SURFACE_DARKER};
                color: {COLOR_TEXT_SECONDARY};
                border: none;
                margin: 0px;
            }}
        """)
        console_layout.addWidget(self.console)

        console_frame.setLayout(console_layout)
        return console_frame

    def apply_dark_theme(self) -> None:
        """Apply dark theme stylesheet to the main window."""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {COLOR_BACKGROUND};
            }}
            QLabel {{
                color: {COLOR_TEXT_SECONDARY};
            }}
        """)

    def run_single_script(self, script_name: str) -> None:
        """
        Execute a single script independently.

        Args:
            script_name: Name of the script to run
        """
        script_state = self.scripts[script_name]
        if script_state.status != ScriptStatus.RUNNING:
            self.update_timer.start(PROGRESS_UPDATE_INTERVAL)
            self.execute_script(script_name, is_all=False)

    def run_all_scripts(self) -> None:
        """Execute all scripts sequentially."""
        if not self.is_running_all:
            self.reset_all()
            self.is_running_all = True
            if self.run_all_button:
                self.run_all_button.setEnabled(False)
            self.update_timer.start(PROGRESS_UPDATE_INTERVAL)
            self.run_next_in_sequence()

    def run_next_in_sequence(self) -> None:
        """Find and execute the next pending script in the sequence."""
        for script_name in self.running_scripts:
            if self.scripts[script_name].status == ScriptStatus.PENDING:
                self.execute_script(script_name, is_all=True)
                return

        # All scripts completed
        self.is_running_all = False
        if self.run_all_button:
            self.run_all_button.setEnabled(True)
        self.update_timer.stop()

    def on_script_order_changed(self, new_order: List[str]) -> None:
        """
        Handle script reordering from drag and drop.

        Args:
            new_order: List of script names in the new order
        """
        self.running_scripts = new_order

    def execute_script(self, script_name: str, is_all: bool) -> None:
        """
        Create and start a script execution thread.

        Args:
            script_name: Name of the script to execute
            is_all: Whether this is part of a "Run All" sequence
        """
        script_state = self.scripts[script_name]
        script_state.set_status(ScriptStatus.RUNNING)
        self.current_script = script_name

        if self.console_header:
            self.console_header.setText(CONSOLE_HEADER_RUNNING.format(script_name))

        if self.console:
            self.console.append(MESSAGE_SCRIPT_STARTED.format(
                CONSOLE_HEADER_SEPARATOR,
                script_name,
                CONSOLE_HEADER_SEPARATOR
            ))

        thread = ScriptRunnerThread(script_name)
        script_state.thread = thread
        thread.line_received.connect(lambda line: self.on_line_received(script_name, line, is_all))
        thread.error_received.connect(lambda err: self.on_error_received(script_name, err, is_all))
        thread.finished.connect(lambda code: self.on_script_finished(script_name, code, is_all))
        thread.start()

    def on_line_received(self, script_name: str, line: str, is_all: bool) -> None:
        """
        Handle output line from script.

        Args:
            script_name: Name of the executing script
            line: Output line
            is_all: Whether part of "Run All" sequence
        """
        if not self.console:
            return

        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.console.setTextCursor(cursor)

        # Color-code the output
        if "error" in line.lower() or line.startswith("ERROR"):
            self.console.setTextColor(QColor("#ff4444"))
        elif "complete" in line.lower() or "success" in line.lower() or "✓" in line:
            self.console.setTextColor(QColor("#00cc66"))
        else:
            self.console.setTextColor(QColor(COLOR_TEXT_SECONDARY))

        self.console.insertPlainText(line + "\n")
        self.console.setTextColor(QColor(COLOR_TEXT_SECONDARY))
        self.console.ensureCursorVisible()

    def on_error_received(self, script_name: str, error: str, is_all: bool) -> None:
        """
        Handle error output from script.

        Args:
            script_name: Name of the executing script
            error: Error message
            is_all: Whether part of "Run All" sequence
        """
        if not self.console:
            return

        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.console.setTextCursor(cursor)
        self.console.setTextColor(QColor("#ff4444"))
        self.console.insertPlainText(error + "\n")
        self.console.setTextColor(QColor(COLOR_TEXT_SECONDARY))
        self.console.ensureCursorVisible()

    def on_script_finished(self, script_name: str, exit_code: int, is_all: bool) -> None:
        """
        Handle script completion.

        Args:
            script_name: Name of the completed script
            exit_code: Process exit code (0 for success)
            is_all: Whether part of "Run All" sequence
        """
        script_state = self.scripts[script_name]

        if not self.console:
            return

        if exit_code == 0:
            script_state.set_status(ScriptStatus.SUCCESS)
            self.console.setTextColor(QColor(COLOR_STATUS_SUCCESS))
            self.console.insertPlainText(MESSAGE_SCRIPT_SUCCESS.format(script_name))
        else:
            script_state.set_status(ScriptStatus.FAILED)
            self.console.setTextColor(QColor(COLOR_STATUS_FAILED))
            self.console.insertPlainText(MESSAGE_SCRIPT_FAILED.format(script_name, exit_code))

        self.console.setTextColor(QColor(COLOR_TEXT_SECONDARY))
        self.console.ensureCursorVisible()
        self.update_progress()

        if is_all:
            if exit_code != 0:
                self.is_running_all = False
                if self.run_all_button:
                    self.run_all_button.setEnabled(True)
                self.update_timer.stop()
                self.console.setTextColor(QColor("#ff4444"))
                self.console.insertPlainText(MESSAGE_RUN_ALL_STOPPED)
                self.console.setTextColor(QColor(COLOR_TEXT_SECONDARY))
            else:
                self.run_next_in_sequence()
        else:
            self.update_timer.stop()

    def update_progress(self) -> None:
        """Update the progress bar based on completed scripts."""
        completed = sum(
            1 for s in self.scripts.values()
            if s.status in (ScriptStatus.SUCCESS, ScriptStatus.FAILED)
        )
        total = TOTAL_SCRIPTS
        if self.progress_bar:
            self.progress_bar.setValue(completed)
        if self.progress_text:
            self.progress_text.setText(f"{completed}/{total}")

    def clear_console(self) -> None:
        """Clear the console output and reset header."""
        if self.console:
            self.console.clear()
        if self.console_header:
            self.console_header.setText(CONSOLE_HEADER_READY)

    def reset_all(self) -> None:
        """Reset all scripts to pending state and clear the console."""
        for script_state in self.scripts.values():
            script_state.set_status(ScriptStatus.PENDING)
        self.current_script = None
        self.is_running_all = False
        if self.run_all_button:
            self.run_all_button.setEnabled(True)
        self.update_timer.stop()
        self.clear_console()
        self.update_progress()
