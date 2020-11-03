import string
import os
from subprocess import PIPE, Popen

with open("Shakespeare.txt", "r") as f:
	words_all = f.read().replace("\n", "").lower()

for ch in string.punctuation:
	words_all = words_all.replace(ch, " ")

words_set = words_all.split(" ")

t = open("shakespeareMR.txt","w+")

for x in words_set:
	n = words_all.count(x)
	t.write("{}: {}\n".format(x,n))

t.close()

hdfs_path = os.path.join(os.sep, "shakespeare", "shakespeareMR.txt")

put = Popen(["hdfs", "dfs", "-put", "-f", "shakespeareMR.txt", hdfs_path], stdin = PIPE, bufsize = -1)
put.communicate

## End the HDFS terminal screen?
