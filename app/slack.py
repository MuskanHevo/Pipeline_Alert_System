import os
from slack_sdk import WebClient

slack_client = WebClient(
    token=os.getenv("SLACK_BOT_TOKEN")
)


def send_slack_alert(log):

    region = log.get("region")
    team_id = log.get("team_id")
    integration_id = log.get("integration_id")
    source_id = log.get("source_id")
    source_type = log.get("source_type")
    error_message = log.get("error_message")
    timestamp = log.get("timestamp")

    message = (
        "🚨 *Pipeline/Source Warning Detected*\n\n"
        f"*Region:* `{region}`\n"
        f"*Team ID:* `{team_id}`\n"
        f"*Integration ID:* `{integration_id}`\n"
        f"*Source ID:* `{source_id}`\n"
        f"*Source Type:* `{source_type}`\n\n"
        f"*Error:*\n{error_message}\n\n"
        f"*Time:* `{timestamp}`"
    )

    response = slack_client.chat_postMessage(
        channel=os.getenv("SLACK_CHANNEL_ID"),
        text=message
    )

    return response