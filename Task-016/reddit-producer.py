import praw
import json
import time
import os
import string
import kafka as kf

## Set auth keys
with open('/home/n/opt/MindBender_BD/Misc/keys') as keys:
    reddit_keys = json.load(keys)
    client_id = reddit_keys["reddit_script"]["client_id"]
    client_secret = reddit_keys["reddit_script"]["client_secret"]
    password = reddit_keys["reddit_script"]["password"]
    user_agent = reddit_keys["reddit_script"]["user_agent"]
    username = reddit_keys["reddit_script"]["username"]

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password, user_agent=user_agent, username=username)

## Choose a subreddit (as shown in the URL after /r/...). Alternatively, use "all" for the entirety of reddit.
subreddit = reddit.subreddit("python")

## Create file for storing titles of submissions per day.
timestr = time.strftime("%Y%m%d")
hot = f"/home/n/opt/MindBender_BD/reddit-pipeline/hot-{timestr}.txt"
keywords = f"/home/n/opt/MindBender_BD/reddit-pipeline/keywords-{timestr}.txt"
if os.path.exists(hot):
    os.remove(hot)
if os.path.exists(keywords):
    os.remove(keywords)

## Store the titles in reddits "hot" section, i.e. popular posts for the day, to file for a wordcount.
for post in subreddit.hot():
    with open(hot, "a") as f:
        f.write(post.title+"\n")

## Check top 10 most occurring words in file.
with open(hot, "r") as f:
    words_all = f.read().replace("\n", "").lower()

for ch in string.punctuation:
	words_all = words_all.replace(ch, " ")

words_set = words_all.split(" ")

words_dict = dict()

for x in words_set:
    ## Filter out blanks, single letters and simple sentence constructors (i.e. "a", "it", "I", "and", etc.)
    if len(x) > 3:
    	words_dict[x] = words_all.count(x)

with open(keywords, "a") as f:
    for word in sorted(words_dict, key=words_dict.get, reverse=True)[:10]:
        f.write(word+"\n")

## Send via Kafka broker
kafka = kf.KafkaClient("localhost:9099,localhost:9092,localhost:9093")
producer = kf.SimpleProducer(kafka)

## Send top 10 words to kafka consumer in JSON, formatted {date, word, freq}
for word in sorted(words_dict, key=words_dict.get, reverse=True)[:10]:
    json = '{"date": "'+timestr+'", "word":"'+word+'", "frequency": "'+str(words_dict[word])+'"}'
    producer.send_messages("reddit", bytes(json, 'utf-8'))





###### Additional potential PRAW usage ######
## Grab a submission (post) from reddit by it's ID (from the URL or submission.id).
#submission = reddit.submission(id="k3u81d")

## Print comments from that submission.
#for top_level_comment in submission.comments:
#    print(top_level_comment.body)
