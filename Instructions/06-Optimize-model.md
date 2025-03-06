---
lab:
    title: 'Optimize your model using a synthetic dataset'
    description: 'Learn how to create synthetic datasets and use them to enhance a model's performance and reliability.'
---

## Optimize your model using a synthetic dataset

Optimizing a generative AI application involves leveraging datasets to enhance the model's performance and reliability. By using synthetic data, developers can simulate a wide range of scenarios and edge cases that might not be present in real-world data. Furthermore, the evaluation of the model's outputs is crucial to obtain high-quality and reliable AI applications. The entire optimization and evaluation process can be efficiently managed using the Azure AI Evaluation SDK, which provides robust tools and frameworks to streamline these tasks.

## Scenario

Imagine you want to build an AI-powered smart guide app to enhance visitors' experiences in a museum. The app aims to answer questions about historical figures. To evaluate the responses from the app, you need to create a comprehensive synthetic question-answer dataset that covers various aspects of these personalities and their work.

You've selected a GPT-4 model to provide generative answers. You now want to put together a simulator that generates contextually relevant interactions, evaluating the AI's performance across different scenarios.

Let's start by deploying the necessary resources to build this application.

## Create an Azure AI hub and project

You can create an Azure AI hub and project manually through the Azure AI Foundry portal, as well as deploy the models used in the exercise. However, you can also automate this process through the use of a template application with [Azure Developer CLI (azd)](https://aka.ms/azd).

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

1. Next, enter the following command to run the Starter template. It will provision an AI Hub with dependent resources, AI project, AI Services and an online endpoint. It will also deploy the models GPT-4 Turbo, GPT-4o, and GPT-4o mini.

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

To quickly experiment and iterate, you'll use a notebook with Python code in Visual Studio (VS) Code. Let's get VS Code ready to use for local ideation.

1. Open VS Code and **Clone** the following Git repo: [https://github.com/MicrosoftLearning/mslearn-genaiops.git](https://github.com/MicrosoftLearning/mslearn-genaiops.git)
1. Store the clone on a local drive, and open the folder after cloning.
1. In the VS Code Explorer (left pane), open the notebook **06-Optimize-your-model.ipynb** in the **Files/06** folder.
1. Run all cells in the notebook.

## Clean up

If you've finished exploring Azure AI Services, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Return to the browser tab containing the Azure portal (or re-open the [Azure portal](https://portal.azure.com?azure-portal=true) in a new browser tab) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
