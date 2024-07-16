#!/bin/bash

# Manually initialize Conda in the current shell
eval "$(/home/arthurcornelio/miniconda3/bin/conda shell.bash hook)"

# Check if the environment exists
if conda env list | grep -q "myenv"; then
    echo "Environment 'myenv' already exists"
else
    # Create the Conda environment with Python 3.10
    conda create -n myenv python=3.10 -y
fi

# Activate the environment and install Jupyter
conda activate myenv
conda install jupyter -y

# Deactivate the environment
conda deactivate

echo "Environment 'myenv' is set up and Jupyter is installed."
