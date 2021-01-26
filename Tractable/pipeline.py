from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os

## Init Spark session
spark = SparkSession.builder.config('spark.driver.bindAddress','127.0.0.1').appName('TractablePipeline').getOrCreate()

## Import files
def import_file(file, subd=""):
    df = spark.read.format('csv').options(header = True).load("file:///home/n/opt/MindBender_BD/Tractable/starter/{}/{}".format(subd, file))
    return df

#import_file("customers.csv")

dfCustomers = spark.read.format('csv').options(header = True).load("file:///home/n/opt/MindBender_BD/Tractable/starter/customers.csv")
dfProducts = spark.read.format('csv').options(header = True).load("file:///home/n/opt/MindBender_BD/Tractable/starter/products.csv")

## on json
df = spark.read.format('json').load("file:///home/n/opt/MindBender_BD/Tractable/starter/transactions/")

## Explode
df = df.select('customer_id', F.explode('basket.product_id').alias('product_id'))


## Join the files
df = dfCustomers.join(df, on = 'customer_id', how = 'inner')
df = df.join(dfProducts.select('product_id', 'product_category'), on = 'product_id', how = 'inner')

## purchase_count
df2 = df.groupBy(['product_id', 'customer_id', 'loyalty_score', 'product_category']).count()
df2 = df2.withColumnRenamed('count', 'product_count')

df2.show()
