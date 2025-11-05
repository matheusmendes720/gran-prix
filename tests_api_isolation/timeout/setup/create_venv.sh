#!/usr/bin/env bash
set -euo pipefail

PYTHON_EXECUTABLE=${1:-python3}
VENV_PATH=".venv"

if [[ -d "$VENV_PATH" ]]; then
  echo "Virtual environment already exists at $VENV_PATH"
  exit 0
fi

echo "Creating virtual environment in $VENV_PATH"
"$PYTHON_EXECUTABLE" -m venv "$VENV_PATH"

echo "Virtual environment created. Activate with:\n\n    source .venv/bin/activate\n"
