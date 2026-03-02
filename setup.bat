@echo off
REM Solar-to-Fertiliser Digital Twin (S2F-DT) Setup Script
REM Windows Batch File

echo.
echo ============================================
echo   S2F-DT Installation Script (Windows)
echo ============================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python --version

echo.
echo [2/5] Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [4/5] Upgrading pip...
python -m pip install --upgrade pip --quiet

echo.
echo [5/5] Installing dependencies...
pip install --no-cache-dir -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed
    echo Try alternative: pip install --upgrade-strategy only-if-needed -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Installation Complete!
echo ============================================
echo.
echo To run the application:
echo   streamlit run app.py
echo.
echo To run tests:
echo   python -m pytest tests/test_process.py -v
echo.
pause
