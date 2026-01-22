---
lab:
    title: 'Manual evaluation workflows'
    description: 'Perform manual quality assessments of AI agents and compare different versions using structured evaluation criteria.'
---

# Manual evaluation workflows

This exercise takes approximately **30 minutes**.

> **Note**: This lab assumes a pre-configured lab environment with Visual Studio Code, Azure CLI, and Python already installed.

## Introduction

In this exercise, you'll manually evaluate different versions of the Trail Guide Agent to assess their quality, accuracy, and user experience. You'll use structured evaluation criteria to compare agent responses, document your findings, and make data-driven decisions about which version performs best.

You'll deploy an agent, test it with specific scenarios, evaluate responses against defined criteria, and document your assessment. This will help you understand the importance of manual evaluation in the AI development lifecycle and how to conduct thorough quality assessments.

## Set up the environment

To complete the tasks in this exercise, you need:

- Visual Studio Code
- Azure subscription with Microsoft Foundry access
- Git and GitHub account
- Python 3.9 or later
- Azure CLI and Azure Developer CLI (azd) installed

All steps in this lab will be performed using Visual Studio Code and its integrated terminal.

### Create repository from template

You'll start by creating your own repository from the template to practice realistic workflows.

1. In a web browser, navigate to `https://github.com/MicrosoftLearning/mslearn-genaiops`.
1. Select **Use this template** > **Create a new repository**.
1. Enter a name for your repository (e.g., `mslearn-genaiops`).
1. Set the repository to **Public** or **Private** based on your preference.
1. Select **Create repository**.

### Clone the repository in Visual Studio Code

After creating your repository, clone it to your local machine.

1. In Visual Studio Code, open the Command Palette by pressing **Ctrl+Shift+P**.
1. Type **Git: Clone** and select it.
1. Enter your repository URL: `https://github.com/[your-username]/mslearn-genaiops.git`
1. Select a location on your local machine to clone the repository.
1. When prompted, select **Open** to open the cloned repository in VS Code.

### Deploy Microsoft Foundry resources

Now you'll use the Azure Developer CLI to deploy all required Azure resources.

1. In Visual Studio Code, open a terminal by selecting **Terminal** > **New Terminal** from the menu.

1. Authenticate with Azure Developer CLI:

    ```powershell
    azd auth login
    ```

    This opens a browser window for Azure authentication. Sign in with your Azure credentials.

1. Authenticate with Azure CLI:

    ```powershell
    az login
    ```

    Sign in with your Azure credentials when prompted.

1. Provision resources:

    ```powershell
    azd up
    ```

    When prompted, provide:
    - **Environment name** (e.g., `dev`, `test`) - Used to name all resources
    - **Azure subscription** - Where resources will be created
    - **Location** - Azure region (recommended: Sweden Central)

    The command deploys the infrastructure from the `infra/` folder, creating:
    - **Resource Group** - Container for all resources
    - **Foundry (AI Services)** - The hub with access to models like GPT-4.1
    - **Foundry Project** - Your workspace for creating and managing agents
    - **Log Analytics Workspace** - Collects logs and telemetry data
    - **Application Insights** - Monitors agent performance and usage

1. Create a `.env` file with the environment variables:

    ```powershell
    azd env get-values > .env
    ```

    This creates a `.env` file in your project root with all the provisioned resource information.

1. Add the agent configuration to your `.env` file:

    ```
    AGENT_NAME=trail-guide
    MODEL_NAME=gpt-4.1
    ```

### Install Python dependencies

With your Azure resources deployed, install the required Python packages to work with Microsoft Foundry.

1. In the VS Code terminal, create and activate a virtual environment:

    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

1. Install the required dependencies:

    ```powershell
    python -m pip install -r requirements.txt
    ```

    This installs all necessary dependencies including:
    - `azure-ai-projects` - SDK for working with AI Foundry agents
    - `azure-identity` - Azure authentication
    - `python-dotenv` - Load environment variables
    - Other evaluation, testing, and development tools

## Deploy trail guide agent

Deploy the first version of the trail guide agent for evaluation.

1. In the VS Code terminal, navigate to the trail guide agent directory:

    ```powershell
    cd src\agents\trail_guide_agent
    ```

1. Open the agent creation script (`trail_guide_agent.py`) and locate the line that reads the prompt file:
   
    ```python
    with open('prompts/v1_instructions.txt', 'r') as f:
        instructions = f.read().strip()
    ```

    Verify it's configured to read from `v1_instructions.txt`.

1. Run the agent creation script:

    ```powershell
    python trail_guide_agent.py
    ```

    You should see output confirming the agent was created:

    ```
    Agent created (id: agent_xxx, name: trail-guide, version: 1)
    ```

    Note the Agent ID for later use.

## Perform manual evaluation

Evaluate the agent's performance using the Microsoft Foundry portal's evaluation features.

### Navigate to the evaluation tab

Access the evaluation interface for your agent.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials.
1. Navigate to **Agents** in the left navigation.
1. Select your **trail-guide** agent from the list.
1. Select the **Evaluation** tab at the top of the page.
1. Select the **Human Evaluation** tab.
1. Select **Create** to start a new evaluation.

### Create evaluation template

Configure an evaluation template with scoring criteria.

1. In the **Create human evaluation template** dialog, enter the following details:
   - **Name**: `Trail Guide Quality Assessment`
   - **Version**: `1`
   - **Description**: `Evaluation template for trail guide agent responses`

1. Remove the default thumb up/down scoring criteria:
   - Locate the **Scoring method: thumb up/down** section
   - Select the trash icon next to **Groundedness** to remove it
   - Select the trash icon next to **Fluency** to remove it

1. Configure the scoring criteria using the **slider** method. Select **Add** under "Scoring method: slider" and add the following three criteria:

   **Criterion 1:**
   - Question: `Intent resolution: Does the response address what the user was asking for?`
   - Scale: `1 - 5`

   **Criterion 2:**
   - Question: `Relevance: How well does the response address the query?`
   - Scale: `1 - 5`

   **Criterion 3:**
   - Question: `Groundedness: Does the response stick to factual information?`
   - Scale: `1 - 5`

1. Remove the default multiple choice evaluation:
   - Locate the **Scoring method: multiple choice** section
   - Select the trash icon next to **How would you rate the quality of this response?** to remove it

1. Add a free-form question for additional feedback. Select **Add** under "Scoring method: free form question":
   - Question: `Additional comments`

1. Select **Create** to save the evaluation template.

1. Set the template as active:
   - Locate your **Trail Guide Quality Assessment** template in the template table
   - Select **Set as active** to enable it for evaluation

### Test agent and conduct evaluations

Test the agent with specific scenarios and evaluate each response.

1. Select **Preview** in the top-right corner of the agent builder experience to open the agent in a web app interface.

1. Test **Scenario 1: Basic trail recommendation**
   - Enter: *"I'm planning a weekend hiking trip near Seattle. What should I know?"*
   - Select **Send** to trigger the agent run
   - After the agent responds, select the **Feedback** button

1. A side panel appears displaying the evaluation template you configured earlier. Evaluate the response:
   - Use the slider to rate **Intent resolution: Does the response address what the user was asking for?** (1-5 scale)
   - Use the slider to rate **Relevance: How well does the response address the query?** (1-5 scale)
   - Use the slider to rate **Groundedness: Does the response stick to factual information?** (1-5 scale)
   - Add any relevant observations in the **Additional comments** field
   - Select **Save** to store the evaluation data

1. Repeat the test and evaluation process for the remaining scenarios:

   **Scenario 2: Gear recommendations**
   - Enter: *"What gear do I need for a day hike in summer?"*
   - Select **Send**, then **Feedback** after the response
   - Complete all three rating criteria and add comments
   - Select **Save**

   **Scenario 3: Safety information**
   - Enter: *"What safety precautions should I take when hiking alone?"*
   - Select **Send**, then **Feedback** after the response
   - Complete all three rating criteria and add comments
   - Select **Save**

### Review evaluation results

Analyze the evaluation data in the portal.

1. Navigate to the template table within the **Human Evaluation** tab.

1. Select your **Trail Guide Quality Assessment** template to review results.

1. All evaluation results appear under the **Evaluation Results** section, with each instance displayed with its timestamp.

1. Select an evaluation instance to view its JSON summary in the **JSON Output** section, which includes:
   - Timestamp
   - User prompt
   - Agent response
   - Questions from the evaluation template
   - Reviewer answers

1. To download all evaluation results:
   - Ensure your template is selected
   - Select **Download Results**
   - The results are exported as a CSV file containing all evaluation data

1. Review the evaluation summary to:
   - Identify average scores across all criteria
   - Identify patterns in the agent's performance
   - Note specific areas where the agent excels or needs improvement

## Clean up

To avoid incurring unnecessary Azure costs, delete the resources you created in this exercise.

1. In the VS Code terminal, run the following command:

    ```powershell
    azd down
    ```

1. When prompted, confirm that you want to delete the resources.

## Next steps

Continue your learning journey by exploring automated evaluation techniques.

In the next lab, you'll learn to automate evaluation processes using scripts and metrics, enabling scalable quality assessment across multiple agent versions.
