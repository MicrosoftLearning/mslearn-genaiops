import os
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv()

# Read instructions from prompt file
prompt_file = Path(__file__).parent / 'prompts' / 'v1_instructions.txt'
with open(prompt_file, 'r') as f:
    instructions = f.read().strip()

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

agent = project_client.agents.create_version(
    agent_name=os.environ["AGENT_NAME"],
    definition=PromptAgentDefinition(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions=instructions,
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")