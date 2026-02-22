---
lab:
    title: 'Prerequisites for GenAIOps Labs'
    description: 'Set up your development environment with the required tools and accounts to complete all labs in this course.'
    level: 100
    duration: 15 minutes
---

# Prerequisites for GenAIOps Labs

Before starting the labs in this course, ensure you have the following tools and accounts set up. This page provides links and instructions for installing everything you'll need.

## Required accounts

### Azure subscription

You need an Azure subscription with access to Microsoft Foundry and Azure OpenAI services.

- **Get a free Azure account**: [https://azure.microsoft.com/free/](https://azure.microsoft.com/free/)

> **Note**: Some Foundry resources are constrained by regional model quotas. If you encounter quota limits, you may need to deploy resources in a different region.

### GitHub account

All labs use GitHub for version control and collaboration.

- **Create a GitHub account**: [https://github.com/signup](https://github.com/signup)

## Required software

### Visual Studio Code

Visual Studio Code is the primary code editor used throughout all labs.

- **Download Visual Studio Code**: [https://code.visualstudio.com/download](https://code.visualstudio.com/download)
- **Installation guide**: [Setting up Visual Studio Code](https://code.visualstudio.com/docs/setup/setup-overview)

**Recommended extensions** (install after VS Code setup):
- **Python**: [Python extension for VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- **Azure Tools**: [Azure Tools extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)
- **GitHub**: [GitHub Pull Requests and Issues](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github)

### Python 3.9 or later

Python is used for all agent development and scripting in the labs.

- **Download Python**: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- **Installation guide**: [Python Installation Guide](https://wiki.python.org/moin/BeginnersGuide/Download)
- **Verify installation**:
  ```bash
  python --version
  # Should show Python 3.9 or later
  ```

> **Tip**: On macOS and Linux, you may need to use `python3` instead of `python`.

### Git

Git is required for version control and working with GitHub repositories.

- **Download Git**: [https://git-scm.com/downloads](https://git-scm.com/downloads)
- **Installation guide**: [Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- **Initial configuration**:
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
  ```
- **Git documentation**: [Git Handbook](https://guides.github.com/introduction/git-handbook/)

### Azure CLI

The Azure Command-Line Interface (CLI) is used to authenticate and interact with Azure services.

- **Download Azure CLI**: [https://learn.microsoft.com/cli/azure/install-azure-cli](https://learn.microsoft.com/cli/azure/install-azure-cli)
- **Installation guide**: [How to install the Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
- **Verify installation**:
  ```bash
  az --version
  # Should show Azure CLI version 2.50.0 or later
  ```

**Platform-specific installation**:
- **Windows**: [Install Azure CLI on Windows](https://learn.microsoft.com/cli/azure/install-azure-cli-windows)
- **macOS**: [Install Azure CLI on macOS](https://learn.microsoft.com/cli/azure/install-azure-cli-macos)
- **Linux**: [Install Azure CLI on Linux](https://learn.microsoft.com/cli/azure/install-azure-cli-linux)

### Azure Developer CLI (azd)

The Azure Developer CLI is used to provision Azure infrastructure and manage deployments.

- **Download Azure Developer CLI**: [https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- **Installation guide**: [Install or update Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/install-azd)
- **Verify installation**:
  ```bash
  azd version
  # Should show Azure Developer CLI version 1.5.0 or later
  ```

**Platform-specific installation**:
- **Windows**:
  ```powershell
  winget install microsoft.azd
  ```
- **macOS**:
  ```bash
  brew tap azure/azd && brew install azd
  ```
- **Linux**:
  ```bash
  curl -fsSL https://aka.ms/install-azd.sh | bash
  ```

## Verification checklist

Before starting the labs, verify all prerequisites are installed:

```bash
# Check Visual Studio Code
code --version

# Check Python
python --version

# Check Git
git --version

# Check Azure CLI
az --version

# Check Azure Developer CLI
azd version
```

All commands should return version numbers without errors.

## Authenticate with Azure

After installing the Azure CLI and Azure Developer CLI, authenticate with your Azure account:

```bash
# Authenticate Azure CLI
az login

# Authenticate Azure Developer CLI
azd auth login
```

Both commands will open a browser window for authentication. Sign in with your Azure credentials.

## Troubleshooting

### Common issues

**Python command not found**:
- Verify Python is in your system PATH
- Try using `python3` instead of `python`
- Reinstall Python and check "Add Python to PATH" option

**Azure CLI authentication fails**:
- Clear cached credentials: `az account clear`
- Try authenticating again: `az login`
- Check your internet connection and firewall settings

**azd command not recognized**:
- Restart your terminal after installation
- Verify installation with: `azd version`
- Check PATH environment variable includes azd installation directory

**Git authentication issues with GitHub**:
- Use SSH keys: [Generating a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- Or use Personal Access Token: [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

## Regional considerations

Some Microsoft Foundry services have regional availability constraints:

- **Recommended regions for these labs**: Sweden Central, East US, West Europe
- **Check model availability**: [Model availability by region](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)
- **Quota limits**: If you encounter quota issues, try deploying in a different region

## Next steps

Once all prerequisites are installed and verified:

1. Start with [Lab 01: Infrastructure Setup](01-infrastructure-setup.md)
2. Follow labs in sequence or jump to specific topics based on your learning path
3. Need help or have questions? The community is here to support you - create an issue in the [GitHub repository](https://github.com/MicrosoftLearning/mslearn-genaiops/issues)
