#imports
import logging
import boto3
from botocore.exceptions import ClientError

def create(name):
    #access S3 api
    s3 = boto3.client('s3')

    try:
        bucket = s3.create_bucket(
            Bucket=name,
            CreateBucketConfiguration={
                'LocationConstraint': 'eu-west-2'
                }
            )
        print(name + ' created successfully')
        
        return bucket
    except ClientError as e:
        #log error
        logging.error(e)