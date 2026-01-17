import json
import prompty
import prompty.azure
from typing import Any
from prompty.tracer import trace, Tracer, console_tracer, PromptyTracer
from dotenv import load_dotenv

load_dotenv()

# add json tracer:
json_tracer = PromptyTracer()
Tracer.add("PromptyTracer", json_tracer.tracer)

@trace

def run(    
      question: Any
) -> str:

  # execute the prompty file
  result = prompty.execute(
    "start.prompty", 
    inputs={
      "question": question
    }
  )

  return result

if __name__ == "__main__":
    while True:
        user_question = input("Enter your question (or type 'quit' to exit): ")
        if user_question.strip().lower() == "quit":
            print("Exiting.")
            break
        result = run(question=user_question)
        print(result)
