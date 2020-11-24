import json
import ast
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession

## Create sessions & contexts
sc = SparkContext("local[*]", "slackScrumBot")
ssc = StreamingContext(sc, 3)
ss = SparkSession.builder.appName(sc.appName).config("spark.sql.warehouse.dir", "/user/hive/warehouse").config("hive.metastore.urls", "thrift://localhost:9083").enableHiveSupport().getOrCreate()

## Set Kafka stream
kafkaStream = KafkaUtils.createStream(ssc, "localhost:2181", "slack", {"slack": 1})

## Parse messages
unparsed = kafkaStream.map(lambda x: ast.literal_eval(x[1]))
parsed = unparsed.map(lambda x: (x.get('user'), x.get('text')))

## Custom function to process parsed messages
def process(rdd):
    if not rdd.isEmpty():
        global ss
        df = ss.createDataFrame(rdd, schema=["user", "text"])
        df.show()
        df.write.saveAsTable(name="slack_db.slack_tbl", format="hive", mode="append")

## Write parsed messages to Hive
parsed.foreachRDD(process)

ssc.start()

ssc.awaitTermination()
