---
lab:
    title: 'Explore prompt engineering with Prompty'
    description: 'Learn how to use Prompty to quickly test and improve on different prompts with your language model and ensure that they are constructed and orchestrated for best results.'
---

## Explore prompt engineering with Prompty

This exercise takes approximately **45 minutes**.

> **Note**: This exercise assumes some familiarity with Azure AI Foundry, which is why some instructions are intentionally less detailed to encourage more active exploration and hands-on learning.

## Introduction

During ideation, you want to quickly test and improve on different prompts with your language model. There are various ways you can approach prompt engineering, through the playground in the Azure AI Foundry portal, or using Prompty for a more code-first approach.

In this exercise, you explore prompt engineering with Prompty in Azure Cloud Shell, using a model deployed through Azure AI Foundry.

## Set up the environment

To complete the tasks in this exercise, you need:

- An Azure AI Foundry hub,
- An Azure AI Foundry project,
- A deployed model (like GPT-4o).

### Create an Azure AI hub and project

> **Note**: If you already have an Azure AI project, you can skip this procedure and use your existing project.

You can create an Azure AI project manually through the Azure AI Foundry portal, as well as deploy the model used in the exercise. However, you can also automate this process through the use of a template application with [Azure Developer CLI (azd)](https://aka.ms/azd).

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

### Set up your virtual environment in Cloud Shell

To quickly experiment and iterate, you'll use a set of Python scripts in Cloud Shell.

1. In the Cloud Shell command-line pane, enter the following command to navigate to the folder with the code files used in this exercise:

     ```powershell
    cd ~/mslearn-genaiops/Files/03/
     ```

1. Enter the following commands to activate a virtual environment and install the libraries you need:

    ```powershell
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install python-dotenv openai tiktoken azure-ai-projects prompty[azure]
    ```

1. Enter the following command to open the configuration file that has been provided:

    ```powershell
   code .env
    ```

    The file is opened in a code editor.

1. In the code file, replace the **ENDPOINTNAME** and **APIKEY** placeholders with the endpoint and key values you copied earlier.
1. *After* you've replaced the placeholders, in the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

## Optimize system prompt

Minimizing the length of system prompts while maintaining functionality in generative AI is fundamental for large-scale deployments. Shorter prompts can lead to faster response times, as the AI model processes fewer tokens, and also uses fewer computational resources.

1. Enter the following command to open the application file that has been provided:

    ```powershell
   code optimize-prompt.py
    ```

    Review the code and note that the script executes the `start.prompty` template file that already has a pre-defined system prompt.

1. Run `code start.prompty` to review the system prompt. Consider how you might shorten it while keeping its intent clear and effective. For example:

   ```python
   original_prompt = "You are a helpful assistant. Your job is to answer questions and provide information to users in a concise and accurate manner."
   optimized_prompt = "You are a helpful assistant. Answer questions concisely and accurately."
   ```

   Remove redundant words and focus on the essential instructions. Save your optimized prompt in the file.

### Test and validate your optimization

Testing prompt changes is important to ensure you reduce token usage without losing quality.

1. Run `code token-count.py` to open and review the token counter app provided in the exercise. If you used an optimized prompt different than what was provided in the example above, you can use it in this app as well.

1. Run the script with `python token-count.py` and observe the difference in token count. Ensure the optimized prompt still produces high-quality responses.

## Analyze user interactions

Understanding how users interact with your app helps identify patterns that increase token usage.

1. Review a sample dataset of user prompts:

    - **"Summarize the plot of *War and Peace*."**
    - **"What are some fun facts about cats?"**
    - **"Write a detailed business plan for a startup that uses AI to optimize supply chains."**
    - **"Translate 'Hello, how are you?' into French."**
    - **"Explain quantum entanglement to a 10-year-old."**
    - **"Give me 10 creative ideas for a sci-fi short story."**

    For each, identify whether it is likely to result in a **short**, **medium**, or **long/complex** response from the AI.

1. Review your categorizations. What patterns do you notice? Consider:

    - Does the **level of abstraction** (e.g., creative vs factual) affect length?
    - Do **open-ended prompts** tend to be longer?
    - How does **instructional complexity** (e.g., “explain like I’m 10”) influence the response?

1. Enter the following command to run the **optimize-prompt** application:

    ```
   python optimize-prompt.py
    ```

1. Use some of the samples provided above to verify your analysis.
1. Now use the following long-form prompt and review its output:

    ```
   Write a comprehensive overview of the history of artificial intelligence, including key milestones, major contributors, and the evolution of machine learning techniques from the 1950s to today.
    ```

1. Rewrite this prompt to:

    - Limit the scope
    - Set expectations for brevity
    - Use formatting or structure to guide the response

1. Compare the responses to verify that you obtained a more concise answer.

> **NOTE**: You can use `token-count.py` to compare token usage in both responses.
<br>
<details>
<summary><b>Example of a rewritten prompt:</b></summary><br>
<p>“Give a bullet-point summary of 5 key milestones in AI history.”</p>
</details>

## [**OPTIONAL**] Apply your optimizations in a real scenario

1. Imagine you are building a customer support chatbot that must provide quick, accurate answers.
1. Integrate your optimized system prompt and template into the chatbot's code (*you can use `optimize-prompt.py` as a starting point*).
1. Test the chatbot with various user queries to ensure it responds efficiently and effectively.

## Conclusion

Prompt optimization is a key skill for reducing costs and improving performance in generative AI applications. By shortening prompts, using templates, and analyzing user interactions, you can create more efficient and scalable solutions.

## Clean up

If you've finished exploring Azure AI Services, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Return to the browser tab containing the Azure portal (or re-open the [Azure portal](https://portal.azure.com?azure-portal=true) in a new browser tab) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
