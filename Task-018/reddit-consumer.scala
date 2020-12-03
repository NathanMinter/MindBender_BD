import org.apache.spark.sql.SparkSession

object redditConsumer {

  def main(arg: Array[String]) {

    //Create SparkContext
    val ss = SparkSession
      	.builder
      	.appName("redditConsumer")
      	.master("local[*]")
      	.getOrCreate()

      import ss.implicits._

	  // Declare Kafka stream server and topic (subscribe)	
      val inputDF = ss
      	.readStream
      	.format("kafka")
      	.option("kafka.bootstrap.servers", "localhost:9099")
      	.option("subscribe", "reddit")
      	.load()

	  // Uses HQL to turn values from Kafka stream into STRING data type.
      val rawDF = inputDF.selectExpr("CAST(value AS STRING)").as[String]

      val query = rawDF
      	.writeStream
		.format("json")
      	.outputMode("update")
      	.format("console")
      	.start()
      
      query.awaitTermination()

  }

}