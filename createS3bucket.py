#imports
import logging
import boto3
from botocore.exceptions import ClientError
import json

#get app secrets
file = open('appsecrets.json')
secrets = json.load(file)

#access S3 api
s3 = boto3.client('s3')

#create bucket
bucketName = 'audio-bucket-' + secrets['studentId']
try:
    bucket = s3.create_bucket(
        Bucket=bucketName,
        CreateBucketConfiguration={
            'LocationConstraint': 'eu-west-2'
            }
        )
    print(bucketName + ' created successfully')
except ClientError as e:
    #log error
    logging.error(e)