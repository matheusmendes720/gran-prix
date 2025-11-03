@echo off
REM Simple reliable backend startup
cd /d %~dp0
echo Starting backend from: %CD%
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5000
pause


