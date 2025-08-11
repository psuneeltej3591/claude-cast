#!/bin/bash

echo "🏀 Starting Dream11 Basketball Pro..."
echo "📱 Opening Streamlit application..."
echo "🌐 The app will open in your browser at http://localhost:8501"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if requirements are installed
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Please ensure you're in the correct directory."
    exit 1
fi

# Install requirements if needed
echo "📦 Installing/updating dependencies..."
pip3 install -r requirements.txt

# Run the Streamlit app
echo "🚀 Launching Dream11 Basketball Pro..."
streamlit run dream11_basketball_pro.py

echo ""
echo "✅ App closed. Thanks for using Dream11 Basketball Pro!"