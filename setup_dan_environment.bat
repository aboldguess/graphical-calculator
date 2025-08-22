@echo off
REM setup_dan_environment.bat
REM Mini-readme: Creates a Python virtual environment for Dan calculator on Windows.
REM Usage: setup_dan_environment.bat
REM Structure:
REM  1. Define environment directory
REM  2. Create virtual environment
REM  3. Activate environment
REM  4. Install dependencies (currently none)
SET ENV_DIR=.venv
python -m venv %ENV_DIR%
CALL %ENV_DIR%\Scripts\activate
python -m pip install --upgrade pip
REM No external dependencies required
ECHO Virtual environment created in %ENV_DIR%. Activate with: CALL %ENV_DIR%\Scripts\activate
