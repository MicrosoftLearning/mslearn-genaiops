"""
Interactive test script for Trail Guide Agent.
Allows you to chat with the agent from the terminal.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient

# Load environment variables from repository root
repo_root = Path(__file__).parent.parent.parent
env_file = repo_root / '.env'
load_dotenv(env_file)

def interact_with_agent():
    """Start an interactive chat session with the Trail Guide Agent."""
    
    # Initialize project client
    project_client = AgentsClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )
    
    agent_Id = None
    
    for agent in project_client.list_agents():
        if getattr(agent, "name", None) == "trail-guide":
            agent_Id = agent.id
            break

    # Get agent name from environment or use default
    agent_name = os.getenv("AGENT_NAME", "trail-guide-v1")
    
    print(f"\n{'='*60}")
    print(f"Trail Guide Agent - Interactive Chat")
    print(f"Agent: {agent_name}")
    print(f"{'='*60}")
    print("\nType your questions or requests. Type 'exit' or 'quit' to end the session.\n")
    
    # Create a thread for the conversation
    thread = project_client.threads.create()
    print(f"Started conversation (Thread ID: {thread.id})\n")
    
    try:
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nEnding session. Goodbye!")
                break
            
            # Send message to agent
            project_client.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input
            )
            
            # Run the agent
            run = project_client.runs.create_and_process(
                thread_id=thread.id,
                agent_id=agent_Id
            )
            
            # Get the assistant's response
            messages = project_client.messages.list(thread_id=thread.id)
            
            # Find the latest assistant message
            for message in messages:
                if message.role == "assistant":
                    print(f"\nAgent: {message.content[0].text.value}\n")
                    break
                    
    except KeyboardInterrupt:
        print("\n\nSession interrupted. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
    finally:
        # Clean up thread
        try:
            project_client.threads.delete(thread.id)
            print(f"Conversation thread cleaned up.")
        except:
            pass

if __name__ == "__main__":
    interact_with_agent()