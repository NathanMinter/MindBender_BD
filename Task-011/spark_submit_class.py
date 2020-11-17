"""
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext("spark://local[*]", "ShakespeareStream")
ssc = StreamingContext(sc, 3)
lines = ssc.textFileStream('/home/n/opt/MindBender_BD/Python/Shakespeare')
counts = lines.flatMap(lambda line: line.split(" ")) \
    .map(lambda x: (x, 1)) \
    .reduceByKey(lambda a, b: a + b)
counts.pprint()

ssc.start()
ssc.awaitTermination()
"""

import sys
from pyspark import SparkContext, SparkConf

## Create Spark context
sc = SparkContext("local","Shakespeare")

## Read data from text file and split each line into words
words = sc.textFile("/home/n/opt/MindBender_BD/Task-011/Shakespeare.txt").flatMap(lambda line: line.split(" "))

## Count the occurrence of each word
wordcount = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a +b)

## Save to output
wordcount.saveAsTextFile("/home/n/opt/MindBender_BD/Task-011/")
