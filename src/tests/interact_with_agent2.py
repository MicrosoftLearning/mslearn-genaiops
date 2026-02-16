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


def _resolve_agent_id(client: AgentsClient, agent_name: str) -> str:
    """
    Resolve agent_id from AGENT_ID or by looking up an agent by name.
    """
    agent_id = os.getenv("AGENT_ID")
    if agent_id:
        return agent_id

    # Fallback: search by name
    matches = []
    for a in client.list_agents():
        if getattr(a, "name", None) == agent_name:
            matches.append(a)

    if not matches:
        # Print a short, actionable hint without requiring copy/paste
        print(f"\nError: AGENT_ID not set and no agent found named '{agent_name}'.")
        print("Available agents (name -> id):")
        for a in client.list_agents():
            print(f"  - {getattr(a, 'name', '<no-name>')} -> {getattr(a, 'id', '<no-id>')}")
        raise RuntimeError(
            "Set AGENT_ID in .env, or set AGENT_NAME to an existing agent name."
        )

    if len(matches) > 1:
        print(f"\nError: Multiple agents found named '{agent_name}'.")
        print("Candidates (id):")
        for a in matches:
            print(f"  - {a.id}")
        raise RuntimeError("Set AGENT_ID in .env to disambiguate.")

    return matches[0].id


def interact_with_agent():
    """Start an interactive chat session with the Trail Guide Agent."""

    client = AgentsClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    agent_name = os.getenv("AGENT_NAME", "trail-guide-v1")
    agent_id = _resolve_agent_id(client, agent_name)

    print(f"\n{'='*60}")
    print("Trail Guide Agent - Interactive Chat")
    print(f"Agent name: {agent_name}")
    print(f"Agent id:   {agent_id}")
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

            client.create_and_process_run(
                thread_id=thread.id,
                agent_id=agent_id,
            )

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