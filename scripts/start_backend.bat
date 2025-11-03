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

REM Check if .env exists, if not create a basic one
if not exist .env (
    echo Creating .env file with defaults...
    (
        echo # Database Configuration
        echo DB_HOST=localhost
        echo DB_PORT=3306
        echo DB_USER=root
        echo DB_PASSWORD=
        echo DB_NAME=STOCK
        echo.
        echo # API Configuration
        echo API_HOST=127.0.0.1
        echo API_PORT=5000
        echo API_RELOAD=true
        echo.
        echo # CORS
        echo CORS_ORIGINS=http://localhost:3000,http://localhost:3001
        echo.
        echo # External APIs (Optional)
        echo INMET_API_KEY=
        echo BACEN_API_KEY=
        echo ANATEL_API_KEY=
        echo OPENWEATHER_API_KEY=
    ) > .env
    echo .env file created with defaults
)

echo.
echo Starting FastAPI server...
echo Current directory: %CD%
echo.

REM Check if run_server.py exists, if not use uvicorn directly
if exist run_server.py (
    echo Using run_server.py...
    python run_server.py
) else (
    echo run_server.py not found, using uvicorn directly...
    python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000
)

