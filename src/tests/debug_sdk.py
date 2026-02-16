import azure.ai.projects
import os
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load env
repo_root = Path(__file__).parent.parent.parent
env_file = repo_root / '.env'
load_dotenv(env_file)

print(f"Azure AI Projects SDK Version: {azure.ai.projects.__version__}")

try:
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )
    
    print("\n--- Project Client Attributes ---")
    print([d for d in dir(project_client) if not d.startswith('_')])

    print("\n--- Agents Operations Attributes (project_client.agents) ---")
    # This will list what commands ARE available (e.g., create_thread, list_agents, etc.)
    print([d for d in dir(project_client.agents) if not d.startswith('_')])

except Exception as e:
    print(f"Error initializing client: {e}")