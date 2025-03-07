#!/bin/bash

# Exit on error
set -e

# Initialize pyenv
eval "$(pyenv init -)"
eval "$(pyenv init --path)"

# Check Python version
python_version=$(python3 -V 2>/dev/null || echo "")
if [[ ! $python_version == *"3.13.1"* ]]; then
    echo "System Python is not 3.13.1, trying pyenv..."
    # Try to use pyenv
    if command -v pyenv &>/dev/null; then
        # Check if Python 3.13.1 is installed in pyenv
        if ! pyenv versions | grep -q "3.13.1"; then
            echo "Python 3.13.1 is not installed in pyenv."
            echo "Available Python 3.13.x versions:"
            pyenv install --list | grep "^  3.13"
            echo "\nTo install Python 3.13.1, run:"
            echo "pyenv install 3.13.1"
            exit 1
        fi
        echo "Setting Python version to 3.13.1 using pyenv..."
        pyenv local 3.13.1
        python_version=$(python3 -V)
    else
        echo "Error: Python 3.13.1 not found and pyenv is not installed"
        echo "Please install Python 3.13.1 or install pyenv and run: pyenv install 3.13.1"
        exit 1
    fi
fi

# Final version check
if [[ ! $python_version == *"3.13.1"* ]]; then
    echo "Error: Could not set Python version to 3.13.1"
    echo "Current version: $python_version"
    echo "Please install Python 3.13.1 via pyenv:"
    echo "pyenv install 3.13.1"
    exit 1
fi

echo "Using Python version: $python_version"

# Remove existing virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf .venv
fi

# Create new virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Setup virtual environment
source .venv/bin/activate && pip install --upgrade pip && pip install poetry

# Configure poetry to use the local virtual environment
poetry config virtualenvs.in-project true
poetry config virtualenvs.path ".venv"

# Install dependencies
echo "Installing project dependencies..."
poetry install --no-interaction

echo "Local development environment setup complete!"
echo "Python version: $(python3 -V)"
echo "Poetry version: $(poetry --version)"
echo "To activate the virtual environment, run: source .venv/bin/activate" 
