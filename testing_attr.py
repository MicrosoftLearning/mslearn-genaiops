import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv

load_dotenv()

client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Get one agent (or filter by name)
agent = next(client.agents.list())

# See all attribute names
print(dir(agent))

# Or see a dict of public attributes
attrs = {k: v for k, v in agent.__dict__.items() if not k.startswith("_")}
for k, v in attrs.items():
    print(k, "=", v)