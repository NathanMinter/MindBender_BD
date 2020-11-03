import scala.io.Source

def wordCount (substr: String): Int =
  wordsAll.sliding(substr.length).count(window => window == substr)

def main(args: Array[String]) {
  val wordsAll = Source.fromFile("Shakespeare.txt").getLines.mkString.replace("\n", "").replaceAll("""[\p{Punct}]""", " ").toLowerCase()

  val wordsSet: Set[String] = wordsAll.split(" ").toSet

  for (x <- wordsSet) {
    var n = wordCount(x)
    println(s"$x: $n")
  }
}