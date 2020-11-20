import os
import json
import tweepy as tw
import kafka as kf
from pyspark.sql import functions as F
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
        data_to_dump = json.loads(data)
        with open('/home/n/opt/MindBender_BD/Task-013/data.json', 'w') as f:
            json.dump(data_to_dump, f)
        ## To send the data directly to Kafka consumer:
        #producer.send_messages(topic, data.encode('utf-8'))
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

## Read json from HDFS into Spark dataframe
df = spark.read.json('/spark/data.json', multiLine=True)

## Transform dataframe to have "id" and "text" aliased as "value", as Spark can only deal with stuff called "value"
## Then format and send to Kafka
df.select(F.to_json(F.struct("id", "text")).alias("value")).write \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9099") \
  .option("topic", topic) \
  .save()
####### Must be run with:
####### spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.2 ~/opt/MindBender_BD/Task-013/twitter_spark_dataframe.py

## Stop Spark session
spark.stop()
