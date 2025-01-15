---
lab:
    title: 'Compare language models from the model catalog'
---

## Compare language models from the model catalog

When you have defined your use case, you can use the model catalog to explore whether an AI model solves your problem. You can use the model catalog to select models to deploy, which you can then compare to explore which model best meets your needs.

In this exercise, you compare two language models through the model catalog in Azure AI Foundry portal.

This exercise will take approximately **25** minutes.

## Scenario

Imagine you want to build an app to help students learn how to code in Python. In the app, you want an automated tutor that can help students write and evaluate code. In one exercise, students need to come up with the necessary Python code to plot a pie chart, based on the following example image:

![Pie chart showing marks obtained in an exam with sections for maths (34.9%), physics (28.6%), chemistry (20.6%), and English (15.9%)](./images/demo.png)

You need to select a language model that accepts images as input, and is able to generate accurate code. The available models that meet those criteria are GPT-4 Turbo, GPT-4o, and GPT-4o mini.

Let's start by deploying the necessary resources to work with these models in the Azure AI Foundry portal.

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

1. Once prompted, give a name to the new environment as it will be used as basis for giving unique names to all the provisioned resources.
        
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
    
## Compare the models

You know that there are three models that accept images as input whose inference infrastructure is fully managed by Azure. Now, you need to compare them to decide which one is ideal for our use case.

1. In a web browser, open [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials.
1. If prompted, select the AI project created earlier.
1. Navigate to the **Model catalog** page using the menu on the left.
1. Select **Compare models** (find the button next to the filters in the search pane).
1. Remove the selected models.
1. One by one, add the three models you want to compare: **gpt-4**, **gpt-4o**, and **gpt-4o-mini**. For **gpt-4**, make sure that the selected version is **turbo-2024-04-09**, as it is the only version that accepts images as input.
1. Change the x-axis to **Accuracy**.
1. Ensure the y-axis is set to **Cost**.

Review the plot and try to answer the following questions:

- *Which model is more accurate?*
- *Which model is cheaper to use?*

The benchmark metric accuracy is calculated based on publicly available generic datasets. From the plot we can already filter out one of the models, as it has the highest cost per token but not the highest accuracy. Before making a decision, let's explore the quality of outputs of the two remaining models specific to your use case.

## Filter for precision

In your use case, you want the model to provide accurate responses when a student asks for a code sample. As a test, let's take the image of a pie chart and ask each model to write code to create the image.

1. Download the pie chart image from the following URL, and store it locally: [https://github.com/MicrosoftLearning/mslearn-genaiops/blob/main/Instructions/images/demo.png](https://raw.githubusercontent.com/MicrosoftLearning/mslearn-genaiops/refs/heads/main/Instructions/images/demo.png)
1. Navigate to the **Playground** page using the menu on the left. And open the **Chat playground**.
1. In the setup pane, select the **gpt-4o** model for deployment.
1. Attach the **demo.png** image and add the prompt: `Please create Python code for image`
1. To easily compare, open the portal in another tab: [ai.azure.com](ai.azure.com).
1. In the newly opened tab, navigate to the playground and make sure the chat is empty. Use the sweeping broom icon to clear the chat if needed.
1. Use the exact same prompt with the deployed **gpt-4o-mini** model.
1. Optionally, you can add aditional prompts to improve the code. For example: `Add a legend to the plot replacing the labels`
You now have two code snippets that a student could use to generate a pie chart. Review the code and try to answer the following questions:

- *How do the two code snippets differ?*
- *Which output would you prefer as a student?*

**Optionally**, you can run the code and explore how the output differs.

## Filter for performance

Now that you have tested both models, you can explore their metrics to evaluate their performance.

1. Navigate to **Models + endpoints**.
1. Select a model, and navigate to the **Metrics** tab.
1. Select the **Last day** filter to get a better view on the tokens usage and requests per minute.
1. Repeat these steps for the other model.

The resulting views allow you to compare the token usage per model. Try to answer the following questions:

- *Which model had a higher token usage?*
- *Why did this model have a higher token usage?*

**Optionally**, you can get a more detailed view if you select **Open in Azure Monitor**. In the Azure portal, you can also explore the costs for each resource.

## Clean up

If you've finished exploring Azure AI Foundry portal, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Return to the browser tab containing the Azure portal (or re-open the [Azure portal](https://portal.azure.com?azure-portal=true) in a new browser tab) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
