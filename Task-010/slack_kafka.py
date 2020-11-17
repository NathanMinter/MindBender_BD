import os
import json
import time
import re
import kafka as kf
import slack
from slack.errors import SlackApiError

## Set auth tokens
with open('/home/n/opt/MindBender_BD/Misc/keys') as keys:
    slack_keys = json.load(keys)
    bot_access_token = slack_keys["slack"]["bot_access_token"]

client = slack.WebClient(token=bot_access_token)

## Post message with bot.
try:
    response = client.chat_postMessage(
        channel='#scrum-bot',
        text="Hello world!")
    assert response["message"]["text"] == "Hello world!"
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")

"""
## Kafka stream listener (topic created in terminal)
topic = "slack"
kafka = kf.KafkaClient("localhost:9099")
producer = kf.SimpleProducer(kafka)
#listen = StdOutListener()
"""
