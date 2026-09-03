import os
import json
import requests


CORALOGIX_API_URL = os.getenv("CORALOGIX_API_URL")
CORALOGIX_API_KEY = os.getenv("CORALOGIX_API_KEY")


def fetch_pipeline_warnings():

    query = """
    source logs
    | filter $d.error_message.contains('MySQL version 8.4')
    | choose $m.timestamp,
         $l.applicationname,
         $d.level,
         $d.team_id,
         $d.integration_id,
         $d.source_id,
         $d.source_type,
         $d.error_message
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

    if response.status_code != 200:
        raise Exception(
            f"Coralogix API error {response.status_code}: {response.text}"
        )

    response.raise_for_status()

    logs = []

    # Coralogix returns NDJSON
    for line in response.text.splitlines():

        if not line.strip():
            continue

        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        if "result" not in data:
            continue

        results = data["result"].get("results", [])

        for result in results:

            user_data = result.get("userData")

            if not user_data:
                continue

            try:
                log = json.loads(user_data)
            except json.JSONDecodeError:
                log = {
                    "raw": user_data
                }

            logs.append(log)

    return logs


# -----------------------------------
# Extract useful fields from each log
# -----------------------------------

def process_log(log):

    region = log.get("client")
    team_id = log.get("team_id")
    integration_id = log.get("integration_id")
    source_id = log.get("source_id")
    source_type = log.get("source_type")
    level = log.get("level")
    error_message = log.get("error_message")
    timestamp = log.get("timestamp")

    return {
        "region": region,
        "team_id": team_id,
        "integration_id": integration_id,
        "source_id": source_id,
        "source_type": source_type,
        "level": level,
        "error_message": error_message,
        "timestamp": timestamp
    }