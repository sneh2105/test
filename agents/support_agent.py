"""
Sample customer-support agent (LangChain-style) for testing AgentScan.
Intentionally combines a web-browsing tool with a secrets-manager tool
to see if AgentScan flags the exfiltration chain.
"""
from langchain.tools import tool
import boto3
import requests


@tool
def web_browser(url: str) -> str:
    """Fetch the contents of a web page to help answer customer questions."""
    resp = requests.get(url, timeout=10)
    return resp.text[:2000]


@tool
def aws_secrets_manager(secret_name: str) -> str:
    """Retrieve a secret value from AWS Secrets Manager for deployment automation."""
    client = boto3.client("secretsmanager")
    resp = client.get_secret_value(SecretId=secret_name)
    return resp["SecretString"]


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression."""
    return str(eval(expression))


TOOLS = [web_browser, aws_secrets_manager, calculator]
