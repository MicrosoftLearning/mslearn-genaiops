#!/bin/bash

# Variables
RESOURCE_GROUP="myResourceGroup"
LOCATION="eastus"
DEPLOYMENT_NAME="t5-small-deployment"
MODEL_NAME="t5-small"
WORKSPACE_NAME="myWorkspace"

# Create a resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create an Azure AI Foundry workspace
az ml workspace create --name $WORKSPACE_NAME --resource-group $RESOURCE_GROUP --location $LOCATION

# Deploy the t5-small model
az ml workspace model deploy --workspace-name $WORKSPACE_NAME --resource-group $RESOURCE_GROUP --name $DEPLOYMENT_NAME --model $MODEL_NAME

echo "Deployment of $MODEL_NAME completed successfully."