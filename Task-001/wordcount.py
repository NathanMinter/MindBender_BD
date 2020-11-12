import string

with open("Shakespeare.txt", "r") as f:
	words_all = f.read().replace("\n", "").lower()

for ch in string.punctuation:
	words_all = words_all.replace(ch, " ")

words_set = words_all.split(" ")

for x in words_set:
	n = words_all.count(x)
	print("{}: {}".format(x,n))u newuser