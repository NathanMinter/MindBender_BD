import json
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession

## Create sessions & contexts
sc = SparkContext("local[*]", "redditPipeline")
ssc = StreamingContext(sc, 3)
ss = SparkSession.builder.appName(sc.appName).config("spark.sql.warehouse.dir", "/user/hive/warehouse").config("hive.metastore.urls", "thrift://localhost:9083").enableHiveSupport().getOrCreate()

## Create Hive table
ss.sql("CREATE TABLE IF NOT EXISTS reddit_tbl (date STRING, word STRING, frequency STRING) USING hive")

## Set Kafka stream
kafkaStream = KafkaUtils.createStream(ssc, "localhost:2181", "reddit", {"reddit": 1})

## Parse messages
unparsed = kafkaStream.map(lambda x: json.loads(x[1]))
parsed = unparsed.map(lambda x: (x.get('date'), x.get('word'), x.get('frequency')))

## Custom function to process parsed messages
def process(rdd):
    if not rdd.isEmpty():
        global ss
        df = ss.createDataFrame(rdd, schema=["date", "word", "frequency"])
        df.show()
        df.write.saveAsTable(name="reddit_db.reddit_tbl", format="hive", mode="append")

## Write parsed messages to Hive
parsed.foreachRDD(process)

ssc.start()

ssc.awaitTermination()
