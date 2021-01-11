import os
import json
import tweepy as tw
import kafka as kf
from tweepy.streaming import StreamListener

## 
class StdOutListener(StreamListener):
    def on_data(self, data):
        producer.send_messages(topic, data.encode('utf-8'))
        print("Right Sent")
        return True
    def on_error(self, status):
        print(status)

## Set access keys from Twitter Developer app info
with open('/home/n/opt/MindBender_BD/Misc/keys') as keys:
    twitter_keys = json.load(keys)
    consumer_key = twitter_keys["twitter"]["consumer_key"]
    consumer_secret = twitter_keys["twitter"]["consumer_secret"]
    access_token = twitter_keys["twitter"]["access_token"]
    access_secret = twitter_keys["twitter"]["access_secret"]

## Set authorizations
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)

## Kafka stream listener (topic created in terminal)
topic = "RightTopic"
kafka = kf.KafkaClient("localhost:9093")
producer = kf.SimpleProducer(kafka)
listen = StdOutListener()
stream = tw.Stream(auth, listen)
stream.filter(track="python")
