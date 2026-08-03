@echo off
REM Build Valorant Crosshair Analyzer Installer for Windows

echo.
echo ==========================================
echo Building Vod Tracker Installer...
echo ==========================================
echo.

cd frontend

echo Installing dependencies...
call npm install

echo.
echo Building desktop application...
call npm run build:desktop

echo.
echo ==========================================
echo Build complete! Installer is in: frontend\dist\
echo ==========================================
echo.
echo File: Vod Tracker Setup 1.0.0.exe
echo Size: ~150-200MB
echo.
pause
