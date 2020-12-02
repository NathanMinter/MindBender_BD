//import org.apache.spark.sql_
import org.apache.spark.sql.SparkSession
import scala.util.parsing.json_

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

//	  val content = rawDF.map(x => readLogs(x._1, x._2.toString))

      val query = rawDF
      	.writeStream
		.format("csv")
      	.outputMode("update")
      	.format("console")
      	.start()
      
      query.awaitTermination()

  }

}