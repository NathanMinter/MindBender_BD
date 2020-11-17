import os
import json
import time
import re
import kafka as kf
import slack
import requests
from slack import RTMClient
from slack.errors import SlackApiError

## Set auth tokens
with open('/home/n/opt/MindBender_BD/Misc/keys') as keys:
    slack_keys = json.load(keys)
    bot_access_token = slack_keys["slack"]["bot_access_token"]
    signing_secret = slack_keys["slack"]["signing_secret"]

## Initialise authentications
client = slack.WebClient(token=bot_access_token)

@RTMClient.run_on(event="message")
def amusebot(**payload):
    ## This function triggers when someone sends a message on the slack
    data = payload["data"]
    web_client = payload["web_client"]
    bot_id = data.get("bot_id", "")

    # If a message is not sent by the bot
    if bot_id == "":
        channel_id = data["channel"]

        # Extracting message sent by the user on the slack
        text = data.get("text", "")
        text = text.split(">")[-1].strip()

        response = ""
        if "help" in text.lower():
            user = data.get("user", "")
            response = f"Hi <@{user}>! I am AmuseBot :)"
        else:
            activity_json_response = requests.get("http://www.boredapi.com/api/activity/").json()
            activity = activity_json_response['activity']
            response = str(activity)
        
        # Sending message back to slack
        web_client.chat_postMessage(channel=channel_id, text=response)

try:
    rtm_client = RTMClient(token=bot_access_token)
    print("Bot is up and running!")
    rtm_client.start()
except Exception as err:
    print(err)


"""
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

"""
## Kafka stream listener (topic created in terminal)
topic = "slack"
kafka = kf.KafkaClient("localhost:9099")
producer = kf.SimpleProducer(kafka)
#listen = StdOutListener()
"""



x = requests.get("https://app.slack.com/client/T01EX004L10/C01FLQUGUE4")
print(x)
