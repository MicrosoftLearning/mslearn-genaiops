"""Verify that traces from run_monitoring.py reached Application Insights.

Queries Log Analytics directly to confirm spans are being exported,
bypassing the Azure AI Foundry portal which has a ~5-10 minute display lag.

Usage:
    python src/tests/check_traces.py
"""
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryStatus
from azure.mgmt.applicationinsights import ApplicationInsightsManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.ai.projects import AIProjectClient
from datetime import timedelta

load_dotenv()

credential = DefaultAzureCredential()

# Resolve the Application Insights connection string from the Foundry project
project_endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
project_client = AIProjectClient(endpoint=project_endpoint, credential=credential)
connection_string = project_client.telemetry.get_application_insights_connection_string()

if not connection_string:
    print("ERROR: No Application Insights connection string found.")
    print("Ensure Application Insights is linked to your AI Foundry project.")
    raise SystemExit(1)

# Extract the InstrumentationKey from the connection string
instrumentation_key = next(
    part.split("=", 1)[1]
    for part in connection_string.split(";")
    if part.startswith("InstrumentationKey")
)
print(f"Application Insights key: {instrumentation_key}")

# Resolve Log Analytics workspace customer ID (required by LogsQueryClient)
print("Resolving Log Analytics workspace...")
sub_client = SubscriptionClient(credential)
subscription_id = next(sub_client.subscriptions.list()).subscription_id

ai_mgmt = ApplicationInsightsManagementClient(credential, subscription_id)
workspace_resource_id = None
for component in ai_mgmt.components.list():
    if instrumentation_key in (component.instrumentation_key or ""):
        workspace_resource_id = component.workspace_resource_id
        break

if not workspace_resource_id:
    print("ERROR: Could not find a matching Application Insights component in your subscription.")
    raise SystemExit(1)

resource_group = workspace_resource_id.split("/")[4]
workspace_name = workspace_resource_id.split("/")[-1]

la_client = LogAnalyticsManagementClient(credential, subscription_id)
workspace = la_client.workspaces.get(resource_group, workspace_name)
workspace_id = workspace.customer_id
print(f"Workspace ID: {workspace_id}\n")

# A single run_monitoring.py execution produces one trace per prompt version.
# Each trace contains a root span (trail_guide_v{n}), test child spans
# (v{n}_{test-name}), and auto-instrumented OpenAI spans (chat gpt-4.1).
#
# Id / ParentId / OperationId are used to reconstruct the tree.
# Custom attributes (prompt.version, response.* tokens) live in Properties.
#
# Note: the query filters to the latest run to avoid mixing multiple executions.
query = """
let latest_root_time = toscalar(
    AppDependencies
    | where TimeGenerated > ago(6h)
    | where Name startswith "trail_guide_"
    | top 1 by TimeGenerated desc
    | project TimeGenerated
);
let ops_in_latest_run = AppDependencies
    | where TimeGenerated between (latest_root_time - 15m .. latest_root_time + 2m)
    | where Name startswith "trail_guide_"
    | distinct OperationId;
AppDependencies
| where TimeGenerated > ago(6h)
| where OperationId in (ops_in_latest_run)
| summarize arg_max(TimeGenerated, *) by Id
| project
    Id,
    ParentId,
    OperationId,
    Name,
    DurationMs,
    Success,
    PromptVersion    = tostring(Properties["prompt.version"]),
    TestName         = tostring(Properties["test.name"]),
    TotalTokens      = tostring(Properties["response.total_tokens"]),
    PromptTokens     = tostring(Properties["response.prompt_tokens"]),
    CompletionTokens = tostring(Properties["response.completion_tokens"])
"""

print("Querying spans from the past 6 hours and building the tree for the latest run...\n")
logs_client = LogsQueryClient(credential)
result = logs_client.query_workspace(
    workspace_id=workspace_id,
    query=query,
    timespan=timedelta(hours=6),
)

if result.status != LogsQueryStatus.SUCCESS:
    print(f"Query error: {result.partial_error}")
    raise SystemExit(1)

rows = result.tables[0].rows
if not rows:
    print("No traces found yet — wait 2-3 more minutes and run again.")
    raise SystemExit(0)

# Build a lookup of span_id → span dict, and a children map
spans = {}
children = {}
for row in rows:
    span_id, parent_id, op_id, name, dur, ok, version, test_name, total, prompt, compl = row
    spans[span_id] = {
        "id": span_id,
        "parent": parent_id,
        "op": op_id,
        "name": name,
        "dur": dur,
        "ok": ok,
        "version": version or "",
        "test": test_name or "",
        "total": total or "",
        "prompt": prompt or "",
        "compl": compl or "",
    }
    children.setdefault(parent_id, []).append(span_id)

# Identify root spans (ParentId not in any span's Id)
all_ids = set(spans.keys())
roots = [s for s in spans.values() if s["parent"] not in all_ids]
# Sort roots by operation ID so versions appear in order
roots.sort(key=lambda s: s["op"])


def print_span(span_id, prefix="", is_last=True):
    """Recursively print a span and its children as an ASCII tree."""
    span = spans[span_id]
    connector = "└── " if is_last else "├── "
    name_str = span["name"]

    # Build inline annotation for test child spans
    details = ""
    if span["total"]:
        details = (
            f"  [{span['dur']}ms | "
            f"tokens: {span['total']} (↑{span['prompt']} ↓{span['compl']})]"
        )
    elif span["dur"]:
        details = f"  [{span['dur']}ms]"

    print(f"{prefix}{connector}{name_str}{details}")

    kids = sorted(children.get(span_id, []), key=lambda k: spans[k]["name"])
    child_prefix = prefix + ("    " if is_last else "│   ")
    for i, kid in enumerate(kids):
        print_span(kid, child_prefix, is_last=(i == len(kids) - 1))


# Print one tree per trace (operation)
seen_ops = []
for root in roots:
    if root["op"] in seen_ops:
        continue
    seen_ops.append(root["op"])
    print(f"Trace: {root['op']}")
    # Find all root spans for this operation
    op_roots = [s for s in roots if s["op"] == root["op"]]
    for i, r in enumerate(op_roots):
        print_span(r["id"], prefix="", is_last=(i == len(op_roots) - 1))
    print()

print(f"Total spans found: {len(spans)}")