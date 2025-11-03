@echo off
echo Checking Dashboard Status...
echo.

echo Backend API:
curl -s http://localhost:5000/health
echo.
echo.

echo Frontend Status:
timeout /t 2 /nobreak >nul
curl -s -o NUL -w "HTTP Status: %%{http_code}\n" http://localhost:3000/main
echo.

echo Open your browser to: http://localhost:3000/main
echo Press any key to exit...
pause >nul

