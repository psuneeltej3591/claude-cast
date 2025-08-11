#!/bin/bash

# Cric Opto - Dream11 Cricket Optimization Launcher Script
# This script sets up and runs the Cric Opto application

echo "🏏 Cric Opto - Dream11 Cricket Optimization"
echo "=============================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher and try again"
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python version $python_version is too old"
    echo "Please install Python 3.8 or higher and try again"
    exit 1
fi

echo "✅ Python $python_version detected"

# Check if virtual environment exists
if [ ! -d "cric_opto_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv cric_opto_env
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        echo "Trying to install dependencies globally..."
        echo "Installing required packages..."
        pip3 install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "❌ Failed to install dependencies"
            exit 1
        fi
    else
        echo "✅ Virtual environment created"
    fi
fi

# Activate virtual environment if it exists
if [ -d "cric_opto_env" ]; then
    echo "🔧 Activating virtual environment..."
    source cric_opto_env/bin/activate
    
    echo "📦 Installing/updating dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
    echo "✅ Dependencies installed"
fi

echo ""
echo "🚀 Starting Cric Opto application..."
echo "The app will open in your default web browser"
echo "If it doesn't open automatically, go to: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run the application
streamlit run cric_opto.py --server.headless true