import json
import boto3
import os
from botocore.config import Config

## Set auth keys
with open('/home/n/opt/MindBender_BD/Misc/keys') as keys:
    s3_keys = json.load(keys)
    access_key = s3_keys["s3_python_test"]["access_key"]
    secret_access_key = s3_keys["s3_python_test"]["secret_access_key"]

s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

## Create new bucket
bucket_name = 'bucket-eit-nathan001'
location = {'LocationConstraint': 'us-east-2'}
s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

## Upload file to S3
s3.upload_file('/home/n/opt/MindBender_BD/Task-021/mock.csv', bucket_name, 'bigdata-eit02/mock.csv')
