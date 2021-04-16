from slack import WebClient
from coinbot import CoinBot
import os

# Create a slack client
slack_web_client = WebClient("xoxb-1972424183652-1966294418434-yIMpffxnlNcFbY7khg1gZfzI")

# Get a new CoinBot
coin_bot = CoinBot("#général")

# Get the onboarding message payload
message = coin_bot.get_message_payload()

# Post the onboarding message in Slack
slack_web_client.chat_postMessage(**message)