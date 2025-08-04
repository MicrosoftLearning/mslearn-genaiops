import os
import base64
import openai
from dotenv import load_dotenv
from mimetypes import guess_type
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Function to encode a local image into a data URL
def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

load_dotenv()
project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment =  os.getenv("MODEL_DEPLOYMENT1")
image_path = './imgs/demo.png'

# Convert the local image to a data URL using the local_image_to_data_url function
data_url = local_image_to_data_url(image_path)

# Initialize the project
project_client = AIProjectClient(            
    credential=DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True
    ),
    endpoint=project_endpoint,
)

# Set up the chat completion client
chat_client = project_client.get_openai_client(api_version="2024-10-21")

# Define the message to send to the model
messages=[
    { 
        "role": "user", 
        "content": [  
            { 
                "type": "text", 
                "text": "Create Python code for image, and use plt to save the new picture under imgs/ and name it gpt-4o.jpg." 
            },
            { 
                "type": "image_url",
                "image_url": {
                    "url": data_url
}}]}]

# Generate a chat completion request
response = chat_client.chat.completions.create(
  model=model_deployment,
  messages=messages,
  max_tokens=2000
)

print("\nAI's response:")
print(response.choices[0].message.content)

# Add the response to the messages as an Assistant Role
messages.append({"role": "assistant", "content": response.choices[0].message.content})

# Define the new prompt that will develop the chat completion further
new_prompt = "Add a legend to the plot replacing the labels"

# Add the user's question to the messages as a User Role
messages.append({"role": "user", "content": new_prompt})

# Submit the new chat completion requests
response = chat_client.chat.completions.create(
    model=model_deployment,
    messages=messages,
    max_tokens=2000 
)

result = response.choices[0].message.content

# Optional - uncomment the lines below if you want to see the response to the new prompt
#print("\nAI's response:")
#print(response.choices[0].message.content)
