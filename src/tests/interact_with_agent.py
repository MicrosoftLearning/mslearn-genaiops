import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables
repo_root = Path(__file__).parent.parent.parent
env_file = repo_root / '.env'
load_dotenv(env_file)

def get_authenticated_client():
    """Robust client creation for both local and VM environments."""
    endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
    
    # Try 'azd' credential first (best for lab VMs)
    try:
        return AIProjectClient(
            endpoint=endpoint,
            credential=AzureDeveloperCliCredential(),
        )
    except Exception:
        # Fallback to default (local debugging, etc.)
        return AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(),
        )

def find_openai_connection(project_client):
    """
    Auto-discovers the Azure OpenAI connection.
    This ensures the script works regardless of what 'azd' names the connection.
    """
    try:
        connections = project_client.connections.list()
        for conn in connections:
            # Check for standard OpenAI connection types
            if "AzureOpenAI" in str(conn) or (hasattr(conn, 'type') and conn.type == "AzureOpenAI"):
                return conn.name
    except Exception as e:
        print(f"Warning: Could not list connections: {e}")
    return None

def interact_with_agent():
    print(f"\n{'='*60}")
    print(f"Trail Guide Agent - Interactive Chat")
    print(f"{'='*60}")
    
    # 1. Initialize Client
    try:
        project_client = get_authenticated_client()
    except Exception as e:
        print(f"Error connecting to project: {e}")
        print("Tip: Run 'azd auth login' if running locally.")
        return

    # 2. Find Agent ID
    agent_name = os.getenv("AGENT_NAME", "trail-guide")
    agent_id = None
    
    print(f"Connecting to Agent: {agent_name}...")
    try:
        agents = project_client.agents.list()
        for agent in agents:
            if agent.name == agent_name:
                agent_id = agent.id
                break
        
        if not agent_id:
            print(f"Error: Agent '{agent_name}' not found.")
            print("Did you run 'python src/trail_guide_agent.py' to create it?")
            return

        print(f"Success! Found Agent ID: {agent_id}")

    except Exception as e:
        print(f"Error listing agents: {e}")
        return

    # 3. Find Connection (The 'Magic' Step)
    connection_name = find_openai_connection(project_client)
    
    if not connection_name:
        # Fallback: Try the one we manually created, just in case
        connection_name = "aoai-connection"
        print(f"Warning: Auto-discovery failed. Trying fallback name: '{connection_name}'")
    else:
        print(f"Auto-detected Inference Connection: '{connection_name}'")

    # 4. Chat Loop
    print("\nInitializing Chat Runtime...")
    
    try:
        # Use the discovered connection name
        with project_client.get_openai_client(connection_name=connection_name) as openai_client:
            
            thread = openai_client.beta.threads.create()
            print(f"Session Started (Thread ID: {thread.id})\n")
            print("Type your questions. Type 'exit' to quit.\n")
            
            while True:
                user_input = input("You: ").strip()
                if not user_input: continue
                if user_input.lower() in ['exit', 'quit', 'q']:
                    break

                # Send
                openai_client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=user_input
                )

                # Run
                run = openai_client.beta.threads.runs.create_and_poll(
                    thread_id=thread.id,
                    assistant_id=agent_id
                )

                # Receive
                if run.status == 'completed':
                    messages = openai_client.beta.threads.messages.list(
                        thread_id=thread.id
                    )
                    for msg in messages:
                        if msg.role == "assistant":
                            for content in msg.content:
                                if content.type == 'text':
                                    print(f"\nAgent: {content.text.value}\n")
                            break
                else:
                    print(f"Run status: {run.status}")

    except Exception as e:
        print(f"\nRuntime Error: {e}")
        if "404" in str(e):
            print("\nTroubleshooting 404:")
            print("1. The project does not have a connection to Azure OpenAI.")
            print("2. Verify 'azd up' completed successfully.")

if __name__ == "__main__":
    interact_with_agent()