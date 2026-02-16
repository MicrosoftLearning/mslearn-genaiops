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
env_file = repo_root / ".env"
load_dotenv(env_file)


def interact_with_agent():
    """Start an interactive chat session with the Trail Guide Agent."""

    client = AgentsClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    # AgentsClient typically uses agent_id (not name)
    agent_id = os.getenv("AGENT_ID")
    if not agent_id:
        raise RuntimeError(
            "Missing AGENT_ID in environment. Set AGENT_ID in your .env to the Agent's ID."
        )

    print(f"\n{'='*60}")
    print("Trail Guide Agent - Interactive Chat")
    print(f"Agent ID: {agent_id}")
    print(f"{'='*60}")
    print("\nType your questions or requests. Type 'exit' or 'quit' to end the session.\n")

    thread = client.create_thread()
    print(f"Started conversation (Thread ID: {thread.id})\n")

    try:
        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "q"]:
                print("\nEnding session. Goodbye!")
                break

            client.create_message(
                thread_id=thread.id,
                role="user",
                content=user_input,
            )

            # Run the agent
            client.create_and_process_run(
                thread_id=thread.id,
                agent_id=agent_id,
            )

            # Show latest assistant message
            messages = client.list_messages(thread_id=thread.id)
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
        try:
            client.delete_thread(thread.id)
            print("Conversation thread cleaned up.")
        except Exception:
            pass


if __name__ == "__main__":
    interact_with_agent()