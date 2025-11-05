@echo off
REM Convert Mermaid .mmd files to Markdown documentation
REM Windows batch script wrapper

echo ========================================
echo MERMAID TO MARKDOWN CONVERTER
echo ========================================
echo.

cd /d "%~dp0\.."
python scripts\convert_mmd_to_markdown.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [!] Conversion failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [OK] Conversion complete!
pause

