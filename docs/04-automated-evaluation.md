---
lab:
    title: 'Automated evaluation with cloud evaluators'
    description: 'Scale quality testing with automated cloud evaluators for systematic evaluation of AI agents'
    level: 300
    duration: 40 minutes
---

# Automated evaluation with cloud evaluators

This exercise takes approximately **40 minutes**.

> **Note**: This lab assumes a pre-configured lab environment with Visual Studio Code, Azure CLI, and Python already installed.

## Introduction

In this exercise, you'll use Microsoft Foundry's cloud evaluators to automatically assess quality at scale for the Adventure Works Trail Guide Agent. You'll run evaluations against a large test dataset (89 query-response pairs) to validate quality metrics and establish an automated evaluation pipeline for future changes.

**Scenario**: You're operating the Adventure Works Trail Guide Agent. You want to evaluate it against a large test dataset (89 query-response pairs) to validate quality metrics and establish an automated evaluation pipeline that can scale as your agent evolves.

You'll use the following evaluation criteria—automated at scale:

- **Intent Resolution**: Does the response fully address what the user asked?
- **Relevance**: Is the response appropriate and on-topic for the query?
- **Groundedness**: Are the claims factually accurate and based on domain knowledge?

## Set up the environment

To complete the tasks in this exercise, you need:

- Visual Studio Code
- Azure subscription with Microsoft Foundry access
- Git and [GitHub](https://github.com) account
- Python 3.9 or later
- Azure CLI and Azure Developer CLI (azd) installed

> **Tip**: If you haven't installed these prerequisites yet, see [Lab 00: Prerequisites](00-prerequisites.md) for installation instructions and links.

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

    > ⚠️ **Important**
    > In some environments, the VS Code integrated terminal may crash or close during the interactive login flow.
    > If this happens, authenticate using explicit credentials instead:
    > ```powershell
    > az login --username <your-username> --password <your-password>
    > ```

1. Provision resources:

    ```powershell
    azd up
    ```

    When prompted, provide:
    - **Environment name** (e.g., `dev`, `test`) - Used to name all resources
    - **Azure subscription** - Where resources will be created
    - **Location** - Azure region (recommended: Sweden Central)

    The command deploys the infrastructure from the `infra\` folder, creating:
    - **Resource Group** - Container for all resources
    - **Foundry (AI Services)** - The hub with access to models like GPT-4.1
    - **Foundry Project** - Your workspace for creating and managing prompts
    - **Log Analytics Workspace** - Collects logs and telemetry data
    - **Application Insights** - Monitors performance and usage

1. Create a `.env` file with the environment variables:

    ```powershell
    azd env get-values > .env
    ```

    > ⚠️ **Important – File Encoding**
    >
    > After generating the `.env` file, make sure it is saved using **UTF-8** encoding.
    >
    > In editors like **VS Code**, check the encoding indicator in the bottom-right corner.  
    > If it shows **UTF-16 LE** (or any encoding other than UTF-8), click it, choose **Save with Encoding**, and select **UTF-8**.
    >
    > Using the wrong encoding may cause environment variables to be read incorrectly.

    This creates a `.env` file in your project root with all the provisioned resource information.

### Install Python dependencies

With your Azure resources deployed, install the required Python packages.

1. In the VS Code terminal, create and activate a virtual environment:

    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

1. Install the required dependencies:

    ```powershell
    python -m pip install -r requirements.txt
    ```

    This installs necessary dependencies including:
    - `azure-ai-projects` - SDK for working with AI Foundry
    - `azure-identity` - Azure authentication
    - `python-dotenv` - Load environment variables

1. Add the agent configuration to your `.env` file:

    Open the `.env` file in your repository root and add:

    ```
    AGENT_NAME="trail-guide"
    MODEL_NAME="gpt-4.1"
    ```

## Understand the evaluation workflow

Cloud evaluation follows a structured workflow:

```text
1. Prepare Dataset
   ↓
2. Define Evaluation Criteria (Evaluators)
   ↓
3. Create Evaluation Definition
   ↓
4. Run Evaluation against Dataset
   ↓
5. Poll for Completion
   ↓
6. Retrieve & Interpret Results
   ↓
7. Analyze and Document Findings
```

### Dataset preparation

The repository includes `data/trail_guide_evaluation_dataset.jsonl` with 89 pre-generated query-response pairs covering diverse hiking scenarios. Each entry includes:

- `query`: User question
- `response`: Agent-generated answer
- `ground_truth`: Reference answer for accuracy comparison

### Evaluators

You'll use Microsoft Foundry's built-in quality evaluators:

| Evaluator | Measures | Output | Use Case |
|-----------|----------|--------|----------|
| **Intent Resolution** | Query intent addressed | 1-5 score | Ensure user needs are met |
| **Relevance** | Response addresses query | 1-5 score | Validate query-response alignment |
| **Groundedness** | Factual accuracy | 1-5 score | Ensure reliable information |

All evaluators use GPT-4.1 as an LLM judge and return:

- **Score**: 1-5 scale (5 = excellent)
- **Label**: Pass/Fail based on threshold (default: 3)
- **Reason**: Explanation of the score
- **Threshold**: Configurable pass/fail cutoff

## Run cloud evaluation

### Verify the evaluation dataset

First, examine the prepared dataset structure.

1. View the first few entries in the dataset:

    ```powershell
    Get-Content data/trail_guide_evaluation_dataset.jsonl -Head 3
    ```

    Output:
    ```json
    {"query": "What essential gear do I need for a summer day hike?", "response": "For a summer day hike, essential gear includes: proper hiking boots with good ankle support, moisture-wicking clothing in layers, a daypack (20-30L), 2 liters of water, high-energy snacks, sun protection (hat, sunglasses, sunscreen SPF 30+), a basic first aid kit, map and compass or GPS device, headlamp with extra batteries, and a whistle for emergencies...", "ground_truth": "Essential day hike gear includes footwear, water, food, sun protection, navigation tools, first aid, and emergency supplies."}
    {"query": "How much water should I bring on a 5-mile hike?", "response": "For a 5-mile hike, plan to bring at least 1-2 liters of water...", "ground_truth": "Bring 1-2 liters of water for a 5-mile hike, adjusting for weather and terrain."}
    ```

1. Count total entries in the dataset:

    ```powershell
    (Get-Content data/trail_guide_evaluation_dataset.jsonl).Count
    ```

    Expected: 89 entries

### Understand the evaluation pipeline

The repository includes a complete evaluation script that handles the entire cloud evaluation workflow. This all-in-one approach simplifies both local execution and CI/CD automation.

**Script: Complete Evaluation** (`src/evaluators/evaluate_agent.py`)

The script performs all evaluation steps automatically:

1. **Upload Dataset** - Uploads the JSONL dataset to Microsoft Foundry
2. **Define Evaluation** - Creates evaluation definition with quality evaluators (Intent Resolution, Relevance, Groundedness)
3. **Run Evaluation** - Starts the cloud evaluation run
4. **Poll for Completion** - Waits for evaluation to complete (5-10 minutes for 89 items)
5. **Display Results** - Retrieves and shows scoring statistics

This single-script approach makes it easy to run evaluations both locally during development and automatically in CI/CD pipelines.

### Run cloud evaluation

Execute the complete evaluation pipeline with one command.

1. **Run the evaluation**

    Run the evaluation script to execute the complete evaluation pipeline:

    ```powershell
    python src/evaluators/evaluate_agent.py
    ```

    Expected output:

    ```
    ================================================================================
     Trail Guide Agent - Cloud Evaluation
    ================================================================================

    Configuration:
      Project: https://<account>.services.ai.azure.com/api/projects/<project>
      Model: gpt-4.1
      Dataset: trail-guide-evaluation-dataset (v1)

    ================================================================================
    Step 1: Uploading evaluation dataset
    ================================================================================

    Dataset: trail_guide_evaluation_dataset.jsonl
    Uploading...

    ✓ Dataset uploaded successfully
      Dataset ID: file-abc123xyz

    ================================================================================
    Step 2: Creating evaluation definition
    ================================================================================

    Configuration:
      Judge Model: gpt-4.1
      Evaluators: Intent Resolution, Relevance, Groundedness

    Creating evaluation...

    ✓ Evaluation definition created
      Evaluation ID: eval-def456uvw

    ================================================================================
    Step 3: Running cloud evaluation
    ================================================================================

    ✓ Evaluation run started
      Run ID: run-ghi789rst
      Status: running

    This may take 5-10 minutes for 89 items...

    ================================================================================
    Step 4: Polling for completion
    ================================================================================
      [487s] Status: running

    ✓ Evaluation completed successfully
      Total time: 512 seconds

    ================================================================================
    Step 5: Retrieving results
    ================================================================================

    Evaluation Summary
      Report URL: https://<account>.services.ai.azure.com/projects/<project>/evaluations/...

    Average Scores (1-5 scale, threshold: 3)
      Intent Resolution: 4.52 (n=89)
      Relevance:         4.41 (n=89)
      Groundedness:      4.18 (n=89)

    Pass Rates (score >= 3)
      Intent Resolution: 96.0%
      Relevance:         95.5%
      Groundedness:      91.0%

    ================================================================================
    Cloud evaluation complete
    ================================================================================

    Next steps:
      1. Review detailed results in Azure AI Foundry portal
      2. Analyze patterns in successful and failed evaluations
      3. Document key findings and recommendations
    ```

    > **Note**: Evaluation runtime varies based on dataset size and model capacity. 89 items typically takes 5-15 minutes.

1. **Commit the results file**

    The script writes a summary to `evaluation_results.txt` in your project root. Commit this file so the GitHub Actions workflow can read it when it runs on your PR:

    ```powershell
    git add evaluation_results.txt
    git commit -m "Add evaluation results"
    git push
    ```

### Automate with GitHub Actions

The evaluation script integrates with GitHub Actions to automatically run evaluations on pull requests that modify agent code, and post results as a PR comment.

1. **Configure Azure authentication**

    Create a service principal for GitHub Actions:

    ```powershell
    az ad sp create-for-rbac --name "github-agent-evaluator"
    ```

    Save the `appId`, `tenant`, and `password` values from the output — you will use them in the next steps.

    Assign the **Azure AI User** role so the service principal can call the Foundry project API:

    ```powershell
    az role assignment create `
      --assignee "<appId>" `
      --role "Azure AI User" `
      --scope "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<ai-account-name>"
    ```

    > **Note**: Use the `AZURE_SUBSCRIPTION_ID`, `AZURE_RESOURCE_GROUP`, and `AZURE_AI_ACCOUNT_NAME` values from your `.env` file to fill in the scope. The `Azure AI Developer` role alone is **not sufficient** for this API.

    Create two federated credentials so the workflow can authenticate via OIDC for both manual runs and pull requests. GitHub sends a different token subject for each trigger type, so one credential is required per subject.

    **Credential 1 — manual runs and pushes to main:**

    Create `federated-credential.json`:

    ```json
    {
      "name": "github-actions",
      "issuer": "https://token.actions.githubusercontent.com",
      "subject": "repo:<your-org>/<your-repo>:ref:refs/heads/main",
      "audiences": ["api://AzureADTokenExchange"]
    }
    ```

    ```powershell
    az ad app federated-credential create `
      --id "<appId>" `
      --parameters @federated-credential.json
    Remove-Item federated-credential.json
    ```

    **Credential 2 — pull requests:**

    Create `federated-credential-pr.json`:

    ```json
    {
      "name": "github-actions-pr",
      "issuer": "https://token.actions.githubusercontent.com",
      "subject": "repo:<your-org>/<your-repo>:pull_request",
      "audiences": ["api://AzureADTokenExchange"]
    }
    ```

    ```powershell
    az ad app federated-credential create `
      --id "<appId>" `
      --parameters @federated-credential-pr.json
    Remove-Item federated-credential-pr.json
    ```

    > **Important**: Replace `<your-org>/<your-repo>` with your exact GitHub username and repository name. Both values are case-sensitive. If either credential is missing, the workflow will fail with an `AADSTS700213` authentication error for that trigger type.

1. **Configure GitHub Secrets**

    Add the following secrets to your repository under **Settings → Secrets and variables → Actions → New repository secret**:

    | Secret Name                    | Where to find it                                        |
    |--------------------------------|---------------------------------------------------------|
    | `AZURE_CLIENT_ID`              | `appId` from `az ad sp create-for-rbac` output          |
    | `AZURE_TENANT_ID`              | `tenant` from `az ad sp create-for-rbac` output         |
    | `AZURE_SUBSCRIPTION_ID`        | `AZURE_SUBSCRIPTION_ID` in your `.env` file             |
    | `AZURE_AI_PROJECT_ENDPOINT`    | `AZURE_AI_PROJECT_ENDPOINT` in your `.env` file         |

    Optionally, add a repository variable (not secret) for the model name:
    - **Settings → Secrets and variables → Actions → Variables → New repository variable**
    - Name: `MODEL_NAME`, Value: `gpt-4.1` (or `gpt-4.1-mini`)

1. **Test the workflow manually**

    Before testing with a PR, verify the workflow runs successfully with a manual trigger:

    1. Go to your repository on GitHub
    1. Navigate to **Actions → Evaluate Trail Guide Agent**
    1. Click **Run workflow**, select `main`, and click **Run workflow**
    1. Wait for the run to complete and verify it passes

1. **Test with a pull request**

    The workflow runs automatically when a PR modifies files under `src/agents/trail_guide_agent/`. To test it, create a branch, make a small change, and open a PR:

    ```powershell
    git checkout -b test/trigger-evaluation
    # Make a small change to any agent file, for example:
    code src/agents/trail_guide_agent/prompts/v1_instructions.txt
    git add .
    git commit -m "test: trigger evaluation workflow"
    git push origin test/trigger-evaluation
    ```

    Then open a pull request from `test/trigger-evaluation` → `main` on GitHub. The workflow will start automatically.

1. **View results in the PR**

    Once the workflow completes, a comment is posted to your PR with:
    - Evaluation scores and pass rates for each criterion
    - Full log output in a collapsible section
    - Link to detailed results in the Azure AI Foundry portal

### Review results in Azure portal

Examine detailed evaluation results in the Foundry portal.

1. Open the Report URL printed in the script output in your browser.

1. In the Azure AI Foundry portal, view:
   - **Aggregate metrics**: Overall pass rates and score distributions
   - **Individual test results**: Score, label (pass/fail), and reasoning for each query-response pair
   - **Evaluator details**: How each evaluator scored each response

1. Filter results:
   - View only failed items (score < 3)
   - Sort by specific evaluators
   - Search for specific queries

1. Identify patterns:
   - Which types of queries score lowest?
   - Are there consistent reasoning themes in failures?
   - Do certain evaluators flag more issues than others?

### Analyze evaluation results

Document your findings and create an analysis report.

1. Create a results directory:

    ```powershell
    New-Item -ItemType Directory -Path experiments/automated -Force
    New-Item -ItemType File -Path experiments/automated/evaluation_analysis.md
    ```

1. Add your evaluation analysis:

    ```markdown
    # Cloud Evaluation Analysis: Trail Guide Agent
    
    ## Evaluation Summary
    
    Evaluated: 89 test cases  
    Time: ~10 minutes  
    Scoring: GPT-4.1 as LLM judge (1-5 scale)
    
    | Evaluator | Average Score | Pass Rate | Assessment |
    |-----------|---------------|-----------|------------|
    | Intent Resolution | 4.52 | 96.0% | Excellent intent understanding |
    | Relevance | 4.41 | 95.5% | High query-response alignment |
    | Groundedness | 4.18 | 91.0% | Good factual accuracy |
    | **Average** | **4.37** | **94.2%** | **High Quality Overall** |
    
    ## Key Findings
    
    ### Strengths
    
    - High average scores across all quality dimensions (>4.0)
    - Excellent intent resolution shows queries are well understood
    - Strong relevance indicates appropriate query-response alignment
    - Pass rates above 90% demonstrate consistent quality
    
    ### Areas for Improvement
    
    - Groundedness slightly lower than other metrics (4.18)
    - Review failed cases (5-10%) to identify common patterns
    - Consider if certain query types need prompt refinement
    
    ### Failed Evaluations Analysis
    
    Review the 5-10% of responses that scored below threshold:
    
    - **Common failure patterns**: [Document patterns you observe]
    - **Query types affected**: [Identify if certain topics are problematic]
    - **Recommended improvements**: [Suggest prompt or agent changes]
    
    ## Automated Evaluation Benefits
    
    - **Scales** to hundreds/thousands of items efficiently
    - **Consistent** scoring criteria across all evaluations
    - **Fast** turnaround (10 minutes for 89 items)
    - **Repeatable** and trackable over time
    - **CI/CD ready** for integration into deployment pipelines
    - **Detailed reasoning** provided for each score
    
    ## Recommended Use Cases
    
    | Scenario | Recommended Approach | Rationale |
    |----------|---------------------|-----------|
    | Testing new prompts (50+ queries) | **Automated** | Scale, speed, consistency |
    | Continuous integration testing | **Automated** | Fast feedback in pipelines |
    | Baseline establishment | **Automated** | Quantifiable metrics at scale |
    | Production monitoring (ongoing) | **Automated** | Continuous quality tracking |
    | Investigating edge cases | **Manual review** | Deep dive into specific failures |
    
    ## Next Steps
    
    1. Use automated evaluation as primary quality gate for agent changes
    2. Set up automated evaluation in CI/CD pipeline
    3. Establish alerting thresholds (e.g., intent_resolution < 4.0 fails deployment)
    4. Schedule regular evaluations to track quality over time
    5. Investigate and address patterns in failed evaluations
    ```

1. Save the file and commit your analysis:

    ```powershell
    git add experiments/automated/
    git commit -m "Complete automated evaluation analysis"
    ```

## Compare evaluation configurations (Optional)

### Investigation goal

Explore how different evaluator configurations affect scoring and identify optimal thresholds for pass/fail decisions.

### Experiment with threshold adjustments

1. Modify `run_cloud_evaluation.py` to test different pass/fail thresholds.

1. Rerun evaluation with stricter thresholds (e.g., 4.0 instead of 3.0).

1. Document impact on pass rates and false positive/negative tradeoffs.

Create `experiments/automated/threshold_analysis.md` with:

- Pass rate comparison at different thresholds
- Recommendation for production threshold settings
- Justification based on risk tolerance

## Evaluate model comparison (Optional)

### Investigation goal

Compare evaluation results between GPT-4.1 and GPT-4.1-mini to understand quality-cost tradeoffs for your specific use case.

### Run evaluation on GPT-4.1-mini responses

1. Generate 89 responses from GPT-4.1-mini for the same queries.

1. Run cloud evaluation on both sets.

1. Compare quality scores to quantify the quality-cost tradeoff.

Create `experiments/automated/model_comparison.md` with:

- Side-by-side quality score comparison
- Cost analysis (estimate based on token usage)
- Validated recommendation: Which model for which use cases

## Troubleshooting

### Evaluation taking longer than expected

**Symptom**: Evaluation runs for 20+ minutes or appears stuck.

**Resolution**:
- Check Azure OpenAI quota and rate limits in Azure portal
- Reduce dataset size for initial testing (e.g., first 50 entries)
- Verify model deployment has sufficient capacity
- If timeout occurs, cancel and restart with smaller batch

### Authentication errors

**Symptom**: `401 Unauthorized` or `403 Forbidden` errors.

**Resolution**:
- Run `az login` to refresh Azure credentials
- Verify the service principal has the **Azure AI User** role at the CognitiveServices account scope — this role has `Microsoft.CognitiveServices/*` wildcard data actions required for `AIServices/agents/write`. `Azure AI Developer` alone is **not sufficient**
- Check `AZURE_AI_PROJECT_ENDPOINT` in `.env` file is correct and includes `/api/projects/<project>`

### OIDC login fails on PR workflows (`AADSTS700213`)

**Symptom**: Workflow succeeds when triggered manually but fails with `AADSTS700213: No matching federated identity record found` when triggered by a pull request.

**Resolution**:

GitHub sends a different OIDC subject depending on the trigger event:
- `workflow_dispatch` or `push` on main → subject is `repo:<org>/<repo>:ref:refs/heads/main`
- `pull_request` → subject is `repo:<org>/<repo>:pull_request`

You need **two** federated credentials, one per subject. Create the missing PR credential:

```powershell
# Create federated-credential-pr.json
@"
{
  "name": "github-actions-pr",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:<your-org>/<your-repo>:pull_request",
  "audiences": ["api://AzureADTokenExchange"]
}
"@ | Set-Content federated-credential-pr.json

az ad app federated-credential create `
  --id "<appId>" `
  --parameters @federated-credential-pr.json

Remove-Item federated-credential-pr.json
```

### Evaluator scoring seems inconsistent

**Symptom**: Automated scores differ significantly from expected manual scores.

**Resolution**:
- Review evaluator reasoning in Azure portal to understand scoring logic
- Check if query-response pairs have sufficient context for evaluation
- Verify `ground_truth` field provides appropriate factual reference
- Consider that LLM judges may prioritize different aspects than humans

### Rate limit errors during evaluation

**Symptom**: Evaluation fails with `429 Too Many Requests` errors.

**Resolution**:
- Check Azure OpenAI deployment tokens-per-minute (TPM) quota
- Increase quota in Azure portal if needed
- Split large datasets into smaller batches
- Add retry logic with exponential backoff

## Next steps

- Continue to [Lab 05: Monitoring](05-monitoring.md) to track production agent performance with Application Insights
- Explore [Lab 06: Tracing](06-tracing.md) to debug and optimize agent behavior using distributed tracing
