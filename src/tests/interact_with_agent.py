import os
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import AzureDeveloperCliCredential
from azure.ai.projects import AIProjectClient

# 1. Setup
load_dotenv(Path(__file__).parent.parent.parent / '.env')

def simple_chat():
    # 2. Connect
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=AzureDeveloperCliCredential()
    )

    # 3. Find Agent
    agent_name = os.getenv("AGENT_NAME", "trail-guide")
    agent = next((a for a in project_client.agents.list() if a.name == agent_name), None)
    
    if not agent:
        print(f"Agent {agent_name} not found."); return

    # 4. Chat using the NATIVE SDK methods
    # This avoids the get_openai_client() 404 issues
    thread = project_client.agents.create_thread()
    print(f"Chat started! (Agent: {agent.name})\n")

    while True:
        user_msg = input("You: ").strip()
        if user_msg.lower() in ['exit', 'quit']: break

        # Send message
        project_client.agents.create_message(thread_id=thread.id, role="user", content=user_msg)

        # Run and Wait (The SDK handles the polling for you here)
        run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)

        # Print Response
        if run.status == "completed":
            messages = project_client.agents.list_messages(thread_id=thread.id)
            # The first message in the list is the most recent
            print(f"\nAgent: {messages.data[0].content[0].text.value}\n")

if __name__ == "__main__":
    simple_chat()
