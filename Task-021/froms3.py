import json
import boto3

## Set auth keys
with open('/home/n/opt/MindBender_BD/Misc/keys') as keys:
    s3_keys = json.load(keys)
    access_key = s3_keys["s3_python_test"]["access_key"]
    secret_access_key = s3_keys["s3_python_test"]["secret_access_key"]

s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

## Downloaf file from S3.
s3.download_file('mindbender0001', 'MOCK_DATA.csv', '/home/n/opt/MindBender_BD/Task-021/mock.csv')
