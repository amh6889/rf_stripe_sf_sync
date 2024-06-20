from slack_sdk import WebClient
from dotenv import load_dotenv
import os

load_dotenv()

def send_message(message):
    slack_channel = os.getenv('SLACK_CHANNEL_ID')
    slack_token = os.getenv('SLACK_TOKEN')
    client = WebClient(token=slack_token)
    client.chat_postMessage(
        channel=slack_channel,
        text=message,
        username="Bot User"
    )
