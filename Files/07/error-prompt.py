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

# Get the tracer instance
tracer = trace.get_tracer(__name__)

# Generate a session ID for this script execution
SESSION_ID = str(uuid.uuid4())

# Configure the tracer to include session ID in all spans
os.environ['AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED'] = 'true'

# Initialize the project
connection_string = os.getenv('PROJECT_CONNECTION_STRING')
if not connection_string:
    raise ValueError("PROJECT_CONNECTION_STRING environment variable is not set")

credential = DefaultAzureCredential()
project = AIProjectClient.from_connection_string(
    conn_str=connection_string,
    credential=credential
)

# Setup OpenTelemetry observability with Azure Monitor
application_insights_connection_string = project.telemetry.get_connection_string()
configure_azure_monitor(connection_string=application_insights_connection_string)
AIInferenceInstrumentor().instrument()

# Set up the chat completion client
default_connection = project.connections.get_default(
    connection_type=ConnectionType.AZURE_OPEN_AI,
    include_credentials=True,
)
chat_client = project.inference.get_chat_completions_client()
model_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")

# Generate a chat completion about camping supplies
with tracer.start_as_current_span("generate_completion") as span:
    try:
        span.set_attribute("session.id", SESSION_ID)

        response = chat_client.complete(
            model=model_name,
            messages=[
                SystemMessage("You are an AI assistant that acts as a travel guide."),
                UserMessage(content=("""
                    Backpacking is a form of low-cost, independent travel that often involves carrying all necessary belongings in a backpack. It encompasses both urban travel, where individuals explore cities and cultures, and wilderness hiking, which involves trekking through natural landscapes with camping gear. This guide delves into the various aspects of backpacking, including its history, types, equipment, skills required, and cultural significance.

                    The concept of backpacking dates back thousands of years. Early humans traveled with their possessions on their backs out of necessity. Notably, Ötzi the Iceman, dating from between 3400 and 3100 BC, was found with a backpack made of animal skins and a wooden frame. In the 17th century, Italian adventurer Giovanni Francesco Gemelli Careri is considered one of the first people to engage in backpacker tourism.

                    The modern popularity of backpacking can be traced to the hippie trail of the 1960s and 1970s, which followed sections of the old Silk Road. Since then, backpacking has evolved into a mainstream form of tourism, attracting individuals seeking authentic experiences and personal growth.

                    Today, backpacking takes many forms. Some travelers wander through foreign cities with nothing but a map, a guidebook, and a sense of curiosity, staying in modest hostels or the homes of locals they meet along the way. Others head deep into the wilderness, hiking trails that span hundreds of miles, sleeping in tents under the stars and cooking meals over portable stoves. There are those who merge both experiences, perhaps beginning their journey in a bustling metropolis and ending it surrounded by mountains or forest. Each backpacker brings their own goals and rhythms to the journey, but all share a common drive: to explore, to experience, and to live simply with what they can carry.
                    """
            ))]
        )

        print("\nAI's response:")
        print(response.choices[0].message.content)

    except Exception as e:
        span.set_status(Status(StatusCode.ERROR, str(e)))
        span.record_exception(e)
        raise