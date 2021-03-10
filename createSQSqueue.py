#imports
import logging
import boto3
from botocore.exceptions import ClientError
import json

#get app secrets
file = open('appsecrets.json')
secrets = json.load(file)

#access SQS api
sqs = boto3.client('sqs')
queueName = 'audio-queue-' + secrets['studentId']

try:
    queue = sqs.create_queue(
        QueueName=queueName
    )
    print(queueName + ' created successfully')
except ClientError as e:
    #log error
    logging.error(e)