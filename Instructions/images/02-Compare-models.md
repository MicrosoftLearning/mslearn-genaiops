---
lab:
    title: 'Compare models'
---



## Discover whether AI can solve your use case

Hugging Face model hub:

On the left there are characteristics to filter through the models.



Azure model catalog:

We have richer filters.

GitHub model catalog:

Which is a subset of the Azure AI model catalog and is powered by Azure. The GitHub model catalog offers Serverless API endpoints.

"I want to use an open-source model from Hugging Face."

1. Filter on models from Hugging Face.

"I want a model suitable for healthcare."

1. Filter for Industry: Health and Life Sciences.

"I want a model that can teach SQL."

1. Search for `sql` in the search bar.

"I want a biomed model."

1. Search for `biomed` in the search bar.

Get a sense of whether a model for the task exists.


## Translate output to the user's language

Use the T5 model which is designed for translation.

1. In the Hugging Face model catalog find the most downloaded model for translation: the google t5-small.
1. Test the translation.
1. Go to the GitHub market place and filter chat multilingual: cohere.
1. Test the translation.
1. In GitHub marketplace go into compare mode and compare two translations.
1. Go to the Azure AI model catalog.
1. Find the t5 model, and test it there.
1. Get the model card in Azure AI model catalog.
1. Find the model card in Hugging Face.
1. Deploy the model on Azure (t5 is a different deployment model), takes 10 minutes.

## Test with playground

Test the model with the playground.
1. Add model instructions in the system message.
1. Ask a relevant question.
1. Ask an irrelevant question.
1. Switch to another model and ask the same question. How does it differ?

Answers will be in a slightly different format.
Costs will be another factor to compare. Look at models+endpoints and navigate to metrics to find the amount of tokens/costs.

How do you evaluate?
Look at benchmarks, which can be criteria to look at initial selection.
How does the model rank on commonly used evaluation metrics?
Find the dataset of a specific benchmark. Find one most relevant for your task?

Hugging Face also offers big benchmark collection with leaderboards.
Look at Open LLM Leaderboard.
Find the best `opensloth` model to fine-tune model.

