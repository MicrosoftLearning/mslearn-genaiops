---
lab:
    title: 'Design and optimize prompts'
    description: 'Compare prompt variations, models, and configurations to understand their impact on token usage, quality, and agent behavior.'
---

# Design and optimize prompts

This exercise takes approximately **40 minutes**.

> **Note**: This lab assumes a pre-configured lab environment with Visual Studio Code, Azure CLI, and Python already installed.

## Introduction

In this exercise, you'll systematically compare different prompt engineering approaches to understand their impact on performance, cost, and quality. You'll run controlled experiments comparing prompt variations, model choices, and agent configurations using Python scripts.

You'll compare baseline vs optimized prompts for token efficiency, test the same prompt across different models (GPT-4 vs GPT-4o-mini), evaluate prompts with and without tool integration, and explore how reasoning patterns affect agent behavior. Each comparison will help you make data-driven decisions about prompt design.

## Set up the environment

To complete the tasks in this exercise, you need:

- Visual Studio Code
- Azure subscription with Microsoft Foundry access
- Git and [GitHub](https://github.com) account
- Python 3.9 or later
- Azure CLI and Azure Developer CLI (azd) installed

All steps in this lab will be performed using Visual Studio Code and its integrated terminal.

### Create repository from template

You'll start by creating your own repository from the template to practice realistic workflows.

1. In a web browser, navigate to the template repository on [GitHub](https://github.com) at `https://github.com/MicrosoftLearning/mslearn-genaiops`.
1. Select **Use this template** > **Create a new repository**.
1. Enter a name for your repository (e.g., `mslearn-genaiops`).
1. Set the repository to **Public** or **Private** based on your preference.
1. Select **Create repository**.

### Clone the repository in Visual Studio Code

After creating your repository, clone it to your local machine.

1. In Visual Studio Code, open the Command Palette by pressing **Ctrl+Shift+P**.
1. Type **Git: Clone** and select it.
1. Enter your repository URL: `https://github.com/[your-username]/mslearn-genaiops.git`
1. Select a location on your local machine to clone the repository.
1. When prompted, select **Open** to open the cloned repository in VS Code.

### Deploy Microsoft Foundry resources

Now you'll use the Azure Developer CLI to deploy all required Azure resources.

> **Note**: This lab uses infrastructure-as-code (IaC) deployment with `azd` because it follows GenAIOps best practices and makes the lab accessible as a standalone exercise. This approach ensures consistent, reproducible environments while teaching real-world deployment patterns.

1. In Visual Studio Code, open a terminal by selecting **Terminal** > **New Terminal** from the menu.

1. Authenticate with Azure Developer CLI:

    ```powershell
    azd auth login
    ```

    This opens a browser window for Azure authentication. Sign in with your Azure credentials.

1. Authenticate with Azure CLI:

    ```powershell
    az login
    ```

    Sign in with your Azure credentials when prompted.

1. Provision resources:

    ```powershell
    azd up
    ```

    When prompted, provide:
    - **Environment name** (e.g., `dev`, `test`) - Used to name all resources
    - **Azure subscription** - Where resources will be created
    - **Location** - Azure region (recommended: Sweden Central)

    The command deploys the infrastructure from the `infra/` folder, creating:
    - **Resource Group** - Container for all resources
    - **Foundry (AI Services)** - The hub with access to models like GPT-4.1
    - **Foundry Project** - Your workspace for creating and managing prompts
    - **Log Analytics Workspace** - Collects logs and telemetry data
    - **Application Insights** - Monitors performance and usage

1. Create a `.env` file with the environment variables:

    ```powershell
    azd env get-values > .env
    ```

    This creates a `.env` file in your project root with all the provisioned resource information.

### Install Python dependencies

With your Azure resources deployed, install the required Python packages.

1. In the VS Code terminal, create and activate a virtual environment:

    ```powershell
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

1. Install the required dependencies:

    ```powershell
    python -m pip install -r requirements.txt
    ```

    This installs necessary dependencies including:
    - `azure-ai-projects` - SDK for working with AI Foundry
    - `azure-identity` - Azure authentication
    - `python-dotenv` - Load environment variables

1. Add the agent configuration to your `.env` file:

    Open the `.env` file in your repository root and add:

    ```
    AGENT_NAME=trail-guide
    MODEL_NAME=gpt-4.1
    ```

## Comparison 1: Optimize prompts for token efficiency

You'll compare the production-ready prompt from your trail guide agent against an optimized version to understand token reduction strategies.

### Set up experiment workflow

Use git branches to isolate prompt changes, following safe deployment practices.

1. In the VS Code terminal, navigate to the prompt optimization directory:

    ```powershell
    cd src\agents\prompt_optimization
    ```

1. Ensure you're on the main branch with latest changes:

    ```powershell
    git checkout main
    git pull origin main
    ```

1. Create an experiment branch for token optimization:

    ```powershell
    git checkout -b experiment/token-optimization
    ```

    > **Note**: Using `experiment/` prefix clearly identifies this as an experimental change. Other common prefixes include `feature/` for new capabilities and `hotfix/` for urgent fixes.

1. Create a subdirectory for comparison experiments:

    ```powershell
    mkdir comparison_experiments
    cd comparison_experiments
    ```

### Create baseline from production prompt

Start with the current production prompt (v3) from your trail guide agent.

1. Copy the production prompt as your baseline:

    ```powershell
    Copy-Item ..\..\trail_guide_agent\prompts\v3_instructions.txt baseline_prompt.txt
    ```

    This file contains the full-featured production prompt with enterprise capabilities, safety frameworks, and comprehensive instructions.

### Create optimized prompt

Now create a token-efficient version that preserves core functionality.

1. Create an optimized prompt file `optimized_prompt.txt`:

    ```powershell
    New-Item optimized_prompt.txt
    ```

1. Open `optimized_prompt.txt` and add this streamlined version:

    ```
    You are an expert trail guide for Adventure Works. Provide practical hiking and camping guidance.

    When recommending:
    - Assess user experience and fitness
    - Consider weather and trail conditions
    - Suggest appropriate gear
    - Emphasize safety protocols
    - Offer backup options

    Keep guidance specific, actionable, and safety-focused.
    ```

    Key optimizations applied:
    - Removed verbose role description
    - Condensed capabilities into action items
    - Simplified framework to essential steps
    - Eliminated redundant safety mentions
    - Focused on core value delivery

1. Commit this optimization with a descriptive message:

    ```powershell
    git add .
    git commit -m "Optimize token usage in trail guide prompt

- Reduced verbose role description
- Condensed capabilities into action items  
- Simplified framework to essential steps
- Measured with Foundry Responses API for accurate token counts"
    git tag experiment-1-token-optimization
    ```

    > **Tip**: Clear commit messages help reviewers understand what changed and why. Document that you used Foundry's API for accurate token measurement.

### Compare token usage

Create a script to measure and compare token counts using the Foundry Responses API.

1. Create a comparison script `compare_token_efficiency.py`:

    ```python
    import os
    from pathlib import Path
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient

    # Load environment
    load_dotenv(Path(__file__).parent.parent.parent.parent / '.env')

    # Load prompts
    baseline = Path("baseline_prompt.txt").read_text().strip()
    optimized = Path("optimized_prompt.txt").read_text().strip()

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
    ```

    > **Note**: This script uses the Foundry Responses API to get actual token usage from real agent runs, providing accurate measurements rather than estimates.

1. Run the comparison:

    ```powershell
    python compare_token_efficiency.py
    ```

    You'll see output showing the actual token counts from the Foundry API, including:
    - Prompt tokens (your system prompt + user message)
    - Completion tokens (the agent's response)
    - Total tokens used
    - Token reduction percentage
    - Cost impact

    The exact numbers will vary based on your actual prompts and the agent's response length.

### Test both prompts with agents

Now test if the optimized prompt maintains quality.

1. Create an agent test script `test_prompts.py`:

    ```python
    import os
    from pathlib import Path
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import PromptAgentDefinition

    # Load environment
    load_dotenv(Path(__file__).parent.parent.parent.parent / '.env')

    # Test questions
    test_questions = [
        "What essential gear do I need for a summer day hike?",
        "How should I prepare for my first overnight camping trip?",
    ]

    # Load prompts
    prompts = {
        "baseline": Path("baseline_prompt.txt").read_text().strip(),
        "optimized": Path("optimized_prompt.txt").read_text().strip(),
    }

    # Create project client
    client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    print("=" * 80)
    print("PROMPT QUALITY COMPARISON")
    print("=" * 80)

    for prompt_name, instructions in prompts.items():
        print(f"\n{'='*80}")
        print(f"Testing: {prompt_name.upper()}")
        print(f"{'='*80}")
        
        # Create agent with this prompt
        agent = client.agents.create_agent(
            model=os.getenv("MODEL_NAME", "gpt-4.1"),
            name=f"test-{prompt_name}",
            instructions=instructions,
        )
        
        # Create thread
        thread = client.agents.create_thread()
        
        # Test each question
        for question in test_questions:
            print(f"\nQ: {question}")
            
            # Send message
            message = client.agents.create_message(
                thread_id=thread.id,
                role="user",
                content=question,
            )
            
            # Run agent
            run = client.agents.create_and_process_run(
                thread_id=thread.id,
                assistant_id=agent.id,
            )
            
            # Get response
            messages = client.agents.list_messages(thread_id=thread.id)
            response = messages.data[0].content[0].text.value
            
            print(f"A: {response}\n")
        
        # Cleanup
        client.agents.delete_agent(agent.id)
        print(f"\n{'='*80}\n")
    ```

1. Run the quality comparison:

    ```powershell
    python test_prompts.py
    ```

    Observe if the optimized prompt produces similar quality responses with fewer tokens.

### Validate the optimization

Before considering this experiment complete, validate the changes meet quality standards.

1. Document your findings in a validation file:

    ```powershell
    New-Item validation_results.md
    ```

1. Open `validation_results.md` and add your test results:

    ```markdown
    # Token Optimization Validation

    ## Experiment: experiment-1-token-optimization

    ### Metrics
    - **Token reduction**: 54.7% (128 → 58 tokens)
    - **Cost savings**: $0.000350 per call
    - **Test cases passed**: 2/2

    ### Quality Assessment
    | Criteria | Baseline | Optimized | Pass/Fail |
    |----------|----------|-----------|-----------|
    | Relevance | ✅ | ✅ | ✅ Pass |
    | Completeness | ✅ | ✅ | ✅ Pass |
    | Safety focus | ✅ | ✅ | ✅ Pass |
    | Actionability | ✅ | ✅ | ✅ Pass |

    ### Recommendation
    **APPROVED** - Token optimization maintains quality while reducing costs by 54%.

    ### Next Steps
    - Open pull request for team review
    - Consider deploying to staging environment
    - Monitor performance metrics before production
    ```

1. Commit the validation results:

    ```powershell
    git add validation_results.md
    git commit -m "Add validation results for token optimization"
    ```

## Comparison 2: Same prompt across different models

Test how model choice affects prompt behavior and requirements using your optimized prompt.

### Create new experiment branch

1. Return to main and create a new experiment branch:

    ```powershell
    git checkout main
    git checkout -b experiment/model-comparison
    ```

1. Copy your optimized prompt to this branch:

    ```powershell
    cd src\agents\prompt_optimization\comparison_experiments
    Copy-Item optimized_prompt.txt model_test_prompt.txt
    ```

### Create model comparison script

1. Create `compare_models.py`:

    ```python
    import os
    from pathlib import Path
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    import tiktoken

    load_dotenv(Path(__file__).parent.parent.parent.parent / '.env')

    # Load optimized prompt
    prompt = Path("model_test_prompt.txt").read_text().strip()

    # Models to compare
    models = ["gpt-4.1", "gpt-4o-mini"]

    # Test question requiring reasoning
    test_question = "I'm planning a 3-day backpacking trip in the mountains in October. What are the most critical safety considerations?"

    client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    print("=" * 80)
    print("MODEL COMPARISON - Same Prompt")
    print("=" * 80)
    print(f"\nPrompt: {prompt}")
    print(f"\nQuestion: {test_question}")
    print("=" * 80)

    for model in models:
        print(f"\n{'='*80}")
        print(f"Model: {model}")
        print(f"{'='*80}")
        
        # Create agent
        agent = client.agents.create_agent(
            model=model,
            name=f"test-{model}",
            instructions=prompt,
        )
        
        # Create thread and message
        thread = client.agents.create_thread()
        message = client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=test_question,
        )
        
        # Run and get response
        run = client.agents.create_and_process_run(
            thread_id=thread.id,
            assistant_id=agent.id,
        )
        
        messages = client.agents.list_messages(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        
        # Count response tokens
        encoding = tiktoken.encoding_for_model(model if model != "gpt-4.1" else "gpt-4o")
        response_tokens = len(encoding.encode(response))
        
        print(f"\nResponse ({response_tokens} tokens):")
        print(response)
        print(f"\n{'='*80}")
        
        # Cleanup
        client.agents.delete_agent(agent.id)
    ```

1. Run the model comparison:

    ```powershell
    python compare_models.py
    ```

    Observe differences in:
    - Response depth and detail
    - Structure and organization
    - Token usage
    - Reasoning quality

1. Tag this experiment:

    ```powershell
    git add .
    git commit -m "Model comparison experiment complete"
    git tag experiment-2-model-comparison
    ```

## Comparison 3: Prompts with and without tools

See how tool integration changes prompt requirements.

### Create tool integration experiment branch

1. Create another experiment branch:

    ```powershell
    git checkout main
    git checkout -b experiment/tool-integration
    cd src\agents\prompt_optimization\comparison_experiments
    ```

### Create prompt without tool instructions

1. Create `prompt_no_tools.txt`:

    ```
    You are an outdoor adventure assistant. When users ask about weather conditions for hiking:
    
    1. Ask them for their location
    2. Remind them to check official weather sources
    3. Provide general seasonal advice for that region
    4. Suggest checking weather 24-48 hours before the trip
    
    Always emphasize safety and being prepared for changing conditions.
    ```

### Create prompt with tool integration

1. Create `prompt_with_tools.txt`:

    ```
    You are an outdoor adventure assistant with access to real-time weather data. 
    
    When users ask about weather, use the get_weather tool to provide accurate forecasts. Focus on interpreting the data for outdoor safety: temperature ranges, precipitation probability, wind conditions, and visibility.
    
    Always emphasize being prepared for changing mountain weather.
    ```

### Compare tool vs no-tool approach

1. Create `compare_tools.py`:

    ```python
    import os
    from pathlib import Path
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from azure.ai.projects.models import FunctionTool
    import tiktoken

    load_dotenv(Path(__file__).parent.parent.parent.parent / '.env')

    # Load prompts
    prompt_no_tool = Path("prompt_no_tools.txt").read_text().strip()
    prompt_with_tool = Path("prompt_with_tools.txt").read_text().strip()

    # Define a mock weather tool
    weather_tool = FunctionTool(
        name="get_weather",
        description="Get current weather forecast for a location",
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and state, e.g. Seattle, WA"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to forecast (1-7)"
                }
            },
            "required": ["location"]
        }
    )

    test_question = "What's the weather forecast for hiking in Seattle this weekend?"

    client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    print("=" * 80)
    print("TOOL INTEGRATION COMPARISON")
    print("=" * 80)
    print(f"\nQuestion: {test_question}\n")

    # Count prompt tokens
    encoding = tiktoken.encoding_for_model("gpt-4o")
    
    print(f"Prompt WITHOUT tool instructions:")
    print(f"  Tokens: {len(encoding.encode(prompt_no_tool))}")
    print(f"  Approach: Manual instructions on how to handle weather questions\n")
    
    print(f"Prompt WITH tool integration:")
    print(f"  Tokens: {len(encoding.encode(prompt_with_tool))}")
    print(f"  Approach: Delegated to tool, focus on interpretation\n")
    
    print("=" * 80)
    print("\nKey Insight:")
    print("  - Without tools: Prompt must explain the entire workflow")
    print("  - With tools: Prompt focuses on interpretation, tool handles execution")
    print("  - Tool-aware prompts are often shorter and more focused")
    print("=" * 80)
    ```

1. Run the comparison:

    ```powershell
    python compare_tools.py
    ```

1. Tag this experiment:

    ```powershell
    git add .
    git commit -m "Tool integration comparison complete"
    git tag experiment-3-tool-integration
    ```

## Comparison 4: Direct vs Chain-of-Thought reasoning

Compare how reasoning patterns affect response quality.

### Create reasoning experiment branch

1. Create a reasoning experiment branch:

    ```powershell
    git checkout main
    git checkout -b experiment/reasoning-patterns
    cd src\agents\prompt_optimization\comparison_experiments
    ```

### Create direct instruction prompt

1. Create `prompt_direct.txt`:

    ```
    You are an outdoor adventure assistant. Recommend appropriate hiking trails based on user skill level and preferences. Provide trail name, difficulty, distance, and key features.
    ```

### Create Chain-of-Thought prompt

1. Create `prompt_cot.txt`:

    ```
    You are an outdoor adventure assistant. When recommending trails:
    
    1. First, assess the user's experience level and physical fitness
    2. Consider their stated preferences (scenery, distance, elevation)
    3. Think about seasonal conditions and current trail status
    4. Match these factors to suitable trails
    5. Provide your recommendation with reasoning
    
    Show your thinking process before giving the final recommendation.
    ```

### Compare reasoning approaches

1. Create `compare_reasoning.py`:

    ```python
    import os
    from pathlib import Path
    from dotenv import load_dotenv
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    import tiktoken

    load_dotenv(Path(__file__).parent.parent.parent.parent / '.env')

    prompts = {
        "direct": Path("prompt_direct.txt").read_text().strip(),
        "chain_of_thought": Path("prompt_cot.txt").read_text().strip(),
    }

    test_question = "I'm a beginner hiker and want a scenic trail under 5 miles near Seattle. I'm afraid of heights."

    client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )

    print("=" * 80)
    print("REASONING PATTERN COMPARISON")
    print("=" * 80)
    print(f"\nQuestion: {test_question}\n")

    for prompt_type, instructions in prompts.items():
        print(f"{'='*80}")
        print(f"{prompt_type.upper().replace('_', '-')} REASONING")
        print(f"{'='*80}\n")
        
        agent = client.agents.create_agent(
            model=os.getenv("MODEL_NAME", "gpt-4.1"),
            name=f"test-{prompt_type}",
            instructions=instructions,
        )
        
        thread = client.agents.create_thread()
        message = client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=test_question,
        )
        
        run = client.agents.create_and_process_run(
            thread_id=thread.id,
            assistant_id=agent.id,
        )
        
        messages = client.agents.list_messages(thread_id=thread.id)
        response = messages.data[0].content[0].text.value
        
        # Count tokens
        encoding = tiktoken.encoding_for_model("gpt-4o")
        response_tokens = len(encoding.encode(response))
        
        print(f"Response ({response_tokens} tokens):\n{response}\n")
        print(f"{'='*80}\n")
        
        client.agents.delete_agent(agent.id)

    print("Observation:")
    print("  - Direct: Faster, concise, may miss context")
    print("  - Chain-of-Thought: More thorough, shows reasoning, longer")
    print("  - Choose based on task complexity and transparency needs")
    print("=" * 80)
    ```

1. Run the reasoning comparison:

    ```powershell
    python compare_reasoning.py
    ```

1. Tag this experiment:

    ```powershell
    git add .
    git commit -m "Reasoning pattern comparison complete"
    git tag experiment-4-reasoning-patterns
    ```

## Review experiment history

View all your experiments using git history.

1. Return to the main branch:

    ```powershell
    git checkout main
    ```

1. View all experiment tags:

    ```powershell
    git tag -l "experiment-*"
    ```

    You should see:
    ```
    experiment-1-token-optimization
    experiment-2-model-comparison
    experiment-3-tool-integration
    experiment-4-reasoning-patterns
    ```

1. View all experiment branches:

    ```powershell
    git branch -a | Select-String "experiment/"
    ```

    This shows your organized experiment workflow, making it easy to revisit any comparison.

## Exercise: Design your own comparison

Apply what you've learned to create a custom comparison experiment.

### Your challenge

1. Create a new experiment branch:

    ```powershell
    git checkout main
    git checkout -b experiment/custom-comparison
    ```

1. Choose one comparison type:
   - **Constraint comparison**: Structured (JSON) vs unstructured output
   - **Context length**: Minimal vs detailed context
   - **Role definition**: Generic vs specialized persona
   - **Temperature**: Same prompt at different temperatures (0.3 vs 0.9)

1. Create two prompt variations in `.txt` files

1. Write a Python script to compare them

1. Run the experiment and document findings

1. Commit and tag your experiment:

    ```powershell
    git add .
    git commit -m "Custom comparison experiment: [your-topic]"
    git tag experiment-5-custom
    ```

## Compare all experiments

Create a summary comparing all the experiments you've run.

1. Create `summary_comparison.py`:

    ```python
    import tiktoken
    from pathlib import Path

    encoding = tiktoken.encoding_for_model("gpt-4o")

    prompts = {
        "Baseline (verbose)": "baseline_prompt.txt",
        "Optimized (concise)": "optimized_prompt.txt",
        "No tools": "prompt_no_tools.txt",
        "With tools": "prompt_with_tools.txt",
        "Direct reasoning": "prompt_direct.txt",
        "Chain-of-thought": "prompt_cot.txt",
    }

    print("=" * 80)
    print("COMPREHENSIVE PROMPT COMPARISON SUMMARY")
    print("=" * 80)
    print(f"\n{'Prompt Type':<25} {'Tokens':>10} {'Characters':>12} {'Purpose':<30}")
    print("-" * 80)

    for name, filename in prompts.items():
        if Path(filename).exists():
            content = Path(filename).read_text().strip()
            tokens = len(encoding.encode(content))
            chars = len(content)
            
            purpose = {
                "Baseline (verbose)": "Learning baseline",
                "Optimized (concise)": "Token efficiency",
                "No tools": "Manual workflow",
                "With tools": "Tool delegation",
                "Direct reasoning": "Quick responses",
                "Chain-of-thought": "Complex reasoning",
            }[name]
            
            print(f"{name:<25} {tokens:>10} {chars:>12}  {purpose:<30}")

    print("-" * 80)
    print("\nKey Learnings:")
    print("1. Token optimization can reduce costs by 50-70% without quality loss")
    print("2. Model choice affects response depth and structure")
    print("3. Tools reduce prompt complexity by delegating execution")
    print("4. Reasoning patterns trade off speed vs transparency")
    print("5. Each optimization has trade-offs - choose based on requirements")
    print("=" * 80)
    ```

1. Run the summary:

    ```powershell
    python summary_comparison.py
    ```

## Clean up and merge experiments

Follow the safe deployment workflow to integrate approved experiments.

### Prepare for production

Review which experiments should move to production.

1. Navigate to repository root:

    ```powershell
    cd ..\..\..\..
    ```

1. Review all experiment branches:

    ```powershell
    git branch
    ```

    You should see branches like:
    - `experiment/token-optimization`
    - `experiment/model-comparison`
    - `experiment/tool-integration`
    - `experiment/reasoning-patterns`

### Merge approved experiments

Use the pull request workflow to merge validated changes.

1. For the approved token optimization, merge to main:

    ```powershell
    git checkout main
    git merge experiment/token-optimization -m "Merge token optimization experiment

Approved optimization reduces prompt tokens by 54% while maintaining quality.

- Validated with production test cases
- All quality criteria met
- Cost savings: $0.000350 per call
- Ready for production deployment"
    ```

1. Create a production release tag:

    ```powershell
    git tag -a v1.4.0 -m "Release v1.4.0: Token-optimized prompts

Changes:
- Optimized trail guide prompt (54% token reduction)
- Validated quality maintenance
- Updated test suite

Migration: Replace baseline_prompt.txt with optimized_prompt.txt"
    ```

### Push to GitHub

Share your experiments and approved changes with your team.

1. Push all experiment branches for team visibility:

    ```powershell
    git push origin experiment/token-optimization
    git push origin experiment/model-comparison
    git push origin experiment/tool-integration
    git push origin experiment/reasoning-patterns
    ```

1. Push main branch with merged changes:

    ```powershell
    git push origin main
    ```

1. Push all tags:

    ```powershell
    git push --tags
    ```

    Your experiments are now saved with full history on [GitHub](https://github.com), making them easy to review, discuss, and deploy.

### Monitor and rollback (if needed)

After deploying to production, monitor performance and be ready to rollback if issues arise.

1. If you need to rollback to a previous version:

    ```powershell
    git checkout v1.3.0  # Previous stable version
    git checkout -b hotfix/rollback-token-optimization
    ```

1. After fixing issues, create a new release:

    ```powershell
    git tag -a v1.4.1 -m "Hotfix: Refined token optimization"
    git push origin main --tags
    ```

## Prompt lifecycle stages

Your experiments followed this workflow:

| Stage | Activities in This Lab | Validation |
|-------|------------------------|------------|
| **Development** | Created experiment branches, drafted optimized prompts | Token counts, initial testing |
| **Validation** | Ran quality tests, compared with baseline | Test results documented |
| **Review** | Documented findings, prepared merge | Validation results committed |
| **Production** | Merged to main, tagged release | Ready for deployment |
| **Monitoring** | (Post-lab) Track performance metrics | Rollback plan established |

> **Important**: Each stage builds on the previous one. Don't skip stages—each provides critical validation that prevents production issues.

## Summary

In this exercise, you:

- ✅ Used the production v3 prompt as a baseline for optimization
- ✅ Created experiment branches following safe deployment practices
- ✅ Optimized prompts for token efficiency (54% reduction from production)
- ✅ Validated changes with comprehensive testing
- ✅ Tested the same prompt across different models (GPT-4 vs GPT-4o-mini)
- ✅ Evaluated prompts with and without tool integration
- ✅ Explored direct vs chain-of-thought reasoning patterns
- ✅ Documented validation results for team review
- ✅ Merged approved experiments using proper git workflow
- ✅ Tagged releases and established rollback procedures

## Key takeaways

1. **Experimentation requires structure** - Git branches and tags organize prompt iterations
2. **Validate before merging** - Test and document results before production
3. **Token optimization is cost optimization** - Reducing tokens from production baseline saves money
4. **Model choice matters** - Different models respond differently to the same prompt
5. **Tools simplify prompts** - Delegation reduces prompt complexity
6. **Use descriptive commits** - Clear messages help reviewers understand changes
7. **Version everything** - Track prompt experiments like code changes
8. **Plan for rollback** - Always have a way to revert problematic changes

## Next steps

- Apply safe deployment workflow to your own prompt changes
- Explore [Optimize RAG solutions for GenAI](04-optimize-rag.md) to enhance context-aware AI
- Review [Microsoft Learn: Safe prompt deployment](https://learn.microsoft.com/training/) for advanced workflows
- Learn about automated testing and CI/CD for prompts

You'll start by examining a basic prompt and understanding its characteristics.

### Review the starter prompt

Navigate to the prompt optimization directory and examine the baseline prompt.

1. In the VS Code terminal, navigate to the prompt optimization directory:

    ```powershell
    cd src\agents\prompt_optimization
    ```

1. Open the `start.prompty` file in VS Code and examine its structure:

    ```yaml
    ---
    name: Optimization Prompty
    description: A template for prompt optimization
    model:
      api: chat
      configuration:
        type: azure_openai
      parameters:
        max_tokens: 2000
    sample:
      question: What are some recommended supplies for a camping trip in the mountains?
    ---

    system:
    You are a helpful assistant. Your job is to answer questions and provide information to users in a concise and accurate manner.

    example:
    user: What's the weather like today?
    assistant: The weather today is sunny with a high of 25°C.

    user:
    {{question}}
    ```

    This `.prompty` file defines:
    - **Metadata** - Name, description, and model configuration
    - **System prompt** - Instructions that define the assistant's behavior
    - **Example** - A demonstration of expected input/output
    - **User input** - The variable `{{question}}` for testing

### Count tokens in the baseline prompt

Understanding token usage is crucial for optimization. Let's measure the baseline.

1. Open the `token-count.py` script:

    ```python
    import tiktoken

    # Choose the model you're targeting
    model = "gpt-4o"

    # Load the appropriate tokenizer
    encoding = tiktoken.encoding_for_model(model)

    # Your prompt
    original_prompt = "You are a helpful assistant. Your job is to answer questions and provide information to users in a concise and accurate manner."
    
    # Encode the prompt and count tokens
    original_tokens = encoding.encode(original_prompt)
    
    print(f"Original prompt tokens: {len(original_tokens)}")
    ```

1. Run the token counting script:

    ```powershell
    python token-count.py
    ```

    You should see output like:

    ```
    Original prompt tokens: 23
    ```

    This baseline measurement will help you track improvements.

### Test the baseline prompt in Microsoft Foundry

Before optimizing, test the baseline prompt to understand its behavior.

1. In a web browser, open the [Microsoft Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in.

1. Navigate to your **Project** from the home page.

1. In the left navigation, select **Playgrounds** > **Chat**.

1. In the **System message** field, paste the system prompt from `start.prompty`:

    ```
    You are a helpful assistant. Your job is to answer questions and provide information to users in a concise and accurate manner.
    ```

1. In the **Chat session**, test with these questions:
   - "What are some recommended supplies for a camping trip in the mountains?"
   - "How do I prepare for a day hike?"
   - "What should I pack for winter camping?"

1. Observe the responses. Note:
   - **Length** - Are responses appropriately detailed?
   - **Clarity** - Are answers easy to understand?
   - **Relevance** - Does it stay on topic?
   - **Tone** - Is the style appropriate?

## Apply prompt optimization techniques

You'll now apply systematic optimization strategies to improve the prompt.

### Optimization Strategy 1: Reduce verbosity

Removing unnecessary words reduces token usage without sacrificing meaning.

1. Create an optimized version of the system prompt. Update your local copy of the prompt to:

    ```
    You are a helpful assistant. Answer questions concisely and accurately.
    ```

    Changes made:
    - Removed "Your job is to" (unnecessary preamble)
    - Reduced "in a concise and accurate manner" to "concisely and accurately"
    - Direct instruction instead of job description

1. Update `token-count.py` to compare both versions:

    ```python
    import tiktoken

    model = "gpt-4o"
    encoding = tiktoken.encoding_for_model(model)

    original_prompt = "You are a helpful assistant. Your job is to answer questions and provide information to users in a concise and accurate manner."
    optimized_prompt = "You are a helpful assistant. Answer questions concisely and accurately."

    original_tokens = encoding.encode(original_prompt)
    optimized_tokens = encoding.encode(optimized_prompt)

    print(f"Original prompt tokens: {len(original_tokens)}")
    print(f"Optimized prompt tokens: {len(optimized_tokens)}")
    print(f"Token reduction: {len(original_tokens) - len(optimized_tokens)} ({((len(original_tokens) - len(optimized_tokens)) / len(original_tokens)) * 100:.1f}%)")
    ```

1. Run the updated token counter:

    ```powershell
    python token-count.py
    ```

    Expected output:

    ```
    Original prompt tokens: 23
    Optimized prompt tokens: 11
    Token reduction: 12 (52.2%)
    ```

1. Test the optimized prompt in the Microsoft Foundry portal:

    - Replace the system message with the optimized version
    - Test with the same questions as before
    - Compare the quality of responses

### Optimization Strategy 2: Add domain context

For specialized use cases, adding relevant context improves response quality.

1. Create a domain-specific optimized prompt for outdoor activities:

    ```
    You are an outdoor adventure assistant specializing in hiking and camping. Provide practical, safety-focused advice on gear, trails, and preparation. Keep responses clear and actionable.
    ```

    Changes made:
    - Specified domain expertise (outdoor adventure)
    - Defined focus areas (gear, trails, preparation)
    - Added quality criteria (practical, safety-focused, clear, actionable)

1. Create a new file `solution-0.prompty` in the `prompt_optimization` folder:

    ```yaml
    ---
    name: Outdoor Adventure Assistant - Optimized
    description: Domain-specific prompt with clarity and safety focus
    model:
      api: chat
      configuration:
        type: azure_openai
      parameters:
        max_tokens: 2000
    sample:
      question: What are some recommended supplies for a camping trip in the mountains?
    ---

    system:
    You are an outdoor adventure assistant specializing in hiking and camping. Provide practical, safety-focused advice on gear, trails, and preparation. Keep responses clear and actionable.

    user:
    {{question}}
    ```

1. Test this version in the Microsoft Foundry portal and compare responses with the previous versions.

### Optimization Strategy 3: Use structured output

Structured responses improve consistency and readability.

1. Create an enhanced prompt with output formatting guidance:

    ```
    You are an outdoor adventure assistant specializing in hiking and camping.

    For gear recommendations:
    - List items by category (essentials, safety, comfort)
    - Include brief rationale for each item
    - Highlight seasonal considerations

    For trail advice:
    - Start with difficulty level
    - Note distance and elevation
    - Mention key safety considerations

    Keep all responses practical, safety-focused, and easy to scan.
    ```

1. Create `solution-1.prompty`:

    ```yaml
    ---
    name: Outdoor Adventure Assistant - Structured
    description: Optimized prompt with output structure guidance
    model:
      api: chat
      configuration:
        type: azure_openai
      parameters:
        max_tokens: 2000
    sample:
      question: What are some recommended supplies for a camping trip in the mountains?
    ---

    system:
    You are an outdoor adventure assistant specializing in hiking and camping.

    For gear recommendations:
    - List items by category (essentials, safety, comfort)
    - Include brief rationale for each item
    - Highlight seasonal considerations

    For trail advice:
    - Start with difficulty level
    - Note distance and elevation
    - Mention key safety considerations

    Keep all responses practical, safety-focused, and easy to scan.

    user:
    {{question}}
    ```

1. Test in the Microsoft Foundry portal with questions like:
   - "What gear do I need for winter camping?"
   - "Recommend a beginner trail near Seattle"

## Compare and validate optimizations

Now you'll systematically compare all prompt versions and validate improvements.

### Create a comparison matrix

Document your findings across all prompt versions.

1. In the VS Code terminal, create a simple test to compare prompts:

    Create a new file `compare-prompts.py`:

    ```python
    prompts = {
        "baseline": "You are a helpful assistant. Your job is to answer questions and provide information to users in a concise and accurate manner.",
        "optimized_concise": "You are a helpful assistant. Answer questions concisely and accurately.",
        "domain_specific": "You are an outdoor adventure assistant specializing in hiking and camping. Provide practical, safety-focused advice on gear, trails, and preparation. Keep responses clear and actionable.",
        "structured": """You are an outdoor adventure assistant specializing in hiking and camping.

    For gear recommendations:
    - List items by category (essentials, safety, comfort)
    - Include brief rationale for each item
    - Highlight seasonal considerations

    For trail advice:
    - Start with difficulty level
    - Note distance and elevation
    - Mention key safety considerations

    Keep all responses practical, safety-focused, and easy to scan."""
    }

    import tiktoken
    encoding = tiktoken.encoding_for_model("gpt-4o")

    print("Prompt Comparison:")
    print("-" * 80)
    for name, prompt in prompts.items():
        tokens = len(encoding.encode(prompt))
        print(f"{name:20} | {tokens:3} tokens | {len(prompt):4} chars")
    print("-" * 80)
    ```

1. Run the comparison:

    ```powershell
    python compare-prompts.py
    ```

    Expected output:

    ```
    Prompt Comparison:
    --------------------------------------------------------------------------------
    baseline             |  23 tokens |  134 chars
    optimized_concise    |  11 tokens |   70 chars
    domain_specific      |  35 tokens |  185 chars
    structured           | 100 tokens |  515 chars
    --------------------------------------------------------------------------------
    ```

### Conduct quality assessment

Evaluate each prompt version against key criteria.

1. In the Microsoft Foundry portal, test each prompt version with the same question set:

    Test questions:
    - "What gear do I need for a day hike in summer?"
    - "How do I prepare for my first overnight camping trip?"
    - "What are the most important safety items for mountain hiking?"

1. Create a quality assessment matrix in a new file `assessment.md`:

    ```markdown
    # Prompt Quality Assessment

    ## Test Question: "What gear do I need for a day hike in summer?"

    | Criteria | Baseline | Optimized Concise | Domain Specific | Structured |
    |----------|----------|-------------------|-----------------|------------|
    | Relevance | ✅ | ✅ | ✅ | ✅ |
    | Completeness | ⚠️ | ⚠️ | ✅ | ✅✅ |
    | Clarity | ✅ | ✅ | ✅ | ✅✅ |
    | Safety Focus | ❌ | ❌ | ✅ | ✅✅ |
    | Actionability | ⚠️ | ⚠️ | ✅ | ✅✅ |
    | Token Efficiency | ⚠️ | ✅✅ | ✅ | ⚠️ |

    ## Recommendation

    - **For general use**: Optimized Concise (best token efficiency)
    - **For outdoor domain**: Domain Specific (good balance)
    - **For consistent format**: Structured (best quality, higher tokens)

    ## Key Learnings

    1. Removing verbosity reduces tokens without sacrificing quality
    2. Domain context significantly improves relevance and safety
    3. Structured output guidance improves consistency
    4. Trade-off exists between token usage and output structure
    ```

1. Save this file in the `src/agents/prompt_optimization` folder.

## Exercise: Create your own optimization

Apply what you've learned to optimize a prompt for a different scenario.

### Your challenge

1. Choose a different domain (e.g., fitness coaching, recipe assistant, study tutor)

1. Create a baseline prompt for that domain

1. Apply at least two optimization strategies:
   - Reduce verbosity
   - Add domain context
   - Structure output format
   - Add examples
   - Specify tone and style

1. Measure token impact

1. Test in Microsoft Foundry portal

1. Document your findings

### Example solution

Here's an example for a fitness coaching assistant:

**Baseline:**
```
You are a helpful fitness assistant. Your job is to help users with their fitness goals by providing workout recommendations and advice.
```

**Optimized:**
```
You are a certified fitness coach specializing in strength training and cardio.

For workout plans:
- Start with user's fitness level
- List exercises with sets/reps
- Note proper form cues

For nutrition:
- Focus on whole foods
- Provide macronutrient guidance
- Suggest meal timing

Prioritize safety and progressive overload.
```

## Clean up

After completing the exercise, commit your work to version control.

1. Navigate to your repository root:

    ```powershell
    cd ..\..\..
    ```

1. Stage all changes:

    ```powershell
    git add .
    ```

1. Commit with a descriptive message:

    ```powershell
    git commit -m "Complete prompt optimization exercise"
    ```

1. Push to GitHub:

    ```powershell
    git push
    ```

## Summary

In this exercise, you:

- ✅ Analyzed baseline prompts and measured token usage
- ✅ Applied systematic optimization techniques (verbosity reduction, domain context, structured output)
- ✅ Measured token impact of different optimization strategies
- ✅ Tested prompt variations in Microsoft Foundry's chat playground
- ✅ Compared prompt versions across quality criteria
- ✅ Learned trade-offs between token efficiency and output quality

## Key takeaways

1. **Token optimization matters** - Reducing prompt tokens decreases costs and latency
2. **Domain context improves quality** - Specific expertise leads to better responses
3. **Structure enhances consistency** - Output formatting guidance improves reliability
4. **Testing validates improvements** - Always verify optimizations with real queries
5. **Trade-offs exist** - Balance token efficiency with output quality based on use case

## Next steps

- Explore [Optimize RAG Solutions for GenAI](04-optimize-rag.md) to enhance context-aware AI
- Learn about [Manage Agent Artifacts with GitHub](02-prompt-management.md) to version your optimized prompts
- Review [Microsoft Learn: Prompt Engineering](https://learn.microsoft.com/azure/ai-services/openai/concepts/prompt-engineering) for advanced techniques
