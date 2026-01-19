param hubName string
param projectName string
param location string = resourceGroup().location
param tags object = {}
param principalId string

resource hub 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = {
  name: hubName
  location: location
  tags: tags
  kind: 'Hub'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: hubName
    description: 'AI Foundry hub for trail guide agent'
  }
}

resource project 'Microsoft.MachineLearningServices/workspaces@2024-04-01' = {
  name: projectName
  location: location
  tags: tags
  kind: 'Project'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    friendlyName: projectName
    description: 'AI Foundry project for trail guide agent'
    hubResourceId: hub.id
  }
}

// Create a default GPT-4o deployment
resource modelDeployment 'Microsoft.MachineLearningServices/workspaces/onlineEndpoints@2024-04-01' = {
  parent: project
  name: 'gpt-4o'
  location: location
  kind: 'managedOnlineEndpoint'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    authMode: 'Key'
    description: 'GPT-4o deployment for trail guide agent'
  }
}

// Assign Cognitive Services User role to the principal
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = if (!empty(principalId)) {
  name: guid(project.id, principalId, 'CognitiveServicesUser')
  scope: project
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'a97b65f3-24c7-4388-baec-2e87135dc908')
    principalId: principalId
    principalType: 'User'
  }
}

output projectEndpoint string = project.properties.discoveryUrl
output projectId string = project.id
output hubId string = hub.id
output modelDeploymentName string = modelDeployment.name
