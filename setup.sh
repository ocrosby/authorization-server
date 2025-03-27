#!/usr/bin/env zsh

# Check if the virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Deactivating the current virtual environment..."
    deactivate
fi

# Remove the .venv directory if it exists
if [[ -d ".venv" ]]; then
    echo "Removing the existing .venv directory..."
    rm -rf .venv
fi

# Create a new virtual environment
python3.13 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install the required packages
pip install invoke flit
pip install -e ".[dev]"
