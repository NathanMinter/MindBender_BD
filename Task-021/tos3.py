from snakebite.client import Client
import json
import boto3
import os

## Set auth keys
with open('/home/n/opt/MindBender_BD/Misc/keys') as keys:
    s3_keys = json.load(keys)
    access_key = s3_keys["s3_python_test"]["access_key"]
    secret_access_key = s3_keys["s3_python_test"]["secret_access_key"]

s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

## Connect to HDFS with Snakebite
client = Client('localhost', 9000)

## Move file locally (temporarily)
for f in client.copyToLocal(['/spark/data.json'], '/home/n/opt/MindBender_BD/Task-021/tmp'):
   print("Moved one file.")

## Upload temp file to S3
s3.upload_file('/home/n/opt/MindBender_BD/Task-021/tmp/data.json', 'mindbender0001', 'data.json')

## Delete tmp file
os.remove('/home/n/opt/MindBender_BD/Task-021/tmp/data.json')
