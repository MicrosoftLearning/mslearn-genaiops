---
lab:
    title: 'Optimize your model using a synthetic dataset'
    description: 'Learn how to create synthetic datasets and use them to enhance performance and reliability of your model.'
---

## Optimize your model using a synthetic dataset

Optimizing a generative AI application involves leveraging datasets to enhance the model's performance and reliability. By using synthetic data, developers can simulate a wide range of scenarios and edge cases that might not be present in real-world data. Furthermore, the evaluation of the model's outputs is crucial to obtain high-quality and reliable AI applications. The entire optimization and evaluation process can be efficiently managed using the Azure AI Evaluation SDK, which provides robust tools and frameworks to streamline these tasks.

This exercise will take approximately **30** minutes\*

> \* This estimate does not include the optional task at the end of the exercise.
## Scenario

Imagine you want to build an AI-powered smart guide app to enhance visitors' experiences in a museum. The app aims to answer questions about historical figures. To evaluate the responses from the app, you need to create a comprehensive synthetic question-answer dataset that covers various aspects of these personalities and their work.

You've selected a GPT-4 model to provide generative answers. You now want to put together a simulator that generates contextually relevant interactions, evaluating the AI's performance across different scenarios.

Let's start by deploying the necessary resources to build this application.

## Create an Azure AI hub and project

You can create an Azure AI hub and project manually through the Azure AI Foundry portal, as well as deploy the models used in the exercise. However, you can also automate this process through the use of a template application with [Azure Developer CLI (azd)](https://aka.ms/azd).

1. In a web browser, open [Azure portal](https://portal.azure.com) at `https://portal.azure.com` and sign in using your Azure credentials.

1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal. For more information about using the Azure Cloud Shell, see the [Azure Cloud Shell documentation](https://docs.microsoft.com/azure/cloud-shell/overview).

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the Cloud Shell toolbar, in the **Settings** menu, select **Go to Classic version**.

    **<font color="red">Ensure you've switched to the Classic version of the Cloud Shell before continuing.</font>**

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
     ```

     ```powershell
    Get-AzCognitiveServicesAccountKey -ResourceGroupName <rg-env_name> -Name <aoai-xxxxxxxxxx> | Select-Object -Property Key1
     ```

1. Copy these values as they will be used later on.

## Set up your development environment in Cloud Shell

To quickly experiment and iterate, you'll use a set of Python scripts in Cloud Shell.

1. In the Cloud Shell command-line pane, enter the following command to navigate to the folder with the code files used in this exercise:

     ```powershell
    cd ~/mslearn-genaiops/Files/06/
     ```

1. Enter the following commands to activate a virtual environment and install the libraries you need:

    ```powershell
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install python-dotenv azure-ai-evaluation azure-ai-projects promptflow wikipedia aiohttp openai==1.77.0
    ```

1. Enter the following command to open the configuration file that has been provided:

    ```powershell
   code .env
    ```

    The file is opened in a code editor.

1. In the code file, replace the **your_azure_openai_service_endpoint** and **your_azure_openai_service_api_key** placeholders with the endpoint and key values you copied earlier.
1. *After* you've replaced the placeholders, in the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

## Generate synthetic data

You'll now run a script that generates a synthetic dataset and uses it to evaluate the quality of your pre-trained model.

1. Run the following command to **edit the script** that has been provided:

    ```powershell
   code generate_synth_data.py
    ```

1. In the script, locate **# Define callback function**.
1. Below this comment, paste the following code:

    ```
    async def callback(
        messages: List[Dict],
        stream: bool = False,
        session_state: Any = None,  # noqa: ANN401
        context: Optional[Dict[str, Any]] = None,
    ) -> dict:
        messages_list = messages["messages"]
        # Get the last message
        latest_message = messages_list[-1]
        query = latest_message["content"]
        context = text
        # Call your endpoint or AI application here
        current_dir = os.getcwd()
        prompty_path = os.path.join(current_dir, "application.prompty")
        _flow = load_flow(source=prompty_path)
        response = _flow(query=query, context=context, conversation_history=messages_list)
        # Format the response to follow the OpenAI chat protocol
        formatted_response = {
            "content": response,
            "role": "assistant",
            "context": context,
        }
        messages["messages"].append(formatted_response)
        return {
            "messages": messages["messages"],
            "stream": stream,
            "session_state": session_state,
            "context": context
        }
    ```

    You can bring any application endpoint to simulate against by specifying a target callback function. In this case, you will use an application that is an LLM with a Prompty file `application.prompty`. The callback function above processes each message generated by the simulator by performing the following tasks:
    * Retrieves the latest user message.
    * Loads a prompt flow from application.prompty.
    * Generates a response using the prompt flow.
    * Formats the response to adhere to the OpenAI chat protocol.
    * Appends the assistant's response to the messages list.

    >**Note**: For more information about using Prompty, see [Prompty's documentation](https://www.prompty.ai/docs).

1. Next, locate **# Run the simulator**.
1. Below this comment, paste the following code:

    ```
    model_config = {
        "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
        "azure_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    }
    
    simulator = Simulator(model_config=model_config)
    
    outputs = asyncio.run(simulator(
        target=callback,
        text=text,
        num_queries=1,  # Minimal number of queries
    ))
    
    output_file = "simulation_output.jsonl"
    with open(output_file, "w") as file:
        for output in outputs:
            file.write(output.to_eval_qr_json_lines())
    ```

   The code above will initialize the simulator and run it to generate synthetic conversations based on a text previously extracted from Wikipedia.

1. Next, locate **# Evaluate the model**.
1. Below this comment, paste the following code:

    ```
    groundedness_evaluator = GroundednessEvaluator(model_config=model_config)
    eval_output = evaluate(
        data=output_file,
        evaluators={
            "groundedness": groundedness_evaluator
        },
        output_path="groundedness_eval_output.json"
    )
    ```

    Now that you have a dataset, you can evaluate the quality and effectiveness of your generative AI application. In the code above, you will use groundedness as your quality metric.

1. Save your changes.
1. In the Cloud Shell command-line pane beneath the code editor, enter the following command to **run the script**:

    ```
   python generate_synth_data.py
    ```

    Once the script is finished, you can download the output files by running `download simulation_output.jsonl` and `download groundedness_eval_output.json` and review their contents. If the groundedness metric isn't close to 3.0, you can change the LLM parameters such as `temperature`, `top_p`, `presence_penalty` or `frequency_penalty` in the `application.prompty` file and re-run the script to generate a new dataset for evaluation. You can also change the `wiki_search_term` to obtain a synthetic dataset based on a different context.

## (OPTIONAL) Fine-tune your model

If you have extra time, you can use the generated dataset to fine-tune your model in Azure AI Foundry. Fine-tuning is dependent on cloud infrastructure resources, which can take a variable amount of time to provision depending on data center capacity and concurrent demand.

1. Open a new browser tab and navigate to [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials.
1. In the AI Foundry's home page, select the project you created at the beginning of the exercise.
1. Navigate to the **Fine-tuning** page under the **Build and customize** section, using the menu on the left.
1. Select the button to add a new fine-tune model, select the **gpt-4o** model and then select **Next**.
1. **Fine-tune** the model using the following configuration:
    - **Model version**: *Select the default version*
    - **Method of customization**: Supervised
    - **Model suffix**: `ft-travel`
    - **Connected AI resource**: *Select the connection that was created when you created your hub. Should be selected by default.*
    - **Training data**: Upload files

    <details>  
    <summary><b>Troubleshooting tip</b>: Permissions error</summary>
    <p>If you receive a permissions error, try the following to troubleshoot:</p>
    <ul>
        <li>In the Azure portal, select the AI Services resource.</li>
        <li>Under Resource Management, in the Identity tab, confirm that it's system assigned managed identity.</li>
        <li>Navigate to the associated Storage Account. On the IAM page, add the role assignment <em>Storage Blob Data Owner</em>.</li>
        <li>Under <strong>Assign access to</strong>, choose <strong>Managed Identity</strong>, <strong>+ Select members</strong>, select the <strong>All system-assigned managed identities</strong>, and select your Azure AI services resource.</li>
        <li>Review and assign to save the new settings and retry the previous step.</li>
    </ul>
    </details>

    - **Upload file**: Select the JSONL file you downloaded in a previous step.
    - **Validation data**: None
    - **Task parameters**: *Keep the default settings*
1. Fine-tuning will start and may take some time to complete.

    > **Note**: Fine-tuning and deployment can take a significant amount of time (30 minutes or longer), so you may need to check back periodically. You can see more details of the progress so far by selecting the fine-tuning model job and viewing its **Logs** tab.

## (OPTIONAL) Deploy the fine-tuned model

When fine-tuning has successfully completed, you can deploy the fine-tuned model.

1. Select the fine-tuning job link to open its details page. Then, select the **Metrics** tab and explore the fine-tune metrics.
1. Deploy the fine-tuned model with the following configurations:
    - **Deployment name**: *A valid name for your model deployment*
    - **Deployment type**: Standard
    - **Tokens per Minute Rate Limit (thousands)**: 5K *(or the maximum available in your subscription if less than 5K)
    - **Content filter**: Default
1. Wait for the deployment to be complete before you can test it, this might take a while. Check the **Provisioning state** until it has succeeded (you may need to refresh the browser to see the updated status).
1. When the deployment is ready, navigate to the fine-tuned model and select **Open in playground**.

    Now that you deployed your fine-tuned model, you can test it in the Chat playground like you would with any base model.

## Conclusion

In this exercise you created a synthetic dataset simulating a conversation between an user and a chat completion app. By using this dataset, you can evaluate the quality of your app's responses and fine-tune it to achieve the desired results.

## Clean up

If you've finished exploring Azure AI Services, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Return to the browser tab containing the Azure portal (or re-open the [Azure portal](https://portal.azure.com?azure-portal=true) in a new browser tab) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
