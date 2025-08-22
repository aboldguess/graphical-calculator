#!/usr/bin/env bash
# setup_dan_environment.sh
# Mini-readme: Creates a Python virtual environment for Dan calculator.
# Usage: bash setup_dan_environment.sh
# Structure:
#  1. Define environment directory
#  2. Create virtual environment
#  3. Activate environment
#  4. Install dependencies (matplotlib)
#  5. Inform user
set -euo pipefail
ENV_DIR=".venv"
python3 -m venv "$ENV_DIR"
# shellcheck disable=SC1091
source "$ENV_DIR/bin/activate"
python -m pip install --upgrade pip matplotlib
echo "Virtual environment created in $ENV_DIR. Activate with: source $ENV_DIR/bin/activate"
