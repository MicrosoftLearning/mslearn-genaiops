#!/bin/bash

# Environment Setup Script for GenAI Ops
# Sets up the development environment with required dependencies

set -e

echo "Setting up GenAI Ops development environment..."

# Check prerequisites
if ! command -v az &> /dev/null; then
    echo "Azure CLI not found. Please install Azure CLI first."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Please install Python 3.9+ first."
    exit 1
fi

# Install Python dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Install Azure Bicep CLI
echo "Installing Bicep CLI..."
az bicep install

# Login to Azure (if not already logged in)
if ! az account show &> /dev/null; then
    echo "Please log in to Azure..."
    az login
fi

echo "Environment setup completed successfully!"
echo "You can now run: ./infrastructure/scripts/deploy.sh"