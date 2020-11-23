import json
import slack
import kafka as kf
#import slack_bolt as slb

## Set access keys from Twitter Developer app info
with open('/home/n/opt/MindBender_BD/Misc/keys') as keys:
    slack_keys = json.load(keys)
    bot_access_token = slack_keys["slack"]["bot_access_token"]
    signing_secret = slack_keys["slack"]["signing_secret"]

## Set authorizations
#app = slb.App(token=bot_access_token, signing_secret=signing_secret)
client = slack.WebClient(token=bot_access_token)

## Start app (for real-time only)
#app.start(port=int(os.environ.get("PORT", 3000)))

## Setup kafka
kafka = kf.KafkaClient("localhost:9099")
producer = kf.SimpleProducer(kafka)

## Get message history from scrum-bot conversation/chat
## Pulled as dict
response = client.conversations_history(channel="C01FLQUGUE4")

## Send each message dict to kafka consumer
for m in response['messages']:
    producer.send_messages("slack", bytes(str(m), 'utf-8'))
