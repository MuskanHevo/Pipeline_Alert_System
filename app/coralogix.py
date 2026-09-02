import os
import requests


CORALOGIX_API_URL = os.getenv("CORALOGIX_API_URL")
CORALOGIX_API_KEY = os.getenv("CORALOGIX_API_KEY")


def fetch_pipeline_warnings():
    query = """
    source logs
    | filter level == 'WARN'
    | filter logger == 'io.hevo.connectors.connectors.ConnectorsTestJobListener'
    | filter message == 'Failed to connect to source with PERMANENT error'
    | filter now() - $m.timestamp < 5m
    | limit 100
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CORALOGIX_API_KEY}"
    }

    response = requests.post(
        CORALOGIX_API_URL,
        headers=headers,
        json={
            "query": query
        },
        timeout=30
    )

    response.raise_for_status()

    return response.text

#Coralogix logs
#Coralogix Alert
#Generic Webhook
#https://your-app.onrender.com/webhooks/coralogix
#FastAPI
#Extract:
#region
#team_id
#pipeline/source ID
#error_message
#Slack
