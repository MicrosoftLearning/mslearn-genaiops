import os
import json
import wikipedia
from dotenv import load_dotenv
from promptflow.client import load_flow
from typing import List, Dict, Any, Optional
from azure.ai.evaluation.simulator import Simulator
from azure.ai.evaluation import GroundednessEvaluator, evaluate

# Load environment variables from a .env file
load_dotenv()

# Prepare the text to send to the simulator
wiki_search_term = "Isaac Asimov"
wiki_title = wikipedia.search(wiki_search_term)[0]
wiki_page = wikipedia.page(wiki_title)
text = wiki_page.summary[:5000]

# Define callback function
async def callback(
    messages: List[Dict],
    stream: bool = False,
    session_state: Any = None,  # noqa: ANN401
    context: Optional[Dict[str, Any]] = None,
) -> dict:
    messages_list = messages["messages"]
    # Get the last message
    latest_message = messages_list[-1]
    query = latest_message["content"]
    context = latest_message.get("context", None) # looks for context, default None
    # Call your endpoint or AI application here
    current_dir = os.getcwd()
    prompty_path = os.path.join(current_dir, "application.prompty")
    _flow = load_flow(source=prompty_path)
    response = _flow(query=query, context=context, conversation_history=messages_list)
    # Format the response to follow the OpenAI chat protocol
    formatted_response = {
        "content": response,
        "role": "assistant",
        "context": context,
    }
    messages["messages"].append(formatted_response)
    return {
        "messages": messages["messages"],
        "stream": stream,
        "session_state": session_state,
        "context": context
    }

model_config = {
    "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
    "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
    "azure_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
}

simulator = Simulator(model_config=model_config)

outputs = await simulator(
    target=callback,
    text=text,
    num_queries=1,  # Minimal number of queries
)

output_file = "simulation_output.jsonl"
with open(output_file, "w") as file:
    for output in outputs:
        file.write(output.to_eval_qr_json_lines())

groundedness_evaluator = GroundednessEvaluator(model_config=model_config)
eval_output = evaluate(
    data=output_file,
    evaluators={
        "groundedness": groundedness_evaluator
    },
    output_path="groundedness_eval_output.json"
)
