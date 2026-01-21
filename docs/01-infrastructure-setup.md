---
lab:
    title: 'Infrastructure Setup'
    description: 'Deploy Microsoft Foundry resources and configure your development environment for building generative AI applications.'
---

# Set up your Microsoft Foundry project

This exercise takes approximately **20 minutes**.

> **Note**: This lab assumes a pre-configured lab environment with Visual Studio Code, Azure CLI, and Python already installed.

## Introduction

In this exercise, you'll set up the foundational infrastructure needed for developing and deploying generative AI applications. You'll use the Azure Developer CLI (azd) to provision a Microsoft Foundry hub and project, along with supporting resources like Application Insights for monitoring.

You'll authenticate with Azure, provision all required cloud resources, and install the necessary Python dependencies. This will prepare your environment for building AI agents and applications in subsequent labs.

## Set up the environment

All steps in this lab will be performed using Visual Studio Code and its integrated terminal.

### Create repository from template

To complete the tasks in this exercise, you'll create your own repository from the template to practice realistic workflows.

1. In a web browser, navigate to `https://github.com/MicrosoftLearning/mslearn-genaiops`.
1. Select **Use this template** > **Create a new repository**.
1. Enter a name for your repository (e.g., `mslearn-genaiops`).
1. Set the repository to **Public** or **Private** based on your preference.
1. Select **Create repository**.

### Clone the repository in Visual Studio Code

1. In Visual Studio Code, open the Command Palette by pressing **Ctrl+Shift+P**.
1. Type **Git: Clone** and select it.
1. Enter your repository URL: `https://github.com/[your-username]/mslearn-genaiops.git`
1. Select a location on your local machine to clone the repository.
1. When prompted, select **Open** to open the cloned repository in VS Code.

### Deploy Microsoft Foundry resources

You'll use the Azure Developer CLI to deploy all required Azure resources using the infrastructure files provided in this repository.

> **Note**: This repository includes pre-configured infrastructure files (`azure.yaml` and `infra/` folder) that define all the Azure resources needed for this lab.

1. In Visual Studio Code, open a new terminal by selecting **Terminal** > **New Terminal** from the menu.
1. Authenticate with Azure Developer CLI:

    ```powershell
    azd auth login
    ```

    This opens a browser window for Azure authentication. Sign in with your Azure credentials.

1. Authenticate with Azure CLI:

    ```powershell
    az login
    ```

    Sign in with your Azure credentials when prompted. This authentication is needed for the Python SDK and other Azure operations in subsequent labs.

1. Provision resources:

    ```powershell
    azd up
    ```

    When prompted, provide:
    - **Environment name** (e.g., `dev`, `test`) - Used to name all resources
    - **Azure subscription** - Where resources will be created
    - **Location** - Azure region (recommended: Sweden Central)

    The command deploys the Bicep templates from the `infra/` folder. You'll see output like:

    ```
    (✓) Done: Resource group: rg-trail-gd-dev-trailguide-pr
    (✓) Done: Foundry: ai-account-pq7b5wqaoqljc
    (✓) Done: Log Analytics workspace: logs-pq7b5wqaoqljc
    (✓) Done: Foundry project: ai-account-pq7b5wqaoqljc/ai-project-dev-trail
    (✓) Done: Application Insights: appi-pq7b5wqaoqljc
    ```

    **Resources created:**
    - **Resource Group** - Container for all resources (e.g., `rg-trail-gd-dev-trailguide-pr`)
    - **Foundry (AI Services)** - The hub with access to Global Standard models like GPT-4.1 (no manual deployment required)
    - **Foundry Project** - Your workspace for creating and managing agents
    - **Log Analytics Workspace** - Collects logs and telemetry data
    - **Application Insights** - Monitors agent performance and usage

    > **Note**: The core components you'll use are the Foundry hub and Project. Global Standard models are available immediately without explicit deployment.

1. Create a `.env` file with the environment variables:

    ```powershell
    azd env get-values > .env
    ```

    This creates a `.env` file in your project root with all the provisioned resource information:
    - Resource names and IDs
    - Endpoints for AI Services and Project
    - Azure subscription and location details

    You can use these variables in your code and notebooks to connect to your Foundry resources.

### Install Python dependencies

Install the required Python packages to work with Microsoft Foundry in your applications.

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

### Configure agent settings

Add the required agent configuration to your environment variables.

1. In VS Code, open the `.env` file in the repository root.
1. Add the following lines at the end of the file:

    ```
    AGENT_NAME=trail-guide
    MODEL_NAME=gpt-4.1
    ```

1. Save the file.

### Create your first agent

Deploy the initial version of the Trail Guide Agent to Microsoft Foundry.

1. In the VS Code terminal, navigate to the agent directory:

    ```powershell
    cd src/agents/trail_guide_agent
    ```

1. Run the agent creation script:

    ```powershell
    python trail_guide_agent.py
    ```

    You should see output confirming the agent was created:

    ```
    Agent created (id: agent_xxx, name: trail-guide, version: 1)
    ```

### Test your agent

Interact with your deployed agent from the terminal to verify it's working correctly.

1. In the VS Code terminal, navigate back to the repository root:

    ```powershell
    cd ..\..\..
    ```

1. Run the interactive test script:

    ```powershell
    python src\tests\interact_with_agent.py
    ```

1. When prompted, ask the agent a question about hiking, for example:

    ```
    You: I want to go hiking this weekend near Seattle. Any suggestions?
    ```

1. The agent will respond with trail recommendations. Continue the conversation or type `exit` to quit.

    ```
    Agent: I'd recommend checking out Rattlesnake Ledge Trail...
    
    You: exit
    ```

## Verify your deployment

After deployment completes, verify that all resources are accessible and your agent is deployed.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials.
1. In the home page, select your newly created project from the list.
1. In the left navigation, select **Agents** to see your deployed Trail Guide Agent.
1. Verify you can see your agent (e.g., `trail-guide`) in the list.

## (OPTIONAL) Explore the Microsoft Foundry starter template

If you have extra time and want to explore alternative project structures, you can experiment with the official Microsoft Foundry starter template.

This is a stretch exercise designed to help you understand different approaches to structuring AI projects.

1. In a **new directory** (outside of this lab), initialize a new project from the starter template:

    ```powershell
    mkdir ai-foundry-exploration
    cd ai-foundry-exploration
    azd init --template Azure-Samples/ai-foundry-starter-basic
    ```

1. Review the generated files and compare them to the structure used in this lab:
    - `azure.yaml` - Project configuration
    - `infra/` - Infrastructure as Code (Bicep) files
    - Additional sample code and configurations

1. *Optionally*, you can deploy this template to a separate Azure environment to see how it compares:

    ```powershell
    azd up
    ```

    > **Important**: This will create additional Azure resources and may incur costs. Be sure to clean up resources when done by running `azd down`.

## Where to find other labs

You can explore additional labs and exercises in the [Microsoft Foundry Learning Portal](https://ai.azure.com) or refer to the course's **lab section** for other available activities.

