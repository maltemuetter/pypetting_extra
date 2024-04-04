#!/bin/bash

# Define your environment name and Python version
ENV_NAME="pypetting_extra_env"
PYTHON_VERSION="3.12.0" # Replace with the version you want

# Create the virtual environment
pyenv virtualenv $PYTHON_VERSION $ENV_NAME

# Set the local environment to use the created virtual environment
pyenv local $ENV_NAME

# Install packages (add your packages here)
pip install git+https://github.com/sirno/pypetting.git@main
pip install numpy pandas

# Generate the requirements.txt file
pip freeze > requirements.txt

echo "Virtual environment '$ENV_NAME' created and configured."
