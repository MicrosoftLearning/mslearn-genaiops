# Cloud Evaluation Pipeline

Complete evaluation script for automated agent quality assessment using Microsoft Foundry.

## Architecture

The evaluation pipeline uses a single, comprehensive script that handles all steps:

```
┌─────────────────────────────────────────────┐
│  evaluate_agent.py                          │
│  ─────────────────────────────────────────  │
│  1. Upload Dataset                          │
│  2. Define Evaluation                       │
│  3. Run Evaluation                          │
│  4. Poll for Completion                     │
│  5. Display Results                         │
└─────────────────────────────────────────────┘
```

Location: `src/evaluators/evaluate_agent.py`

## Usage

### Local Execution

Run the complete evaluation pipeline with one command:

```bash
python src/evaluators/evaluate_agent.py
```

The script automatically:
- Uploads the JSONL dataset to Microsoft Foundry
- Creates an evaluation definition with quality evaluators
- Runs the evaluation against 200 test cases
- Polls for completion (typically 5-10 minutes)
- Displays summary results and detailed statistics

### CI/CD Execution

The GitHub Actions workflow (`.github/workflows/evaluate-agent.yml`) runs the same script automatically:

- **Trigger**: Pull requests modifying agent code
- **Authentication**: Azure OIDC (Federated Identity)
- **Results**: Posted as PR comment and uploaded as artifact
- **Runtime**: ~6-12 minutes for complete evaluation

### Prerequisites

**Environment Variables:**
- `PROJECT_ENDPOINT`: Microsoft Foundry project endpoint
- `MODEL_NAME`: Judge model deployment name (default: gpt-4.1)

**Azure Authentication:**
- Local: `az login` (DefaultAzureCredential)
- CI/CD: Azure OIDC connection with GitHub

**Python Dependencies:**
```bash
pip install azure-ai-projects azure-identity python-dotenv openai
```

## Evaluation Criteria

The pipeline uses three Microsoft Foundry built-in evaluators:

| Evaluator          | Description                                    | Threshold |
|--------------------|------------------------------------------------|-----------|
| Intent Resolution  | Does the response address the user's query?    | ≥ 3       |
| Relevance          | Is the response relevant to the question?      | ≥ 3       |
| Groundedness       | Is the response grounded in provided context?  | ≥ 3       |

Scores: 1 (Poor) to 5 (Excellent)

## Dataset

**Location**: `data/datasets/trail_guide_evaluation_dataset.jsonl`

**Format**: JSONL with fields:
```json
{
  "query": "User question",
  "response": "Agent response",
  "ground_truth": "Reference answer"
}
```

**Size**: 200 evaluation items covering:
- Hiking gear recommendations
- Trail safety and navigation
- Weather and seasonal considerations
- Camping techniques
- Wildlife encounters

## GitHub Actions Configuration

### One-Time Setup

Before enabling automated PR evaluations, run the setup scripts locally:

```bash
# Upload dataset and get ID
python data/datasets/upload_dataset.py
# Copy the DATASET_ID from output

# Define evaluation and get ID  
python src/evaluators/define_evaluation.py
# Copy the EVAL_ID from output
```

### Required Secrets

Add to repository settings → Secrets and variables → Actions:

| Secret                  | Description                           | How to Get                |
|-------------------------|---------------------------------------|---------------------------|
| `AZURE_CLIENT_ID`       | Service principal client ID           | From `az ad sp` command   |
| `AZURE_TENANT_ID`       | Azure tenant ID                       | From `az ad sp` command   |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID                 | From `az ad sp` command   |
| `PROJECT_ENDPOINT`      | Microsoft Foundry project endpoint    | From `.env` file          |
| `DATASET_ID`            | Dataset ID from upload script         | From upload output        |
| `EVAL_ID`               | Evaluation ID from define script      | From define output        |

### Optional Variables

| Variable     | Description                      | Default   |
|--------------|----------------------------------|-----------|
| `MODEL_NAME` | Judge model deployment name      | `gpt-4.1` |

### Required Secrets

Add to repository settings → Secrets and variables → Actions:

| Secret                  | Description                           | How to Get                |
|-------------------------|---------------------------------------|---------------------------|
| `AZURE_CLIENT_ID`       | Service principal client ID           | From `az ad sp` command   |
| `AZURE_TENANT_ID`       | Azure tenant ID                       | From `az ad sp` command   |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription ID                 | From `az ad sp` command   |
| `PROJECT_ENDPOINT`      | Microsoft Foundry project endpoint    | From `.env` file  

**Console Output:**
- Average scores per evaluator
- Pass rates (percentage scoring ≥ 3)
- Total evaluation time
- Azure portal link

**Azure AI Foundry Portal:**
- Detailed per-item scores
- Evaluator reasoning
- Filtering and sorting
- Historical comparisons

**GitHub PR Comment (CI/CD):**
- Summary statistics
- Pass/fail status
- Link to full results

## Extending the Pipeline

### Add New Evaluators

Edit `src/evaluators/define_evaluation.py`:

```python
testing_criteria.append({
    "type": "azure_ai_evaluator",
    Update Evaluation Frequency

The main PR workflow only runs evaluations. To update dataset or evaluation definition:

**Manual approach:**
1. Run upload/define scripts locally
2. Update GitHub secrets with new IDs

**Automated approach:**
Use the `update-evaluation-dataset.yml` workflow:

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'data/datasets/trail_guide_evaluation_dataset.jsonl'
```

This workflow:
1. Triggers when dataset file changes
2. Uploads new dataset
3. Creates new evaluation definition
4. Outputs new IDs to update in secrets

### Update Dataset

Replace `data/datasets/trail_guide_evaluation_dataset.jsonl` with new JSONL file maintaining the same schema.

### Change Evaluation Frequency

Edit `.github/workflows/evaluate-agent.yml` triggers:

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  pull_request:
    branches: [main]
```

## Troubleshooting

**"Error: PROJECT_ENDPOINT environment variable not set"**
- Create `.env` file with `PROJECT_ENDPOINT=https://...`
- Or export environment variable

**"Dataset not found"**
- Verify `trail_guide_evaluation_dataset.jsonl` exists
- Check file path resolution

**"Authentication failed"**
- Run `az login` for local execution
- Verify service principal credentials for CI/CD

**"Evaluation failed" status**
- Check Azure portal logs
- Verify model deployment accessibility
- Confirm sufficient quota

## References

- [Microsoft Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Built-in Evaluators](https://learn.microsoft.com/azure/ai-studio/how-to/evaluate-generative-ai-app)
- [GitHub Actions for Azure](https://github.com/Azure/actions)
