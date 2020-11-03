import scala.io.Source
import java.io.File
import java.io.PrintWriter
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.FileSystem
import org.apache.hadoop.fs.Path

def wordCount (substr: String): Int =
  wordsAll.sliding(substr.length).count(window => window == substr)

def main(args: Array[String]) {
  val wordsAll = Source.fromFile("Shakespeare.txt").getLines.mkString.replace("\n", "").replaceAll("""[\p{Punct}]""", " ").toLowerCase()

  val wordsSet: Set[String] = wordsAll.split(" ").toSet

  val writer = new PrintWriter(new File("shakespeareMR.txt", false))

  for (x <- wordsSet) {
    var n = wordCount(x)
    writer.write(s"$x: $n\n")
  }

  writer.close()

  val hadoopConf = new Configuration()
  val hdfs = FileSystem.get(hadoopConf)

  val srcPath = new Path("shakespeareMR.txt")
  val destPath = new Path("/shakespeare/shakespeareMR.txt")

  hdfs.copyFromLocalFile(srcPath, destPath)
}

// Error: Could not find or load main class scala.tools.nsc.MainGenericRunner
// It was working, then the laptop died and now it's not working.
