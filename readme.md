# GenAI Operations (GenAIOps) workload repository

This repository demonstrates a production-ready GenAI Operations (GenAIOps) workload structure using Microsoft Foundry and Azure AI services. It includes comprehensive labs covering infrastructure as code, prompt management, evaluation workflows, and deployment practices for AI agents and applications.

## Repository structure

This repository is organized like a real-world GenAI Ops workload, with additional files specific to these learning labs:

```
├── .github/                          # GitHub Actions workflows and templates
│   └── workflows/                    # CI/CD pipelines for GenAI operations
│       ├── evaluation-pipeline.yml   # Automated evaluation workflows
│       ├── prompt-validation.yml     # Prompt versioning and validation
│       ├── infrastructure-deploy.yml # Infrastructure deployment
│       └── safety-testing.yml       # Automated safety testing
│
├── infrastructure/                   # Infrastructure as Code (IaC)
│   ├── bicep/                       # Azure Bicep templates
│   │   ├── main.bicep               # Main infrastructure template
│   │   ├── ai-services.bicep        # AI services configuration
│   │   ├── foundry-workspace.bicep  # Microsoft Foundry workspace setup
│   │   └── monitoring.bicep         # Observability and monitoring
│   └── scripts/                     # Deployment and setup scripts
│       ├── deploy.sh                # Main deployment script
│       └── setup-environment.sh     # Environment initialization
│
├── src/                             # Source code
│   ├── agents/                      # AI Agents (Python scripts using Foundry SDK)
│   │   ├── model_comparison/        # Model comparison and optimization
│   │   ├── prompt_optimization/     # Prompt engineering tools
│   │   ├── rag_agent/              # RAG implementation
│   │   └── monitoring_agent/       # Monitoring and tracing
│   └── evaluators/                  # Custom evaluation logic
│       ├── quality_evaluators.py    # Quality assessment evaluators
│       └── safety_evaluators.py     # Safety and harm detection
│
├── data/                            # All data files and datasets
│   ├── datasets/                    # Application and evaluation datasets
│   │   ├── app_hotel_reviews.csv    # Sample application data
│   │   ├── quality_test_set.csv     # Quality evaluation test data
│   │   ├── safety_test_set.csv      # Safety evaluation test data
│   │   └── evaluation_rubrics.md    # Evaluation criteria and rubrics
│   ├── results/                     # Evaluation results and outputs
│   │   ├── manual_evaluations/      # Manual evaluation CSV results
│   │   ├── automated_evaluations/   # Automated evaluation outputs
│   │   └── shadow_rating_analysis/  # Automated vs manual comparisons
│   └── reports/                     # Evaluation summary reports
│
├── docs/                            # Lab instructions and documentation
│   ├── 01-infrastructure-setup.md   # Lab 1: Infrastructure as Code
│   ├── 02-prompt-management.md      # Lab 2: Prompt Versioning & Management
│   ├── 03-manual-evaluation.md      # Lab 3: Manual Evaluation Workflows
│   ├── 04-automated-evaluation.md   # Lab 4: Automated Evaluation Pipelines
│   ├── 05-safety-red-teaming.md     # Lab 5: Safety Testing & Red Teaming
│   └── 06-deployment-monitoring.md  # Lab 6: Production Deployment & Monitoring
│
├── requirements.txt                  # Python dependencies
├── LICENSE                          # License file
├── readme.md                        # Repository documentation
│
└── Lab Infrastructure Files (GitHub Pages specific):
    ├── index.md                     # GitHub Pages homepage for lab instructions
    ├── _config.yml                  # Jekyll configuration for rendering labs
    └── _build.yml                   # Build pipeline for lab content distribution
```

### File structure explained

**Production GenAI Ops Files** (would exist in real workloads):
- `infrastructure/` - Bicep templates and deployment scripts
- `src/` - Application source code (agents and evaluators)
- `data/` - Datasets, evaluation results, and analysis reports
- `.github/workflows/` - CI/CD automation pipelines
- `requirements.txt` - Python package dependencies

**Lab-Specific Files** (for educational purposes only):
- `docs/` - Step-by-step lab instructions rendered via GitHub Pages
- `index.md` - Homepage that lists and links to all lab exercises  
- `_config.yml` - Jekyll configuration for rendering Markdown labs as web pages
- `_build.yml` - Microsoft Learn build pipeline for lab content distribution

## Learning path overview

This repository supports hands-on learning through progressive labs that mirror real-world GenAI Ops scenarios:

### Core labs

1. **[Infrastructure as Code for GenAI Workloads](docs/01-infrastructure-setup.md)**
   - Deploy Microsoft Foundry workspace and AI services using Bicep
   - Configure monitoring, networking, and security
   - Implement infrastructure versioning and governance

2. **[Prompt Management and Versioning](docs/02-prompt-management.md)**
   - Structure prompts for version control and collaboration
   - Implement prompt testing and validation workflows  
   - Manage prompt deployment across environments

3. **[Manual Evaluation Workflows](docs/03-manual-evaluation.md)**
   - Create structured evaluation datasets and rubrics
   - Conduct quality assessments (groundedness, relevance, coherence)
   - Implement collaborative evaluation using GitHub workflows

4. **[Automated Evaluation Pipelines](docs/04-automated-evaluation.md)**
   - Set up automated evaluation using Microsoft Foundry SDK
   - Configure GitHub Actions for continuous evaluation
   - Implement shadow rating and cost optimization

5. **[Safety Testing and Red Teaming](docs/05-safety-red-teaming.md)**
   - Implement automated safety monitoring systems
   - Configure red teaming agents and scenarios
   - Set up incident response procedures

6. **[Production Deployment and Monitoring](docs/06-deployment-monitoring.md)**
   - Deploy agents to production environments
   - Implement observability and alerting
   - Configure deployment strategies (blue-green, canary)

### Advanced topics (future labs)

- **Fine-tuning Workflows**: Custom model training and deployment
- **Retrieval Performance Optimization**: RAG system optimization and monitoring
- **Multi-agent Orchestration**: Complex agent workflow management
- **Compliance and Governance**: Regulatory compliance and audit trails

## Getting started

### Prerequisites

- Azure subscription with appropriate permissions
- Microsoft Foundry workspace access
- GitHub account with Actions enabled
- Python 3.9+ with pip
- Azure CLI and Bicep CLI installed
- Docker (for containerized deployments)

### Quick start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/genaiops-workload.git
   cd genaiops-workload
   ```

2. **Set up your environment**
   ```bash
   ./infrastructure/scripts/setup-environment.sh
   ```

3. **Deploy base infrastructure**
   ```bash
   ./infrastructure/scripts/deploy.sh --environment development
   ```

4. **Start with Lab 1**
   - Open [docs/01-infrastructure-setup.md](docs/01-infrastructure-setup.md)
   - Follow the step-by-step instructions
   - Or view the rendered labs at: https://your-username.github.io/mslearn-genaiops/

## Development workflow

This repository follows GitOps principles:

- **Infrastructure Changes**: Bicep templates in `infrastructure/`, deployed via GitHub Actions
- **Agent Development**: Python scripts in `agents/`, with automated testing
- **Evaluation Updates**: Custom evaluators in `evaluators/`, with CI validation  
- **Prompt Management**: Version-controlled prompts within agent Python files

## Monitoring and observability

The infrastructure includes monitoring for:

- **Agent Performance**: Response times, success rates, token usage
- **Infrastructure**: Azure Monitor, Application Insights integration  
- **Evaluation Results**: Automated reporting and trend analysis
- **Costs**: Resource usage tracking and optimization alerts

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details on:

- Code standards and review process
- Testing requirements
- Documentation expectations
- Security considerations

## Related learning resources

This repository supports the [Microsoft Learn GenAI Ops learning path](https://learn.microsoft.com/en-us/training/paths/create-custom-copilots-ai-studio/) and provides practical, hands-on experience with:

- Microsoft Foundry agent development
- Azure AI services integration  
- MLOps and GenAI Ops best practices
- Production deployment patterns

## Reporting issues

If you encounter problems with the exercises or infrastructure, please create an **issue** in this repository with:

- Clear description of the problem
- Steps to reproduce
- Environment details (Azure region, subscription type, etc.)
- Relevant logs or error messages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
