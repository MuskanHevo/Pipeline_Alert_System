import os
import json
import requests

CORALOGIX_API_URL = os.getenv("CORALOGIX_API_URL")
CORALOGIX_API_KEY = os.getenv("CORALOGIX_API_KEY")


def fetch_pipeline_warnings():

    query = """
    source logs
    | filter $d.error_message.contains('MySQL version 8.4')
    | limit 100
    """

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

    if response.status_code != 200:
        raise Exception(
            f"Coralogix API error {response.status_code}: {response.text}"
        )

    logs = []

    for line in response.text.splitlines():

        if not line.strip():
            continue

        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Only process the result line
        if "result" not in data:
            continue

        results = data["result"].get("results", [])

        for result in results:

            # -------------------------
            # Parse userData
            # -------------------------
            user_data = result.get("userData")

            if not user_data:
                continue

            try:
                log = json.loads(user_data)
            except json.JSONDecodeError:
                continue

            # -------------------------
            # Parse labels
            # -------------------------
            labels = {}

            for label in result.get("labels", []):
                key = label.get("key")
                value = label.get("value")

                if key:
                    labels[key] = value

            # -------------------------
            # Add region
            # -------------------------
            log["region"] = labels.get("applicationname")

            logs.append(log)

    return logs


def process_log(log):

    return {
        "region": log.get("region"),
        "team_id": log.get("team_id"),
        "integration_id": log.get("integration_id"),
        "source_id": log.get("source_id"),
        "source_type": log.get("source_type"),
        "level": log.get("level"),
        "error_message": log.get("error_message"),
        "timestamp": log.get("timestamp")
    }