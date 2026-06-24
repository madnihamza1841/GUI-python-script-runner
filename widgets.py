"""Custom PyQt6 widgets for the Script Runner Dashboard."""

from typing import Dict, List
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QWidget
from PyQt6.QtCore import pyqtSignal, QTimer, Qt, QMimeData
from PyQt6.QtGui import QFont, QColor, QDrag

from models import ScriptState, ScriptStatus
from constants import (
    COLOR_SURFACE,
    COLOR_SURFACE_LIGHT,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_DIM,
    COLOR_STATUS_PENDING,
    COLOR_STATUS_RUNNING,
    COLOR_STATUS_SUCCESS,
    COLOR_STATUS_FAILED,
    COLOR_BUTTON_PRIMARY,
    COLOR_BUTTON_PRIMARY_HOVER,
    COLOR_BUTTON_PRIMARY_PRESS,
    FONT_FAMILY_MONOSPACE,
    FONT_SIZE_SCRIPT_NAME,
    FONT_SIZE_SCRIPT_DESC,
    FONT_SIZE_BUTTON,
    FONT_SIZE_STATUS_DOT,
    PADDING_ROW,
    SPACING_ROW,
    SPACING_SECTION,
    MIN_ROW_HEIGHT,
    BUTTON_WIDTH_RUN,
    TIME_LABEL_WIDTH,
    BORDER_RADIUS_LARGE,
    ELAPSED_TIME_UPDATE_INTERVAL,
)


class ScriptRow(QFrame):
    """Visual row widget representing a single script in the script list."""

    run_clicked = pyqtSignal(str)

    def __init__(self, script_state: ScriptState):
        """
        Initialize script row widget.

        Args:
            script_state: ScriptState object to visualize
        """
        super().__init__()
        self.script_state = script_state
        self.setup_ui()
        self.script_state.status_changed.connect(self.on_status_changed)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_elapsed)

    def setup_ui(self) -> None:
        """Build the UI layout with status dot, name, description, time, and run button."""
        self.setStyleSheet(f"""
            ScriptRow {{
                background-color: {COLOR_SURFACE};
                border-radius: {BORDER_RADIUS_LARGE}px;
                padding: {PADDING_ROW}px;
            }}
            ScriptRow:hover {{
                background-color: {COLOR_SURFACE_LIGHT};
            }}
        """)
        self.setFrameShape(QFrame.Shape.Box)
        self.setLineWidth(0)

        layout = QHBoxLayout()
        layout.setContentsMargins(PADDING_ROW, 10, PADDING_ROW, 10)
        layout.setSpacing(SPACING_ROW)

        # Status dot
        self.status_dot = QLabel("●")
        self.status_dot.setFont(QFont(FONT_FAMILY_MONOSPACE, FONT_SIZE_STATUS_DOT))
        self.status_dot.setStyleSheet(f"color: {COLOR_STATUS_PENDING};")
        layout.addWidget(self.status_dot, 0, Qt.AlignmentFlag.AlignCenter)

        # Script name and description
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        name_label = QLabel(self.script_state.name)
        name_label.setFont(QFont(FONT_FAMILY_MONOSPACE, FONT_SIZE_SCRIPT_NAME, QFont.Weight.Bold))
        name_label.setStyleSheet(f"color: {COLOR_TEXT_PRIMARY};")
        info_layout.addWidget(name_label)

        desc_label = QLabel(self.script_state.description)
        desc_label.setFont(QFont(FONT_FAMILY_MONOSPACE, FONT_SIZE_SCRIPT_DESC))
        desc_label.setStyleSheet(f"color: {COLOR_TEXT_MUTED};")
        info_layout.addWidget(desc_label)

        layout.addLayout(info_layout, 1)

        # Elapsed time
        self.time_label = QLabel("0s")
        self.time_label.setFont(QFont(FONT_FAMILY_MONOSPACE, FONT_SIZE_BUTTON))
        self.time_label.setStyleSheet(f"color: {COLOR_TEXT_DIM};")
        self.time_label.setMinimumWidth(TIME_LABEL_WIDTH)
        layout.addWidget(self.time_label, 0, Qt.AlignmentFlag.AlignRight)

        # Run button
        self.run_button = self._create_run_button()
        layout.addWidget(self.run_button, 0)

        self.setLayout(layout)
        self.setMinimumHeight(MIN_ROW_HEIGHT)

    def _create_run_button(self) -> QPushButton:
        """Create and style the run button."""
        button = QPushButton("Run")
        button.setFont(QFont(FONT_FAMILY_MONOSPACE, FONT_SIZE_BUTTON, QFont.Weight.Bold))
        button.setMaximumWidth(BUTTON_WIDTH_RUN)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_BUTTON_PRIMARY};
                color: {COLOR_TEXT_PRIMARY};
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLOR_BUTTON_PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {COLOR_BUTTON_PRIMARY_PRESS};
            }}
        """)
        button.clicked.connect(lambda: self.run_clicked.emit(self.script_state.name))
        return button

    def on_status_changed(self, script_name: str, status: ScriptStatus) -> None:
        """
        Handle script status changes and update UI accordingly.

        Args:
            script_name: Name of the script (for verification)
            status: New ScriptStatus
        """
        if status == ScriptStatus.PENDING:
            self._set_pending_state()
        elif status == ScriptStatus.RUNNING:
            self._set_running_state()
        elif status == ScriptStatus.SUCCESS:
            self._set_success_state()
        elif status == ScriptStatus.FAILED:
            self._set_failed_state()

    def _set_pending_state(self) -> None:
        """Update UI for PENDING state."""
        self.status_dot.setStyleSheet(f"color: {COLOR_STATUS_PENDING};")
        self.time_label.setText("0s")
        self.timer.stop()
        self.run_button.setEnabled(True)

    def _set_running_state(self) -> None:
        """Update UI for RUNNING state."""
        self.status_dot.setStyleSheet(f"color: {COLOR_STATUS_RUNNING};")
        self.script_state.start_timer()
        self.timer.start(ELAPSED_TIME_UPDATE_INTERVAL)
        self.run_button.setEnabled(False)

    def _set_success_state(self) -> None:
        """Update UI for SUCCESS state."""
        self.status_dot.setStyleSheet(f"color: {COLOR_STATUS_SUCCESS};")
        self.timer.stop()
        self.run_button.setEnabled(True)

    def _set_failed_state(self) -> None:
        """Update UI for FAILED state."""
        self.status_dot.setStyleSheet(f"color: {COLOR_STATUS_FAILED};")
        self.time_label.setText("Failed")
        self.timer.stop()
        self.run_button.setEnabled(True)

    def update_elapsed(self) -> None:
        """Update the elapsed time display if script is running."""
        if self.script_state.status == ScriptStatus.RUNNING:
            elapsed = self.script_state.update_elapsed()
            self.time_label.setText(f"{elapsed}s")

    def mousePressEvent(self, event):
        """Handle mouse press to initiate drag."""
        if event.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.script_state.name)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.MoveAction)
        super().mousePressEvent(event)


class ScriptListContainer(QWidget):
    """Container widget that manages script rows with drag-and-drop reordering."""

    order_changed = pyqtSignal(list)

    def __init__(self):
        """Initialize the script list container."""
        super().__init__()
        self.script_rows: Dict[str, ScriptRow] = {}
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(SPACING_SECTION)
        self.setLayout(self.layout)
        self.setAcceptDrops(True)

    def add_script_row(self, script_name: str, row: ScriptRow) -> None:
        """
        Add a script row to the container.

        Args:
            script_name: Name of the script
            row: ScriptRow widget to add
        """
        self.script_rows[script_name] = row
        self.layout.insertWidget(self.layout.count() - 1, row)

    def dragEnterEvent(self, event):
        """Accept drag events."""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop event to reorder scripts."""
        if not event.mimeData().hasText():
            return

        script_name = event.mimeData().text()
        if script_name not in self.script_rows:
            return

        # Get the drop position
        drop_pos = event.position()
        target_row = None
        target_index = 0

        # Find which row the script was dropped on
        for i in range(self.layout.count() - 1):
            widget = self.layout.itemAt(i).widget()
            if widget and widget != self.script_rows[script_name]:
                widget_bottom = widget.mapToGlobal(widget.rect().bottomLeft()).y()
                drop_global_y = self.mapToGlobal(drop_pos.toPoint()).y()

                if drop_global_y < widget_bottom:
                    target_index = i
                    break
                target_index = i + 1

        # Remove the dragged row from layout
        row = self.script_rows[script_name]
        self.layout.removeWidget(row)

        # Insert at the new position
        self.layout.insertWidget(target_index, row)

        # Emit the new order
        self._emit_order_changed()
        event.acceptProposedAction()

    def _emit_order_changed(self) -> None:
        """Emit the current script order."""
        order = []
        for i in range(self.layout.count() - 1):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, ScriptRow):
                order.append(widget.script_state.name)
        self.order_changed.emit(order)

    def get_script_order(self) -> List[str]:
        """
        Get the current order of scripts.

        Returns:
            List of script names in current order
        """
        order = []
        for i in range(self.layout.count() - 1):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, ScriptRow):
                order.append(widget.script_state.name)
        return order
