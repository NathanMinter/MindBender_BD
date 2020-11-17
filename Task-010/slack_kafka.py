import os
import kafka as kf
import slack
from slack.errors import SlackApiError

"""
## 
class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages(topic, data.encode('utf-8'))
        print("Tweet Sent")
        return True
    def on_error(self, status):
        print(status)
"""

slack_api_token = ""

client = slack.WebClient(token=os.environ['slack_api_token'])

try:
    response = client.chat_postMessage(
        channel='#random',
        text="Hello world!")
    assert response["message"]["text"] == "Hello world!"
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")

## Set authorizations
#auth = tw.OAuthHandler(consumer_key, consumer_secret)

## Kafka stream listener (topic created in terminal)
topic = "slack"
kafka = kf.KafkaClient("localhost:9099")
producer = kf.SimpleProducer(kafka)
#listen = StdOutListener()

