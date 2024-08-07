#!/bin/bash

# Variables
FRONTEND_SCRIPT="deploy_frontend.sh"
BACKEND_SCRIPT="deploy_backend.sh"

# Function to check for required dependencies
check_dependencies() {
  echo "Checking for required dependencies..."
  local dependencies=("ssh" "git" "nvm" "npm" "virtualenv")
  for cmd in "${dependencies[@]}"; do
    if ! command -v $cmd &> /dev/null; then
      echo "Error: $cmd is not installed. Please install it before proceeding."
      exit 1
    fi
  done
  echo "All required dependencies are installed."
}

# Main deployment function
main() {
  check_dependencies

  echo "Starting deployment..."

  # Deploy Frontend
  echo "Deploying frontend..."
  chmod +x $FRONTEND_SCRIPT
  ./$FRONTEND_SCRIPT

  if [ $? -ne 0 ]; then
    echo "Error: Frontend deployment failed."
    exit 1
  fi

  # Deploy Backend
  echo "Deploying backend..."
  chmod +x $BACKEND_SCRIPT
  ./$BACKEND_SCRIPT

  if [ $? -ne 0 ]; then
    echo "Error: Backend deployment failed."
    exit 1
  fi

  echo "Deployment completed successfully."
}

# Run the main function
main
