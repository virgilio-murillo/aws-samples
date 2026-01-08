from strands import Agent, tool
from strands_tools import calculator # Import the calculator tool
import argparse
import json
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands.models import BedrockModel
import boto3

app = BedrockAgentCoreApp()

# Create a custom tool 
@tool
def list_running_ec2_instances():
    """List running EC2 instances in us-east-1"""
    ec2 = boto3.client("ec2", region_name="us-east-1")
    response = ec2.describe_instances(Filters=[{"Name": "instance-state-name", "Values": ["running"]}])
    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append(instance["InstanceId"])
    return f"Running EC2 instances: {', '.join(instances)}" if instances else "No running instances found."

@tool
def query_config_aggregator(expression: str, aggregator_name: str = "TestName"):
    """Run a custom AWS Config aggregator query using select_aggregate_resource_config"""
    client = boto3.client("config", region_name="us-east-1")
    try:
        response = client.select_aggregate_resource_config(
            ConfigurationAggregatorName=aggregator_name,
            Expression=expression
        )
        results = response.get("Results", [])
        return f"Query returned {len(results)} results:\n" + "\n".join(results)
    except Exception as e:
        return f"Error running Config query: {str(e)}"

@tool
def list_config_resources(resource_type: str, aggregator_name: str = "TestName"):
    """List discovered resources of a given type using AWS Config aggregator"""
    client = boto3.client("config", region_name="us-east-1")
    try:
        response = client.list_aggregate_discovered_resources(
            ConfigurationAggregatorName=aggregator_name,
            ResourceType=resource_type
        )
        resources = response.get("ResourceIdentifiers", [])
        return f"Found {len(resources)} resources of type {resource_type}:\n" + "\n".join([r["ResourceId"] for r in resources])
    except Exception as e:
        return f"Error listing resources: {str(e)}"


model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
model = BedrockModel(
    model_id=model_id,
)
agent = Agent(
    model=model,
    tools=[calculator, list_config_resources, query_config_aggregator, list_running_ec2_instances],
    system_prompt="You are a helpful assistand that helps me with my AWS resources"
)

@app.entrypoint
def strands_agent_bedrock(payload):
    """
    Invoke the agent with a payload
    """
    user_input = payload.get("prompt")
    print("User input:", user_input)
    response = agent(user_input)
    return response.message['content'][0]['text']

if __name__ == "__main__":
    app.run()
