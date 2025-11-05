@echo off
echo ================================================================================
echo Starting Nova Corrente Backend API Server
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

REM Check if run_server.py exists
if not exist run_server.py (
    echo ERROR: run_server.py not found in %BACKEND_DIR%
    echo Current directory: %CD%
    dir run_server.py
    pause
    exit /b 1
)

echo.
echo Starting FastAPI server from: %CD%
echo.

REM Run the server using uvicorn directly as fallback
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000

pause







