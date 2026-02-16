"""
Interactive test script for Trail Guide Agent.
Allows you to chat with the agent from the terminal.
"""
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables from repository root
repo_root = Path(__file__).parent.parent.parent
env_file = repo_root / ".env"
load_dotenv(env_file)


def _extract_message_text(message) -> str:
    """
    SDK message shapes vary by version. Handle common cases:
    - message.content is a string
    - message.content is a list with items that have .text.value
    - message.content is a list with items that have .text
    """
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content

    if isinstance(content, list) and content:
        first = content[0]
        text = getattr(first, "text", None)
        if isinstance(text, str):
            return text
        if text is not None and hasattr(text, "value"):
            return text.value  # type: ignore[attr-defined]

        # Last resort: stringify the first content item
        return str(first)

    return str(content)


def _run_agent(agents_client, thread_id: str, agent_name: str):
    """
    Prefer newer 'create_and_process_run' if available.
    Otherwise: create_run + poll get_run until terminal state.
    """
    if hasattr(agents_client, "create_and_process_run"):
        return agents_client.create_and_process_run(thread_id=thread_id, agent_name=agent_name)

    if not hasattr(agents_client, "create_run"):
        raise AttributeError(
            "No compatible run method found on project_client.agents "
            "(expected create_and_process_run or create_run)."
        )

    run = agents_client.create_run(thread_id=thread_id, agent_name=agent_name)

    # Poll until run completes (status names vary slightly across versions)
    terminal_statuses = {"completed", "failed", "cancelled", "canceled", "expired"}
    in_progress_statuses = {"queued", "in_progress", "running"}

    get_run = getattr(agents_client, "get_run", None)
    if get_run is None:
        # If SDK doesn't support polling, return the run object we have.
        return run

    while True:
        status = str(getattr(run, "status", "")).lower()
        if status in terminal_statuses:
            return run
        if status not in in_progress_statuses and status:
            # Unknown status; stop polling to avoid infinite loop.
            return run
        time.sleep(0.8)
        run = get_run(thread_id=thread_id, run_id=run.id)


def interact_with_agent():
    """Start an interactive chat session with the Trail Guide Agent."""

    # Initialize project client
    project_client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    # Get agent name from environment or use default
    agent_name = os.getenv("AGENT_NAME", "trail-guide-v1")

    print(f"\n{'='*60}")
    print("Trail Guide Agent - Interactive Chat")
    print(f"Agent: {agent_name}")
    print(f"{'='*60}")
    print("\nType your questions or requests. Type 'exit' or 'quit' to end the session.\n")

    agents = project_client.agents

    # Create a thread for the conversation
    thread = agents.create_thread()
    print(f"Started conversation (Thread ID: {thread.id})\n")

    try:
        while True:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "q"]:
                print("\nEnding session. Goodbye!")
                break

            # Send message to agent
            agents.create_message(
                thread_id=thread.id,
                role="user",
                content=user_input,
            )

            # Run the agent (SDK-version tolerant)
            _run_agent(agents, thread.id, agent_name)

            # Get latest assistant response
            messages = agents.list_messages(thread_id=thread.id)

            latest_assistant = None
            for m in messages:
                if getattr(m, "role", None) == "assistant":
                    latest_assistant = m
                    break

            if latest_assistant is None:
                print("\nAgent: (No assistant message returned.)\n")
            else:
                print(f"\nAgent: {_extract_message_text(latest_assistant)}\n")

    except KeyboardInterrupt:
        print("\n\nSession interrupted. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
    finally:
        # Clean up thread
        try:
            agents.delete_thread(thread.id)
            print("Conversation thread cleaned up.")
        except Exception:
            pass


if __name__ == "__main__":
    interact_with_agent()