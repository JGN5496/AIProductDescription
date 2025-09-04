#!/bin/bash

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment and run the Flask app
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python not found in virtual environment"
    exit 1
fi

# Check if required packages are installed
if ! python -c "import flask, transformers, torch, dotenv" &> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

echo "🚀 Starting AI Product Description Generator..."
echo "📱 The application will be available at: http://localhost:8001"
echo "⏹️  Press Ctrl+C to stop the application"
echo ""
python app.py
