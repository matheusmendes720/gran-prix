@echo off
echo ================================================================================
echo Nova Corrente Dashboard - Starting Servers
echo ================================================================================

REM Start backend API
echo Starting Backend API on port 5000...
start "Nova Corrente API" cmd /k "cd /d %~dp0 && python api_standalone.py"

REM Wait 3 seconds for API to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo Starting Frontend on port 3000...
start "Nova Corrente Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ================================================================================
echo Both servers started!
echo.
echo API: http://localhost:5000
echo Dashboard: http://localhost:3000/main
echo.
echo Close the terminal windows to stop the servers
echo ================================================================================
timeout /t 3 /nobreak >nul

