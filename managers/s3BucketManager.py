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


def uploadFile(name, fileName, dir):
    try:
        #access api
        s3 = boto3.resource('s3')

        #open file
        file = open(dir + fileName, 'rb')

        #begin upload
        s3.Bucket(name).put_object(Key=fileName, Body=file)

        print(fileName + " uploaded")
        return True
    except ClientError as e:
        logging.error(e)
        return False
    