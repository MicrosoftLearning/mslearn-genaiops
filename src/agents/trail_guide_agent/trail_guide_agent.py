import os
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

# Find and load .env from repo root (walk upwards until found)
current = Path(__file__).resolve()
env_file = None
for parent in [current.parent, *current.parents]:
    candidate = parent / ".env"
    if candidate.exists():
        env_file = candidate
        break

if env_file is None:
    raise FileNotFoundError("Could not find a .env file by walking up from this script location.")

loaded = load_dotenv(env_file)
if not loaded:
    raise RuntimeError(f"Failed to load .env from: {env_file}")

# Use the exact key name you set in .env (case-sensitive)
endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
if not endpoint:
    raise KeyError(
        f"Missing AZURE_AI_PROJECT_ENDPOINT. .env loaded from: {env_file}. "
        "Ensure the key name matches exactly (including casing)."
    )

# Read instructions from prompt file
prompt_file = Path(__file__).parent / "prompts" / "v2_instructions.txt"
with open(prompt_file, "r", encoding="utf-8") as f:
    instructions = f.read().strip()

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

agent = project_client.agents.create_version(
    agent_name=os.environ["AGENT_NAME"],
    definition=PromptAgentDefinition(
        model=os.getenv("MODEL_NAME", "gpt-4.1"),
        instructions=instructions,
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")