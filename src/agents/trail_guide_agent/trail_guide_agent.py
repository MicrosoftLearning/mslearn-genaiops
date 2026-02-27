import os
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

# Load environment variables from .env file
load_dotenv()

# Read instructions from prompt file
prompt_file = Path(__file__).parent / 'prompts' / 'v4_optimized_concise.txt'
with open(prompt_file, 'r') as f:
    instructions = f.read().strip()

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

agent = project_client.agents.create_version(
    agent_name=os.environ["AGENT_NAME"],
    definition=PromptAgentDefinition(
        model=os.getenv("MODEL_NAME", "gpt-4.1"),  # Use Global Standard model
        instructions=instructions,
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")