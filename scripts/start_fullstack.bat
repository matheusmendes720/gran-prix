@echo off
echo ================================================================================
echo Nova Corrente Fullstack Dashboard - Starting Servers
echo ================================================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Starting Backend API Server on port 5000...

REM Get absolute paths
set PROJECT_ROOT=%~dp0..
set BACKEND_DIR=%PROJECT_ROOT%\backend

REM Navigate to backend directory
cd /d %BACKEND_DIR%

if not exist run_server.py (
    echo WARNING: run_server.py not found, using uvicorn directly...
    start "Nova Corrente Backend API" cmd /k "cd /d %BACKEND_DIR% && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000"
) else (
    start "Nova Corrente Backend API" cmd /k "cd /d %BACKEND_DIR% && python run_server.py"
)

REM Wait 8 seconds for backend to start and initialize all services
echo Waiting for backend to initialize all services...
timeout /t 8 /nobreak >nul

echo.
echo Starting Frontend Development Server on port 3000...
cd ..\frontend
start "Nova Corrente Frontend" cmd /k "npm run dev"

echo.
echo ================================================================================
echo Both servers are starting!
echo.
echo Backend API: http://localhost:5000
echo Backend Docs: http://localhost:5000/docs
echo Frontend: http://localhost:3000
echo.
echo Close the terminal windows to stop the servers
echo ================================================================================
cd ..
timeout /t 3 /nobreak >nul

