#!/bin/bash
# execute with: source build_local.sh

echo "Building local environment"
echo "Installing python3-venv"
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3-venv
echo "Removing old venv"
rm -rf venv/
echo "Creating new venv"
python3 -m venv venv
echo "Activating venv"
source /workspaces/processing_service/venv/bin/activate
echo "Installing requirements"
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements.dev.txt