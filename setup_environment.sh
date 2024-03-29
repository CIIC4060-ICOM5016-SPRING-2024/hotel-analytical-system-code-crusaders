#!/bin/bash

# Define the name of the virtual environment
VENV_NAME="virtual-application"

# Check if virtualenv is installed, if not install it
if ! command -v virtualenv &> /dev/null; then
    echo "Installing virtualenv..."
    pip install virtualenv
fi

# Create a virtual environment
echo "Creating virtual environment..."
virtualenv "$VENV_NAME"

# Activate the virtual environment
source "$VENV_NAME/bin/activate"

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Virtual environment created and dependencies installed successfully."
