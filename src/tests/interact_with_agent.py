"""
Interactive test script for Trail Guide Agent.
Allows you to chat with the agent from the terminal.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables from repository root
repo_root = Path(__file__).parent.parent.parent
env_file = repo_root / '.env'
load_dotenv(env_file)

def interact_with_agent():
    """Start an interactive chat session with the Trail Guide Agent."""
    
    # Initialize project client
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )
    
    # Get agent name from environment or use default
    agent_name = os.getenv("AGENT_NAME", "trail-guide-v1")

    openai_client = project_client.get_openai_client()
    
    print(f"\n{'='*60}")
    print(f"Trail Guide Agent - Interactive Chat")
    print(f"Agent: {agent_name}")
    print(f"{'='*60}")
    print("\nType your questions or requests. Type 'exit' or 'quit' to end the session.\n")
    
    # Create a thread for the conversation
    conversation = openai_client.conversations.create()
    print(f"Started conversation (Conversation ID: {conversation.id})\n")
    
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
            response = openai_client.responses.create(
                conversation_id=conversation.id,
                extra_body={"agent": {"name": agent_name, "type": "agent_reference"}},
                input=user_input,
                )
            print(f"Response output: {response.output_text}")
                    
    except KeyboardInterrupt:
        print("\n\nSession interrupted. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
    finally:
        # Clean up thread
        try:
            openai_client.conversations.delete(conversation.id)
            print(f"Conversation thread cleaned up.")
        except:
            pass

if __name__ == "__main__":
    interact_with_agent()