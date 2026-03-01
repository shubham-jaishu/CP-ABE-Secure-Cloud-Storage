#!/bin/bash

# Installation script for CP-ABE Secure Cloud Storage System

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   CP-ABE Secure Cloud Storage System - Installation      ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✅ Python $PYTHON_VERSION found"
else
    echo "❌ Python 3 is not installed"
    echo "   Please install Python 3.8 or higher"
    exit 1
fi

# Check pip
echo ""
echo "🔍 Checking pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 found"
else
    echo "❌ pip3 is not installed"
    echo "   Please install pip3"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "   Recreate? (y/n): " recreate
    if [ "$recreate" = "y" ]; then
        rm -rf venv
        python3 -m venv venv
        echo "✅ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ All dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p encrypted_files metadata
echo "✅ Directories created"

# Check AWS CLI (optional)
echo ""
echo "🔍 Checking AWS CLI (optional for S3 storage)..."
if command -v aws &> /dev/null; then
    AWS_VERSION=$(aws --version 2>&1)
    echo "✅ AWS CLI found: $AWS_VERSION"
else
    echo "⚠️  AWS CLI not found (optional)"
    echo "   Install if you plan to use S3 storage:"
    echo "   pip install awscli"
fi

# Check Docker (optional)
echo ""
echo "🔍 Checking Docker (optional)..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version 2>&1)
    echo "✅ Docker found: $DOCKER_VERSION"
else
    echo "⚠️  Docker not found (optional)"
    echo "   Install if you plan to use Docker deployment"
fi

# Installation complete
echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║              ✅ Installation Complete!                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1️⃣  Start the server:"
echo "   python3 app.py"
echo ""
echo "2️⃣  Test the system (in another terminal):"
echo "   cd $(pwd)"
echo "   source venv/bin/activate"
echo "   python3 test_system.py"
echo ""
echo "3️⃣  Try the web interface:"
echo "   Open web_interface.html in your browser"
echo ""
echo "4️⃣  Run examples:"
echo "   python3 examples.py"
echo ""
echo "📚 Documentation:"
echo "   • Quick Start:  QUICKSTART.md"
echo "   • User Guide:   README.md"
echo "   • Deployment:   DEPLOYMENT.md"
echo "   • Overview:     PROJECT_SUMMARY.md"
echo ""
echo "🎉 Happy encrypting!"
