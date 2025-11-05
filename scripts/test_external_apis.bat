@echo off
echo ================================================================================
echo Testing External API Reliability
echo ================================================================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Navigate to backend directory
cd /d %~dp0..\backend

echo.
echo Running external API reliability tests...
echo.

REM Run the test script
python run_api_tests.py

echo.
echo ================================================================================
echo Test Complete!
echo ================================================================================
echo.
pause








