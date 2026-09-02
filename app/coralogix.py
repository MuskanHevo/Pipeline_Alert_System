import os
import requests


CORALOGIX_API_URL = os.getenv("CORALOGIX_API_URL")
CORALOGIX_API_KEY = os.getenv("CORALOGIX_API_KEY")



def fetch_pipeline_warnings():

    query = "source logs | limit 10"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CORALOGIX_API_KEY}"
    }

    response = requests.post(
        CORALOGIX_API_URL,
        headers=headers,
        json={"query": query},
        timeout=30
    )

    print("========== CORALOGIX ==========")
    print("Status:", response.status_code)
    print("Response:", response.text)
    print("================================")

    return {
        "status_code": response.status_code,
        "response": response.text
    }

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
