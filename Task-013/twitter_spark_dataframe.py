import os
import json
import tweepy as tw
import kafka as kf
from tweepy.streaming import StreamListener
from pyspark.sql import SparkSession
from subprocess import PIPE, Popen

## Setup Spark session
spark = SparkSession \
    .builder \
    .appName("twitter_dataframe") \
    .config("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse") \
    .getOrCreate()

## Function to ouput json to consumer and update in-console
class StdOutListener(StreamListener):
    def on_data(self, data):
        with open('/home/n/opt/MindBender_BD/Task-013/data.json', 'w') as f:
            json.dump(data, f)
        producer.send_messages(topic, data.encode('utf-8'))
        print("Tweet Sent")
        stream.disconnect()
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
topic = "tweets"
kafka = kf.KafkaClient("localhost:9099")
producer = kf.SimpleProducer(kafka)
listen = StdOutListener()
stream = tw.Stream(auth, listen)
stream.filter(track="bigdata")

## Push json dump to HDFS
put = Popen(["hdfs", "dfs", "-put", "-f", "/home/n/opt/MindBender_BD/Task-013/data.json", "/spark/data.json"], stdin=PIPE, bufsize=-1)
put.communicate()

df = spark.read.json('/spark/data.json')
df.show()
#producer.send_messages(topic, df.show())

## Stop Spark session
spark.stop()
