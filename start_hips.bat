@echo off
title HIPS - Host Intrusion Prevention System

echo ============================================
echo   HIPS - Starting Backend Service
echo ============================================
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

REM Auto-update if this is a git repo and git is installed
git --version >nul 2>&1
if not errorlevel 1 (
    git rev-parse --is-inside-work-tree >nul 2>&1
    if not errorlevel 1 (
        echo Checking for updates...
        git pull origin main >nul 2>&1
        echo Update check complete.
    )
)

echo.

cd /d "%~dp0backend"

REM Install dependencies if needed
echo Checking dependencies...
pip install -r requirements.txt --quiet

echo.
echo Starting HIPS backend on http://localhost:8000
echo Keep this window open while using HIPS.
echo Close this window to stop HIPS.
echo.

python -m hips_service.main

pause