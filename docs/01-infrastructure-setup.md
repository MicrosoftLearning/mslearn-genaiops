---
lab:
    title: 'Deploy Trail Guide Agent with Azure Developer CLI'
    description: 'Provision Microsoft Foundry infrastructure and deploy the Trail Guide Agent using automated IaC workflows'
---

# Lab 01: Deploy Trail Guide Agent infrastructure

Learn how to provision Azure AI infrastructure and deploy a conversational AI agent using Azure Developer CLI (azd) and Infrastructure as Code (IaC) practices.

This exercise will take approximately **20-30** minutes.

## Scenario

Adventure Works wants to deploy an AI-powered Trail Guide Agent to help customers discover hiking trails and gear recommendations. You'll use Azure Developer CLI to provision a complete AI environment and deploy the agent to Microsoft Foundry.

## Learning objectives

By the end of this lab, you will be able to:

- Provision Microsoft Foundry infrastructure using Azure Developer CLI
- Deploy an AI agent to Microsoft Foundry
- Configure your local development environment to connect to the deployed agent
- Understand how Bicep templates define cloud resources

## Prerequisites

Before starting this lab, ensure you have:

- An active Azure subscription with permissions to create resources
- Azure CLI installed locally ([Install guide](https://learn.microsoft.com/cli/azure/install-azure-cli))
- Azure Developer CLI (azd) installed ([Install guide](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd))
- Visual Studio Code with Python extension installed
- Python 3.11 or later installed
- Git and GitHub account

## Lab outcomes

**Core Outcome (Required):**
✅ Successfully provision Azure AI infrastructure and deploy the Trail Guide Agent

**Core Artifact (Required):**
📸 Screenshot showing successful agent response in your local CLI

**Stretch Outcome (Optional):**
✅ Deploy a web chat interface for public access to the agent

**Stretch Artifact (Optional):**
📸 Screenshot showing web chat interface with successful agent interaction

---

## Lab setup

### Create repository from template

To complete this lab, you'll create your own repository from the template to enable proper version control and infrastructure deployment.

1. Navigate to `https://github.com/[your-org]/mslearn-genaiops` in your web browser.

2. Click **Use this template** → **Create a new repository**.

3. Enter a name for your repository such as `mslearn-genaiops`.

4. Set the repository to **Public** or **Private** based on your preference.

5. Click **Create repository**.

6. Open **Visual Studio Code**.

7. Open the **integrated terminal** in VS Code by selecting **Terminal** > **New Terminal** from the menu (or press `` Ctrl+` ``).

8. In the terminal, clone your repository:

   ```bash
   git clone https://github.com/[your-username]/mslearn-genaiops.git
   cd mslearn-genaiops
   ```

9. Open the repository folder in VS Code by selecting **File** > **Open Folder** and choosing the `mslearn-genaiops` folder you just cloned.

**✓ Checkpoint:** You should have the repository open in VS Code.

---

## Task 1: Authenticate with Azure

Before provisioning resources, you need to authenticate with your Azure subscription.

1. In Visual Studio Code, open the **integrated terminal** by selecting **Terminal** > **New Terminal** from the menu (or press `` Ctrl+` ``)

2. Sign in to Azure CLI using device code authentication:

    ```bash
    az login --use-device-code
    ```

3. The terminal will display:
   - A unique device code (e.g., `A1B2C3D4E`)
   - A URL: `https://microsoft.com/devicelogin`

4. Open your web browser and navigate to the URL

5. Enter the device code displayed in your terminal

6. Sign in with your Azure credentials when prompted

7. Return to your terminal. After successful authentication, you'll see:
   - "Retrieving tenants and subscriptions for the selection..."
   - A table showing your available subscriptions
   - The default subscription is marked with an asterisk (*)

8. **Select a subscription:**
   - If the default subscription (marked with *) is correct, press **Enter**
   - If you want to use a different subscription, type its number and press **Enter**

9. Verify your active subscription:

    ```bash
    az account show --output table
    ```

**✓ Checkpoint:** You should see your subscription details displayed.

---

## Task 2: Initialize Azure Developer CLI

Azure Developer CLI (azd) will orchestrate the deployment of all required Azure resources.

1. In the VS Code integrated terminal, ensure you're in the repository root:

    ```bash
    pwd
    # Should show: /path/to/mslearn-genaiops
    ```

2. Initialize azd for this project:

    ```bash
    azd init
    ```

3. When prompted:
   - **Environment name**: Choose a short, unique name (e.g., `trailguide-dev`)
   - This name will be used as a prefix for all Azure resources

**What just happened?**
- azd created a `.azure` folder in your project
- This folder stores environment configuration (not committed to git)

**✓ Checkpoint:** You should see a message confirming environment initialization.

---

## Task 3: Provision Azure infrastructure

Now you'll provision all required Azure resources with a single command.

1. Run the provisioning command:

    ```bash
    azd up
    ```

2. When prompted, select:
   - **Azure subscription**: Choose your subscription from the list
   - **Azure region**: Choose one of these regions:
     - `eastus2`
     - `swedencentral`
     - `westus`
     
   > **Why these regions?** These regions have Azure OpenAI capacity for GPT-4 deployments and support Microsoft Foundry features.

3. Wait for provisioning to complete (approximately **8-12 minutes**)

**What's being created?**

The Bicep templates (`infrastructure/bicep/`) define these resources:

- **Microsoft Foundry Hub**: Central workspace for AI projects
- **Microsoft Foundry Project**: Isolated project environment for the Trail Guide Agent
- **Azure OpenAI Service**: Hosts GPT-4 model deployment
- **GPT-4 Model Deployment**: Language model for the agent
- **Trail Guide Agent**: Pre-configured agent deployed to Foundry
- **Azure Storage Account**: Stores project artifacts
- **Azure Key Vault**: Manages secrets securely
- **Azure Monitor / Application Insights**: Tracks agent performance

4. Monitor the deployment output. You should see:
   - ✅ Resource group created
   - ✅ Microsoft Foundry hub provisioned
   - ✅ Microsoft Foundry project created
   - ✅ Azure OpenAI service deployed
   - ✅ GPT-4 model deployed
   - ✅ Trail Guide Agent deployed to Foundry

**✓ Checkpoint:** Deployment should complete with "SUCCESS" message.

---

## Task 4: Verify deployment in Azure Portal

Let's confirm your resources were created successfully.

1. Open the [Azure Portal](https://portal.azure.com) in your browser

2. Navigate to **Resource Groups**

3. Find your resource group (named similar to `rg-trailguide-dev`)

4. Verify you see these resources:
   - Microsoft Foundry hub (type: `Microsoft.MachineLearningServices/workspaces`)
   - Azure OpenAI (type: `Microsoft.CognitiveServices/accounts`)
   - Storage account
   - Key Vault
   - Application Insights

5. Click on the **Microsoft Foundry hub** resource

6. Select **Launch studio** to open Microsoft Foundry portal

7. In Microsoft Foundry portal:
   - Navigate to **Agents** in the left menu
   - You should see **Trail Guide Agent** listed
   - Click on the agent to view its configuration

**✓ Checkpoint:** You should see your Trail Guide Agent in Microsoft Foundry.

---

## Task 5: Configure local development environment

azd automatically generated connection configuration. Now you'll set up your Python environment to use it.

1. In your terminal, verify the `.env` file was created:

    ```bash
    ls -la .env
    ```

2. View the generated configuration (don't commit this file!):

    ```bash
    cat .env
    ```

   You should see variables like:
   ```
   AZURE_PROJECT_CONNECTION_STRING="<connection-string>"
   AZURE_AGENT_ID="<agent-id>"
   ```

3. Create a Python virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    **macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

    **Windows (PowerShell):**
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```

5. Install required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

   This installs:
   - `azure-ai-projects` (Microsoft Foundry SDK)
   - `azure-identity` (Authentication)
   - `python-dotenv` (Environment variable management)

**✓ Checkpoint:** You should see packages installed successfully without errors.

---

## Task 6: Test the Trail Guide Agent locally

Now you'll run the agent from your local machine and verify it connects to the deployed agent in Foundry.

1. Navigate to the agent directory:

    ```bash
    cd src/agents/trail_guide_agent
    ```

2. Run the agent:

    ```bash
    python trail_guide_agent.py
    ```

3. You should see a welcome message:

    ```
    ========================================
    Welcome to the Trail Guide Agent!
    ========================================
    I can help you discover hiking trails and recommend gear.
    
    Type 'exit', 'quit', or 'bye' to end the conversation.
    ========================================
    
    You:
    ```

4. Test with a sample query:

    ```
    I'm a beginner hiker looking for easy trails near Seattle. What do you recommend?
    ```

5. The agent should respond with trail recommendations.

6. Test multi-turn conversation (context retention):

    ```
    What gear should I bring for the trails you just recommended?
    ```

7. Verify the agent remembers the previous conversation about Seattle trails.

8. Exit the agent:

    ```
    exit
    ```

**✓ Checkpoint:** Agent responds appropriately to both queries and maintains conversation context.

---

## Task 7: Capture your lab artifact (required)

**Post-Lab Artifact:** Screenshot of successful agent interaction

1. Run the agent again:

    ```bash
    python trail_guide_agent.py
    ```

2. Ask a question about trails or gear

3. Take a screenshot showing:
   - Your terminal with the agent welcome message
   - Your question
   - The agent's response

4. Save the screenshot as `lab01-artifact-trailguide-response.png`

**This artifact proves you successfully:**
- ✅ Provisioned Azure infrastructure
- ✅ Deployed the agent to Microsoft Foundry
- ✅ Connected your local environment to the cloud agent
- ✅ Tested the agent's conversational capabilities

---

## Part 2: Deploy web interface (optional stretch)

**Time estimate: 15-20 minutes**

In this optional section, you'll deploy a simple web interface for the Trail Guide Agent, making it accessible via a public URL without requiring command-line access.

### Task 8: Deploy web chat interface

The repository includes a pre-built web chat interface using Azure Static Web Apps. You'll deploy it alongside your agent.

1. Navigate back to the repository root:

    ```bash
    cd ../../../
    ```

2. Deploy the web application:

    ```bash
    azd deploy web
    ```

   This deploys:
   - A simple HTML/JavaScript chat interface
   - Hosted on Azure Static Web Apps
   - Connected to your deployed agent

3. Wait for deployment to complete (approximately **3-5 minutes**)

4. After deployment completes, azd will display the web app URL:

    ```
    Deploying web app...
    SUCCESS: Web app deployed!
    URL: https://trailguide-dev-abc123.azurestaticapps.net
    ```

5. Copy the URL and open it in your web browser

**✓ Checkpoint:** You should see a chat interface with the Trail Guide Agent branding.

---

### Task 9: Test the web interface

1. In the web chat interface, type a message:

    ```
    I'm planning a family hike near Portland. Any suggestions for beginners?
    ```

2. Verify the agent responds with trail recommendations

3. Test multi-turn conversation by asking a follow-up:

    ```
    What's the best time of year to visit those trails?
    ```

4. Verify context is maintained

5. Share the URL with a colleague or friend to test external access (optional)

**✓ Checkpoint:** Web interface successfully communicates with your deployed agent.

---

### Task 10: Review the web app code

Understanding the web interface helps you see how external applications connect to agents in Microsoft Foundry.

1. In VS Code, open the web app files:

    ```
    src/web/
    ├── index.html       # Chat UI
    ├── chat.js          # Agent connection logic
    └── styles.css       # Styling
    ```

2. Open `chat.js` and review the key sections:

   **Agent connection:**
   ```javascript
   // Uses azure-ai-projects SDK to connect to deployed agent
   const client = new AIProjectsClient(
       process.env.AZURE_PROJECT_CONNECTION_STRING
   );
   ```

   **Sending messages:**
   ```javascript
   // Sends user message and receives agent response
   const response = await client.agents.createRun(
       agentId,
       { message: userMessage }
   );
   ```

   **Displaying responses:**
   ```javascript
   // Appends agent response to chat history
   appendMessage('agent', response.content);
   ```

3. Note how the web app:
   - Uses the same `.env` configuration as the CLI version
   - Maintains conversation history in browser session storage
   - Handles errors gracefully with user-friendly messages
   - **Matches Adventure Works branding** with outdoor-inspired design

4. Open `styles.css` and observe the Adventure Works styling:

   **Design elements:**
   - Dark, dramatic background inspired by outdoor imagery
   - Bold white typography for headings
   - Clean rounded buttons matching the Adventure Works website
   - High contrast for readability
   - Professional outdoor/adventure aesthetic

   **Key CSS variables:**
   ```css
   :root {
       --aw-dark-bg: #1a1a2e;          /* Dark background */
       --aw-accent: #16213e;           /* Accent panels */
       --aw-primary: #0f3460;          /* Primary blue */
       --aw-text-light: #ffffff;       /* White text */
       --aw-button-bg: #ffffff;        /* White buttons */
       --aw-button-text: #1a1a2e;      /* Dark button text */
   }
   ```

**✓ Checkpoint:** You understand how the web interface connects to the agent and matches Adventure Works branding.

---

### Understanding the web deployment

**What was deployed:**

- **Azure Static Web App**: Hosts the HTML/CSS/JavaScript files
  - Serverless, scales automatically
  - Free tier for low traffic
  - Custom domain support (optional)
  - HTTPS enabled by default

- **API Backend**: Azure Functions (serverless)
  - Proxies requests to Microsoft Foundry agent
  - Handles authentication securely (API keys not exposed to browser)
  - Auto-scales based on usage

**How it works:**

```
User Browser
    ↓
Azure Static Web App (HTML/JS)
    ↓
Azure Functions (API backend)
    ↓
Microsoft Foundry Agent
    ↓
Azure OpenAI (GPT-4)
```

**Why this architecture:**

- **Security**: API keys stay on server-side (Functions), not in browser
- **Simplicity**: Static Web Apps require minimal configuration
- **Cost**: Free tier suitable for educational use and demos
- **Speed**: CDN distribution for fast loading worldwide

**Constitutional compliance:**

- ✅ Azure-only (Static Web Apps + Functions)
- ✅ Minimal approach (simple HTML/JS, no frameworks)
- ✅ Fast deployment (single azd command)
- ✅ Uses existing Bicep templates (in `infrastructure/bicep/web.bicep`)

---

### Optional: Customize the web interface

**Stretch activities for advanced learners:**

1. **Personalize the hero section** in `index.html`:
   - Update the welcome message: "Discover Your Next Adventure"
   - Add Adventure Works tagline or mission statement
   - Include outdoor imagery in the header background

2. **Refine Adventure Works styling** in `styles.css`:
   - Adjust color scheme to match seasonal campaigns
   - Add custom fonts (Adventure Works uses bold sans-serif + script fonts)
   - Implement responsive design for mobile devices
   - Add subtle animations for message send/receive

3. **Add suggested prompts** for common queries:
   - Create clickable prompt buttons:
     - "Find beginner trails near me"
     - "What gear do I need for winter hiking?"
     - "Recommend trails for families"
   - Edit `chat.js` to add button click handlers
   - Style buttons to match Adventure Works call-to-action design

4. **Enhance the user experience**:
   - Add typing indicators: "Trail Guide is thinking..."
   - Implement conversation history persistence (localStorage)
   - Add download conversation transcript feature
   - Include Adventure Works logo in header

5. **Advanced branding integration**:
   - Add footer with Adventure Works store locator link
   - Include navigation to product categories
   - Embed related product recommendations based on trail difficulty
   - Link to Adventure Works blog or community resources

**Design inspiration:**
- Match the dramatic outdoor imagery from adventure-works.com
- Use high-contrast white text on dark backgrounds
- Keep buttons clean with rounded corners and white backgrounds
- Maintain professional outdoor/adventure aesthetic throughout

---

### Web deployment artifact (optional)

**Post-Lab Artifact:** Screenshot of web chat interface

1. In your web browser with the chat interface open, have a conversation with the agent

2. Take a screenshot showing:
   - The web URL in the browser address bar
   - The chat interface with your messages
   - Agent responses

3. Save as `lab01-artifact-web-interface.png`

**This demonstrates:**
- ✅ Successful web deployment
- ✅ Public accessibility of the agent
- ✅ Understanding of multi-tier architecture
- ✅ Readiness for production-style deployments

---

### Clean up web resources

When cleaning up at the end of the lab, the web app will be deleted automatically:

```bash
azd down
```

This removes:
- Azure Static Web App
- Azure Functions (API backend)
- All infrastructure from Part 1

If you want to keep the agent but remove only the web interface:

```bash
azd deploy web --down
```

---

## Understanding what you built

### How Bicep and azd work together

**What you ran:**
```bash
azd up
```

**What happened behind the scenes:**

1. **azd reads `azure.yaml`**
   - Defines this as a Microsoft Foundry project
   - Points to Bicep templates in `infrastructure/bicep/`

2. **Bicep templates define infrastructure**
   - `main.bicep`: Creates Microsoft Foundry hub, OpenAI, storage, Key Vault
   - `agent.bicep`: Defines the Trail Guide Agent configuration
   - Resources are described declaratively (what, not how)

3. **azd provisions resources**
   - Compiles Bicep to ARM templates
   - Deploys to Azure Resource Manager
   - Creates resources in order based on dependencies

4. **azd deploys the agent**
   - Uploads agent definition to Microsoft Foundry
   - Configures system prompt, model settings

5. **azd generates configuration**
   - Extracts connection strings and IDs
   - Writes to `.env` file automatically

**Why this matters:**
- **Repeatable**: Run `azd up` again in a new subscription → identical environment
- **Version-controlled**: Bicep files in git track infrastructure changes
- **Fast**: No manual clicking in Portal
- **Educational**: Students learn modern DevOps practices

### Key files in this project

```
mslearn-genaiops/
├── azure.yaml                          ← azd configuration
├── infrastructure/
│   └── bicep/
│       ├── main.bicep                  ← Infrastructure definition
│       ├── agent.bicep                 ← Agent configuration
│       └── core/                       ← Reusable Bicep modules
├── src/
│   └── agents/
│       └── trail_guide_agent/
│           ├── trail_guide_agent.py    ← Python client code
│           ├── system_prompt.txt       ← Agent instructions
│           └── README.md
├── .env                                ← Generated config (DO NOT COMMIT)
├── .env.example                        ← Template for .env
└── requirements.txt                    ← Python dependencies
```

---

## Troubleshooting

### Error: "Quota exceeded for GPT-4"

**Problem:** Your selected region doesn't have GPT-4 capacity.

**Solution:**
1. Choose a different region:
   ```bash
   azd env set AZURE_LOCATION swedencentral
   azd up
   ```

2. Or create a new environment:
   ```bash
   azd env new trailguide-dev2
   azd up
   ```

### Error: "Authentication failed"

**Problem:** Azure CLI session expired.

**Solution:**
```bash
az login
azd up
```

### Error: ".env file not found"

**Problem:** azd didn't generate .env (deployment may have failed).

**Solution:**
1. Check azd deployment logs
2. Re-run: `azd up`
3. Verify `.env` exists: `ls -la .env`

### Agent doesn't respond / Connection error

**Problem:** Environment variables not loaded or incorrect.

**Solution:**
1. Verify .env exists and contains values:
   ```bash
   cat .env
   ```
2. Ensure you activated the virtual environment:
   ```bash
   source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
   ```
3. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Clean up resources

**Important:** Azure resources incur costs. Clean up when you're done with the lab.

### Option 1: Delete via azd (Recommended)

```bash
azd down
```

This deletes:
- All Azure resources
- The resource group
- Local .azure environment files

### Option 2: Delete via Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Resource Groups**
3. Select your resource group (e.g., `rg-trailguide-dev`)
4. Click **Delete resource group**
5. Type the resource group name to confirm
6. Click **Delete**

**✓ Checkpoint:** Resource group and all resources are deleted.

---

## Summary

In this lab, you:

**Part 1: Core deployment**
✅ **Provisioned Azure AI infrastructure** using Azure Developer CLI  
✅ **Deployed a Trail Guide Agent** to Microsoft Foundry  
✅ **Connected your local environment** to the cloud agent  
✅ **Tested conversational AI** with multi-turn context  
✅ **Learned IaC practices** with Bicep and azd

**Part 2: Web interface (optional)**
✅ **Deployed a web chat interface** using Azure Static Web Apps  
✅ **Published the agent** for public access via URL  
✅ **Understood multi-tier architecture** (browser → API → agent)  
✅ **Explored customization options** for production deployments

**Key Takeaways:**

- **azd simplifies deployment**: One command provisions everything
- **Bicep defines infrastructure**: Version-controlled, repeatable IaC
- **Microsoft Foundry hosts agents**: Managed platform for AI applications
- **.env stores secrets**: Auto-generated, never committed to git
- **Web deployment is simple**: Static Web Apps + Functions = public agent access
- **GenAIOps starts with infrastructure**: Solid foundation for evaluation, monitoring, deployment

---

## Next steps

Now that your agent is deployed, you're ready to:

- **Lab 02: Prompt Management** — Learn how to version and optimize agent prompts
- **Lab 03: Manual Evaluation** — Assess agent quality through human review
- **Lab 04: Automated Evaluation** — Implement metrics for response quality

Continue to the next lab to deepen your GenAIOps skills!
