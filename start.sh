#!/bin/bash

# Quick Start Script for CP-ABE Secure Cloud Storage System

echo "================================================"
echo "CP-ABE Secure Cloud Storage - Quick Start"
echo "================================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "================================================"
echo "Starting Flask Application..."
echo "================================================"
echo ""
echo "Server will be available at: http://localhost:5000"
echo ""
echo "To test the system, open another terminal and run:"
echo "  cd $(pwd)"
echo "  source venv/bin/activate"
echo "  python test_system.py"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Flask app
python app.py
