@echo off
title Instalador Oficial de Viernes - Groovi Developer
cd /d "%~dp0"
echo ====================================================
echo   VIERNES - INSTALADOR OFICIAL (Groovi Developer)
echo ====================================================
echo.
where py >nul 2>nul
if %errorlevel%==0 (
    py -3.12 -m pip install --quiet PyQt6 PyQt6-WebEngine
    py -3.12 installer.py
) else (
    python -m pip install --quiet PyQt6 PyQt6-WebEngine
    python installer.py
)
pause
