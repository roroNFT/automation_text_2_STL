#!/bin/bash
# Script de démarrage rapide pour l'automation 3D

set -e

echo "==================================="
echo "3D Model Automation - Quick Start"
echo "==================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found!"
    echo "Please copy .env.example to .env and add your API keys"
    echo "Command: cp .env.example .env"
    exit 1
fi

# Run the main script
cd src
echo ""
echo "Running automation..."
echo ""
python main.py "$@"
