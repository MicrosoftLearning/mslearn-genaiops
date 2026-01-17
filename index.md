---
title: GenAI Operations Exercises  
permalink: index.html
layout: home
---

# GenAI Operations (GenAIOps) Workload Labs

The following hands-on exercises provide practical experience with GenAI Operations patterns and practices. You'll learn to deploy infrastructure, manage prompts, implement evaluation workflows, and monitor production GenAI applications using Microsoft Foundry and Azure services.

> **Note**: To complete the exercises, you'll need an Azure subscription with sufficient permissions and quota to provision Azure AI services and deploy Microsoft Foundry workspaces. If you don't have an Azure subscription, you can sign up for an [Azure account](https://azure.microsoft.com/free) with free credits for new users.

## Quickstart exercises

{% assign labs = site.pages | where_exp:"page", "page.url contains '/docs'" %}
{% for activity in labs  %}
<hr>
### [{{ activity.lab.title }}]({{ site.github.url }}{{ activity.url }})

{{activity.lab.description}}

{% endfor %}

> **Note**: While you can complete these exercises on their own, they're designed to complement modules on [Microsoft Learn](https://learn.microsoft.com/training/paths/operationalize-gen-ai-apps/); in which you'll find a deeper dive into some of the underlying concepts on which these exercises are based.
