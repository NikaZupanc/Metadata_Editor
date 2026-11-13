
#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

VENV_DIR="$PROJECT_ROOT/.venv"

# Create virtual environment if it doesn't exist
if [[ ! -f "$VENV_DIR/Scripts/python.exe" && ! -f "$VENV_DIR/bin/python" ]]; then
    echo "Creating virtual environment..."

    if command -v py >/dev/null 2>&1; then
        py -3 -m venv "$VENV_DIR"
    elif command -v python3 >/dev/null 2>&1; then
        python3 -m venv "$VENV_DIR"
    else
        echo "Error: Python 3 is not installed."
        exit 1
    fi
fi

# Select virtual environment Python
if [[ -f "$VENV_DIR/Scripts/python.exe" ]]; then
    PYTHON="$VENV_DIR/Scripts/python.exe"
else
    PYTHON="$VENV_DIR/bin/python"
fi

# Install dependencies
echo "Checking dependencies..."
"$PYTHON" -m pip install -r requirements.txt --disable-pip-version-check --quiet


# Run application
"$PYTHON" main.py
#"$PYTHON" test_comments.py