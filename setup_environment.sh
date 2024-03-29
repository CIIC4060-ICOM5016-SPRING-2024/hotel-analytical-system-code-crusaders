#!/bin/bash

# Define the name of the virtual environment
VENV_NAME="virtual-application"

# Create the virtual enviroment
echo "Creating virtual environment..."
python3 -m venv $VENV_NAME

# Activate the virtual environment
echo "Activating virtual environment..."
source ./$VENV_NAME/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Virtual environment created and dependencies installed successfully."

deactivate
