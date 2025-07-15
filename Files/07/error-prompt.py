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
        "content": """
                    Backpacking is a form of low-cost, independent travel that often involves carrying all necessary belongings in a backpack. It encompasses both urban travel, where individuals explore cities and cultures, and wilderness hiking, which involves trekking through natural landscapes with camping gear. This guide delves into the various aspects of backpacking, including its history, types, equipment, skills required, and cultural significance.

                    The concept of backpacking dates back thousands of years. Early humans traveled with their possessions on their backs out of necessity. Notably, Ötzi the Iceman, dating from between 3400 and 3100 BC, was found with a backpack made of animal skins and a wooden frame. In the 17th century, Italian adventurer Giovanni Francesco Gemelli Careri is considered one of the first people to engage in backpacker tourism.

                    The modern popularity of backpacking can be traced to the hippie trail of the 1960s and 1970s, which followed sections of the old Silk Road. Since then, backpacking has evolved into a mainstream form of tourism, attracting individuals seeking authentic experiences and personal growth.

                    Today, backpacking takes many forms. Some travelers wander through foreign cities with nothing but a map, a guidebook, and a sense of curiosity, staying in modest hostels or the homes of locals they meet along the way. Others head deep into the wilderness, hiking trails that span hundreds of miles, sleeping in tents under the stars and cooking meals over portable stoves. There are those who merge both experiences, perhaps beginning their journey in a bustling metropolis and ending it surrounded by mountains or forest. Each backpacker brings their own goals and rhythms to the journey, but all share a common drive: to explore, to experience, and to live simply with what they can carry.
                    """
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
