#!/bin/bash

echo "Building Application..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/Upgrade required packages
pip install -r requirements.txt

# Build the application
pyinstaller --clean --name "نظام_الحضانة" --icon "images/Nursery-icon.ico" --noconsole main.py

echo "Build completed!"
echo "The executable can be found in the 'dist' folder."