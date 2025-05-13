---
lab:
    title: 'Analyze and debug your generative AI app with tracing'
    description: 'Learn how to debug your generative AI application by tracing its workflow from user input to model response and post-processing.'
---

# Analyze and debug your generative AI app with tracing

This exercise takes approximately **30 minutes**.

> **Note**: This exercise assumes some familiarity with Azure AI Foundry, which is why some instructions are intentionally less detailed to encourage more active exploration and hands-on learning.

## Introduction

In this exercise, you’ll run a multi-step generative AI assistant that recommends hiking trips and suggests outdoor gear. You’ll use the Azure AI Inference SDK’s tracing features to analyze how your application executes and identify key decision points made by the model and surrounding logic.

You’ll interact with a deployed model to simulate a real user journey, trace each stage of the application from user input to model response to post-processing, and view the trace data in Azure AI Foundry. This will help you understand how tracing enhances observability, simplifies debugging, and supports performance optimization of generative AI applications.

## Set up the environment

To complete the tasks in this exercise, you need:

- An Azure AI Foundry hub,
- An Azure AI Foundry project,
- A deployed model (like GPT-4o),
- A connected Application Insights resource.

### Create an AI Foundry hub and project

To quickly setup a hub and project, simple instructions to use the Azure AI Foundry portal UI are provided below.

1. In a web browser, open the [Azure AI Foundry portal](https://ai.azure.com) at `https://ai.azure.com` and sign in using your Azure credentials.
1. In the home page, select **+ Create project**.
1. In the **Create a project** wizard, enter a valid name for your project and if an existing hub is suggested, choose the option to create a new one. Then review the Azure resources that will be automatically created to support your hub and project.
1. Select **Customize** and specify the following settings for your hub:
    - **Hub name**: *A valid name for your hub*
    - **Subscription**: *Your Azure subscription*
    - **Resource group**: *Create or select a resource group*
    - **Location**: Select **Help me choose** and then select **gpt-4o** in the Location helper window and use the recommended region\*
    - **Connect Azure AI Services or Azure OpenAI**: *Create a new AI Services resource*
    - **Connect Azure AI Search**: Skip connecting

    > \* Azure OpenAI resources are constrained by regional model quotas. In the event of a quota limit being exceeded later in the exercise, there's a possibility you may need to create another resource in a different region.

1. Select **Next** and review your configuration. Then select **Create** and wait for the process to complete.

### Deploy a model

To generate data that you can monitor, you first need to deploy a model and interact with it. In the instructions you're asked to deploy a GPT-4o model, but **you can use any model** from the Azure OpenAI Service collection that is available to you.

1. Use the menu on the left, in the **My assets**, select the **Models + endpoints** page.
1. In the **+ Deploy model** menu, select **Deploy base model**.
1. Select the **gpt-4o** model in the list and deploy it with the following settings by selecting **Customize** in the deployment details:
    - **Deployment name**: *A valid name for your model deployment*
    - **Deployment type**: Standard
    - **Automatic version update**: Enabled
    - **Model version**: *Select the most recent available version*
    - **Connected AI resource**: *Select your Azure OpenAI resource connection*
    - **Tokens per Minute Rate Limit (thousands)**: 5K
    - **Content filter**: DefaultV2
    - **Enable dynamic quota**: Disabled

    > **Note**: Reducing the TPM helps avoid over-using the quota available in the subscription you are using. 5,000 TPM should be sufficient for the data used in this exercise. If your available quota is lower than this, you will be able to complete the exercise but you may experience errors if the rate limit is exceeded.

1. Wait for the deployment to complete.

### Connect Application Insights

Connect Application Insights to your project in Azure AI Foundry to start collecting data for analysis.

1. Use the menu on the left, and select the **Tracing** page.
1. **Create a new** Application Insights resource to connect to your app.
1. Enter an Application Insights resource name and select **Create**.

Application Insights is now connected to your project, and data will begin to be collected for analysis.

## Run a generative AI app with the Cloud Shell

You'll connect to your Azure AI Foundry project from Azure Cloud Shell and programmatically interact with a deployed model as part of a generative AI application.

### Interact with a deployed model

Start by retrieving the necessary information to be authenticated to interact with your deployed model. Then, you'll access the Azure Cloud Shell and update the code of your generative AI app.

1. In the Azure AI Foundry portal, view the **Overview** page for your project.
1. In the **Project details** area, note the **Project connection string**.
1. **Save** the string in a notepad. You'll use this connection string to connect to your project in a client application.
1. Open a new browser tab (keeping the Azure AI Foundry portal open in the existing tab).
1. In the new tab, browse to the [Azure portal](https://portal.azure.com) at `https://portal.azure.com`; signing in with your Azure credentials if prompted.
1. Use the **[\>_]** button to the right of the search bar at the top of the page to create a new Cloud Shell in the Azure portal, selecting a ***PowerShell*** environment with no storage in your subscription.
1. In the Cloud Shell toolbar, in the **Settings** menu, select **Go to Classic version**.

    **<font color="red">Ensure you've switched to the Classic version of the Cloud Shell before continuing.</font>**

1. In the Cloud Shell pane, enter and run the following commands:

    ```
    rm -r mslearn-genaiops -f
    git clone https://github.com/microsoftlearning/mslearn-genaiops mslearn-genaiops
    ```

    This command clones the GitHub repository containing the code files for this exercise.

1. After the repo has been cloned, navigate to the folder containing the application code files:  

    ```
   cd mslearn-genaiops/Files/08
    ```

1. In the Cloud Shell command-line pane, enter the following command to install the libraries you need:

    ```
   python -m venv labenv
   ./labenv/bin/Activate.ps1
   pip install python-dotenv azure-identity azure-ai-projects azure-ai-inference azure-monitor-opentelemetry
    ```

1. Enter the following command to open the configuration file that has been provided:

    ```
   code .env
    ```

    The file is opened in a code editor.

1. In the code file:

    1. Replace the **your_project_connection_string** placeholder with the connection string for your project (copied from the project **Overview** page in the Azure AI Foundry portal).
    1. Replace the **your_model_deployment** placeholder with the name you assigned to your GPT-4o model deployment (by default `gpt-4o`).

1. *After* you've replaced the placeholders, in the code editor, use the **CTRL+S** command or **Right-click > Save** to **save your changes** and then use the **CTRL+Q** command or **Right-click > Quit** to close the code editor while keeping the cloud shell command line open.

### Update the code for your generative AI app

Now that your environment is set up and your .env file is configured, it's time to prepare your AI assistant script for execution. Next to connecting with an AI project and enabling Application Insights, you need to:

- Interact with your deployed model.
- Define the function to specify your prompt.
- Define the main flow that calls all functions.

You will add these three parts to a starting script.

1. Run the following command to **open the script** that has been provided:

    ```
   code start-prompt.py
    ```

    You'll see that several key lines have been left blank or marked with empty # Comments. Your task is to complete the script by copying and pasting the correct lines below into the appropriate locations.

1. In the script, locate **# Function to call the model and handle tracing**.
1. Below this comment, paste the following code:

    ```
   def call_model(system_prompt, user_prompt, span_name):
        with tracer.start_as_current_span(span_name) as span:
            span.set_attribute("session.id", SESSION_ID)
            span.set_attribute("prompt.user", user_prompt)
            start_time = time.time()
    
            response = chat_client.complete(
                model=model_name,
                messages=[SystemMessage(system_prompt), UserMessage(user_prompt)]
            )
    
            duration = time.time() - start_time
            output = response.choices[0].message.content
            span.set_attribute("response.time", duration)
            span.set_attribute("response.tokens", len(output.split()))
            return output
    ```

1. In the script, locate **# Function to recommend a hike based on user preferences**.
1. Below this comment, paste the following code:

    ```
   def recommend_hike(preferences):
        with tracer.start_as_current_span("recommend_hike") as span:
            prompt = f"""
            Recommend a named hiking trail based on the following user preferences.
            Provide only the name of the trail and a one-sentence summary.
            Preferences: {preferences}
            """
            response = call_model(
                "You are an expert hiking trail recommender.",
                prompt,
                "recommend_model_call"
            )
            span.set_attribute("hike_recommendation", response.strip())
            return response.strip()
    ```

1. In the script, locate **# ---- Main Flow ----**.
1. Below this comment, paste the following code:

    ```
   if __name__ == "__main__":
       with tracer.start_as_current_span("trail_guide_session") as session_span:
           session_span.set_attribute("session.id", SESSION_ID)
           print("\n--- Trail Guide AI Assistant ---")
           preferences = input("Tell me what kind of hike you're looking for (location, difficulty, scenery):\n> ")

           hike = recommend_hike(preferences)
           print(f"\n✅ Recommended Hike: {hike}")

           # Run profile function


           # Run match product function


           print(f"\n🔍 Trace ID available in Application Insights for session: {SESSION_ID}")
    ```

1. **Save the changes** you made in the script.
1. In the Cloud Shell command-line pane beneath the code editor, enter the following command to **run the script**:

    ```
   python start-prompt.py
    ```

1. Give some description of the kind of hike you're looking for, for example:

    ```
   A one-day hike in the mountains
    ```

    The model will generate a response, which will be captured with Application Insights. You can visualize the traces in the **Azure AI Foundry portal**.

> **Note**: It may take a few minutes for monitoring data to show in Azure Monitor.

## View traces data in the Azure AI Foundry portal

After running the script, you captured a trace of your AI application’s execution. Now you'll explore it using Application Insights in Azure AI Foundry.

> **Note:** Later, you'll run the code again, and view the traces in the Azure AI Foundry portal again. Let's first explore where to find the traces to visualize them.

### Navigate to the Azure AI Foundry portal

1. **Keep you Cloud Shell open!** You'll come back to this to update the code and run it again.
1. Navigate to the tab in your browser with the **Azure AI Foundry portal** open.
1. Use the menu on the left, select **Tracing**.
1. *If* no data is shown, **refresh** your view.
1. Select the trace **train_guide_session** to open a new window that shows more details.

### Review your trace

This view shows the trace for one full session of the Trail Guide AI Assistant.

- **Top-level span**: trail_guide_session
    This is the parent span. It represents the entire execution of your assistant from start to finish.

- **Nested child spans**:
    Each indented line represents a nested operation. You’ll find:

    - **recommend_hike** which captures your logic to decide on a hike.
    - **recommend_model_call** which is the span created by call_model() inside recommend_hike.
    - **chat gpt-4o** which is automatically instrumented by the Azure AI Inference SDK to show actual LLM interaction.

1. You can click on any span to view:

    1. Its duration.
    1. Its attributes like user prompt, tokens used, response time.
    1. Any errors or custom data attached with **span.set_attribute(...)**.

## Add more functions to your code

1. Navigate to the tab in your browser with the **Azure Portal** open.
1. Run the following command to **re-open the script:**

    ```
   code start-prompt.py
    ```

1. In the script, locate **# Function to generate a trip profile for the recommended hike**.
1. Below this comment, paste the following code:

    ```
   def generate_trip_profile(hike_name):
       with tracer.start_as_current_span("trip_profile_generation") as span:
           prompt = f"""
           Hike: {hike_name}
           Respond ONLY with a valid JSON object and nothing else.
           Do not include any intro text, commentary, or markdown formatting.
           Format: {{ "trailType": ..., "typicalWeather": ..., "recommendedGear": [ ... ] }}
           """
           response = call_model(
               "You are an AI assistant that returns structured hiking trip data in JSON format.",
               prompt,
               "trip_profile_model_call"
           )
           print("🔍 Raw model response:", response)
           try:
               profile = json.loads(response)
               span.set_attribute("profile.success", True)
               return profile
           except json.JSONDecodeError as e:
               print("❌ JSON decode error:", e)
               span.set_attribute("profile.success", False)
               return {}
    ```

1. In the script, locate **# Function to match recommended gear with products in the catalog**.
1. Below this comment, paste the following code:

    ```
   def match_products(recommended_gear):
       with tracer.start_as_current_span("product_matching") as span:
           matched = []
           for gear_item in recommended_gear:
               for product in mock_product_catalog:
                   if any(word in product.lower() for word in gear_item.lower().split()):
                       matched.append(product)
                       break
           span.set_attribute("matched.count", len(matched))
           return matched
    ```

1. In the script, locate **# Run profile function**.
1. Below and **aligned with** this comment, paste the following code:

    ```
           profile = generate_trip_profile(hike)
           if not profile:
               print("Failed to generate trip profile. Please check Application Insights for trace.")
               exit(1)

           print(f"\n📋 Trip Profile for {hike}:")
           print(json.dumps(profile, indent=2))
    ```

1. In the script, locate **# Run match product function**.
1. Below and **aligned with** this comment, paste the following code:

    ```
           matched = match_products(profile.get("recommendedGear", []))
           print("\n🛒 Recommended Products from Lakeshore Retail:")
           print("\n".join(matched))
    ```

1. **Save the changes** you made in the script.
1. In the Cloud Shell command-line pane beneath the code editor, enter the following command to **run the script**:

    ```
   python start-prompt.py
    ```

1. Give some description of the kind of hike you're looking for, for example:

    ```
   I want to go for a multi-day adventure along the beach
    ```

> **Note**: It may take a few minutes for monitoring data to show in Azure Monitor.

### View the new traces in the Azure AI Foundry portal

1. Navigate back to the Azure AI Foundry portal.
1. A new trace with the same name **trail_guide_session** should appear. Refresh your view if necesary.
1. Select the new trace to open the more detailed view.
1. Review the new nested child spans **trip_profile_generation** and **product_matching**.
1. Select **product_matching** and review the metadata that appears.

    In the product_matching function, you included **span.set_attribute("matched.count", len(matched))**. By setting the attribute with the key-value pair **matched.count** and the length of the variable matched, you added this information to the **product_matching** trace. You can find this key-value pair under **attributes** in the metadata.

## (OPTIONAL) Trace an error

If you have extra time, you can review how to use traces when you have an error. A script that is likely to throw an error is provided to you. Run it and review the traces.

This is an exercise designed to challenge you, which means instructions are intentionally less detailed.

1. In the Cloud Shell, open the **error-prompt.py** script. This script is located in the same directory as the **start-prompt.py** script. Review its content.
1. Run the **error-prompt.py** script. Provide an answer in the command-line when prompted.
1. *Hopefully*, the output message includes **Failed to generate trip profile. Please check Application Insights for trace.**.
1. Navigate to the trace for the **trip_profile_generation** and inspect why there was an error.

<br>
<details>
<summary><b>Get the answer on</b>: Why you may have experienced an error...</summary><br>
<p>If you inspect the LLM trace for the generate_trip_profile function, you'll notice that the assistant's response includes backticks and the word json to format the output as a code block.

While this is helpful for display, it causes issues in the code because the output is no longer valid JSON. This leads to a parsing error during further processing.

The error is likely caused by how the LLM is instructed to adhere to a specific format for its output. Including the instructions in the user prompt appears more effective than to put it in the system prompt.</p>
</details>

## Where to find other labs

You can explore additional labs and exercises in the [Azure AI Foundry Learning Portal](https://ai.azure.com) or refer to the course's **lab section** for other available activities.
