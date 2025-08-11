@echo off
REM Cric Opto - Dream11 Cricket Optimization Launcher Script for Windows
REM This script sets up and runs the Cric Opto application

echo 🏏 Cric Opto - Dream11 Cricket Optimization
echo ==============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    pause
    exit /b 1
)

echo ✅ Python detected

REM Check if virtual environment exists
if not exist "cric_opto_env" (
    echo 📦 Creating virtual environment...
    python -m venv cric_opto_env
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        echo Trying to install dependencies globally...
        echo Installing required packages...
        pip install -r requirements.txt
        if %errorlevel% neq 0 (
            echo ❌ Failed to install dependencies
            pause
            exit /b 1
        )
    ) else (
        echo ✅ Virtual environment created
    )
)

REM Activate virtual environment if it exists
if exist "cric_opto_env" (
    echo 🔧 Activating virtual environment...
    call cric_opto_env\Scripts\activate.bat
    
    echo 📦 Installing/updating dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
)

echo.
echo 🚀 Starting Cric Opto application...
echo The app will open in your default web browser
echo If it doesn't open automatically, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

REM Run the application
streamlit run cric_opto.py --server.headless true

pause