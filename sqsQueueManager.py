#imports
import logging
import boto3
from botocore.exceptions import ClientError

def create(name):
    #access SQS api
    sqs = boto3.client('sqs')

    try:
        queue = sqs.create_queue(
            QueueName=name
        )
        print(name + ' created successfully')
        return queue
    except ClientError as e:
        #log error
        logging.error(e)