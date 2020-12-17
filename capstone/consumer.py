import json
import pandas as pd
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import StructType, StructField, StringType

## Create sessions & contexts
sc = SparkContext("local[*]", "capstone")
ssc = StreamingContext(sc, 3)
ss = SparkSession.builder.appName(sc.appName).config("spark.mongodb.input.uri", "mongodb://127.0.0.1/capstone_db.data.coll").config("spark.mongodb.output.uri", "mongodb://127.0.0.1/capstone_db.data.coll").getOrCreate()

## Set Kafka stream
kafkaStream = KafkaUtils.createStream(ssc, "localhost:2181", "capstone", {"capstone": 1})

## Parse messages
info = ['adult', 'budget', 'genres', 'id', 'original_language', 'popularity', 'production_companies', 'production_countries', 'release_date', 'revenue', 'runtime', 'spoken_languages', 'status', 'title', 'vote_average', 'vote_count']
unparsed = kafkaStream.map(lambda x: json.loads(x[1]))
parsed = unparsed.map(lambda x: (x.get('adult'), x.get('budget'), x.get('genres'), x.get('id'), x.get('original_language'), x.get('popularity'), x.get('production_companies'), x.get('production_countries'), x.get('release_date'), x.get('revenue'), x.get('runtime'), x.get('spoken_languages'), x.get('status'), x.get('title'), x.get('vote_average'), x.get('vote_count')))
fields = [StructField(a, StringType(), True) for a in info]
schema = StructType(fields)

## Custom function to process parsed messages
def process(rdd):
    if not rdd.isEmpty():
        global ss
        df = ss.createDataFrame(rdd, schema=schema)
        df.show()
        df.write.format("mongo").mode("append").option("database", "capstone_db").option("collection", "capstone_tbl").save()

## Write parsed messages to Hive
parsed.foreachRDD(process)

ssc.start()

ssc.awaitTermination()
