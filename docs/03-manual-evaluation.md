---
lab:
    title: 'Manual Evaluation Workflows'
    description: 'Create structured evaluation datasets, conduct quality assessments, and implement collaborative evaluation using GitHub workflows.'
---

## Orchestrate a RAG system

Retrieval-Augmented Generation (RAG) systems combine the power of large language models with efficient retrieval mechanisms to enhance the accuracy and relevance of generated responses. By leveraging LangChain for orchestration and Azure AI Foundry for AI capabilities, we can create a robust pipeline that retrieves relevant information from a dataset and generates coherent responses. In this exercise, you will go through the steps of setting up your environment, preprocessing data, creating embeddings, and building a index, ultimately enabling you to implement a RAG system effectively.

This exercise will take approximately **30** minutes.

## Scenario

Imagine you want to build an app that gives recommendations about hotels in London. In the app, you want an agent that can not only recommend hotels but answer questions that the users might have about them.

You've selected a GPT-4 model to provide generative answers. You now want to put together a RAG system that will provide grounding data to the model based on other users reviews, guiding the chat's behavior into giving personalized recommendations.

Let's start by deploying the necessary resources to build this application.

## Create an Azure AI hub and project

You can create an Azure AI hub and project manually through the Azure AI Foundry portal, as well as deploy the models used in the exercise. However, you can also automate this process through the use of a template application with [Azure Developer CLI (azd)](https://aka.ms/azd).

1. In a web browser, open [Azure portal](https://portal.azure.com) at `https://portal.azure.com` and sign in using your Azure credentials.

1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment. The cloud shell provides a command line interface in a pane at the bottom of the Azure portal. For more information about using the Azure Cloud Shell, see the [Azure Cloud Shell documentation](https://docs.microsoft.com/azure/cloud-shell/overview).

    > **Note**: If you have previously created a cloud shell that uses a *Bash* environment, switch it to ***PowerShell***.

1. In the Cloud Shell toolbar, in the **Settings** menu, select **Go to Classic version**.

    **<font color="red">Ensure you've switched to the Classic version of the Cloud Shell before continuing.</font>**

1. In the PowerShell pane, enter the following commands to clone this exercise's repo:

    ```powershell
   rm -r mslearn-genaiops -f
   git clone https://github.com/MicrosoftLearning/mslearn-genaiops
    ```

1. After the repo has been cloned, enter the following commands to initialize the Starter template. 
   
    ```powershell
   cd ./mslearn-genaiops/Starter
   azd init
    ```

1. Once prompted, give the new environment a name as it will be used as basis for giving unique names to all the provisioned resources.
        
1. Next, enter the following command to run the Starter template. It will provision an AI Hub with dependent resources, AI project, AI Services and an online endpoint. It will also deploy the models GPT-4 Turbo, GPT-4o, and GPT-4o mini.

    ```powershell
   azd up  
    ```

1. When prompted, choose which subscription you want to use and then choose one of the following locations for resource provision:
   - East US
   - East US 2
   - North Central US
   - South Central US
   - Sweden Central
   - West US
   - West US 3
    
1. Wait for the script to complete - this typically takes around 10 minutes, but in some cases may take longer.

    > **Note**: Azure OpenAI resources are constrained at the tenant level by regional quotas. The listed regions above include default quota for the model type(s) used in this exercise. Randomly choosing a region reduces the risk of a single region reaching its quota limit. In the event of a quota limit being reached, there's a possibility you may need to create another resource group in a different region. Learn more about [model availability per region](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=standard%2Cstandard-chat-completions#global-standard-model-availability)

    <details>
      <summary><b>Troubleshooting tip</b>: No quota available in a given region</summary>
        <p>If you receive a deployment error for any of the models due to no quota available in the region you chose, try running the following commands:</p>
        <ul>
          <pre><code>azd env set AZURE_ENV_NAME new_env_name
   azd env set AZURE_RESOURCE_GROUP new_rg_name
   azd env set AZURE_LOCATION new_location
   azd up</code></pre>
        Replacing <code>new_env_name</code>, <code>new_rg_name</code>, and <code>new_location</code> with new values. The new location must be one of the regions listed at the beginning of the exercise, e.g <code>eastus2</code>, <code>northcentralus</code>, etc.
        </ul>
    </details>

1. Once all resources have been provisioned, use the following commands to fetch the endpoint and access key to your AI Services resource. Note that you must replace `<rg-env_name>` and `<aoai-xxxxxxxxxx>` with the names of your resource group and AI Services resource. Both are printed in the deployment's output.

     ```powershell
    Get-AzCognitiveServicesAccount -ResourceGroupName <rg-env_name> -Name <aoai-xxxxxxxxxx> | Select-Object -Property endpoint
     ```

     ```powershell
    Get-AzCognitiveServicesAccountKey -ResourceGroupName <rg-env_name> -Name <aoai-xxxxxxxxxx> | Select-Object -Property Key1
     ```

1. Copy these values as they will be used later on.

## Set up your development environment in Cloud Shell

To quickly experiment and iterate, you'll use a set of Python scripts in Cloud Shell.

1. In the Cloud Shell command-line pane, enter the following command to navigate to the folder with the code files used in this exercise:

     ```powershell
    cd ~/mslearn-genaiops/Files/04/
     ```

1. Enter the following commands to activate a virtual environment and install the libraries you need:

    ```powershell
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install python-dotenv langchain-text-splitters langchain-community langchain-openai
    ```

1. Enter the following command to open the configuration file that has been provided:

    ```powershell
   code .env
    ```

    The file is opened in a code editor.

1. In the code file, replace the **your_azure_openai_service_endpoint** and **your_azure_openai_service_api_key** placeholders with the endpoint and key values you copied earlier.
1. *After* you've replaced the placeholders, in the code editor, use the **CTRL+S** command or **Right-click > Save** to save your changes and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

## Implement RAG

You'll now run a script that ingests and preprocesses data, creates embeddings, and builds a vector store and index, ultimately enabling you to implement a RAG system effectively.

1. Run the following command to **edit the script** that has been provided:

    ```powershell
   code RAG.py
    ```

1. In the script, locate **# Initialize the components that will be used from LangChain's suite of integrations**. Below this comment, paste the following code:

    ```python
   # Initialize the components that will be used from LangChain's suite of integrations
   llm = AzureChatOpenAI(azure_deployment=llm_name)
   embeddings = AzureOpenAIEmbeddings(azure_deployment=embeddings_name)
   vector_store = InMemoryVectorStore(embeddings)
    ```

1. Review the script and notice that it uses a .csv file with hotel reviews as grounding data. You can see the contents of this file by running the command `download app_hotel_reviews.csv` in the command-line pane and opening the file.
1. Next, locate **# Split the documents into chunks for embedding and vector storage**. Below this comment, paste the following code:

    ```python
   # Split the documents into chunks for embedding and vector storage
   text_splitter = RecursiveCharacterTextSplitter(
       chunk_size=200,
       chunk_overlap=20,
       add_start_index=True,
   )
   all_splits = text_splitter.split_documents(docs)
    
   print(f"Split documents into {len(all_splits)} sub-documents.")
    ```

    The code above will split a set of large documents into smaller chunks. This is important because many embedding models (like those used for semantic search or vector databases) have a token limit and perform better on shorter texts.

1. Next, locate **# Embed the contents of each text chunk and insert these embeddings into a vector store**. Below this comment, paste the following code:

    ```python
   # Embed the contents of each text chunk and insert these embeddings into a vector store
   document_ids = vector_store.add_documents(documents=all_splits)
    ```

1. Next, locate **# Retrieve relevant documents from the vector store based on user input**. Below this comment, paste the following code, observing proper identation:

    ```python
   # Retrieve relevant documents from the vector store based on user input
   retrieved_docs = vector_store.similarity_search(question, k=10)
   docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
    ```

    The code above searches the vector store for the documents most similar to the user's input question. The question is converted into a vector using the same embedding model used for the documents. The system then compares this vector to all stored vectors and retrieves the most similar ones.

1. Save your changes.
1. **Run the script** by entering the following command in the command-line:

    ```powershell
   python RAG.py
    ```

1. Once the application is running, you can start asking questions such as `Where can I stay in London?` and then follow up with more specific inquiries.

## Conclusion

In this exercise you built a typical RAG system with its main components. By using your own documents to inform a model's responses, you provide grounding data used by the LLM when it formulates a response. For an enterprise solution, that means that you can constrain generative AI to your enterprise content.

## Clean up

If you've finished exploring Azure AI Services, you should delete the resources you have created in this exercise to avoid incurring unnecessary Azure costs.

1. Return to the browser tab containing the Azure portal (or re-open the [Azure portal](https://portal.azure.com?azure-portal=true) in a new browser tab) and view the contents of the resource group where you deployed the resources used in this exercise.
1. On the toolbar, select **Delete resource group**.
1. Enter the resource group name and confirm that you want to delete it.
