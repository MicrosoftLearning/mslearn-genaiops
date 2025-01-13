---
lab:
    title: 'Explore prompt engineering with Prompty'
---

## Explore prompt engineering with Prompty

During ideation, you want to quickly test and improve on different prompts with your language model. There are various ways you can approach prompt engineering, through the playground in the Azure AI Foundry portal, or using Prompty for a more code-first approach.

In this exercise, you explore prompt engineering with Prompty in Visual Studio Code, using a model deployed through Azure AI Foundry.

This exercise will take approximately **40** minutes.

## Scenario

Imagine you want to build an app to help students learn how to code in Python. In the app, you want an automated tutor that can help students write and evaluate code. However, you don't want the chat app to just provide all the answers. You want students to receive personalized hints that encourage them to think about how to proceed.

You've selected a GPT-4 model to start experimenting with. You now want to apply prompt engineering to guide the chat's behavior into being a tutor that generates personalized hints.

Let's start by deploying a model through Azure AI Foundry, that you then can use for local ideation with Prompty.

## Create an AI project in the Azure AI Foundry portal

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

    > \* Azure OpenAI resources are constrained at the tenant level by regional quotas. The listed regions in the location helper include default quota for the model type(s) used in this exercise. Randomly choosing a region reduces the risk of a single region reaching its quota limit. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region. Learn more about [Azure OpenAI model regions](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=python-secure%2Cglobal-standard%2Cstandard-chat-completions#fine-tuning-models)

1. Review your configuration and create your project.
1. Wait for your project to be created.

## Deploy the model

When you have an AI project, you can deploy a GPT-4 model.

1. Navigate to the **Models + endpoints** page using the menu on the left.
1. Deploy a `gpt-4` base model, with the default settings. Select **Customize** to ensure the **Tokens per Minute Rate Limit** is set to **10K**.
1. When the model is deployed, copy the following values from the deployment overview page and store them in a notepad:

![Screenshot of the required variables](./images/environment-variables.png)

    - **Deployment name**.
    - **Endpoint target URI**.
    - **Endpoint key**

## Set up your local development environment

To quickly experiment and iterate, you'll use Prompty in Visual Studio (VS) Code. Let's get VS Code ready to use for local ideation.

1. Open VS Code and **Clone** the following Git repo: [https://github.com/MicrosoftLearning/mslearn-genaiops.git](https://github.com/MicrosoftLearning/mslearn-genaiops.git)
1. Store the clone on a local drive, and open the folder after cloning.
1. In the extensions pane in VS Code, search and install the **Prompty** extension.
1. In the VS Code Explorer (left pane), right-click on the **Files/03** folder.
1. Select **New Prompty** from the drop-down menu.
1. Open the newly created file named **basic.prompty**.
1. Run the Prompty file by selecting the **play** button a the top-left corner (or press F5).
1. An **Output** pane will open with an error message. The error message should tell you that the deployed model isn't specified or can't be found.

To fix the error, you need to configure a model for Prompty to use.

## Update prompt metadata

To execute the Prompty file, you need to specify the language model to use for generating the response. The metadata is defined in the *frontmatter* of the Prompty file. Let's update the metadata with the model configuration and other information.

1. Open the Visual Studio Code terminal pane.
1. Copy the **basic.prompty** file (in the same folder) and rename the copy to `chat-1.prompty`.
1. Open **chat-1.prompty** and update the following fields to change some basic information:

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

1. Next, add the following placeholder for the API key under the **azure_deployment** parameter.

    - **Endpoint key**:

        ```yaml
        api_key: ${env:AZURE_OPENAI_API_KEY}
        ```