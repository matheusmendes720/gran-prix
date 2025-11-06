@echo off
REM Nova Corrente Complete Setup and Run Script
REM This script sets up PostgreSQL and starts the Flask API

echo ============================================================
echo Nova Corrente - Complete Setup
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Step 1: Installing Python dependencies...
cd /d "%~dp0backend"
pip install -r requirements_deployment.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Setting up PostgreSQL database...
echo Make sure PostgreSQL is running on localhost:5432
echo.
timeout /t 3 /nobreak >nul

python scripts/setup_database.py
if errorlevel 1 (
    echo.
    echo WARNING: Database setup encountered issues
    echo You may need to start PostgreSQL first
    echo.
)

echo.
echo Step 3: Starting Flask API server...
echo.
python run_flask_api.py

pause
