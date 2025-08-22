# Dan Graphical Calculator

Dan is a green-themed graphical calculator built with Python's standard library.
The application offers both a Tkinter-based GUI and a command-line mode for quick evaluations.

## Features
- Safe evaluation of arithmetic expressions (no `eval` usage).
- Modern green styling with clear on-screen instructions.
- Keyboard and button input support.
- Debug-friendly logging to `dan_calculator.log`.

## Prerequisites
- Python 3.10 or newer with Tkinter support.
- No external Python packages are required.

## Quick Start
### Linux / macOS / Raspberry Pi
```bash
# Option 1: using setup script
bash setup_dan_environment.sh
source .venv/bin/activate
python dan_graphical_calculator.py

# Option 2: manual steps
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python dan_graphical_calculator.py
```

### Windows
```bat
:: Option 1: using setup script
setup_dan_environment.bat
call .venv\Scripts\activate
python dan_graphical_calculator.py

:: Option 2: manual steps
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
python dan_graphical_calculator.py
```

## Command-Line Evaluation
Evaluate an expression without launching the GUI:
```bash
python dan_graphical_calculator.py --expression "2+2"
```

## Logs
Runtime information is stored in `dan_calculator.log` for debugging purposes.

## Usage
- Click buttons or use the keyboard to enter expressions.
- Press `=` to compute or `C` to clear.
- On-screen instructions guide basic usage, so no manual reading is required.

## License
This project is provided as-is for educational purposes.
