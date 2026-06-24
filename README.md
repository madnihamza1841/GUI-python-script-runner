# GUI Python Script Runner

A professional, production-ready PyQt6 desktop application for managing and executing scripts with real-time output streaming, drag-and-drop reordering, and comprehensive progress tracking. Built as a portfolio piece demonstrating modern desktop application architecture, threading, and user experience design.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.7.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

## Features

### Core Functionality
- **Real-time Script Execution** - Execute Python scripts as subprocesses with live stdout/stderr streaming
- **Threading Architecture** - Non-blocking UI using QThread; GUI never freezes during script execution
- **Sequential & Individual Execution** - Run all scripts in sequence or execute individual scripts on-demand
- **Progress Tracking** - Visual progress bar and counter showing overall completion status
- **Status Indicators** - Color-coded status dots for each script (pending, running, success, failed)

### User Experience
- **Drag-and-Drop Reordering** - Rearrange script execution order by dragging rows; order persists in "Run All" mode
- **Live Output Console** - Real-time output display with auto-scrolling
- **Color-Coded Output** - Automatic syntax highlighting:
  - Red for errors
  - Green for success messages
  - Gray for normal output
- **Elapsed Time Tracking** - Per-script elapsed time display that updates live
- **Error Handling** - Clear error messages and graceful failure reporting

### UI/UX Design
- **Professional Dark Theme** - Custom dark palette optimized for technical work
- **Clean, Modular Layout** - Logical separation of header, script list, progress, and console
- **Responsive Design** - Smooth animations and responsive feedback to user actions
- **Accessible Controls** - Large, easy-to-click buttons; clear visual hierarchy

## Architecture

```
script-runner/
├── main.py                 # Application entry point
├── dashboard.py            # Main window and orchestration logic
├── widgets.py              # Custom UI components (ScriptRow, ScriptListContainer)
├── runner.py               # Subprocess management and threading
├── models.py               # Data models (ScriptStatus, ScriptState)
├── constants.py            # Centralized configuration (colors, fonts, sizes, messages)
├── scripts/                # Demo scripts (power engineering simulation)
│   ├── load_data.py
│   ├── validate_input.py
│   ├── run_simulation.py
│   ├── process_results.py
│   └── export_results.py
├── requirements.txt
├── README.md
└── .gitignore
```

### Design Principles

1. **Separation of Concerns** - Each module has a single, well-defined responsibility
2. **Signal-Based Architecture** - PyQt signals decouple components and handle thread-safe communication
3. **Configuration as Code** - All constants centralized in `constants.py` for easy customization
4. **Type Hints** - Full type annotations for code clarity and IDE support
5. **Minimal Abstractions** - No unnecessary layers; pragmatic design focused on functionality

## Technical Highlights

### Threading Model
- **ScriptRunner** - Manages `subprocess.Popen` with line-by-line output capture
- **ScriptRunnerThread** - Wraps ScriptRunner in QThread for non-blocking execution
- **Signal Emission** - Thread-safe output streaming via PyQt signals

### Drag-and-Drop Implementation
- Custom MIME data handling for script name passing
- Intelligent drop position detection
- Real-time list reordering with visual feedback
- Automatic order persistence in execution list

### State Management
- **ScriptState** - Encapsulates individual script state with status tracking and timing
- **ScriptStatus Enum** - Type-safe status representation
- **Signal Broadcasting** - Status changes broadcast to UI via Qt signals

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/GUI-python-script-runner.git
   cd GUI-python-script-runner
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main.py
```

The dashboard will launch with all scripts in pending (gray) state.

### Basic Operations

**Run All Scripts Sequentially**
- Click the green "Run All" button
- Scripts execute in order (respecting any drag-and-drop reordering)
- If any script fails, the sequence stops and shows an error

**Run Individual Script**
- Click the blue "Run" button on any script row
- Script executes independently
- Does not affect other scripts

**Reorder Scripts**
- Click and drag any script row up or down
- Visual position updates immediately
- New order is used in next "Run All" execution

**Reset Dashboard**
- Click the orange "Reset" button
- All scripts return to pending state
- Console is cleared
- Progress bar resets to 0/5

**Clear Console**
- Click the "Clear" button in the console panel
- Only output is cleared; script states remain unchanged

### Understanding the UI

**Script List**
- **Status Dot** - Color indicates script state:
  - Gray ● = Pending
  - Blue ● = Running
  - Green ● = Success
  - Red ● = Failed
- **Script Name & Description** - Identifies the script and its purpose
- **Elapsed Time** - Updates live during execution, shows "Failed" on error
- **Run Button** - Execute this script individually

**Progress Bar**
- Shows X/5 scripts completed (success or failed)
- Animates smoothly as scripts complete
- Reaches 100% when all scripts finish

**Console Panel**
- **Header** - Shows "▶ script_name" while executing, "Ready" when idle
- **Output** - Real-time streaming with color coding
- **Auto-Scroll** - Automatically scrolls to newest output
- **Clear Button** - Clears output without affecting script states

## Configuration

All application configuration is centralized in `constants.py`:

```python
# Customize colors
COLOR_BACKGROUND = "#1e1e1e"
COLOR_STATUS_SUCCESS = "#00cc66"

# Change font sizes
FONT_SIZE_TITLE = 18
FONT_SIZE_CONSOLE = 9

# Adjust spacing
PADDING_MAIN = 16
SPACING_SECTION = 8

# Define scripts
SCRIPT_NAMES = ["script1.py", "script2.py", ...]
SCRIPT_DESCRIPTIONS = {
    "script1.py": "Description here",
    ...
}
```

## Demo Scripts

The `scripts/` folder contains five dummy scripts simulating HVDC (High Voltage Direct Current) power engineering work:

1. **load_data.py** - Simulates loading grid topology data
2. **validate_input.py** - Validates converter parameters
3. **run_simulation.py** - Runs load flow analysis
4. **process_results.py** - Post-processes simulation results
5. **export_results.py** - Exports results to file

Each script:
- Prints realistic engineering workflow messages
- Takes 1–3 seconds to complete
- Randomly fails ~15% of the time (for testing error handling)
- Exits with code 0 (success) or 1 (failure)

### Running Custom Scripts

To use your own scripts:

1. Place script files in the `scripts/` folder
2. Update `SCRIPT_NAMES` and `SCRIPT_DESCRIPTIONS` in `constants.py`
3. Restart the application

Scripts can be any executable: Python, shell scripts, MATLAB sessions, compiled binaries, etc.

## Project Structure Explained

### main.py
Minimal entry point. Initializes Qt application and launches the dashboard window.

### dashboard.py
Main orchestration logic:
- `ScriptRunnerDashboard` - QMainWindow subclass
- Layout construction and UI setup
- Signal connections and event handling
- Script execution workflow and sequencing
- Progress updates and state management

### widgets.py
Custom PyQt6 widgets:
- `ScriptRow` - Individual script UI with status, time, and run button
- `ScriptListContainer` - Container managing script list with drag-and-drop support
- Drag-and-drop event handlers for reordering

### runner.py
Subprocess and threading management:
- `ScriptRunner` - Wraps subprocess.Popen, emits signals for each output line
- `ScriptRunnerThread` - QThread wrapper for non-blocking execution

### models.py
Data models and state management:
- `ScriptStatus` - Enum for script states
- `ScriptState` - Encapsulates individual script state, timing, and status signals

### constants.py
Centralized configuration:
- All colors, fonts, sizes, and spacing
- Script names and descriptions
- Timer intervals and messages
- No hardcoded values in code

## Development

### Code Style

The project uses:
- Type hints throughout for clarity and IDE support
- Clear, descriptive variable and function names
- Minimal comments (code is self-documenting)
- Single-responsibility functions and classes

### Extending the Application

**Add a New Feature**
1. Identify which module it belongs in
2. Implement the feature
3. Update `constants.py` if adding configuration
4. Update signals if adding data flow

**Add a New Widget**
1. Create class in `widgets.py`
2. Import in `dashboard.py`
3. Use in appropriate layout method

**Change Color Scheme**
1. Update `COLOR_*` constants in `constants.py`
2. No code changes needed; all widgets use constant references

## Performance

- **Subprocess Execution**: Efficient line-by-line I/O using `bufsize=1`
- **Threading**: Non-blocking UI using QThread; main thread always responsive
- **Memory**: Minimal overhead; console output is streamed, not buffered
- **Responsiveness**: 100ms update intervals for progress bar and timers

## Production Use

While built as a portfolio piece, this application is production-ready. For production deployment:

1. **Script Integration** - Replace demo scripts with your actual scripts
2. **Error Logging** - Add structured logging to `constants.py` messages
3. **Configuration File** - Move `constants.py` settings to JSON/YAML config
4. **Data Persistence** - Add database integration for results storage
5. **Authentication** - Add user authentication if needed
6. **Testing** - Add unit tests for models and runners

## Troubleshooting

### Application Won't Start
- Ensure Python 3.8+ is installed
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Scripts Not Executing
- Check script paths in `SCRIPT_NAMES`
- Verify scripts have execute permissions: `chmod +x scripts/*.py`
- Check console for error messages

### UI Freezing
- This should not happen; threading is implemented correctly
- If it does, check for blocking operations in custom code

### Drag-and-Drop Not Working
- Ensure you're clicking on the script row itself (not buttons)
- Drag with left mouse button
- Drop on another script row

## Future Enhancements

Potential improvements for future versions:
- Persistent script execution history
- Advanced filtering and search
- Custom script templates
- Scheduled execution
- Remote script execution over SSH
- Web-based dashboard
- Multi-project management
- Advanced error recovery and retry logic

## Contributing

This is a portfolio project, but improvements are welcome! Please feel free to:
- Report issues and bugs
- Suggest UI/UX improvements
- Propose architectural enhancements
- Submit pull requests with new features

## License

MIT License - see LICENSE file for details

## Author

Hamza Madni - [GitHub](https://github.com/yourusername)

## Acknowledgments

- PyQt6 documentation and community
- Python subprocess and threading best practices
- Modern desktop application UI/UX design principles

---

**Built with ❤️ as a portfolio piece demonstrating professional Python desktop application development.**
