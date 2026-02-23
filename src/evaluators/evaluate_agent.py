"""
Complete Cloud Evaluation Script for Trail Guide Agent

Runs the full evaluation pipeline:
1. Uploads evaluation dataset to Microsoft Foundry
2. Creates evaluation definition with quality evaluators
3. Runs evaluation and polls for completion
4. Retrieves and displays results

Evaluates: Intent Resolution, Relevance, and Groundedness
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai.types.eval_create_params import DataSourceConfigCustom
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileID,
)

# Load environment variables
load_dotenv()
endpoint = os.environ.get("PROJECT_ENDPOINT")
model_deployment_name = os.environ.get("MODEL_NAME", "gpt-4.1")
dataset_name = "trail-guide-evaluation-dataset"
dataset_version = "1"

if not endpoint:
    print("Error: PROJECT_ENDPOINT environment variable not set")
    sys.exit(1)

# Initialize project client
project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

# Get OpenAI client for evaluation API
client = project_client.get_openai_client()

def upload_dataset():
    """Upload the evaluation dataset to Foundry."""
    print("\n" + "=" * 80)
    print("Step 1: Uploading evaluation dataset")
    print("=" * 80)
    
    dataset_path = Path(__file__).parent.parent.parent / "data" / "datasets" / "trail_guide_evaluation_dataset.jsonl"
    
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")
    
    print(f"\nDataset: {dataset_path.name}")
    print(f"Uploading...")
    
    data_id = project_client.datasets.upload_file(
        name=dataset_name,
        version=dataset_version,
        file_path=str(dataset_path),
    ).id
    
    print(f"\n✓ Dataset uploaded successfully")
    print(f"  Dataset ID: {data_id}")
    
    return data_id

def create_evaluation_definition():
    """Create the evaluation definition with quality evaluators."""
    print("\n" + "=" * 80)
    print("Step 2: Creating evaluation definition")
    print("=" * 80)
    
    print(f"\nConfiguration:")
    print(f"  Judge Model: {model_deployment_name}")
    print(f"  Evaluators: Intent Resolution, Relevance, Groundedness")
    
    # Define data schema (what fields are in our JSONL)
    data_source_config = DataSourceConfigCustom(
        type="custom",
        item_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "response": {"type": "string"},
                "ground_truth": {"type": "string"},
            },
            "required": ["query", "response", "ground_truth"],
        },
    )
    
    # Define testing criteria (evaluators)
    testing_criteria = [
        {
            "type": "azure_ai_evaluator",
            "name": "intent_resolution",
            "evaluator_name": "builtin.intent_resolution",
            "initialization_parameters": {
                "deployment_name": model_deployment_name,
            },
            "data_mapping": {
                "query": "{{item.query}}",
                "response": "{{item.response}}",
            },
        },
        {
            "type": "azure_ai_evaluator",
            "name": "relevance",
            "evaluator_name": "builtin.relevance",
            "initialization_parameters": {
                "deployment_name": model_deployment_name,
            },
            "data_mapping": {
                "query": "{{item.query}}",
                "response": "{{item.response}}",
            },
        },
        {
            "type": "azure_ai_evaluator",
            "name": "groundedness",
            "evaluator_name": "builtin.groundedness",
            "initialization_parameters": {
                "deployment_name": model_deployment_name,
            },
            "data_mapping": {
                "query": "{{item.query}}",
                "response": "{{item.response}}",
            },
        },
    ]
    
    # Create the evaluation definition
    print("\nCreating evaluation...")
    eval_object = client.evals.create(
        name="Trail Guide Quality Evaluation",
        data_source_config=data_source_config,
        testing_criteria=testing_criteria,
    )
    
    print(f"\n✓ Evaluation definition created")
    print(f"  Evaluation ID: {eval_object.id}")
    
    return eval_object

def run_evaluation(eval_object, data_id):
    """Run the evaluation against the uploaded dataset."""
    print("\n" + "=" * 80)
    print("Step 3: Running cloud evaluation")
    print("=" * 80)
    
    eval_run = client.evals.runs.create(
        eval_id=eval_object.id,
        name="trail-guide-baseline-eval",
        data_source=CreateEvalJSONLRunDataSourceParam(
            type="jsonl",
            source=SourceFileID(
                type="file_id",
                id=data_id,
            ),
        ),
    )
    
    print(f"\n✓ Evaluation run started")
    print(f"  Run ID: {eval_run.id}")
    print(f"  Status: {eval_run.status}")
    print(f"\nThis may take 5-10 minutes for 200 items...")
    
    return eval_run

def poll_for_results(eval_object, eval_run):
    """Poll the evaluation run until complete."""
    print("\n" + "=" * 80)
    print("Step 4: Polling for completion")
    print("=" * 80)
    
    start_time = time.time()
    while True:
        run = client.evals.runs.retrieve(
            run_id=eval_run.id,
            eval_id=eval_object.id
        )
        
        elapsed = int(time.time() - start_time)
        status_msg = f"  [{elapsed}s] Status: {run.status}"
        
        if run.status == "completed":
            print(f"\n\n✓ Evaluation completed successfully")
            print(f"  Total time: {elapsed} seconds")
            break
        elif run.status == "failed":
            print(f"\n\n✗ Evaluation failed")
            print(f"  Check Azure portal for details")
            sys.exit(1)
        else:
            print(f"{status_msg}", end="\r", flush=True)
            time.sleep(10)
    
    return run

def retrieve_and_display_results(eval_object, run):
    """Retrieve evaluation results and display summary."""
    print("\n" + "=" * 80)
    print("Step 5: Retrieving results")
    print("=" * 80)
    
    # Get aggregate results
    print(f"\nEvaluation Summary")
    print(f"  Report URL: {run.report_url}")
    
    # Retrieve detailed output items
    output_items = list(
        client.evals.runs.output_items.list(
            run_id=run.id,
            eval_id=eval_object.id
        )
    )
    
    # Calculate statistics
    intent_resolution_scores = []
    relevance_scores = []
    groundedness_scores = []
    
    for item in output_items:
        if hasattr(item, 'evaluator_outputs'):
            for output in item.evaluator_outputs:
                if output.name == "intent_resolution" and hasattr(output, 'score'):
                    intent_resolution_scores.append(output.score)
                elif output.name == "relevance" and hasattr(output, 'score'):
                    relevance_scores.append(output.score)
                elif output.name == "groundedness" and hasattr(output, 'score'):
                    groundedness_scores.append(output.score)
    
    # Display averages
    print(f"\nAverage Scores (1-5 scale, threshold: 3)")
    if intent_resolution_scores:
        avg_intent = sum(intent_resolution_scores) / len(intent_resolution_scores)
        print(f"  Intent Resolution: {avg_intent:.2f} (n={len(intent_resolution_scores)})")
    
    if relevance_scores:
        avg_relevance = sum(relevance_scores) / len(relevance_scores)
        print(f"  Relevance:         {avg_relevance:.2f} (n={len(relevance_scores)})")
    
    if groundedness_scores:
        avg_groundedness = sum(groundedness_scores) / len(groundedness_scores)
        print(f"  Groundedness:      {avg_groundedness:.2f} (n={len(groundedness_scores)})")
    
    # Calculate pass rates
    if intent_resolution_scores:
        intent_pass_rate = sum(1 for s in intent_resolution_scores if s >= 3) / len(intent_resolution_scores) * 100
        print(f"\nPass Rates (score >= 3)")
        print(f"  Intent Resolution: {intent_pass_rate:.1f}%")
    
    if relevance_scores:
        relevance_pass_rate = sum(1 for s in relevance_scores if s >= 3) / len(relevance_scores) * 100
        print(f"  Relevance:         {relevance_pass_rate:.1f}%")
    
    if groundedness_scores:
        groundedness_pass_rate = sum(1 for s in groundedness_scores if s >= 3) / len(groundedness_scores) * 100
        print(f"  Groundedness:      {groundedness_pass_rate:.1f}%")
    
    return output_items

def main():
    """Main execution flow."""
    print("\n" + "=" * 80)
    print(" Trail Guide Agent - Cloud Evaluation")
    print("=" * 80)
    print(f"\nConfiguration:")
    print(f"  Project: {endpoint}")
    print(f"  Model: {model_deployment_name}")
    print(f"  Dataset: {dataset_name} (v{dataset_version})")
    
    try:
        # Step 1: Upload dataset
        data_id = upload_dataset()
        
        # Step 2: Create evaluation definition
        eval_object = create_evaluation_definition()
        
        # Step 3: Run evaluation
        eval_run = run_evaluation(eval_object, data_id)
        
        # Step 4: Poll for results
        run = poll_for_results(eval_object, eval_run)
        
        # Step 5: Retrieve and display results
        output_items = retrieve_and_display_results(eval_object, run)
        
        print("\n" + "=" * 80)
        print("Cloud evaluation complete")
        print("=" * 80)
        print(f"\nNext steps:")
        print(f"  1. Review detailed results in Azure AI Foundry portal")
        print(f"  2. Analyze patterns in successful and failed evaluations")
        print(f"  3. Document key findings and recommendations")
        
    except Exception as e:
        print(f"\nError: {e}")
        print(f"\nTroubleshooting:")
        print(f"  - Verify PROJECT_ENDPOINT in .env file")
        print(f"  - Check Azure credentials: az login")
        print(f"  - Ensure GPT-4.1 model is deployed and accessible")
        sys.exit(1)

if __name__ == "__main__":
    main()
