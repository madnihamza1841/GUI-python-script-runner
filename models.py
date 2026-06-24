"""Data models for script state management."""

from enum import Enum
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal, QTime


class ScriptStatus(Enum):
    """Enumeration of possible script execution states."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class ScriptState(QObject):
    """Manages state and lifecycle for a single script."""

    status_changed = pyqtSignal(str, ScriptStatus)

    def __init__(self, name: str, description: str):
        """
        Initialize script state.

        Args:
            name: Script filename (e.g., "load_data.py")
            description: Human-readable description for the UI
        """
        super().__init__()
        self.name = name
        self.description = description
        self.status = ScriptStatus.PENDING
        self.elapsed_time = 0
        self.start_time: Optional[QTime] = None
        self.thread = None

    def set_status(self, status: ScriptStatus) -> None:
        """
        Update script status and emit signal.

        Args:
            status: New ScriptStatus
        """
        self.status = status
        self.status_changed.emit(self.name, status)

    def start_timer(self) -> None:
        """Record the current time as script start time."""
        self.start_time = QTime.currentTime()

    def update_elapsed(self) -> int:
        """
        Calculate elapsed seconds since script started.

        Returns:
            Elapsed time in seconds, or 0 if not started
        """
        if self.start_time:
            return self.start_time.msecsTo(QTime.currentTime()) // 1000
        return 0
