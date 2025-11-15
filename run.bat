@echo off
REM Script de démarrage rapide pour Windows

echo ===================================
echo 3D Model Automation - Quick Start
echo ===================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
if not exist "venv\.installed" (
    echo Installing dependencies...
    pip install -r requirements.txt
    type nul > venv\.installed
)

REM Check if .env exists
if not exist ".env" (
    echo WARNING: No .env file found!
    echo Please copy .env.example to .env and add your API keys
    echo Command: copy .env.example .env
    exit /b 1
)

REM Run the main script
cd src
echo.
echo Running automation...
echo.
python main.py %*
