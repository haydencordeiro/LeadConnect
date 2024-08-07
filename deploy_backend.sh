#!/bin/bash

# Variables
REPO="api-server-flask"
SERVER_NAME="leadconnectai.in"
SERVER_USER="root"
SERVER_DIR="/path/to/server/$REPO"  # Replace with your app's directory on the server
SSH_KEY="~/.ssh/id_rsa"  # Path to your SSH private key
VENV_DIR="venv"  # Virtual environment directory

# Exit immediately if a command exits with a non-zero status
set -e

# Function to deploy backend
deploy_backend() {
  echo "Deploying backend to DigitalOcean Server..."

  # SSH into the server and set up the virtual environment
  ssh -i $SSH_KEY $SERVER_USER@$SERVER_NAME << EOF
    set -e
    echo "Navigating to server directory..."
    cd $SERVER_DIR

    # Check if virtual environment exists, create if it doesn't
    if [ ! -d "$VENV_DIR" ]; then
      echo "Creating virtual environment..."
      virtualenv -p python3 $VENV_DIR
    fi

    echo "Activating virtual environment..."
    source $VENV_DIR/bin/activate

    echo "Pulling latest code..."
    git pull origin main

    echo "Installing Python dependencies..."
    pip install -r requirements.txt

    echo "Setting environment variables..."
    export FLASK_APP=run.py
    export FLASK_ENV=development

    echo "Running Flask server..."
    nohup flask run --host=0.0.0.0 --port=5137 &

    echo "Backend deployment completed successfully."
    exit
EOF
}

# Run the deployment function
deploy_backend
