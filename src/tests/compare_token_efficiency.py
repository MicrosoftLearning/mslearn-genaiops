"""Compare token efficiency between baseline and optimized prompts using Foundry SDK."""
import os
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment
load_dotenv(Path(__file__).parent.parent.parent / '.env')

# Load prompts
baseline = Path("../src/agents/prompt_optimization/comparison_experiments/baseline_prompt.txt").read_text().strip()
optimized = Path("../src/agents/prompt_optimization/comparison_experiments/optimized_prompt.txt").read_text().strip()

# Create project client
client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Test question to measure token usage
test_question = "What essential gear do I need for a summer day hike?"

print("=" * 80)
print("TOKEN EFFICIENCY COMPARISON")
print("=" * 80)

results = {}

for prompt_name, instructions in [("baseline", baseline), ("optimized", optimized)]:
    # Create agent with this prompt
    agent = client.agents.create_agent(
        model=os.getenv("MODEL_NAME", "gpt-4.1"),
        name=f"token-test-{prompt_name}",
        instructions=instructions,
    )
    
    # Create thread and message
    thread = client.agents.create_thread()
    message = client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content=test_question,
    )
    
    # Run agent and get token usage
    run = client.agents.create_and_process_run(
        thread_id=thread.id,
        assistant_id=agent.id,
    )
    
    # Get token usage from run
    prompt_tokens = run.usage.prompt_tokens
    completion_tokens = run.usage.completion_tokens
    total_tokens = run.usage.total_tokens
    
    results[prompt_name] = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "characters": len(instructions)
    }
    
    # Cleanup
    client.agents.delete_agent(agent.id)

# Display comparison
print(f"\nBaseline prompt:")
print(f"  Prompt tokens: {results['baseline']['prompt_tokens']}")
print(f"  Completion tokens: {results['baseline']['completion_tokens']}")
print(f"  Total tokens: {results['baseline']['total_tokens']}")
print(f"  Characters: {results['baseline']['characters']}")

print(f"\nOptimized prompt:")
print(f"  Prompt tokens: {results['optimized']['prompt_tokens']}")
print(f"  Completion tokens: {results['optimized']['completion_tokens']}")
print(f"  Total tokens: {results['optimized']['total_tokens']}")
print(f"  Characters: {results['optimized']['characters']}")

# Calculate reduction
prompt_reduction = results['baseline']['prompt_tokens'] - results['optimized']['prompt_tokens']
prompt_reduction_pct = (prompt_reduction / results['baseline']['prompt_tokens']) * 100

print(f"\nReduction:")
print(f"  {prompt_reduction} prompt tokens ({prompt_reduction_pct:.1f}% reduction)")

# Cost impact (example pricing)
cost_per_1m_prompt = 5  # Example: $5 per 1M tokens
baseline_cost = (results['baseline']['prompt_tokens'] / 1_000_000) * cost_per_1m_prompt
optimized_cost = (results['optimized']['prompt_tokens'] / 1_000_000) * cost_per_1m_prompt

print(f"\nCost impact (per 1M tokens at ${cost_per_1m_prompt}/1M):")
print(f"  Baseline: ${baseline_cost:.6f} per call")
print(f"  Optimized: ${optimized_cost:.6f} per call")
print(f"  Savings: ${(baseline_cost - optimized_cost):.6f} per call")
print("=" * 80)
