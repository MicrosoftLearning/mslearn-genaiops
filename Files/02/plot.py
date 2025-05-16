import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
token = credential.get_token("https://management.azure.com/.default")
access_token = token.token

# Define the resource ID and the metric name
resource_id = "your_resource_id"
metric_name = "TokenTransaction"
model_deployment_names = ["gpt-4o", "gpt-4o-mini"]

# Calculate the timespan for the last 30 minutes
end_time = datetime.now()
start_time = end_time - timedelta(minutes=30) # Feel free to change timedelta to (hours=1), if necessary 
timespan = f"{start_time.isoformat()}Z/{end_time.isoformat()}Z"

# Create the filter condition for multiple model deployment names
filter_condition = " or ".join([f"ModelDeploymentName eq '{name}'" for name in model_deployment_names])

# Define the API endpoint with timespan and filter condition
url = f"https://management.azure.com{resource_id}/providers/microsoft.insights/metrics?api-version=2018-01-01&metricnames={metric_name}&timespan={timespan}&$filter={filter_condition}"

# Set the headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Make the request
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    data = response.json()

    # Extract time series data for each model deployment name
    time_series_data = {}
    for value in data['value']:
        for timeseries in value['timeseries']:
            model_name = timeseries['metadatavalues'][0]['value']
            if model_name not in time_series_data:
                time_series_data[model_name] = []
            for data_point in timeseries['data']:
                time_series_data[model_name].append((data_point['timeStamp'], data_point['total']))

    # Plot the metrics over the timespan for each model deployment name
    plt.figure(figsize=(12, 6))
    for model_name, series in time_series_data.items():
        timestamps, values = zip(*series)
        plt.plot(timestamps, values, label=model_name)

    plt.xlabel('Timestamp')
    plt.ylabel('Processed Inference Tokens')
    plt.title('Processed Inference Tokens Usage Over Time')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('imgs/plot.png')
else:
    print("Failed to retrieve metrics:", response.status_code, response.text)
