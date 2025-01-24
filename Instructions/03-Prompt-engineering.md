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

Let's start by deploying the necessary resources to work with this model in the Azure AI Foundry portal.

## Create an Azure AI hub and project

> **Note**: If you already have an Azure AI hub and project, you can skip this procedure and use your existing project.

You can create an Azure AI hub and project manually through the Azure AI Foundry portal, as well as deploy the model used in the exercise. However, you can also automate this process through the use of a template application with [Azure Developer CLI (azd)](https://aka.ms/azd).

1. In a web browser, open [Azure portal](https://portal.azure.com) at `https://portal.azure.com` and sign in using your Azure credentials.

1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal. For more information about using the Azure Cloud Shell, see the [Azure Cloud Shell documentation](https://docs.microsoft.com/azure/cloud-shell/overview).

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the PowerShell pane, enter the following commands to clone this exercise's repo:

     ```powershell
    rm -r mslearn-genaiops -f
    git clone https://github.com/MicrosoftLearning/mslearn-genaiops
     ```

1. After the repo has been cloned, enter the following commands to initialize the Starter template. 
   
     ```powershell
    cd ./mslearn-genaiops/Starter
    azd init
     ```

1. Once prompted, give the new environment a name as it will be used as basis for giving unique names to all the provisioned resources.
        
1. Next, enter the following command to run the Starter template. It will provision an AI Hub with dependent resources, AI project, AI Services and an online endpoint.

     ```powershell
    azd up
     ```

1. When prompted, choose which subscription you want to use and then choose one of the following locations for resource provision:
   - East US
   - East US 2
   - North Central US
   - South Central US
   - Sweden Central
   - West US
   - West US 3
    
1. Wait for the script to complete - this typically takes around 10 minutes, but in some cases may take longer.

    > **Note**: Azure OpenAI resources are constrained at the tenant level by regional quotas. The listed regions above include default quota for the model type(s) used in this exercise. Randomly choosing a region reduces the risk of a single region reaching its quota limit. In the event of a quota limit being reached, there's a possibility you may need to create another resource group in a different region. Learn more about [model availability per region](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=standard%2Cstandard-chat-completions#global-standard-model-availability)

    <details>
      <summary><b>Troubleshooting tip</b>: No quota available in a given region</summary>
        <p>If you receive a deployment error for any of the models due to no quota available in the region you chose, try running the following commands:</p>
        <ul>
          <pre><code>azd env set AZURE_ENV_NAME new_env_name
   azd env set AZURE_RESOURCE_GROUP new_rg_name
   azd env set AZURE_LOCATION new_location
   azd up</code></pre>
        Replacing <code>new_env_name</code>, <code>new_rg_name</code>, and <code>new_location</code> with new values. The new location must be one of the regions listed at the beginning of the exercise, e.g <code>eastus2</code>, <code>northcentralus</code>, etc.
        </ul>
    </details>

1. Once all resources have been provisioned, use the following commands to fetch the endpoint and access key to your AI Services resource. Note that you must replace `<rg-env_name>` and `<aoai-xxxxxxxxxx>` with the names of your resource group and AI Services resource. Both are printed in the deployment's output.

     ```powershell
    Get-AzCognitiveServicesAccount -ResourceGroupName <rg-env_name> -Name <aoai-xxxxxxxxxx> | Select-Object -Property endpoint
    Get-AzCognitiveServicesAccountKey -ResourceGroupName <rg-env_name> -Name <aoai-xxxxxxxxxx> | Select-Object -Property Key1
     ```

1. Copy these values as they will be used later on.
   
## Set up your local development environment

To quickly experiment and iterate, you'll use Prompty in Visual Studio (VS) Code. Let's get VS Code ready to use for local ideation.

1. Open VS Code and **Clone** the following Git repo: [https://github.com/MicrosoftLearning/mslearn-genaiops.git](https://github.com/MicrosoftLearning/mslearn-genaiops.git)
1. Store the clone on a local drive, and open the folder after cloning.
1. In the extensions pane in VS Code, search and install the **Prompty** extension.
1. In the VS Code Explorer (left pane), right-click on the **Files/03** folder.
1. Select **New Prompty** from the drop-down menu.
1. Open the newly created file named **basic.prompty**.
1. Run the Prompty file by selecting the **play** button at the top-right corner (or press F5).
1. When prompted to sign in, select **Allow**.
1. Select your Azure account and sign in.
1. Go back to VS Code, where an **Output** pane will open with an error message. The error message should tell you that the deployed model isn't specified or can't be found.

To fix the error, you need to configure a model for Prompty to use.

## Update prompt metadata

To execute the Prompty file, you need to specify the language model to use for generating the response. The metadata is defined in the *frontmatter* of the Prompty file. Let's update the metadata with the model configuration and other information.

1. Open the Visual Studio Code terminal pane.
1. Copy the **basic.prompty** file (in the same folder) and rename the copy to `chat-1.prompty`.
1. Open **chat-1.prompty** and update the following fields to change some basic information:

    - **Name**:

        ```yaml
        name: Python Tutor Prompt
        ```

    - **Description**:

        ```yaml
        description: A teaching assistant for students wanting to learn how to write and edit Python code.
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

1. Save the updated Prompty file.

The Prompty file now has all the necessary parameters, but some parameters use placeholders to obtain the required values. The placeholders are stored in the **.env** file in the same folder.

## Update model configuration

To specify which model Prompty uses, you need to provide your model's information in the .env file.

1. Open the **.env** file in the **Files/03** folder.
1. Update each of the placeholders with the values you copied earlier from the model deployment's output in the Azure Portal:

    ```yaml
    - AZURE_OPENAI_CHAT_DEPLOYMENT="gpt-4"
    - AZURE_OPENAI_ENDPOINT="<Your endpoint target URI>"
    - AZURE_OPENAI_API_KEY="<Your endpoint key>"
    ```

1. Save the .env file.
1. Run the **chat-1.prompty** file again.

You should now get an AI generated response, albeit unrelated to your scenario as it just uses the sample input. Let's update the template to make it an AI teaching assistant.

## Edit the sample section

The sample section specifies the inputs to the Prompty, and supplies default values to use if no inputs are provided.

1. Edit the fields of the following paramaters:

    - **firstName**: Choose any other name.
    - **context**: Remove this entire section.
    - **question**: Replace the provided text with:

    ```yaml
    What is the difference between 'for' loops and 'while' loops?
    ```

    You **sample** section should now look like this:
    
    ```yaml
    sample:
    firstName: Daniel
    question: What is the difference between 'for' loops and 'while' loops?
    ```

    1. Run the updated Prompty file and review the output.

