#!/bin/bash

# GenAI Ops Infrastructure Deployment Script
# This script deploys the Microsoft Foundry workspace and AI services

set -e

ENVIRONMENT=${1:-development}
RESOURCE_GROUP_NAME="genaiops-$ENVIRONMENT-rg"
LOCATION=${2:-eastus}

echo "Deploying GenAI Ops infrastructure for environment: $ENVIRONMENT"
echo "Resource Group: $RESOURCE_GROUP_NAME"
echo "Location: $LOCATION"

# Create resource group
az group create --name $RESOURCE_GROUP_NAME --location $LOCATION

# Deploy main Bicep template
az deployment group create \
  --resource-group $RESOURCE_GROUP_NAME \
  --template-file infrastructure/bicep/main.bicep \
  --parameters environment=$ENVIRONMENT

echo "Deployment completed successfully!"