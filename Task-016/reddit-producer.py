import praw
import json

## Set auth keys
with open('/home/n/opt/MindBender_BD/Misc/keys') as keys:
    reddit_keys = json.load(keys)
    client_id = reddit_keys["reddit_script"]["client_id"]
    client_secret = reddit_keys["reddit_script"]["client_secret"]
    password = reddit_keys["reddit_script"]["password"]
    user_agent = reddit_keys["reddit_script"]["user_agent"]
    username = reddit_keys["reddit_script"]["username"]

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password, user_agent=user_agent, username=username)

## Grab a submission (post) from reddit by it's ID (from the URL).
submission = reddit.submission(id="k3u81d")

## 
subreddit = reddit.subreddit("python")

for post in subreddit.hot():
    print(post.id)

## 
#for top_level_comment in submission.comments:
#    print(top_level_comment.body)


