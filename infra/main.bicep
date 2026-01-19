targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Id of the user or app to assign application roles')
param principalId string = ''

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

module ai 'core/ai/hub.bicep' = {
  name: 'ai'
  scope: rg
  params: {
    hubName: '${abbrs.cognitiveServicesAccounts}hub-${resourceToken}'
    projectName: '${abbrs.cognitiveServicesAccounts}project-${resourceToken}'
    location: location
    tags: tags
    principalId: principalId
  }
}

output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = rg.name
output PROJECT_ENDPOINT string = ai.outputs.projectEndpoint
output MODEL_DEPLOYMENT_NAME string = ai.outputs.modelDeploymentName
