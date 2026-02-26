"""
Run all test prompts against the deployed agent and store responses.

This script:
1. Loads test prompts from test-prompts/ directory
2. Retrieves the most recent agent version by name
3. Calls the agent for each prompt
4. Captures responses with metadata
5. Saves results to experiments/{experiment-name}/agent-responses.json
"""
import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables from repository root
repo_root = Path(__file__).parent.parent.parent
env_file = repo_root / '.env'
load_dotenv(env_file)

def load_test_prompts(test_prompts_dir):
    """Load all test prompt files from the test-prompts directory."""
    prompts = {}
    for prompt_file in Path(test_prompts_dir).glob("*.txt"):
        test_name = prompt_file.stem
        with open(prompt_file, 'r') as f:
            prompts[test_name] = f.read().strip()
    return prompts

def run_batch_tests(experiment_name):
    """
    Run all test prompts against the deployed agent and capture responses.
    
    Args:
        experiment_name: Name of the experiment (e.g., 'optimized-concise')
    """
    # Load test prompts
    test_prompts_dir = Path(__file__).parent / 'test-prompts'
    test_prompts = load_test_prompts(test_prompts_dir)
    
    if not test_prompts:
        print(f"No test prompts found in {test_prompts_dir}")
        return
    
    print(f"Running {len(test_prompts)} test prompts for experiment: {experiment_name}")
    print("=" * 80)
    
    # Create project client
    client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    openai_client = client.get_openai_client()
    
    # Get the agent by name (assumes trail_guide_agent.py already created it)
    agent_name = os.environ.get("AGENT_NAME", "trail-guide")
    
    # List agents and find the one with our name
    agents = client.agents.list()
    agent = None
    for a in agents:
        if a.name == agent_name:
            agent = a
            break
    
    if not agent:
        print(f"Error: No agent found with name '{agent_name}'")
        print("Please run 'python src/agents/trail_guide_agent/trail_guide_agent.py' first to create the agent.")
        return
    
    print(f"Using agent: {agent.name} (id: {agent.id}, version: {agent.versions})")
    
    # Capture all results
    results = {
        "experiment": experiment_name,
        "timestamp": datetime.now().isoformat(),
        "agent_id": agent.id,
        "agent_name": agent.name,
        "agent_version": agent.versions.as_dict() if hasattr(agent.versions, "as_dict") else str(agent.versions),
        "agent_object": getattr(agent, "object", None),
        "test_results": []
    }
    
    # Run each test prompt
    for test_name, prompt_text in test_prompts.items():
        print(f"\nTesting: {test_name}")
        print(f"   Prompt: {prompt_text[:60]}...")

        # Create a fresh conversation for this test
        conversation = openai_client.conversations.create()

        # Send user message into the conversation
        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[{
                "type": "message",
                "role": "user",
                "content": prompt_text,
            }],
        )

        # Ask the agent to respond using the Responses API with agent_reference
        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
            input="",
        )

        # Extract text from the response; fall back to str(response) if shape changes
        try:
            response_text = response.output[0].content[0].text
        except Exception:
            response_text = str(response)

        usage = getattr(response, "usage", None)
        token_usage = {
            "prompt_tokens": getattr(usage, "input_tokens", None) if usage else None,
            "completion_tokens": getattr(usage, "output_tokens", None) if usage else None,
            "total_tokens": getattr(usage, "total_tokens", None) if usage else None,
        }

        # Store result
        results["test_results"].append({
            "test_name": test_name,
            "prompt": prompt_text,
            "response": response_text,
            "token_usage": token_usage,
            "run_id": getattr(response, "id", None),
        })

        print(f"   Response captured ({token_usage['total_tokens']} tokens)")
    
    # Save results to experiment folder (at repository root)
    repo_root = Path(__file__).parent.parent.parent
    experiment_dir = repo_root / 'experiments' / experiment_name
    experiment_dir.mkdir(parents=True, exist_ok=True)
    
    results_file = experiment_dir / 'agent-responses.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 80)
    print(f"Results saved to: {results_file}")
    print(f"Total tests: {len(test_prompts)}")
    print(f"Total tokens used: {sum(r['token_usage']['total_tokens'] for r in results['test_results'] if r['token_usage']['total_tokens'])}")
    
    return results_file

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python run-batch-tests.py <experiment-name>")
        print("\nExample:")
        print("  python run-batch-tests.py optimized-concise")
        print("\nNote: Make sure to run 'python src/agents/trail_guide_agent/trail_guide_agent.py' first")
        sys.exit(1)
    
    experiment_name = sys.argv[1]
    run_batch_tests(experiment_name)
