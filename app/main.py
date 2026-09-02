from fastapi import FastAPI, Request

from app.slack import send_slack_alert

app = FastAPI()


@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "pipeline-alert-system"
    }


@app.post("/webhooks/coralogix")
async def coralogix_webhook(request: Request):
    payload = await request.json()

    region = payload.get("client")
    team_id = payload.get("team_id")
    integration_id = payload.get("integration_id")
    source_type = payload.get("source_type")
    error_message = payload.get("error_message")
    timestamp = payload.get("timestamp")

    send_slack_alert(
        region=region,
        team_id=team_id,
        integration_id=integration_id,
        source_type=source_type,
        error_message=error_message,
        timestamp=timestamp
    )

    return {
        "status": "received",
        "slack_alert": "sent"
    }

#POST /webhooks/coralogix
#Read incoming JSON
#Extract fields
#send_slack_alert()
#app/slack.py
#Slack API
#pipeline-alerts