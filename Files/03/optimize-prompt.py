import json
import prompty
import prompty.azure
from prompty.tracer import trace, Tracer, console_tracer, PromptyTracer
from dotenv import load_dotenv

load_dotenv()

# add console and json tracer:
Tracer.add("console", console_tracer)
json_tracer = PromptyTracer()
Tracer.add("PromptyTracer", json_tracer.tracer)

@trace
def run(    
      question: any
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
   json_input = '''{
  "question": "What are some recommended supplies for a camping trip in the mountains?"
}'''
   args = json.loads(json_input)

   result = run(**args)
   print(result)
