# Manage prompts for agents in Microsoft Foundry with GitHub

## Role(s)

- MLOps Engineer
- ML Engineer
- AI Engineer

## Level

Intermediate

## Product(s)

- Microsoft Foundry
- GitHub

## Prerequisites

- Experience with Python for data science and machine learning
- Understanding of AI/ML model development and prompts
- Intermediate Git skills including creating commits, writing meaningful commit messages, and working with branches

## Summary

Learn how to apply DevOps practices to manage prompts in AI applications using Microsoft Foundry. As an MLOps engineer, you discover how to treat prompts as production assets that need the same care as your ML models. This module shows you how to organize and track prompt changes through development lifecycles, combining Microsoft Foundry's agent versioning with Git-based source control to create reliable change management for AI systems.

## Learning objectives

By the end of this module, you can:

1. Explain how Microsoft Foundry creates versions when you update agent instructions
2. Organize prompts in Python projects so you can track changes effectively
3. Use Git to track prompt changes with meaningful commit messages and branching strategies
4. Move agents with updated instructions from development to production environments

## Chunk your content into subtasks

Identify the subtasks of versioning prompts in Microsoft Foundry.

| Subtask | How do you assess it? (Exercise or Knowledge check) | Which learning objective(s) does this help meet? | Does the subtask have enough learning content to justify an entire unit? If not, which other subtask do you combine it with? |
| ---- | ---- | ---- | ---- |
| Understand how prompts (instructions) define agent behavior and are versioned in Microsoft Foundry | Knowledge check | 1 | Yes - foundational concepts need dedicated unit |
| Structure Python projects for prompt version management | Knowledge check + Exercise | 2 | Yes - hands-on organization and file structure |
| Track prompt changes with Git and create meaningful commit history | Exercise | 3 | No - combine with promotion workflow |
| Promote agents with updated instructions across environments (dev to production) | Exercise | 3, 4 | No - combine with Git tracking |

## Outline the units

1. **Introduction**

    You're already managing ML models as production assets. Now you need to do the same thing with prompts. This module shows you how to extend the DevOps practices you know to prompt management in AI applications. You learn how Microsoft Foundry creates agent versions when you update instructions, and how to use Git alongside this feature to create a complete change management system for your AI applications.

    **What you'll build**: By the end of this module, you'll have a working Python project with structured prompt management, connected to Microsoft Foundry agents, and tracked with Git version control - ready for production deployment.

2. **How Microsoft Foundry handles prompt versioning**

    Learn how Microsoft Foundry manages versions when you update prompts:

    - How instructions define what your agent does
        - Instructions are the core component that controls how agents respond
        - When you create an agent with `create_version()`, Microsoft Foundry automatically creates an immutable version
        - Each agent version captures a specific snapshot of instructions, model configuration, and tools
        - You can reference specific versions for controlled deployment and rollback
        - Version immutability ensures consistency - modifications require creating a new version
    - The Microsoft Foundry Python SDK for agent creation
        - Use `AIProjectClient` to connect to your Microsoft Foundry project
        - Create agents with `PromptAgentDefinition` that includes model and instructions
        - Example: `project_client.agents.create_version(agent_name="MyAgent", definition=PromptAgentDefinition(model="gpt-4o-mini", instructions="You are a helpful assistant"))`
        - The SDK returns agent metadata including id, name, and version number
        - Environment variables control project endpoint and authentication
    - Why you still need source control alongside platform versioning
        - Git tracks the "why" behind your changes with meaningful commit messages
        - Git bridges the gap between automatic platform versions and development governance
        - You get human-readable change history that your team can understand
        - Git gives you the same workflow you use for other production assets
        - Git enables branching strategies for testing prompt changes safely
        - Platform versions are sequential numbers; Git provides semantic context
    - What happens when you change instructions
        - Instruction changes trigger new agent versions automatically
        - Small prompt tweaks can impact agent behavior and downstream systems
        - You need to trace changes to reproduce previous behavior
        - Draft state allows testing without creating versions; save frequently to preserve changes
        - Published agents get stable endpoints for production use

    **Knowledge check**

    - Multiple choice questions testing understanding of Microsoft Foundry's automatic versioning
    - Scenario-based questions about when `create_version()` creates new versions vs. updates
    - Questions about the relationship between Git commits and Microsoft Foundry agent versions
    - Code comprehension questions about `PromptAgentDefinition` parameters
    - Scenario questions about managing prompt changes in team environments

3. **Structure Python projects for effective prompt management**

    Learn to organize your code and prompts for maintainable AI applications:

    - Project structure best practices for prompt management
        - Separate prompt files from application logic (`prompts/` directory)
        - Use consistent naming: `agent_name_instructions.md` or `agent_name_v1.txt`
        - Organize prompts by agent type or application feature
        - Include metadata files documenting prompt purpose and expected behavior
        - Store environment configurations in `.env` files (excluded from Git)
    - Integration patterns with Microsoft Foundry SDK
        - Use `AIProjectClient` with `DefaultAzureCredential()` for authentication
        - Load prompts from files: `instructions = open('prompts/assistant_v1.md').read()`
        - Create agents programmatically: `create_version(agent_name, PromptAgentDefinition(model, instructions))`
        - Environment variables for different stages: `PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`, `AGENT_NAME`
        - Testing locally with agent playground before committing changes
    - Code organization patterns
        - Separate agent creation scripts from business logic
        - Use configuration classes to manage multiple environments
        - Implement helper functions for common agent operations
        - Create templates for consistent prompt formatting
    - Documentation and maintenance practices
        - Document prompt changes and their expected impact in README files
        - Use semantic commit messages linking to agent version numbers
        - Plan for prompt rollbacks using Git tags and agent version references
        - Track agent performance metrics alongside Git commit history

    **Knowledge check**

    - Questions about Python project organization for prompt management
    - Code completion exercises using `AIProjectClient` and `PromptAgentDefinition`
    - Scenario-based questions about environment configuration management
    - Questions about linking Git commits to Microsoft Foundry agent versions

4. **Exercise - Build a complete prompt versioning workflow**

    Put prompt versioning into practice by building a structured workflow:

    1. **Set up your Python environment and project structure**
       - Install Microsoft Foundry SDK: `pip install azure-ai-projects azure-identity python-dotenv`
       - Create project directories: `mkdir prompts agents utils`
       - Set up environment variables in `.env` file with your project endpoint
       - Authenticate with Azure CLI: `az login`

    2. **Create your first agent using the Python SDK**
       - Write a script using `AIProjectClient` and `DefaultAzureCredential`
       - Create a `PromptAgentDefinition` with model and instructions
       - Use `create_version()` to deploy your first agent
       - Verify agent creation and note the returned version number

    3. **Implement file-based prompt management**
       - Store instructions in `prompts/helpful_assistant_v1.md`
       - Load prompts dynamically: `instructions = Path('prompts/helpful_assistant_v1.md').read_text()`
       - Update your agent creation script to use file-based prompts
       - Test the workflow by creating an agent version with file-loaded instructions

    4. **Establish Git workflow for prompt changes**
       - Initialize Git repository and commit initial structure
       - Make your first prompt modification in the markdown file
       - Commit with descriptive message: "Update assistant instructions: add technical writing focus"
       - Tag the commit with agent version: `git tag agent-v2`

    5. **Deploy updated prompts and verify versioning**
       - Run your script to create a new agent version with updated instructions
       - Compare the new version output with the previous version
       - Document the relationship between Git commit hash and agent version

    6. **Practice branching for experimental changes**
       - Create feature branch: `git checkout -b experiment/creative-writing-agent`
       - Modify prompts for creative writing use case
       - Test the experimental agent version without affecting main branch
       - Use agent version comparison in Microsoft Foundry portal

    7. **Implement promotion workflow**
       - Merge successful experiments to main branch
       - Create production environment variables
       - Deploy the same agent configuration to production project
       - Verify consistent behavior across environments

    8. **Test rollback procedures**
       - Use Git to revert to previous prompt version: `git revert HEAD`
       - Redeploy agent with reverted instructions
       - Compare behavior with previous agent version
       - Document rollback process for team use

    9. **Create team documentation**
       - Write README with setup instructions and workflow steps
       - Document environment variable requirements
       - Create templates for new agent creation
       - Establish commit message conventions linking to agent versions

5. **Summary**

    You now know how to treat prompts like the production assets they are. Microsoft Foundry creates agent versions when you update instructions, and Git gives you the change tracking and governance you need. Together, they create a complete system for managing prompt changes from development to production. Use this workflow to keep your AI applications reliable as you iterate on prompts, just like you do with your ML models.

    **Next steps**: Apply this workflow to your own AI projects, establish team standards for prompt changes, and consider integrating prompt versioning into your existing CI/CD pipelines.

## Notes

- **Target duration**: 45-50 minutes total (15 minutes concept learning + 15 minutes project structure + 25-30 minutes hands-on exercise)
- **Audience approach**: Build on MLOps engineers' Python/ML expertise while introducing DevOps practices using familiar, everyday language
- **Writing style**: Use second person ("you"), present tense, active voice, and conversational tone following Microsoft Learn guidelines
- **Technical grounding**: Use actual Microsoft Foundry Python SDK code examples from official documentation
- **SDK integration**: Demonstrate `azure-ai-projects` library with `AIProjectClient`, `PromptAgentDefinition`, and `create_version()` methods
- **Authentication pattern**: Use `DefaultAzureCredential` and Azure CLI authentication as recommended by Microsoft
- **Code examples**: Include working Python snippets that learners can run in their own environments
- **Environment management**: Show proper use of environment variables for different deployment stages
- **Integration approach**: Show how Microsoft Foundry's automatic versioning complements traditional Git-based workflows
- **Practical emphasis**: Exercise provides end-to-end workflow from local development to production deployment
- **Assessment strategy**: Balance conceptual understanding with hands-on coding exercises using real SDK methods
- **Technical validation**: All code examples tested against Microsoft Foundry Python SDK documentation
- **Troubleshooting support**: Include common issues with authentication, environment setup, and API integration
- **Team focus**: Emphasize collaborative workflows using both Git and Microsoft Foundry versioning systems