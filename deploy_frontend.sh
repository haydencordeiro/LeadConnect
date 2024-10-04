#!/bin/bash

# Variables
REPO="leadconnect-frontend"
NODE_VERSION=18
DIST_DIR="./leadconnect-frontend/dist"
GITHUB_TOKEN="fae189123bjh1234jhg2"  # Hardcoded token
SERVER_NAME="leadconnectai.in"
SERVER_USER="root"
SSH_KEY="~/.ssh/id_rsa"  # Path to your SSH private key

# Exit immediately if a command exits with a non-zero status
set -e

# Function to deploy frontend
deploy_frontend() {
  echo "Deploying frontend to GitHub Pages..."

  # Check if the current branch is the main branch
  CURRENT_BRANCH=$(git branch --show-current)
  if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "Error: This script should be run on the 'main' branch. Current branch is '$CURRENT_BRANCH'. Exiting."
    exit 1
  fi

  # Checkout the latest code
  echo "Checking out the latest code..."
  git checkout main
  git pull origin main

  # Install nvm (Node Version Manager) if not already installed
  if ! command -v nvm &> /dev/null; then
    echo "nvm could not be found, installing..."
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
    source ~/.nvm/nvm.sh
  fi

  # Use the specified node version
  echo "Setting up Node.js version $NODE_VERSION..."
  nvm install $NODE_VERSION
  nvm use $NODE_VERSION

  # Navigate to the project directory
  cd $REPO

  # Install dependencies
  echo "Installing dependencies..."
  npm ci

  # Build the project
  echo "Building the project..."
  npm run build

  # Deploy to GitHub Pages
  echo "Deploying to GitHub Pages..."
  git init
  git add .
  git commit -m "Deploy to GitHub Pages"

  # Setup GitHub Pages
  if [ ! -d ".git" ]; then
    git init
  fi

  # Configure Git
  git config --global user.name "GitHub Actions"
  git config --global user.email "actions@github.com" #replace with your user email

  # Add the GitHub Pages remote URL
  REMOTE_REPO="https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
  git remote add origin $REMOTE_REPO || git remote set-url origin $REMOTE_REPO

  # Create a new orphan branch called gh-pages
  git checkout --orphan gh-pages

  # Remove all files from the previous state
  git rm -rf .

  # Copy the build files
  cp -r $DIST_DIR/* .

  # Commit the changes
  git add .
  git commit -m "Deploy to GitHub Pages"

  # Push the changes to the gh-pages branch
  git push --force origin gh-pages

  echo "Frontend deployment to GitHub Pages completed successfully."
}

# Run the deployment function
deploy_frontend
