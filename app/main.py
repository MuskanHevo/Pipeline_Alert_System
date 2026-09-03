import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.coralogix import fetch_pipeline_warnings, process_log
from app.slack import send_slack_alert


processed_logs = set()


def get_log_id(log):
    return (
        log.get("timestamp"),
        log.get("team_id"),
        log.get("integration_id"),
        log.get("source_id"),
        log.get("error_message"),
    )


async def poll_coralogix():
    while True:
        try:
            logs = fetch_pipeline_warnings()

            print(f"Found {len(logs)} matching logs")

            for raw_log in logs:
                log = process_log(raw_log)

                log_id = get_log_id(log)

                if log_id in processed_logs:
                    print(f"Skipping duplicate log: {log_id}")
                    continue

                send_slack_alert(log)

                processed_logs.add(log_id)

                print(
                    f"Slack alert sent: "
                    f"region={log.get('region')}, "
                    f"team_id={log.get('team_id')}, "
                    f"integration_id={log.get('integration_id')}, "
                    f"source_id={log.get('source_id')}"
                )

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

@app.get("/test-slack")
def test_slack():
    test_log = {
        "region": "asia",
        "team_id": "3196",
        "integration_id": "18691",
        "source_id": "18855",
        "source_type": "AWS_RDS_MYSQL",
        "level": "WARN",
        "error_message": "TEST ALERT - Pipeline Alert System is working",
        "timestamp": "2026-09-03 11:04:10",
    }

    send_slack_alert(test_log)

    return {
        "status": "success",
        "message": "Test Slack alert sent",
    }