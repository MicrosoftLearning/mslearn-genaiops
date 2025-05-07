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
def call_model(system_prompt, user_prompt, span_name):
    with tracer.start_as_current_span(span_name) as span:
        span.set_attribute("session.id", SESSION_ID)
        span.set_attribute("prompt.user", user_prompt)
        start_time = time.time()

        response = chat_client.complete(
            model=model_name,
            messages=[SystemMessage(system_prompt), UserMessage(user_prompt)]
        )

        duration = time.time() - start_time
        output = response.choices[0].message.content
        span.set_attribute("response.time", duration)
        span.set_attribute("response.tokens", len(output.split()))
        return output

# Function to recommend a hike based on user preferences
def recommend_hike(preferences):
    with tracer.start_as_current_span("recommend_hike") as span:
        prompt = f"""
        Recommend a named hiking trail based on the following user preferences.
        Provide only the name of the trail and a one-sentence summary.
        Preferences: {preferences}
        """
        response = call_model(
            "You are an expert hiking trail recommender.",
            prompt,
            "recommend_model_call"
        )
        span.set_attribute("hike_recommendation", response.strip())
        return response.strip()

# Function to generate a trip profile for the recommended hike
def generate_trip_profile(hike_name):
    with tracer.start_as_current_span("trip_profile_generation") as span:
        prompt = f"Hike: {hike_name}"
        response = call_model(
            "You are an AI assistant that returns structured hiking trip data in JSON format. Do not include any explanations—only return a valid JSON object. Include: trailType, typicalWeather, and recommendedGear (list of 3 items).",
            prompt,
            "trip_profile_model_call"
        )
        print("🔍 Raw model response:", response)
        try:
            profile = json.loads(response)
            span.set_attribute("profile.success", True)
            return profile
        except json.JSONDecodeError:
            span.set_attribute("profile.success", False)
            return {}

# Function to match recommended gear with products in the catalog
def match_products(recommended_gear):
    with tracer.start_as_current_span("product_matching") as span:
        matched = []
        for gear_item in recommended_gear:
            for product in mock_product_catalog:
                if any(word in product.lower() for word in gear_item.lower().split()):
                    matched.append(product)
                    break
        span.set_attribute("matched.count", len(matched))
        return matched

# ---- Main Flow ----
if __name__ == "__main__":
    with tracer.start_as_current_span("trail_guide_session") as session_span:
        session_span.set_attribute("session.id", SESSION_ID)
        print("\n--- Trail Guide AI Assistant ---")
        preferences = input("Tell me what kind of hike you're looking for (location, difficulty, scenery):\n> ")

        hike = recommend_hike(preferences)
        print(f"\n✅ Recommended Hike: {hike}")

        profile = generate_trip_profile(hike)
        if not profile:
            print("Failed to generate trip profile. Please check Application Insights for trace.")
            exit(1)

        print(f"\n📋 Trip Profile for {hike}:")
        print(json.dumps(profile, indent=2))

        matched = match_products(profile.get("recommendedGear", []))
        print("\n🛒 Recommended Products from Lakeshore Retail:")
        print("\n".join(matched))

        print(f"\n🔍 Trace ID available in Application Insights for session: {SESSION_ID}")
