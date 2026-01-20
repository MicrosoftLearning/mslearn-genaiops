# GenAI Operations - Trail Guide Agent Workshop

This repository contains a comprehensive workshop for building, evaluating, and deploying GenAI applications using Microsoft Foundry. The project demonstrates end-to-end GenAIOps practices including prompt management, manual and automated evaluation, safety testing, deployment, and monitoring.

**Adventure Works Outdoor Gear - AI Trail Assistant**: Build an intelligent trail guide agent that helps outdoor enthusiasts find and explore hiking trails.

[Repository Structure](#repository-structure) • [Getting Started](#getting-started) • [Workshop Labs](#workshop-labs) • [Documentation](#documentation)

## Repository Structure

```
mslearn-genaiops/
├── infra/                          # Infrastructure as Code (Bicep)
│   ├── main.bicep                  # Main infrastructure definition
│   ├── main.parameters.json        # Infrastructure parameters
│   └── core/                       # Modular infrastructure components
│       ├── ai/                     # Microsoft Foundry project & connections
│       └── monitor/                # Application Insights & Log Analytics
│
├── src/
│   ├── agents/                     # AI Agent implementations
│   │   ├── trail_guide_agent/      # Main trail recommendation agent
│   │   │   ├── trail_guide_agent.py
│   │   │   ├── agent.yaml
│   │   │   └── prompts/            # Versioned prompt instructions
│   │   ├── model_comparison/       # Model evaluation & comparison
│   │   ├── prompt_optimization/    # Prompt engineering workflows
│   │   └── monitoring_agent/       # Observability demonstrations
│   │
│   ├── evaluators/                 # Custom evaluation logic
│   │   ├── quality_evaluators.py   # Quality metrics (relevance, coherence)
│   │   └── safety_evaluators.py    # Safety & red-teaming evaluators
│   │
│   └── tests/                      # Test suites
│       ├── test_trail_guide_agents.py
│       └── interact_with_agent.py  # Interactive CLI chat
│
├── data/
│   └── datasets/                   # Workshop data assets
│       ├── app_hotel_reviews.csv   # Sample review dataset
│       └── evaluation_rubrics.md   # Evaluation criteria
│
├── docs/                           # Workshop documentation
│   ├── 01-infrastructure-setup.md  # Lab 1: Setup
│   ├── 02-prompt-management.md     # Lab 2: Prompt versioning
│   ├── 03-manual-evaluation.md     # Lab 3: Manual evaluation
│   ├── 04-automated-evaluation.md  # Lab 4: Automated testing
│   ├── 05-safety-red-teaming.md    # Lab 5: Safety testing
│   ├── 06-deployment-monitoring.md # Lab 6: Deployment & monitoring
│   ├── scenario.md                 # Use case overview
│   ├── spec.md                     # Technical specifications
│   └── modules/                    # Learning modules
│
├── requirements.txt                # Python dependencies
├──What You'll Build

### Trail Guide Agent

The main application - an AI agent that provides personalized hiking trail recommendations for Adventure Works Outdoor Gear customers.

**Key Components**:
- `trail_guide_agent.py`: Agent implementation using Azure AI Projects SDK
- `agent.yaml`: Agent configuration
- `prompts/`: Versioned prompt instructions (v1, v2, v3)
- `interact_with_agent.py`: Interactive CLI for testing

**Capabilities**:
- Natural language trail queries
- Personalized recommendations based on user preferences
- Safety information and trail conditions
- Multi-turn conversational interactions

## Workshop Labs

Follow the labs in sequence for a complete GenAIOps learning experience:

| Lab | Title | Description | Duration |
|-----|-------|-------------|----------|
| 1 | [Infrastructure Setup](docs/01-infrastructure-setup.md) | Deploy Microsoft Foundry resources and create your first agent | 20 min |
| 2 | [Prompt Management](docs/02-prompt-management.md) | Version control and iterate on prompts | 30 min |
| 3 | [Manual Evaluation](docs/03-manual-evaluation.md) | Human-in-the-loop quality assessment | 30 min |
| 4 | [Automated Evaluation](docs/04-automated-evaluation.md) | Programmatic testing and metrics | 30 min |
| 5 | [Safety & Red-teaming](docs/05-safety-red-teaming.md) | Adversarial testing for safety | 30 min |
| 6 | [Deployment & Monitoring](docs/06-deployment-monitoring.md) | Production deployment with tracing | 30 min |

### Additional Resources

- [Scenario](docs/scenario.md): Adventure Works use case and business context
- [Technical Spec](docs/spec.md): Technical specifications and requirements
- [Learning Modules](docs/modules/): Standalone learning modules

- `docs/modules/prompt-versioning-microsoft-foundry.md`
- `docs/modules/manual-evaluation-genai-applications.md`
- `docs/modules/automated-evaluation-genai-workflows.md`

## Getting Started

### Prerequisites

- **Azure Subscription**: Active subscription with appropriate permissions
- **Visual Studio Code**: Recommended IDE for the workshop
- **Azure Developer CLI (azd)**: 
  - Windows: `winget install microsoft.azd`
  - macOS: `brew tap azure/azd && brew install azd`
  - Linux: `curl -fsSL https://aka.ms/install-azd.sh | bash`
- **Python 3.9+**: Required for running agents

### Quick Start

Follow Lab 1 to get started:

```powershell
# Clone your forked repository
git clone https://github.com/[your-username]/mslearn-genaiops.git
cd mslearn-genaiops

# Authenticate with Azure
azd auth login
az login

# Provision infrastructure
azd up

# Generate environment variables
azd env get-values > .env

# Create virtual environment and install dependencies
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

# Add agent configuration to .env
# AGENT_NAME=trail-guide-v1
# MODEL_NAME=gpt-4.1

# Create your first agent
cd src/agents/trail_guide_agent
python trail_guide_agent.py

# Test the agent interactively
cd ../../..
python src\tests\interact_with_agent.py
```

For detailed instructions, see [Lab 1: Infrastructure Setup](docs/01-infrastructure-setup.md).
For detailed instructions, see [Lab 1: Infrastructure Setup](docs/01-infrastructure-setup.md).

## Azure Resources Deployed

| Resource | Description |
|----------|-------------|
| **Microsoft Foundry Hub & Project** | Collaborative workspace with access to AI models and development tools |
| **Application Insights** | Application performance monitoring and telemetry |
| **Log Analytics Workspace** | Centralized logging and monitoring data |

### Architecture

```
Azure Resource Group
├── Microsoft Foundry Hub
│   └── Microsoft Foundry Project (trail-guide)
├── Application Insights
└── Log Analytics Workspace
```

## Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `azure-ai-projects` | `>=1.0.0b1` | Microsoft Foundry SDK (preview) |
| `azure-identity` | `>=1.15.0` | Azure authentication |
| `pandas` | `>=2.1.0` | Data processing for evaluations |
| `pytest` | `>=7.4.0` | Testing framework |
| `python-dotenv` | `>=1.0.0` | Environment configuration |

> **Note**: This project requires the **preview version** of `azure-ai-projects` for agent functionality.

## Testing

Run the test suite:
```powershell
pytest src/tests/
```

Interactive agent testing:
```powershell
python src\tests\interact_with_agent.py
```

## Resource Cleanup

To prevent unnecessary charges, clean up resources after completing the workshop:

```powershell
azd down
```

Alternatively, delete the resource group directly from the Azure Portal.

## Cost Considerations

Pricing varies by region and usage. The majority of resources use usage-based pricing:

- **Microsoft Foundry**: Standard tier with Global Standard models (gpt-4.1)
- **Application Insights**: Pay-as-you-go based on data ingestion
- **Log Analytics**: Pay-as-you-go based on data ingested

⚠️ Remember to run `azd down` when finished to avoid unnecessary costs.

## Security Best Practices

This project implements Azure security best practices:

- **Managed Identity**: Keyless authentication using DefaultAzureCredential
- **No hardcoded secrets**: All credentials via environment variables
- **Principle of least privilege**: Minimal required permissions

For production deployments, consider:
- Enable [Microsoft Defender for Cloud](https://learn.microsoft.com/azure/defender-for-cloud/)
- Implement network security controls and private endpoints
- Enable [Microsoft Purview](https://learn.microsoft.com/azure/purview/) for data governance

## Support

- **GitHub Issues**: Report bugs or request features
- **Documentation**: See the `docs/` directory
- **Microsoft Learn**: [Microsoft Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/)

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Disclaimers

**Trademarks** This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow [Microsoft’s Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general). Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party’s policies.

To the extent that the Software includes components or code used in or derived from Microsoft products or services, including without limitation Microsoft Azure Services (collectively, “Microsoft Products and Services”), you must also comply with the Product Terms applicable to such Microsoft Products and Services. You acknowledge and agree that the license governing the Software does not grant you a license or other right to use Microsoft Products and Services. Nothing in the license or this ReadMe file will serve to supersede, amend, terminate or modify any terms in the Product Terms for any Microsoft Products and Services.

You must also comply with all domestic and international export laws and regulations that apply to the Software, which include restrictions on destinations, end users, and end use. For further information on export restrictions, visit <https://aka.ms/exporting>.

You acknowledge that the Software and Microsoft Products and Services (1) are not designed, intended or made available as a medical device(s), and (2) are not designed or intended to be a substitute for professional medical advice, diagnosis, treatment, or judgment and should not be used to replace or as a substitute for professional medical advice, diagnosis, treatment, or judgment. Customer is solely responsible for displaying and/or obtaining appropriate consents, warnings, disclaimers, and acknowledgements to end users of Customer’s implementation of the Online Services.

You acknowledge the Software is not subject to SOC 1 and SOC 2 compliance audits. No Microsoft technology, nor any of its component technologies, including the Software, is intended or made available as a substitute for the professional advice, opinion, or judgement of a certified financial services professional. Do not use the Software to replace, substitute, or provide professional financial advice or judgment.  

BY ACCESSING OR USING THE SOFTWARE, YOU ACKNOWLEDGE THAT THE SOFTWARE IS NOT DESIGNED OR INTENDED TO SUPPORT ANY USE IN WHICH A SERVICE INTERRUPTION, DEFECT, ERROR, OR OTHER FAILURE OF THE SOFTWARE COULD RESULT IN THE DEATH OR SERIOUS BODILY INJURY OF ANY PERSON OR IN PHYSICAL OR ENVIRONMENTAL DAMAGE (COLLECTIVELY, “HIGH-RISK USE”), AND THAT YOU WILL ENSURE THAT, IN THE EVENT OF ANY INTERRUPTION, DEFECT, ERROR, OR OTHER FAILURE OF THE SOFTWARE, THE SAFETY OF PEOPLE, PROPERTY, AND THE ENVIRONMENT ARE NOT REDUCED BELOW A LEVEL THAT IS REASONABLY, APPROPRIATE, AND LEGAL, WHETHER IN GENERAL OR IN A SPECIFIC INDUSTRY. BY ACCESSING THE SOFTWARE, YOU FURTHER ACKNOWLEDGE THAT YOUR HIGH-RISK USE OF THE SOFTWARE IS AT YOUR OWN RISK.
