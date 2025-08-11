@echo off
echo 🏀 Starting Dream11 Basketball Pro...
echo 📱 Opening Streamlit application...
echo 🌐 The app will open in your browser at http://localhost:8501
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if requirements file exists
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found. Please ensure you're in the correct directory.
    pause
    exit /b 1
)

REM Install requirements if needed
echo 📦 Installing/updating dependencies...
pip install -r requirements.txt

REM Run the Streamlit app
echo 🚀 Launching Dream11 Basketball Pro...
streamlit run dream11_basketball_pro.py

echo.
echo ✅ App closed. Thanks for using Dream11 Basketball Pro!
pause