---
lab:
    title: 'Compare language models from the model catalog'
---

## Compare language models from the model catalog

When you have defined your use case, you can use the model catalog to explore whether an AI model solves your problem. You can use the model catalog to select models to deploy, which you can then compare to explore which model best meets your needs.

In this exercise, you compare two language models through the model catalog in Azure AI Foundry portal.

This exercise will take approximately **25** minutes.

## Scenario

Imagine you want to build an app to help students learn how to code in Python. In the app, you want an automated tutor that can help students write and evaluate code. In one exercise, students need to come up with the necessary Python code to plot a pie chart, based on the following example image:

![Pie chart showing marks obtained in an exam with sections for maths (34.9%), physics (28.6%), chemistry (20.6%), and English (15.9%)](./images/demo.png)

You need to select a language model that accepts images as input, and is able to generate accurate code.

Let's start by selecting a model from the Azure AI Foundry model catalog, based on the necessary characteristics.

## Create an Azure AI hub and project

You can access the model catalog without having a hub and project. However, since you know you also want to deploy models to evaluate their precision and performance, you need a project, so let's create one.

1. In a web browser, open [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials.

1. In the home page, select **+ Create project**. In the **Create a project** wizard you can see all the Azure resources that will be automatically created with your project, or you can customize the following settings by selecting **Customize** before selecting **Create**:

    - **Hub name**: *A unique name*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *A new resource group*
    - **Location**: Select **Help me choose** and then select **gpt-4o** in the Location helper window and use the recommended region\*
    - **Connect Azure AI Services or Azure OpenAI**: (New) *Autofills with your selected hub name*
    - **Connect Azure AI Search**: Skip connecting

    > \* Azure OpenAI resources are constrained at the tenant level by regional quotas. The listed regions in the location helper include default quota for the model type(s) used in this exercise. Randomly choosing a region reduces the risk of a single region reaching its quota limit. In the event of a quota limit being reached later in the exercise, there's a possibility you may need to create another resource in a different region. Learn more about [model availability per region](https://learn.microsoft.com/azure/ai-services/openai/concepts/models#gpt-35-turbo-model-availability)

1. If you selected **Customize**, select **Next** and review your configuration.
1. Select **Create** and wait for the process to complete.

## Select the model

You know that the model you select needs to accept images as input. You also want to start with a model whose inference infrastructure is fully managed by Azure. So, you opt for the Azure OpenAI model GPT-4o.

1. Navigate to the **Model catalog** page using the menu on the left.
1. Add a filter to only show models from the **Collections**: **Azure OpenAI**.
1. Add another filter to only show models with **Inference tasks**: **Chat completion**.
1. Search for `gpt-4o` and review the results.

    You notice that you can use the gpt-4o model, or the gpt-4o-mini model. Let's compare them based on benchmarks to explore their differences.

1. Select **Compare models** (find the button next to the filters in the search pane).
1. Remove the selected models.
1. One by one, add the two models you want to compare: **gpt-4o** and **gpt-4o-mini**.
1. Change the x-axis to **Accuracy**.
1. Ensure the y-axis is set to **Cost**.

Review the plot and try to answer the following questions:

- *Which model is more accurate?*
- *Which model is cheaper to use?*

The benchmark metric accuracy is calculated based on publicly available generic datasets. Before making a decision, let's explore the quality of outputs of the two models specific to our use case.

## Deploy two models to compare

To compare the precision and performance of two models, let's deploy the models through the Azure AI Foundry portal.

1. Navigate to the **Models + endpoints** page using the menu on the left.
1. Deploy a `gpt-4o` base model, with the default settings. Select **Customize** to ensure the **Tokens per Minute Rate Limit** is set to **10K**.
1. Deploy a `gpt-4o-mini` base model. Similarly, ensure the **Tokens per Minute Rate Limit** is set to **50K**.

Now that the models are deployed, you can interact with them through the **Chat playground** to evaluate their responses.

## Filter for precision

In your use case, you want the model to provide accurate responses when a student asks for a code sample. As a test, let's take the image of a pie chart and ask each model to write code to create the image.

1. Download the pie chart image from the following URL, and store it locally: [https://github.com/MicrosoftLearning/mslearn-genaiops/blob/main/Instructions/images/demo.png](https://raw.githubusercontent.com/MicrosoftLearning/mslearn-genaiops/refs/heads/main/Instructions/images/demo.png)
1. Navigate to the **Playground** page using the menu on the left. And open the **Chat playground**.
1. In the setup pane, select the **gpt-4o** model for deployment.
1. Attach the **demo.png** image and add the prompt: `Please create Python code for image`
1. To easily compare, open the portal in another tab: [ai.azure.com](ai.azure.com).
1. In the newly opened tab, navigate to the playground and make sure the chat is empty. Use the sweeping broom icon to clear the chat if needed.
1. Use the exact same prompt with the deployed **gpt-4o-mini** model.

You now have two code snippets that a student could use to generate a pie chart. Review the code and try to answer the following questions:

- *How do the two code snippets differ?*
- *Which output would you prefer as a student?*

**Optionally**, you can run the code and explore how the output differs.

## Filter for performance

Now that you have tested both models, you can explore their metrics to evaluate their performance.

1. Navigate to **Models + endpoints**.
1. Select a model, and navigate to the **Metrics** tab.
1. Select the **Last day** filter to get a better view on the tokens usage and requests per minute.
1. Repeat these steps for the other model.

The resulting views allow you to compare the token usage per model. Try to answer the following questions:

- *Which model had a higher token usage?*
- *Why did this model have a higher token usage?*

**Optionally**, you can get a more detailed view if you select **Open in Azure Monitor**. In the Azure portal, you can also explore the costs for each resource.

## Clean up

If you've finished exploring Azure AI Foundry portal, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Return to the browser tab containing the Azure portal (or re-open the [Azure portal](https://portal.azure.com?azure-portal=true) in a new browser tab) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
