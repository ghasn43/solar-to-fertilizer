#!/bin/bash

# Solar-to-Fertiliser Digital Twin (S2F-DT) Setup Script
# macOS/Linux Bash Script

echo ""
echo "============================================"
echo "  S2F-DT Installation Script (macOS/Linux)"
echo "============================================"
echo ""

# Check Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org"
    exit 1
fi

echo "[1/5] Checking Python version..."
python3 --version

echo ""
echo "[2/5] Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo ""
echo "[3/5] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[4/5] Upgrading pip..."
python -m pip install --upgrade pip --quiet

echo ""
echo "[5/5] Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Installation failed"
    echo "Try alternative: pip install --upgrade-strategy only-if-needed -r requirements.txt"
    exit 1
fi

echo ""
echo "============================================"
echo "  Installation Complete!"
echo "============================================"
echo ""
echo "To run the application:"
echo "  streamlit run app.py"
echo ""
echo "To run tests:"
echo "  python -m pytest tests/test_process.py -v"
echo ""
