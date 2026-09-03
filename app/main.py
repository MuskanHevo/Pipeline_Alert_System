import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.slack import send_slack_alert

from app.coralogix import fetch_pipeline_warnings, process_log

async def poll_coralogix():

    while True:

        try:
            logs = fetch_pipeline_warnings()

            print(f"Found {len(logs)} matching logs")

            # Process logs here

        except Exception as e:
            print(f"Polling error: {e}")

        await asyncio.sleep(60)


@asynccontextmanager
async def lifespan(app: FastAPI):

    task = asyncio.create_task(poll_coralogix())

    yield

    task.cancel()


app = FastAPI(lifespan=lifespan)


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

@app.post("/webhooks/coralogix")
async def coralogix_webhook(request: Request):
    payload = await request.json()

    print("\n========== CORALOGIX ALERT ==========")
    print(payload)
    print("=====================================\n")

    return {"status": "received"}

@app.get("/test-coralogix")
def test_coralogix():

    logs = fetch_pipeline_warnings()

    processed_logs = []

    for log in logs:
        processed_logs.append(process_log(log))

    return {
        "status": "success",
        "count": len(processed_logs),
        "logs": processed_logs
    }


#Slack Integration
@app.get("/test-alert")
def test_alert():

    from app.slack import send_slack_alert

    logs = fetch_pipeline_warnings()

    sent = 0

    for log in logs:

        region = log.get("client")
        team_id = log.get("team_id")
        integration_id = log.get("integration_id")
        source_type = log.get("source_type")
        error_message = log.get("error_message")
        timestamp = log.get("timestamp")

        send_slack_alert(
            region=region,
            team_id=team_id,
            integration_id=integration_id,
            source_type=source_type,
            error_message=error_message,
            timestamp=timestamp
        )

        sent += 1

    return {
        "status": "success",
        "logs_found": len(logs),
        "alerts_sent": sent
    }