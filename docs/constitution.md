# GenAIOps Learning Project Constitution

## Project Purpose

This repository exists to teach GenAIOps principles through hands-on, practical examples. All design decisions prioritize:

- **Educational clarity** over production complexity
- **Fast setup** over enterprise-grade features
- **Individual learner experience** over team collaboration features
- **Observable outcomes** over comprehensive coverage

This is a learning sandbox, not a production reference architecture.

## Technology Standards

### Cloud Platform
- **All cloud resources must be hosted on Microsoft Azure**
- No multi-cloud or on-premises alternatives
- Leverage Microsoft Foundry, Azure OpenAI Service, and Azure AI Services
- Use Azure-native services for monitoring, storage, and secrets management

### Programming Languages and Frameworks
- **Primary language: Python 3.11+** for all agent definitions and application code
- **Use the latest Microsoft Foundry SDK** (`azure-ai-projects`) for AI agent development
  - Stay current with the newest SDK version to teach modern patterns
  - Avoid deprecated or legacy Azure AI SDKs
- Jupyter notebooks (.ipynb) for exploratory and demonstration code
- Bicep for infrastructure-as-code (alternatives allowed when explicitly requested)

### Infrastructure as Code
- **Default: Bicep templates** for all Azure resource provisioning
- Infrastructure organized under `/infrastructure/bicep`
- Alternative IaC tools (Terraform, ARM) allowed only when student explicitly requests them
- Keep templates minimal—provision only what's needed for the learning objective

### Secret and Configuration Management
- **Azure Key Vault** for all secrets (API keys, connection strings, credentials)
- Azure App Configuration for feature flags and non-sensitive configuration (when needed)
- Environment variables for local development references to Azure resources
- **Never commit secrets, API keys, or credentials to source code**

## Security Requirements

### Authentication and Authorization
- Use **Azure authentication methods optimized for individual learners**:
  - Azure CLI authentication (`az login`) for local development
  - Managed Identity for Azure-hosted resources
  - DefaultAzureCredential pattern in Python code
- No complex multi-tenant authentication
- No custom authentication implementations
- Assume single-user Azure subscription context

### Data Protection
- No encryption requirements for learning datasets (they contain synthetic data)
- Sensitive data patterns (PII) used only in examples, not actual data
- Log sanitization: no API keys or secrets in logs or outputs

### Secret Management
- **Store no secrets in source code or configuration files**
- All secrets retrieved at runtime from Azure Key Vault
- `.env` files (if used) must be in `.gitignore`
- README must clearly instruct learners how to configure their own secrets

## Educational Design Principles

### Learning Experience
- Every lab/module must define **1-3 clear, testable outcomes**
- Every lab/module must require a **post-workshop artifact** (diagram, decision, screenshot, finding)
- Support **short core path** (20-40 min) plus **optional stretch paths**
- Verification checkpoints: learners must prove success, not just complete steps

### Code and Documentation
- **Minimal viable implementation** over feature-complete examples
- Code clarity over performance optimization
- Inline comments explain *why*, not *what*
- READMEs must be runnable by a beginner with their own Azure account

### Setup Requirements
- Assume learners have:
  - Their own Azure subscription (free tier or student account)
  - Local VS Code with Python extension
  - A forked/templated copy of this repository
  - Azure CLI installed locally
- Setup time should not exceed 15 minutes for any module

## Performance and Scalability

**Not priorities for this educational project.**

Acceptable approaches:
- Synchronous API calls (no async required unless teaching async patterns)
- Basic error handling (retries not required unless teaching resilience)
- Single-region deployments
- Development/Basic pricing tiers for Azure resources

## Coding Standards

### Python Code
- Follow PEP 8 conventions
- Use type hints for function signatures
- Prefer `azure-identity` and Azure SDK libraries over custom HTTP clients
- Structure:
  ```
  src/
    agents/          # Agent implementations
    evaluators/      # Evaluation code
    tests/           # Test files
  ```

### Notebooks
- Clear markdown cells explaining each step
- Runnable top-to-bottom without manual intervention
- Output cells preserved to show expected results
- Kernel: Python 3.11+

### Bicep Templates
- Modular: separate files for logical resource groups
- Parameters for customization (resource names, SKUs)
- Outputs for values needed in application code
- Comments for non-obvious configuration choices

## Compliance and Governance

### Learning Environment Constraints
- **No production data, no production systems, no production compliance requirements**
- Synthetic datasets only (hotel reviews, trail guides, etc.)
- No GDPR, HIPAA, or regulatory considerations
- Telemetry: minimal, opt-in, Azure-native (Application Insights)

### Resource Cleanup
- All labs must include cleanup instructions
- Prefer resource groups for easy bulk deletion
- Warn learners about costs before deploying expensive resources

### Accessibility
- Documentation: clear headings, alt text for images
- Code samples: readable font sizes in notebooks
- No color-only indicators in visualizations

## Development Workflow with GitHub Spec Kit

When using GitHub Spec Kit (if applicable):

1. **Constitution (this file)** governs all specs, plans, and implementations
2. **Specifications** must align with educational outcomes (1-3 testable results)
3. **Plans** must prioritize minimal Azure resources and fast setup
4. **Implementation** must be runnable by individual learners with their own Azure account

## Prohibited Practices

**Never:**
- Require learners to set up complex networking (VNets, private endpoints) unless that's the learning objective
- Assume learners have organizational Azure AD tenant (use personal Microsoft accounts)
- Use enterprise-only features (Azure Front Door, Traffic Manager) without justification
- Commit `.env` files, API keys, or connection strings
- Create infrastructure that costs more than $5/day to run

**Avoid:**
- Production-grade patterns (circuit breakers, bulkheads) unless teaching reliability
- Multi-region deployments
- Premium SKUs for Azure resources
- Complex CI/CD pipelines (keep deployments manual or use Azure Developer CLI)

## Example: Applying These Principles

**Scenario:** Create a trail guide agent with RAG (retrieval-augmented generation)

**Constitution compliance:**
- ✅ Agent code in Python (`src/agents/trail_guide_agent/`)
- ✅ Azure OpenAI Service for LLM
- ✅ Azure AI Search for vector storage
- ✅ Bicep template provisions OpenAI, AI Search, Key Vault
- ✅ Secrets (API keys) in Key Vault, retrieved via `DefaultAzureCredential`
- ✅ 30-minute core lab: deploy agent, run one query, verify response
- ✅ Stretch lab: compare embedding models, produce decision artifact
- ✅ Resource group cleanup script provided
- ❌ No multi-tenant auth
- ❌ No production monitoring dashboards
- ❌ No autoscaling configuration

---

## Summary

This constitution ensures every component in this repository prioritizes the **learner's experience**:
- Fast to set up
- Easy to understand
- Cheap to run
- Clear outcomes

When in doubt, choose the **simplest Azure-native approach** that teaches the GenAIOps principle effectively.
