---
lab:
    title: 'Deploy Trail Guide Agent with Azure Developer CLI'
    description: 'Provision Azure AI infrastructure and run a trail guide agent'
---

# Lab 01: Deploy Trail Guide Agent

Deploy an AI trail guide agent to Azure using a single command.

This exercise will take approximately **20-30** minutes.

## Outcomes

✅ **Outcome 1:** Azure AI infrastructure is provisioned  
✅ **Outcome 2:** Trail guide agent runs successfully using deployed resources  
✅ **Outcome 3:** Environment variables are automatically configured in `.env`

## Post-Workshop Artifact

📸 Screenshot showing successful agent creation output in your terminal

---

## Prerequisites

- Active Azure subscription
- [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd) installed
- Python 3.11+ installed
- This repository cloned locally

---

## Task 1: Deploy infrastructure

1. Open a terminal in the repository root

2. Authenticate with Azure:

    ```bash
    az login
    ```

3. Deploy everything with one command:

    ```bash
    azd up
    ```

4. When prompted:
   - Enter an environment name (e.g., `trail-guide-dev`)
   - Select your Azure subscription
   - Select a location (e.g., `eastus2`)

**What happens during deployment:**
- Azure AI Foundry hub and project are created
- GPT-4o model deployment is provisioned
- Environment variables are saved to `.env` file

**✓ Verification:** Deployment completes successfully (15-20 minutes)

---

## Task 2: Run the trail guide agent

1. Install Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Run the trail guide agent:

    ```bash
    cd src/agents/trail_guide_agent
    python trail_guide_agent.py
    ```

3. Verify the output shows:
   - Agent created with ID and version
   - Agent name: `trail-guide`

**✓ Verification:** Agent creation succeeds without errors

---

## Task 3: Create your artifact

Take a screenshot showing the successful agent creation output in your terminal.

Your screenshot should include:
- The agent ID
- The agent name (`trail-guide`)
- The agent version

---

## Clean up resources

When you're done, delete all Azure resources:

```bash
azd down
```

Confirm with `y` when prompted.


