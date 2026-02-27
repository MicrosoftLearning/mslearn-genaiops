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

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()  # reads variables from the .env file in your project root

endpoint              = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
model_deployment_name = os.environ.get("MODEL_NAME", "gpt-4.1")
dataset_name          = "trail-guide-evaluation-dataset"
dataset_version       = "1"

# The script writes a plain-text summary here when it finishes.
# This file is committed to the branch so the GitHub Actions workflow
# can read it and post results as a PR comment — no re-running needed.
RESULTS_FILE = Path("evaluation_results.txt")

if not endpoint:
    print("ERROR: AZURE_AI_PROJECT_ENDPOINT is not set.")
    print("       Add it to your .env file and try again.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Azure clients
# ---------------------------------------------------------------------------

# AIProjectClient connects to your Azure AI Foundry project
project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

# The OpenAI-compatible client exposes the Evals API
client = project_client.get_openai_client()


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def section(title: str) -> None:
    """Print a clearly visible section header to make the log easy to skim."""
    print(f"\n{'=' * 80}")
    print(f"{title}")
    print(f"{'=' * 80}")


# ---------------------------------------------------------------------------
# Step 1 – Upload the evaluation dataset
# ---------------------------------------------------------------------------

def upload_dataset() -> str:
    """
    Upload the JSONL evaluation dataset to Azure AI Foundry and return its ID.

    The dataset is a list of JSON objects, each containing:
      - query        : the user question sent to the agent
      - response     : the agent's answer
      - ground_truth : the expected correct answer (used by some evaluators)
    """
    section("Step 1: Uploading evaluation dataset")

    dataset_path = (
        Path(__file__).parent.parent.parent
        / "data"
        / "trail_guide_evaluation_dataset.jsonl"
    )

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {dataset_path}.\n"
            "Make sure you are running the script from the repository root."
        )

    print(f"\nDataset: {dataset_path.name}")
    print("Uploading...")

    try:
        data_id = project_client.datasets.upload_file(
            name=dataset_name,
            version=dataset_version,
            file_path=str(dataset_path),
        ).id
        print(f"\n✓ Dataset uploaded successfully")

    except Exception as upload_error:
        # If this version was already uploaded in a previous run, reuse it.
        # Foundry does not allow uploading the same name+version twice.
        if "already exists" in str(upload_error):
            print(f"\n  Dataset version {dataset_version} already exists in Foundry.")
            print(f"  Retrieving existing dataset ID...")
            dataset_obj = project_client.datasets.get(name=dataset_name, version=dataset_version)
            data_id = dataset_obj.id
            print(f"  ✓ Using existing dataset")
        else:
            # Any other upload error is unexpected — re-raise so main() catches it
            raise

    print(f"  Dataset ID: {data_id}")
    return data_id


# ---------------------------------------------------------------------------
# Step 2 – Create the evaluation definition
# ---------------------------------------------------------------------------

def create_evaluation_definition():
    """
    Register an evaluation definition in Foundry.

    This tells the platform:
      - What data schema to expect (query / response / ground_truth)
      - Which built-in evaluators to run and how to map dataset fields to them

    Returns the evaluation object (its ID is needed in later steps).
    """
    section("Step 2: Creating evaluation definition")

    print(f"\nConfiguration:")
    print(f"  Judge Model: {model_deployment_name}")
    print(f"  Evaluators: Intent Resolution, Relevance, Groundedness")

    # Tell Foundry the shape of each record in the dataset
    data_source_config = DataSourceConfigCustom(
        type="custom",
        item_schema={
            "type": "object",
            "properties": {
                "query":        {"type": "string"},
                "response":     {"type": "string"},
                "ground_truth": {"type": "string"},
            },
            "required": ["query", "response", "ground_truth"],
        },
    )

    # Each entry names a built-in evaluator and maps dataset columns to its
    # expected parameters using the {{item.<column>}} template syntax.
    testing_criteria = [
        {
            "type": "azure_ai_evaluator",
            "name": "intent_resolution",
            "evaluator_name": "builtin.intent_resolution",
            "initialization_parameters": {"deployment_name": model_deployment_name},
            "data_mapping": {
                "query":    "{{item.query}}",
                "response": "{{item.response}}",
            },
        },
        {
            "type": "azure_ai_evaluator",
            "name": "relevance",
            "evaluator_name": "builtin.relevance",
            "initialization_parameters": {"deployment_name": model_deployment_name},
            "data_mapping": {
                "query":    "{{item.query}}",
                "response": "{{item.response}}",
            },
        },
        {
            "type": "azure_ai_evaluator",
            "name": "groundedness",
            "evaluator_name": "builtin.groundedness",
            "initialization_parameters": {"deployment_name": model_deployment_name},
            "data_mapping": {
                "query":    "{{item.query}}",
                "response": "{{item.response}}",
            },
        },
    ]

    print("\nCreating evaluation...")
    eval_object = client.evals.create(
        name="Trail Guide Quality Evaluation",
        data_source_config=data_source_config,
        testing_criteria=testing_criteria,
    )

    print(f"\n✓ Evaluation definition created")
    print(f"  Evaluation ID: {eval_object.id}")
    return eval_object


# ---------------------------------------------------------------------------
# Step 3 – Start the evaluation run
# ---------------------------------------------------------------------------

def run_evaluation(eval_object, data_id):
    """
    Start a cloud evaluation run that scores every record in the dataset.

    The run is asynchronous — Foundry processes items in parallel in the cloud.
    We get a run object immediately; its status starts as 'queued' or 'running'.
    """
    section("Step 3: Running cloud evaluation")

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


# ---------------------------------------------------------------------------
# Step 4 – Poll until the run finishes
# ---------------------------------------------------------------------------

def poll_for_results(eval_object, eval_run):
    """
    Repeatedly check the run status every 10 seconds until it is 'completed'.

    Returns the final run object (which contains the report URL and results).
    Exits with code 1 if the run fails so CI pipelines surface the error.
    """
    section("Step 4: Polling for completion")

    start_time = time.time()
    while True:
        run = client.evals.runs.retrieve(
            run_id=eval_run.id,
            eval_id=eval_object.id,
        )

        elapsed = int(time.time() - start_time)

        if run.status == "completed":
            print(f"\n\n✓ Evaluation completed in {elapsed} seconds")
            break
        elif run.status == "failed":
            # Raise so main() catches it, writes RESULTS_FILE, then exits
            error_detail = getattr(run, "error", None) or "No additional details available."
            raise RuntimeError(
                f"Evaluation run failed after {elapsed}s.\n"
                f"  Run ID     : {eval_run.id}\n"
                f"  Error      : {error_detail}\n"
                f"  Report URL : {getattr(run, 'report_url', 'N/A')}\n"
                f"  Open the Report URL in Azure AI Foundry portal for full details."
            )
        else:
            # Overwrite the same line so the terminal isn't flooded
            print(f"  [{elapsed}s] Status: {run.status}", end="\r", flush=True)
            time.sleep(10)

    return run


# ---------------------------------------------------------------------------
# Step 5 – Collect scores and save results
# ---------------------------------------------------------------------------

def retrieve_and_display_results(eval_object, run):
    """
    Fetch per-item evaluator outputs, compute aggregate statistics, print a
    human-readable summary, and write the same summary to RESULTS_FILE.

    Scores are on a 1-5 scale; a score >= 3 is considered a pass.

    The written file is intended to be committed to the branch so the
    GitHub Actions workflow can read it without re-running the evaluation.

    Returns the raw list of output items for any further inspection.
    """
    section("Step 5: Retrieving results")

    print(f"\nEvaluation Summary")
    print(f"  Report URL: {run.report_url}")

    # Retrieve every scored item from the run
    output_items = list(
        client.evals.runs.output_items.list(
            run_id=run.id,
            eval_id=eval_object.id,
        )
    )

    # Debug: print the raw structure of the first item so we can verify
    # the attribute names match what the API actually returns.
    # Remove this block once scores are confirmed working.
    if output_items:
        first = output_items[0]
        print(f"\n  [DEBUG] First item type : {type(first)}")
        print(f"  [DEBUG] First item attrs: {[a for a in dir(first) if not a.startswith('_')]}")
        if hasattr(first, "evaluator_outputs"):
            print(f"  [DEBUG] evaluator_outputs: {first.evaluator_outputs}")
        if hasattr(first, "__dict__"):
            print(f"  [DEBUG] item.__dict__: {first.__dict__}")

    # Separate items by status so we can report errors alongside scores
    errored_items = [
        item for item in output_items
        if getattr(item, "status", None) == "error"
    ]
    scored_items = [
        item for item in output_items
        if getattr(item, "status", None) != "error"
    ]

    if errored_items:
        print(f"\n  ⚠ {len(errored_items)} item(s) errored during evaluation.")
        print(f"    First error: {getattr(errored_items[0], 'error', 'details unavailable')}")
        print(f"    Open the Report URL in Foundry portal to inspect all failed items.")

    # Collect individual scores grouped by metric name
    scores: dict[str, list[float]] = {
        "intent_resolution": [],
        "relevance":         [],
        "groundedness":      [],
    }

    for item in scored_items:
        if hasattr(item, "evaluator_outputs"):
            for output in item.evaluator_outputs:
                if output.name in scores and hasattr(output, "score"):
                    scores[output.name].append(output.score)

    # --- Build summary text (printed to console and written to file) ---
    # Everything written to `lines` ends up both on screen and in the file,
    # so the file always has useful content regardless of whether scores loaded.

    metric_labels = {
        "intent_resolution": "Intent Resolution",
        "relevance":         "Relevance        ",
        "groundedness":      "Groundedness     ",
    }

    lines = [
        "=" * 80,
        " Trail Guide Agent - Evaluation Results",
        "=" * 80,
        f"\n  Report URL   : {run.report_url}",
        f"  Total items  : {len(output_items)}",
        f"  Errored items: {len(errored_items)}",
        f"  Scored items : {len(scored_items)}",
        "\nAverage Scores (1-5 scale, threshold: 3)",
    ]

    any_scores = False
    pass_lines = ["\nPass Rates (score >= 3)"]

    for key, label in metric_labels.items():
        values = scores[key]
        if values:
            any_scores = True
            avg  = sum(values) / len(values)
            rate = sum(1 for v in values if v >= 3) / len(values) * 100
            lines.append(f"  {label}: {avg:.2f} (n={len(values)})")
            pass_lines.append(f"  {label}: {rate:.1f}%")

    if not any_scores:
        # Scores missing — the evaluation may have completed but returned no
        # evaluator_outputs. Open the Report URL above to inspect in the portal.
        lines.append("  No scores returned — check the Report URL for details.")
        pass_lines.append("  No scores returned.")

    lines.extend(pass_lines)
    summary = "\n".join(lines)

    print(summary)

    # Write to file so the GitHub Actions 'comment' job can read it directly
    RESULTS_FILE.write_text(summary, encoding="utf-8")
    print(f"\n  Results saved to {RESULTS_FILE}")
    print(f"  Commit this file so the GitHub Actions workflow can read it.")

    return output_items


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Orchestrate the full evaluation pipeline step by step."""
    section(" Trail Guide Agent - Cloud Evaluation")
    print(f"\nConfiguration:")
    print(f"  Project: {endpoint}")
    print(f"  Model:   {model_deployment_name}")
    print(f"  Dataset: {dataset_name} (v{dataset_version})")

    try:
        data_id     = upload_dataset()                          # Step 1
        eval_object = create_evaluation_definition()            # Step 2
        eval_run    = run_evaluation(eval_object, data_id)      # Step 3
        run         = poll_for_results(eval_object, eval_run)   # Step 4
        retrieve_and_display_results(eval_object, run)          # Step 5

        section("Cloud evaluation complete")
        print(f"\nNext steps:")
        print(f"  1. Review detailed results in Azure AI Foundry portal")
        print(f"  2. Analyze patterns in successful and failed evaluations")
        print(f"  3. Commit {RESULTS_FILE} and push so the PR workflow can use it")

    except Exception as e:
        error_message = (
            f"{'=' * 80}\n"
            f" Trail Guide Agent - Evaluation FAILED\n"
            f"{'=' * 80}\n"
            f"\nError: {e}\n"
            f"\nTroubleshooting:\n"
            f"  - Verify AZURE_AI_PROJECT_ENDPOINT in .env file\n"
            f"  - Check Azure credentials: az login\n"
            f"  - Ensure GPT-4.1 model is deployed and accessible\n"
        )
        print(error_message)
        # Write the error to the results file so it's never left empty
        RESULTS_FILE.write_text(error_message, encoding="utf-8")
        sys.exit(1)


if __name__ == "__main__":
    main()
