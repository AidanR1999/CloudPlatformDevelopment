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


def getUrl(name):
    #access SQS api
    sqs = boto3.client('sqs')

    #get queue url
    res = sqs.get_queue_url(QueueName=name)
    return res['QueueUrl']


def sendMessage(fileName, queueUrl):
    #access SQS api
    sqs = boto3.client('sqs')

    # Send message to SQS queue
    sqs.send_message(
        QueueUrl=queueUrl,
        MessageAttributes={
            'FileName': {
                'DataType': 'String',
                'StringValue': fileName
            }
        },
        MessageBody=(
            fileName
        )
    )

    print('message send')
