---
lab:
    title: 'Develop prompt and agent versions'
    description: 'Create and deploy multiple versions of AI agents using prompt engineering and version management in Microsoft Foundry.'
    level: 200
    duration: 30 minutes
---

# Develop prompt and agent versions

This exercise takes approximately **30 minutes**.

> **Note**: This lab assumes a pre-configured lab environment with Visual Studio Code, Azure CLI, and Python already installed.

## Introduction

In this exercise, you'll deploy multiple versions of a Trail Guide Agent to Microsoft Foundry, each with progressively enhanced capabilities. You'll use Python scripts to create agents with different system prompts, test their behavior in the portal, and run automated tests to compare their performance.

You'll modify a single Python script to deploy three agent versions (V1, V2, and V3), review each deployment in the Microsoft Foundry portal, and analyze how prompt evolution affects agent behavior. This will help you understand version management strategies and the relationship between programmatic deployment and portal-based agent management.

## Set up the environment

To complete the tasks in this exercise, you need:

- Visual Studio Code
- Azure subscription with Microsoft Foundry access
- Git and [GitHub](https://github.com) account
- Python 3.9 or later
- Azure CLI and Azure Developer CLI (azd) installed

All steps in this lab will be performed using Visual Studio Code and its integrated terminal.

### Create repository from template

You'll start by creating your own repository from the template to practice realistic workflows.

1. In a web browser, navigate to the template repository on [GitHub](https://github.com) at `https://github.com/MicrosoftLearning/mslearn-genaiops`.
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

> **Note**: This lab uses infrastructure-as-code (IaC) deployment with `azd` because it follows GenAIOps best practices and makes the lab accessible as a standalone exercise. This approach ensures consistent, reproducible environments while teaching real-world deployment patterns.

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
    .venv/Scripts/Activate.ps1
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

## Deploy and test agent versions

You'll deploy three versions of the Trail Guide Agent, each with different system prompts that progressively enhance capabilities.

### Deploy trail guide agent V1

Start by deploying the first version of the trail guide agent.

1. In the VS Code terminal, navigate to the trail guide agent directory:

    ```powershell
    cd src/agents/trail_guide_agent
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

1. Commit your changes and tag the version:

    ```powershell
    git add trail_guide_agent.py
    git commit -m "Deploy trail guide agent V1"
    git tag v1
    ```

### Test agent V1

Verify your agent is working by testing it in the Microsoft Foundry portal.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials.
1. Navigate to **Agents** in the left navigation.
1. Select your trail-guide agent from the list.
1. Test the agent by asking questions like:
   - "What gear do I need for a day hike?"
   - "Recommend a trail near Seattle for beginners"

### Deploy trail guide agent V2

Next, deploy a second version with enhanced capabilities.

1. Open `trail_guide_agent.py` and update the prompt file path:
   
   Change:
   ```python
   with open('prompts/v1_instructions.txt', 'r') as f:
   ```
   
   To:
   ```python
   with open('prompts/v2_instructions.txt', 'r') as f:
   ```

1. Run the agent creation script:

    ```powershell
    python trail_guide_agent.py
    ```

    You should see output confirming the agent was created:

    ```
    Agent created (id: agent_yyy, name: trail-guide, version: 2)
    ```

    Note the Agent ID for later use.

1. Commit your changes and tag the version:

    ```powershell
    git add trail_guide_agent.py
    git commit -m "Deploy trail guide agent V2 with enhanced capabilities"
    git tag v2
    ```

### Deploy trail guide agent V3

Finally, deploy the third version with production-ready features.

1. Open `trail_guide_agent.py` and update the prompt file path:
   
   Change:
   ```python
   with open('prompts/v2_instructions.txt', 'r') as f:
   ```
   
   To:
   ```python
   with open('prompts/v3_instructions.txt', 'r') as f:
   ```

1. Run the agent creation script:

    ```powershell
    python trail_guide_agent.py
    ```

    You should see output confirming the agent was created:

    ```
    Agent created (id: agent_zzz, name: trail-guide, version: 3)
    ```

    Note the Agent ID for later use.

1. Commit your changes and tag the version:

    ```powershell
    git add trail_guide_agent.py
    git commit -m "Deploy trail guide agent V3 with production features"
    git tag v3
    ```

## Compare agent versions

Now that you have three agent versions deployed, compare their behavior and prompt evolution.

### Review version history

Examine your Git tags to see the version history.

1. View all version tags:

    ```powershell
    git tag
    ```

    You should see:
    ```
    v1
    v2
    v3
    ```

1. View the commit history with tags:

    ```powershell
    git log --oneline --decorate
    ```

    This shows each deployment milestone marked with its corresponding tag.

### Review prompt differences

Examine the prompt files to understand how each version evolved.

1. In VS Code, open the three prompt files in the `prompts/` directory:
   - `v1_instructions.txt` - Basic trail guide functionality
   - `v2_instructions.txt` - Enhanced with personalization
   - `v3_instructions.txt` - Production-ready with advanced capabilities

1. Notice the evolution:
   - **V1 → V2**: Added personalization and enhanced guidance
   - **V2 → V3**: Added structured framework and enterprise features

1. In the Microsoft Foundry portal, test each agent version with the same question to observe behavior differences.
   
   Try this question: *"I'm planning a weekend hiking trip near Seattle. What should I know?"*
   
   Observe how each version responds:
   - **V1**: Provides basic trail recommendations and general advice
   - **V2**: Adds personalized suggestions based on experience level and preferences
   - **V3**: Includes comprehensive guidance with safety considerations, weather factors, and detailed planning steps

## Clean up

To avoid incurring unnecessary Azure costs, delete the resources you created in this exercise.

1. In the VS Code terminal, run the following command:

    ```powershell
    azd down
    ```

1. When prompted, confirm that you want to delete the resources.

## Next steps

Continue your learning journey by exploring agent evaluation techniques.

In the next lab, you'll learn to evaluate these agent versions using manual testing processes to determine which performs better for different scenarios and customer segments.
