from fastapi import FastAPI, Request

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
    level = payload.get("level")
    error_message = payload.get("error_message")
    timestamp = payload.get("timestamp")

    print("========== PIPELINE ALERT ==========")
    print(f"Region:        {region}")
    print(f"Team ID:       {team_id}")
    print(f"Integration:   {integration_id}")
    print(f"Source:         {source_type}")
    print(f"Level:         {level}")
    print(f"Error:          {error_message}")
    print(f"Timestamp:      {timestamp}")
    print("====================================")

    return {
        "status": "received"
    }