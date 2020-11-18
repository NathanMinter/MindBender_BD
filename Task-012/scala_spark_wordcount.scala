import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

def main(args: Array[String]) {
        // Create Spark context
        val sc = new SparkContext(new SparkConf().setAppName("ShakespeareScalaCount"))

        // Read text file and split into words
        val tokenized = sc.textFile("/home/n/opt/MindBender_BD/Task-012/Shakespeare.txt").flatMap(_.split(" "))

        // Count the occurrence of each word
        val wordCounts = tokenized.map((_, 1)).reduceByKey(_ + _)

        System.out.println(wordCounts.collect().mkString(", "))
}
