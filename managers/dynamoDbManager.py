#imports
import logging
import boto3
from botocore.exceptions import ClientError

def create(name):
    #access dynamoDb api
    db = boto3.client('dynamodb')

    try:
        #create table
        table = db.create_table(
            TableName=name,
            KeySchema=[
                {
                    'AttributeName': 'trackname',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'sentiment',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'trackname',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'sentiment',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        #wait for table to be created
        table.meta.client.get_waiter('table_exists').wait(TableName=name)

        print(name + "created successfully")
        return table

    except ClientError as e:
        logging.error(e)