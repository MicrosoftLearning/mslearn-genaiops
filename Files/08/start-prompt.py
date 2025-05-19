import os
import uuid
import json
import time
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference.tracing import AIInferenceInstrumentor
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

# Load environment and set session ID
load_dotenv()
tracer = trace.get_tracer(__name__)
SESSION_ID = str(uuid.uuid4())
os.environ['AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED'] = 'true'

# Initialize AI Project
conn_str = os.getenv("PROJECT_CONNECTION_STRING")
if not conn_str:
    raise ValueError("Missing PROJECT_CONNECTION_STRING in environment.")
credential = DefaultAzureCredential()
project = AIProjectClient.from_connection_string(conn_str, credential=credential)

# Configure telemetry and instrument tracing
ai_conn_str = project.telemetry.get_connection_string()
configure_azure_monitor(connection_string=ai_conn_str)
AIInferenceInstrumentor().instrument()

# Prepare chat client
chat_client = project.inference.get_chat_completions_client()
model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")

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
