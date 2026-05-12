#!/bin/bash

# Arcade Launcher Setup & Run Script (Linux)

# Get script directory (USB root location)
DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PATH="$DIR/venv"

sudo apt update
sudo apt install -y python3-pip python3.12-venv wine openjdk-17-jdk

# If venv doesn't exist, create it and install dependencies
if [ ! -d "$VENV_PATH" ]; then
    echo "🔥 First-time setup: Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
    source "$VENV_PATH/bin/activate"
    echo "📦 Installing requirements..."
    pip install --upgrade pip
    pip install py5
    pip install pynput
else
    echo "✅ Environment detected — launching instantly..."
    source "$VENV_PATH/bin/activate"
fi

# Launch your arcade launcher
echo "🎮 Starting arcade launcher..."
python "$DIR/launcherLinux.py"
