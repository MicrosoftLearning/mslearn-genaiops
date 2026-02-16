import os
import sys
import subprocess
import json
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables
repo_root = Path(__file__).parent.parent.parent
env_file = repo_root / '.env'
load_dotenv(env_file)

def get_real_project_name(rg_name):
    """Auto-detects the actual AI Project name from Azure."""
    try:
        cmd = [
            "az", "resource", "list", "-g", rg_name,
            "--resource-type", "Microsoft.MachineLearningServices/workspaces",
            "--query", "[0].name", "-o", "tsv"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return os.environ.get("AZURE_AI_PROJECT_NAME")

def ensure_connection_exists(rg_name, project_name):
    """Checks for an OpenAI connection and creates it if missing."""
    print("Verifying OpenAI connection...")
    
    # 1. Check existing connections
    try:
        cmd = [
            "az", "rest", "--method", "get",
            "--url", f"https://management.azure.com/subscriptions/{os.environ.get('AZURE_SUBSCRIPTION_ID')}/resourceGroups/{rg_name}/providers/Microsoft.MachineLearningServices/workspaces/{project_name}/connections?api-version=2024-04-01-preview"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            connections = json.loads(result.stdout)
            for conn in connections.get('value', []):
                if conn['properties']['category'] == 'AzureOpenAI':
                    print(f"Found existing connection: {conn['name']}")
                    return conn['name']
    except Exception:
        pass

    # 2. If missing, find OpenAI Resource ID and Create
    print("Connection missing. Attempting auto-fix...")
    try:
        # Find OpenAI ID
        cmd = ["az", "resource", "list", "-g", rg_name, "--resource-type", "Microsoft.CognitiveServices/accounts", "--query", "[0].id", "-o", "tsv"]
        openai_id = subprocess.run(cmd, capture_output=True, text=True).stdout.strip()
        
        if not openai_id:
            print("Error: No OpenAI resource found.")
            return None

        # Create Connection
        body = {
            "properties": {
                "authType": "ApiKey",
                "category": "AI",
                "target": openai_id,
                "isSharedToAll": True,
                "metadata": {"ApiType": "Azure", "ResourceId": openai_id}
            }
        }
        
        url = f"https://management.azure.com/subscriptions/{os.environ.get('AZURE_SUBSCRIPTION_ID')}/resourceGroups/{rg_name}/providers/Microsoft.MachineLearningServices/workspaces/{project_name}/connections/aoai-connection?api-version=2024-04-01-preview"
        
        subprocess.run(
            ["az", "rest", "--method", "put", "--url", url, "--body", json.dumps(body)],
            capture_output=True, text=True
        )
        print("Success: Created 'aoai-connection'")
        return "aoai-connection"
    except Exception as e:
        print(f"Auto-fix failed: {e}")
        return None

def interact_with_agent():
    print(f"\n{'='*60}")
    print(f"Trail Guide Agent - Interactive Chat")
    print(f"{'='*60}")

    # 1. Resolve Resources
    rg_name = os.environ.get("AZURE_RESOURCE_GROUP")
    project_name = get_real_project_name(rg_name)
    
    print(f"Project: {project_name}")
    print(f"Resource Group: {rg_name}")

    # 2. Ensure Connection Exists (Self-Healing)
    connection_name = ensure_connection_exists(rg_name, project_name)

    # 3. Initialize Client
    try:
        project_client = AIProjectClient(
            endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
            credential=AzureDeveloperCliCredential(),
        )
    except Exception as e:
        print(f"Error connecting: {e}")
        return

    # 4. Find Agent
    agent_name = os.getenv("AGENT_NAME", "trail-guide")
    agent_id = None
    try:
        agents = project_client.agents.list()
        for agent in agents:
            if agent.name == agent_name:
                agent_id = agent.id
                break
        if not agent_id:
            print(f"Agent '{agent_name}' not found.")
            return
        print(f"Agent ID: {agent_id}")
    except Exception:
        print("Error listing agents.")
        return

    # 5. Chat Loop
    print("\nInitializing Chat Runtime...")
    try:
        # Use simple get_openai_client (v2 standard)
        # The auto-fix above ensures the default connection now exists!
        with project_client.get_openai_client() as openai_client:
            thread = openai_client.beta.threads.create()
            print(f"Session Started (Thread: {thread.id})\n")
            
            while True:
                user_input = input("You: ").strip()
                if user_input.lower() in ['exit', 'quit', 'q']: break
                if not user_input: continue

                openai_client.beta.threads.messages.create(
                    thread_id=thread.id, role="user", content=user_input
                )
                run = openai_client.beta.threads.runs.create_and_poll(
                    thread_id=thread.id, assistant_id=agent_id
                )

                if run.status == 'completed':
                    messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
                    for msg in messages:
                        if msg.role == "assistant":
                            for content in msg.content:
                                if content.type == 'text':
                                    print(f"\nAgent: {content.text.value}\n")
                            break
                else:
                    print(f"Run failed: {run.status}")

    except Exception as e:
        print(f"\nRuntime Error: {e}")

if __name__ == "__main__":
    interact_with_agent()
