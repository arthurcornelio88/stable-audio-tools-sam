#!/bin/bash

# Function to install a package if not already installed
function install_if_not_installed {
    PACKAGE_NAME=$1
    if ! pip show $PACKAGE_NAME > /dev/null; then
        pip install $PACKAGE_NAME
    else
        echo "Requirement already satisfied: $PACKAGE_NAME"
    fi
}

# Activate Conda environment
source ~/miniconda3/etc/profile.d/conda.sh
conda activate myenv

# Install from requirements.txt
pip install -r requirements.txt

# Install additional packages if not already installed
install_if_not_installed stable-audio-tools
install_if_not_installed flash-attn
install_if_not_installed deepspeed

# Deactivate Conda environment
conda deactivate
