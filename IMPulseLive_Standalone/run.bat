@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Starting IMPulse Live from source...
python app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application stopped with error code %ERRORLEVEL%.
    pause
)
