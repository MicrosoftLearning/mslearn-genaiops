---
lab:
    title: 'Monitor your generative AI application'
---

# Monitor your generative AI application

This exercise takes approximately **30 minutes**.

> **Note**: This exercise assumes some familiarity with Azure AI Foundry, which is why some instructions are intentionally less detailed to encourage more active exploration and hands-on learning.

## Introduction

In this exercise, you enable monitoring for a chat completion app and view its performance in Azure Monitor. You interact with your deployed model to generate data, view the generated data through the Insights for Generative AI applications dashboard, and set up alerts to help optimize the model's deployment.

## Set up the environment

To complete the tasks in this exercise, you need:

- An Azure AI Foundry hub,
- An Azure AI Foundry project,
- A deployed model (like GPT-4o),
- A connected Application Insights resource.

### Create an AI Foundry hub and project

To quickly setup a hub and project, simple instructions to use the Azure AI Foundry portal UI are provided below.

1. In a web browser, open the [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials.
1. In the home page, select **+ Create project**.
1. In the **Create a project** wizard, enter a valid name for your project and if an existing hub is suggested, choose the option to create a new one. Then review the Azure resources that will be automatically created to support your hub and project.
1. Select **Customize** and specify the following settings for your hub:
    - **Hub name**: *A valid name for your hub*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Location**: Select **Help me choose** and then select **gpt-4o** in the Location helper window and use the recommended region\*
    - **Connect Azure AI Services or Azure OpenAI**: *Create a new AI Services resource*
    - **Connect Azure AI Search**: Skip connecting

    > \* Azure OpenAI resources are constrained by regional model quotas. In the event of a quota limit being exceeded later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Next** and review your configuration. Then select **Create** and wait for the process to complete.

### Deploy a model

To generate data that you can monitor, you first need to deploy a model and interact with it. In the instructions you're asked to deploy a GPT-4o model, but **you can use any model** from the Azure OpenAI Service collection that is available to you.

1. Use the menu on the left, in the **My assets**, select the **Models + endpoints** page.
1. In the **Models + endpoints** page, in the **+ Deploy model** menu, select **Deploy base model**.
1. Select the **gpt-4o** model in the list and deploy it with the following settings by selecting **Customize** in the deployment details:
    - **Deployment name**: *A valid name for your model deployment*
    - **Deployment type**: Standard
    - **Automatic version update**: Enabled
    - **Model version**: *Select the most recent available version*
    - **Connected AI resource**: *Select your Azure OpenAI resource connection*
    - **Tokens per Minute Rate Limit (thousands)**: 1K
    - **Content filter**: DefaultV2
    - **Enable dynamic quota**: Disabled

    > **Note**: Reducing the TPM helps avoid over-using the quota available in the subscription you are using. 1,000 TPM should be sufficient for the data used in this exercise. If your available quota is lower than this, you will be able to complete the exercise but you may experience errors if the rate limit is exceeded.

1. Wait for the deployment to complete.

### Connect Application Insights

Connect Application Insights to your project in Azure AI Foundry to start collecting data for monitoring.

1. Use the menu on the left, and select the **Tracing** page.
1. **Create a new** Application Insights resource to connect to your app.
1. Enter an Application Insights resource name and select **Create**.

Application Insights is now connected to your project, and data will begin to be collected for analysis.

## Interact with a deployed model

You'll interact with your deployed model programmatically by setting up a connection to your Azure AI Foundry project using Azure Cloud Shell. This will allow you to send a prompt to the model and generate monitoring data.

### Connect with a model through the Cloud Shell

Start by retrieving the necessary information to be authenticated to interact with your model. Then, you'll access the Azure Cloud Shell and update the configuration to send the provided prompts to your own deployed model.

1. In the Azure AI Foundry portal, view the **Overview** page for your project.
1. In the **Project details** area, note the **Project connection string**.
1. **Save** the string in a notepad. You'll use this connection string to connect to your project in a client application.
1. Open a new browser tab (keeping the Azure AI Foundry portal open in the existing tab).
1. In the new tab, browse to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`; signing in with your Azure credentials if prompted.
1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment with no storage in your subscription.
1. In the Cloud Shell toolbar, in the **Settings** menu, select **Go to Classic version**.

    **<font color="red">Ensure you've switched to the Classic version of the Cloud Shell before continuing.</font>**

1. In the Cloud Shell pane, enter and run the following commands:

    ```
    rm -r mslearn-genaiops -f
    git clone https://github.com/microsoftlearning/mslearn-genaiops mslearn-genaiops
    ```

    This command clones the GitHub repository containing the code files for this exercise.

    > **Tip**: As you paste commands into the cloudshell, the output may take up a large amount of the screen buffer. You can clear the screen by entering the `cls` command to make it easier to focus on each task.

1. After the repo has been cloned, navigate to the folder containing the application code files:  

    ```
   cd mslearn-genaiops/Files/07
    ```

1. In the Cloud Shell command-line pane, enter the following command to install the libraries you need:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install python-dotenv azure-identity azure-ai-projects azure-ai-inference azure-monitor-opentelemetry
    ```

1. Enter the following command to open the configuration file that has been provided:

    ```
   code .env
    ```

    The file is opened in a code editor.

1. In the code file:

    1. Replace the **your_project_connection_string** placeholder with the connection string for your project (copied from the project **Overview** page in the Azure AI Foundry portal).
    1. Replace the **your_model_deployment** placeholder with the name you assigned to your GPT-4o model deployment (by default `gpt-4o`).

1. *After* you've replaced the placeholders, in the code editor, use the **CTRL+S** command or **Right-click > Save** to **save your changes** and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

### Send prompts to your deployed model

You'll now run multiple scripts that send different prompts to your deployed model. These interactions generate data that you can later observe in Azure Monitor.

1. Run the following command to **view the first script** that has been provided:

    ```
   code start-prompt.py
    ```

1. In the Cloud Shell command-line pane beneath the code editor, enter the following command to **run the script**:

    ```
   python start-prompt.py
    ```

    The model will generate a response, which will be captured with Application Insights for further analysis. Let's vary our prompts to explore their effects.

1. **Open and review the script**, where the prompt instructs the model to **only answer with one sentence and a list**:

    ```
   code short-prompt.py
    ```

1. **Run the script** by entering the following command in the command-line:

    ```
   python short-prompt.py
    ```

1. The next script has a similar objective, but includes the instructions for the output in the **system message** instead of the user message:

    ```
   code system-prompt.py
    ```

1. **Run the script** by entering the following command in the command-line:

    ```
   python system-prompt.py
    ```

1. Finally, let's try to trigger an error by running a prompt with **too many tokens**:

    ```
   code error-prompt.py
    ```

1. **Run the script** by entering the following command in the command-line. Note that you're very **likely to experience an error!**

    ```
   python error-prompt.py
    ```

Now that you have interacted with the model, you can review the data in Azure Monitor.

> **Note**: It may take a few minutes for monitoring data to show in Azure Monitor.

## View monitoring data in Azure Monitor

To view data collected from your model interactions, you'll access the dashboard that links to a workbook in Azure Monitor.

### Navigate to Azure Monitor from the Azure AI Foundry portal

1. Navigate to the tab in your browser with the **Azure AI Foundry portal** open.
1. Use the menu on the left, select **Tracing**.
1. Select link at the top, that says **Check out your Insights for Generative AI applications dashboard**. The link will open Azure Monitor in a new tab.
1. Review the **Overview** providing summarized data of the interactions with your deployed model.

## Interpret monitoring metrics in Azure Monitor

Now it's time to dig into the data and begin interpreting what it tells you.

### Review the token usage

Focus on the **token usage** section first and review the following metrics:

- **Prompt tokens**: The total number of tokens used in the input (the prompts you sent) across all model calls.

> Think of this as the *cost of asking* the model a question.

- **Completion tokens**: The number of tokens the model returned as output, essentially the length of the responses.

> The generated completion tokens often represent the bulk of token usage and cost, especially for long or verbose answers.

- **Total tokens**: The combined total prompt tokens and completion tokens.

> Most important metric for billing and performance, as it drives latency and cost.

- **Total calls**: The number of separate inference requests, which is how many times the model was called.

> Useful for analyzing throughput and understanding average cost per call.

### Compare the individual prompts

Scroll down to find the **Gen AI Spans**, which is visualized as a table where each prompt is represented as a new row of data. Review and compare the contents of the following columns:

- **Status**: Whether a model call succeeded or failed.

> Use this to identify problematic prompts or configuration errors. The last prompt likely failed because the prompt was too long.

- **Duration**: Shows how long the model took to respond, in milliseconds.

> Compare across rows to explore which prompt patterns result in longer processing times.

- **Input**: Displays the user message that was sent to the model.

> Use this column to assess which prompt formulations are efficient or problematic.

- **System**: Shows the system message used in the prompt (if there was any).

> Compare entries to evaluate the impact of using or changing system messages.

- **Output**: Contains the model's response.

> Use it to assess verbosity, relevance, and consistency. Especially in relation to token counts and duration.

## (OPTIONAL) Create an alert

If you have extra time, try setting up an alert to notify you when model latency exceeds a certain threshold. This is an exercise designed to challenge you, which means instructions are intentionally less detailed.

- In Azure Monitor, create a **new alert rule** for your Azure AI Foundry project and model.
- Choose a metric such as **Request duration (ms)** and define a threshold (for example, greater than 4000 ms).
- Create a **new action group** to define how you'll be notified.

Alerts help you prepare for production by establishing proactive monitoring. The alerts you configure will depend on your project's priorities and how your team has decided to measure and mitigate risks.

## Where to find other labs

You can explore additional labs and exercises in the [Azure AI Foundry Learning Portal](https://ai.azure.com) or refer to the course's **lab section** for other available activities.
