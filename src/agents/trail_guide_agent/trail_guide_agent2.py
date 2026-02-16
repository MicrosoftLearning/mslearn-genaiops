import os
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Newer SDKs sometimes rename or move models; keep a safe import fallback.
try:
    from azure.ai.projects.models import PromptAgentDefinition  # type: ignore
except Exception:  # pragma: no cover
    PromptAgentDefinition = None  # type: ignore

# Load environment variables from repository root
repo_root = Path(__file__).parent.parent.parent.parent
env_file = repo_root / ".env"
load_dotenv(env_file)

# Read instructions from prompt file
prompt_file = Path(__file__).parent / "prompts" / "v2_instructions.txt"
with open(prompt_file, "r", encoding="utf-8") as f:
    instructions = f.read().strip()

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

agent_name = os.getenv("AGENT_NAME", "trail-guide")
model_name = os.getenv("MODEL_NAME", "gpt-4.1")

agents = project_client.agents

# Prefer the newer create_agent API when present; fall back to older create_version.
if hasattr(agents, "create_agent"):
    if PromptAgentDefinition is not None:
        agent = agents.create_agent(
            agent_name=agent_name,
            definition=PromptAgentDefinition(
                model=model_name,
                instructions=instructions,
            ),
        )
    else:
        # Fallback for SDKs that accept flat parameters (keeps script working across versions).
        agent = agents.create_agent(
            agent_name=agent_name,
            model=model_name,
            instructions=instructions,
        )
elif hasattr(agents, "create_version"):
    # Older template-style API
    agent = agents.create_version(
        agent_name=agent_name,
        definition=PromptAgentDefinition(  # type: ignore[misc]
            model=model_name,
            instructions=instructions,
        ),
    )
else:
    raise AttributeError(
        "No compatible agent creation method found on project_client.agents "
        "(expected create_agent or create_version)."
    )

print(
    f"Agent created (id: {getattr(agent, 'id', '<unknown>')}, "
    f"name: {getattr(agent, 'name', agent_name)}, "
    f"version: {getattr(agent, 'version', '<n/a>')})"
)