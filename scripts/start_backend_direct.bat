@echo off
echo ================================================================================
echo Starting Nova Corrente Backend API Server (Direct Uvicorn)
echo ================================================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Get absolute paths
set PROJECT_ROOT=%~dp0..
set BACKEND_DIR=%PROJECT_ROOT%\backend

echo.
echo Project Root: %PROJECT_ROOT%
echo Backend Directory: %BACKEND_DIR%
echo.

REM Navigate to backend directory
cd /d %BACKEND_DIR%

echo Current directory: %CD%
echo.

REM Check if app/main.py exists
if not exist app\main.py (
    echo ERROR: app\main.py not found!
    echo Please ensure you're in the correct backend directory
    dir app\main.py
    pause
    exit /b 1
)

echo Starting FastAPI server with uvicorn...
echo Host: 127.0.0.1
echo Port: 5000
echo.
echo API Docs will be available at: http://127.0.0.1:5000/docs
echo.
echo Press Ctrl+C to stop the server
echo ================================================================================
echo.

REM Run uvicorn directly - most reliable method
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000

pause




















