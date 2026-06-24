"""Script execution and threading management."""

import subprocess
import sys
from pathlib import Path
from typing import Optional
from PyQt6.QtCore import QThread, pyqtSignal, QObject

from constants import MESSAGE_SCRIPT_NOT_FOUND, MESSAGE_SCRIPT_EXECUTION_ERROR


class ScriptRunner(QObject):
    """Manages script execution as a subprocess with real-time output streaming."""

    line_received = pyqtSignal(str)
    error_received = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self):
        """Initialize the script runner."""
        super().__init__()
        self.process: Optional[subprocess.Popen] = None

    def run_script(self, script_name: str) -> None:
        """
        Execute a script as a subprocess and emit output line by line.

        Args:
            script_name: Name of the script to execute
        """
        script_path = Path(__file__).parent / "scripts" / script_name

        if not script_path.exists():
            self.error_received.emit(MESSAGE_SCRIPT_NOT_FOUND.format(script_path))
            self.finished.emit(1)
            return

        try:
            self.process = subprocess.Popen(
                [sys.executable, str(script_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            # Read stdout line by line
            if self.process.stdout:
                for line in self.process.stdout:
                    self.line_received.emit(line.rstrip())

            # Wait for process to finish
            returncode = self.process.wait()

            # Read any remaining stderr
            if self.process.stderr:
                for line in self.process.stderr:
                    self.error_received.emit(line.rstrip())

            self.finished.emit(returncode)

        except Exception as e:
            self.error_received.emit(MESSAGE_SCRIPT_EXECUTION_ERROR.format(str(e)))
            self.finished.emit(1)

    def stop(self) -> None:
        """Terminate the running process if it's still active."""
        if self.process and self.process.poll() is None:
            self.process.terminate()


class ScriptRunnerThread(QThread):
    """Worker thread for running scripts without blocking the UI."""

    line_received = pyqtSignal(str)
    error_received = pyqtSignal(str)
    finished = pyqtSignal(int)

    def __init__(self, script_name: str):
        """
        Initialize the script runner thread.

        Args:
            script_name: Name of the script to run in this thread
        """
        super().__init__()
        self.script_name = script_name
        self.runner: Optional[ScriptRunner] = None

    def run(self) -> None:
        """Execute the script in this thread, routing output via signals."""
        self.runner = ScriptRunner()
        self.runner.line_received.connect(self.line_received.emit)
        self.runner.error_received.connect(self.error_received.emit)
        self.runner.finished.connect(self.finished.emit)

        self.runner.run_script(self.script_name)
