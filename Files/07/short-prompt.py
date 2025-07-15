import os
import uuid
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference.tracing import AIInferenceInstrumentor
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.ai.projects.models import ConnectionType
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

# Load environment variables from a .env file
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment =  os.getenv("MODEL_DEPLOYMENT")

# Get the tracer instance
tracer = trace.get_tracer(__name__)

# Generate a session ID for this script execution
SESSION_ID = str(uuid.uuid4())

# Configure the tracer to include session ID in all spans
os.environ['AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED'] = 'true'

# Initialize the project
project_client = AIProjectClient(            
    credential=DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True
    ),
    endpoint=project_endpoint,
)

# Setup OpenTelemetry observability with Azure Monitor
application_insights_connection_string = project_client.telemetry.get_connection_string()
configure_azure_monitor(connection_string=application_insights_connection_string)
AIInferenceInstrumentor().instrument()

# Set up the chat completion client
chat_client = project_client.inference.get_azure_openai_client(api_version="2024-10-21")

# Define the message to send to the model
messages=[
    { 
        "role": "system", 
        "content": "You are an AI assistant that acts as a travel guide." 
    },
    { 
        "role": "user", 
        "content": ("What are some recommended supplies for a camping trip in the mountains?"
                    "(1 sentence with bullet points)"
        )
    }
]

# Generate a chat completion about camping supplies
with tracer.start_as_current_span("generate_completion") as span:
    try:
        span.set_attribute("session.id", SESSION_ID)

        response = chat_client.chat.completions.create(
          model=model_deployment,
          messages=messages
        )

        print("\nAI's response:")
        print(response.choices[0].message.content)

    except Exception as e:
        span.set_status(Status(StatusCode.ERROR, str(e)))
        span.record_exception(e)
        raise
