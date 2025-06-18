import os
import json
import asyncio
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


# Run the simulator


# Evaluate the model

