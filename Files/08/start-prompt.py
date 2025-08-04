import os
import uuid
import json
import time
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor

# Load environment and set session ID
load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment =  os.getenv("MODEL_DEPLOYMENT")
tracer = trace.get_tracer(__name__)
SESSION_ID = str(uuid.uuid4())
os.environ['OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT'] = 'true'

# Initialize AI Project
project_client = AIProjectClient(            
    credential=DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True
    ),
    endpoint=project_endpoint,
)
# Configure telemetry and instrument tracing
ai_conn_str = project_client.telemetry.get_application_insights_connection_string()
configure_azure_monitor(connection_string=ai_conn_str)
OpenAIInstrumentor().instrument()

# Prepare chat client
chat_client = project_client.get_openai_client(api_version="2024-10-21")

# Mock product list
mock_product_catalog = [
    "Alpine Trekking Boots",
    "Waterproof Backpack",
    "Carbon Fiber Hiking Poles",
    "Thermal Base Layers",
    "Ultralight Tent",
    "Solar-Powered Lantern",
    "Comfort Fit Hiking Shoes",
    "Insulated Water Bottles",
    "Lightweight Dog Harness",
    "Dog Hiking Saddle Bags",
    "Compact First Aid Kit",
    "Multi-Tool Knife",
    "Trail Mix Energy Bars"
]

# Function to call the model and handle tracing


# Function to recommend a hike based on user preferences


# Function to generate a trip profile for the recommended hike


# Function to match recommended gear with products in the catalog


# ---- Main Flow ----
