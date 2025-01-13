---
lab:
    title: 'Prompt engineering'
---

## Create an AI hub and project in the Azure AI Foundry portal

You start by creating an Azure AI Foundry portal project within an Azure AI hub:

1. In a web browser, open [https://ai.azure.com](https://ai.azure.com) and sign in using your Azure credentials.
1. From the home page, select **+ Create project**.
1. In the **Create a new project** wizard, create a project with the following settings:
    - **Project name**: *A unique name for your project*
    - Select **Customize**
        - **Hub**: *Autofills with default name*
        - **Subscription**: *Autofills with your signed in account*
        - **Resource group**: (New) *Autofills with your project name*
        - **Location**: Choose one of the following regions **East US2**, **North Central US**, **Sweden Central**, **Switzerland West**\*
        - **Connect Azure AI Services or Azure OpenAI**: (New) *Autofills with your selected hub name*
        - **Connect Azure AI Search**: Skip connecting

    > \* Azure OpenAI resources are constrained at the tenant level by regional quotas. The listed regions in the location helper include default quota for the model type(s) used in this exercise. Randomly choosing a region reduces the risk of a single region reaching its quota limit. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region. Learn more about [Fine-tuning model regions](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=python-secure%2Cglobal-standard%2Cstandard-chat-completions#fine-tuning-models)

1. Review your configuration and create your project.
1. Wait for your project to be created.



Clone the repo https://github.com/MicrosoftLearning/mslearn-genaiops.git
Install the Prompty extension

## Create new Prompty

1. In the VS Code Explorer (left pane), right-click on the new `sandbox` folder.
1. Select **New Prompty** from the drop-down menu.
1. Open the newly created file named **basic.prompty**.
1. Run the Prompty file by selecting the **play** button a the top-left corner (or press F5).
1. A new **Settings** tab opens, and an error message appears in the output window stating that the endpoint is missing.

To fix the error, you need to configure a model for Prompty to use.

## Update prompt metadata

To execute the Prompty file, you need to specify the language model to use for generating the response. The metadata is defined in the *frontmatter* of the Prompty file. Let's update the metadata with the model configuration and other information.

1. Open the Visual Studio Code terminal pane.
1. Use the following command to copy the existing Prompty file to a new one.

    ```python
    cp basic.prompty chat-0.prompty
    ```

1. Open **chat-0.prompty** and update the following fields to change some basic information:
    - **Name**:

        ```yaml
        name: Contoso Chat Prompt
        ```

    - **Description**:

        ```yaml
        description: A retail assistant for Contoso Outdoors products retailer.
        ```

    - **Deployed model**:

        ```yaml
        azure_deployment: ${env:AZURE_OPENAI_CHAT_DEPLOYMENT}
        ```

1. 
    
    
