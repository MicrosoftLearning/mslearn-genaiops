"""
Upload evaluation dataset to Microsoft Foundry

Uploads the trail guide evaluation dataset and outputs the dataset ID
for use in subsequent evaluation steps.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables
load_dotenv()
endpoint = os.environ.get("PROJECT_ENDPOINT")

if not endpoint:
    print("Error: PROJECT_ENDPOINT environment variable not set")
    sys.exit(1)

# Configuration
dataset_name = "trail-guide-evaluation-dataset"
dataset_version = "1"
dataset_filename = "trail_guide_evaluation_dataset.jsonl"

# Initialize project client
project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

def upload_dataset():
    """Upload the evaluation dataset to Foundry."""
    print("=" * 80)
    print("Uploading evaluation dataset to Microsoft Foundry")
    print("=" * 80)
    
    # Get dataset path (same directory as this script)
    dataset_path = Path(__file__).parent / dataset_filename
    
    if not dataset_path.exists():
        print(f"Error: Dataset not found at {dataset_path}")
        sys.exit(1)
    
    print(f"\nDataset: {dataset_path.name}")
    print(f"Name: {dataset_name}")
    print(f"Version: {dataset_version}")
    
    # Upload dataset
    print("\nUploading...")
    data_id = project_client.datasets.upload_file(
        name=dataset_name,
        version=dataset_version,
        file_path=str(dataset_path),
    ).id
    
    print(f"\n✓ Dataset uploaded successfully")
    print(f"  Dataset ID: {data_id}")
    
    # Save dataset ID for next steps
    state_file = Path(__file__).parent.parent.parent / ".evaluation_state"
    with open(state_file, "w") as f:
        f.write(f"DATASET_ID={data_id}\n")
    
    print(f"\n✓ Dataset ID saved to .evaluation_state")
    
    # Output for GitHub Actions
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"dataset_id={data_id}\n")
    
    return data_id

if __name__ == "__main__":
    try:
        data_id = upload_dataset()
        print("\n" + "=" * 80)
        print("Next step: Define evaluation")
        print(f"  python src/evaluators/define_evaluation.py")
        print("=" * 80)
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("  - Verify PROJECT_ENDPOINT in .env file")
        print("  - Check Azure credentials: az login")
        print("  - Ensure dataset file exists in data/datasets/")
        sys.exit(1)
