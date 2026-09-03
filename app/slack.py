import os
from slack_sdk import WebClient

slack_client = WebClient(
    token=os.getenv("SLACK_BOT_TOKEN")
)


def send_slack_alert(
        region,
        team_id,
        integration_id,
        source_type,
        error_message,
        timestamp
):

    message = (
        "🚨 *Pipeline Warning*\n\n"
        f"*Region:* `{region}`\n"
        f"*Team ID:* `{team_id}`\n"
        f"*Integration ID:* `{integration_id}`\n"
        f"*Source:* `{source_type}`\n\n"
        f"*Error:*\n{error_message}\n\n"
        f"*Time:* `{timestamp}`"
    )

    response = slack_client.chat_postMessage(
        channel=os.getenv("SLACK_CHANNEL_ID"),
        text=message
    )

    return response