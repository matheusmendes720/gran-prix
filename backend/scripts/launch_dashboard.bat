@echo off
echo.
echo ========================================
echo 🇧🇷 NOVA CORRENTE DASHBOARD LAUNCHER
echo ========================================
echo.

cd /d "%~dp0"
python run_dashboard.py --port 8050

pause

