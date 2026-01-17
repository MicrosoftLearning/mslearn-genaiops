---
lab:
    title: 'Develop prompt and agent versions'
    description: 'Learn to manage agent versions with incremental improvements and Git workflows'
---

# Develop prompt and agent versions

## Learning objective

Learn to manage generative AI agents through version control, implementing incremental improvements from basic functionality to advanced personalization while maintaining traceability between code and deployed systems.

## Scenario

As part of Adventure Works' AI initiative, you're tasked with developing an intelligent trail guide agent that helps hikers plan outdoor adventures. The agent needs to evolve from basic functionality to advanced personalization while maintaining excellent user experience.

Starting with basic trail and accommodation assistance, you'll progressively enhance the agent with sentiment analysis for hiker satisfaction, expertise in safety and weather conditions, and personalization features for returning customers. Each version must be tracked, tested, and deployed independently while maintaining the ability to rollback or compare performance across different user segments.

*Reference the [business scenario](scenario.md) for complete context about Adventure Works' objectives and customer needs.*

## Overview

This lab demonstrates version management and iterative development of AI agents using Microsoft Foundry. You'll work with Python scripts to deploy different versions of a Trail Guide Agent, then navigate to the portal to review your deployments and understand the relationship between programmatic deployment and portal management.

## Lab structure

1. **Deploy agent versions using single Python script** - Modify script to deploy V1, V2, and V3 versions
2. **Review deployments in Microsoft Foundry portal** - Navigate to portal to see your agents
3. **Compare prompt evolution** - Understand how prompts evolved across versions
4. **Run comprehensive tests** - Validate agent performance across versions
5. **Compare version improvements** - Analyze evolution from V1 → V2 → V3

## Prerequisites

- Python 3.9 or later
- Visual Studio Code
- Git and GitHub account  
- Azure subscription with Microsoft Foundry access
- Basic understanding of Python and Git workflows

## Lab setup

### Create repository from template

To complete the tasks in this exercise, you'll create your own repository from the template to practice realistic version control workflows.

1. Navigate to `https://github.com/[your-org]/mslearn-genaiops` in your web browser.
1. Click **Use this template** → **Create a new repository**.
1. Enter a name for your repository such as `mslearn-genaiops`.
1. Set the repository to **Public** or **Private** based on your preference.
1. Click **Create repository**.
1. Open your terminal and clone the repository:

   ```bash
   git clone https://github.com/[your-username]/mslearn-genaiops.git
   cd mslearn-genaiops
   ```

1. Open the repository in Visual Studio Code:

   ```bash
   code .
   ```

4. **Configure your environment variables** by editing the `.env` file with your Azure AI Projects details:
   ```bash
   PROJECT_ENDPOINT=https://your-project-endpoint.cognitiveservices.azure.com
   AGENT_NAME=trail-guide-v1
   MODEL_DEPLOYMENT_NAME=gpt-4o-mini
   ```

5. **Install the required Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   This command installs the Azure AI Projects SDK and all required dependencies.

## Deploy and review agent versions

You'll deploy two agent versions using Python scripts, then review them in the Microsoft Foundry portal.

### Deploy Trail Guide Agent V1

1. Navigate to the trail guide agent directory:

   ```bash
   cd src/agents/trail_guide_agent
   ```

1. **Review the agent creation script** (`trail_guide_agent.py`) to understand the pattern:
   ```python
   # Read instructions from prompt file
   # TODO: Update this line to point to the correct instruction file
   # v1_instructions.txt - Basic trail guide
   # v2_instructions.txt - Enhanced with personalization 
   # v3_instructions.txt - Production-ready with advanced capabilities
   with open('prompts/v1_instructions.txt', 'r') as f:
       instructions = f.read().strip()
   ```

1. **Verify the script is configured for V1** by ensuring it reads from `v1_instructions.txt`.

1. Run the agent creation script:

   ```bash
   python trail_guide_agent.py
   ```

1. **Observe the deployment output** and note the following information:
   - The Agent ID that gets generated
   - The agent name and version number
   - The simple creation pattern used

1. **Navigate to the Azure AI Foundry portal** at `https://ai.azure.com/build/agents`.
1. **Find your agent** in the list and click on it to explore:
   - The system instructions (currently from v1_instructions.txt)
   - The model configuration
   - The deployment parameters

1. **Test the agent interactively** in the portal by asking it questions like:
   - "What gear do I need for a day hike?"
   - "Recommend a trail near Seattle for beginners"

### Deploy Trail Guide Agent V2

1. **Copy the Agent ID from V1** for comparison:
   - Note the Agent ID from the V1 output
   - Set it as an environment variable:
   ```bash
   export V1_AGENT_ID="your-v1-agent-id-here"
   ```

1. **Update your environment variables** for V2:
   ```bash
   AGENT_NAME=trail-guide-v2
   ```

1. **Modify the script** to use V2 instructions by editing `trail_guide_agent.py`:
   
   **Find this line:**
   ```python
   with open('prompts/v1_instructions.txt', 'r') as f:
   ```
   
   **Change it to:**
   ```python
   with open('prompts/v2_instructions.txt', 'r') as f:
   ```

1. Run the agent creation script:

   ```bash
   python trail_guide_agent.py
   ```

1. **Navigate to both agents in the portal** and compare their configurations side-by-side.
1. **Notice the enhanced features in V2** by comparing the instructions:
   - More detailed and nuanced system prompt
   - Personalization capabilities
   - Enhanced response quality and detail

## Review prompt evolution

Now examine how the prompts evolved across versions to understand the progression from basic to advanced capabilities.

### Create V3 agent

1. **Update your environment variables** for V3:
   ```bash
   AGENT_NAME=trail-guide-v3
   ```

1. **Modify the script** to use V3 instructions by editing `trail_guide_agent.py`:
   
   **Find this line:**
   ```python
   with open('prompts/v2_instructions.txt', 'r') as f:
   ```
   
   **Change it to:**
   ```python
   with open('prompts/v3_instructions.txt', 'r') as f:
   ```

1. Run the agent creation script:

   ```bash
   python trail_guide_agent.py
   ```

1. **Set the Agent ID as an environment variable:**

   ```bash
   export V3_AGENT_ID="your-v3-agent-id-here"
   ```

### Compare prompt evolution

1. **Review the prompt files** in the `prompts/` directory:
   - `v1_instructions.txt` - Basic trail guide functionality
   - `v2_instructions.txt` - Enhanced with personalization
   - `v3_instructions.txt` - Production-ready with advanced capabilities

1. **Compare the instruction content** and notice:
   - **V1 → V2**: Added personalization factors and knowledge base references
   - **V2 → V3**: Added structured framework and enterprise features
   - **Progression**: From simple to comprehensive guidance

1. **Test each agent version** in the Azure AI Foundry portal to see how the different prompts affect behavior.

### Why this workflow matters

- **Consistency**: Single script prevents version drift
- **Maintainability**: Prompt changes don't require code updates
- **Learning**: Students understand which prompt creates which agent
- **Version control**: Clear tracking of prompt evolution
- **Testing integration**: Portal agents can be included in automated tests

## Run comprehensive tests

Use the automated test suite to validate all agent versions and compare their performance.

### Set up all agent IDs

1. Configure environment variables with the Agent IDs from your deployed agents:

   ```bash
   export V1_AGENT_ID="your-v1-agent-id"
   export V2_AGENT_ID="your-v2-agent-id" 
   export V3_AGENT_ID="your-v3-agent-id"
   ```

### Execute comprehensive tests

1. Navigate to the tests directory:

   ```bash
   cd src/tests
   ```

1. Run the comprehensive test suite:

   ```bash
   python test_trail_guide_agents.py
   ```

1. **Review the test results** which include:
   - **Functional tests**: Validate basic functionality across all versions
   - **Performance tests**: Measure response times and quality metrics
   - **Regression tests**: Compare versions to ensure improvements
   - **Feature validation**: Verify expected capabilities are working correctly

### Analyze test outputs

The test suite generates several types of output:

- **Individual results**: `test_results/functional-v1-[timestamp].json`
- **Performance metrics**: `test_results/performance-v2-[timestamp].json`
- **Version comparisons**: `test_results/regression-[timestamp].json`
- **Summary report**: `test_results/test-report-[timestamp].md`

### Key metrics to observe

- **Success rate**: Percentage of tests passing per version
- **Response time**: Average time for agent responses
- **Feature coverage**: Which capabilities are working in each version
- **Quality indicators**: Relevance and completeness of responses

## Analyze version management insights

Analyze the evolution from V1 → V2 → V3 and understand different development workflows.

### Compare development approaches

1. **V1 & V2**: Script-based deployment
   - **Advantages**: Version controlled, repeatable, testable
   - **Use case**: Initial development, experimentation
   - **Workflow**: Code → Deploy → Test → Iterate

2. **V3**: Portal-created with documentation
   - **Advantages**: Visual interface, rapid prototyping, business user friendly
   - **Use case**: Production configuration, stakeholder collaboration
   - **Workflow**: Portal → Document → Test → Maintain

### Analyze version evolution

1. Navigate back to the trail guide agent directory:

   ```bash
   cd src/agents/trail_guide_agent
   ```

1. Run a comparison test by switching between agent versions:

   **Test V1:**
   ```bash
   # Update script to use v1_instructions.txt
   python trail_guide_agent.py
   ```
   
   **Test V2:**
   ```bash
   # Update script to use v2_instructions.txt  
   python trail_guide_agent.py
   ```
   
   **Test V3:**
   ```bash
   # Update script to use v3_instructions.txt
   python trail_guide_agent.py
   ```

1. **Review the key improvements** across versions:
   - **V1 → V2**: Enhanced prompts, tool integration, knowledge base connectivity
   - **V2 → V3**: Multi-modal capabilities, enterprise features, real-time data access
   - **Performance metrics**: Response times, accuracy scores, feature coverage

1. **Examine the comparison results** saved in the `comparisons/` folder.

### Best practices learned

1. **Hybrid workflow**:
   - Use scripts for initial development and testing
   - Use portal for production configuration and stakeholder review
   - Always document portal changes in version control

2. **Testing integration**:
   - Automated tests work with both script-deployed and portal-created agents
   - Maintain test coverage across all versions
   - Use regression tests to prevent capability loss

3. **Traceability**:
   - Keep deployment records in `deployments/` folder
   - Document portal changes with configuration scripts
   - Maintain test results for compliance and analysis

## Key takeaways

You've successfully implemented a comprehensive prompt management system that provides:

✅ **Script-based deployment**: V1 and V2 agents deployed programmatically  
✅ **Portal integration**: V3 agent created via UI with documentation workflow  
✅ **Version traceability**: All agents documented in version control  
✅ **Automated testing**: Comprehensive test suite across all versions  
✅ **Performance comparison**: Metrics and analytics for version evolution  
✅ **Hybrid workflow**: Best practices for code + portal development  

## Next steps

In the next lab, you'll learn to evaluate these agent versions using manual testing processes to determine which performs better for different scenarios and customer segments.
