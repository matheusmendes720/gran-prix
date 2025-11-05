@echo off
echo ================================================================================
echo Checking Backend Server Status
echo ================================================================================

REM Check if backend is running
curl http://localhost:5000/health >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Backend server is NOT running on port 5000
    echo.
    echo To start the backend server, run:
    echo   scripts\start_backend.bat
    echo.
    echo OR manually:
    echo   cd backend
    echo   python run_server.py
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo [SUCCESS] Backend server is running on port 5000
    echo.
    echo Testing health endpoint...
    curl http://localhost:5000/health
    echo.
    echo.
    echo Backend is ready!
)

pause








