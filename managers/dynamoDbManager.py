#imports
import logging
import boto3
from botocore.exceptions import ClientError

def create(name):
    #access cloud formation api
    cf = boto3.client('cloudformation')

    #template url
    url = 'https://s3.us-west-2.amazonaws.com/cloudformation-templates-us-west-2/DynamoDB_Table.template'

    #create table using cloudformation template
    response = cf.create_stack(
        StackName=name,
        TemplateUrl=url,
        Parameters=[
            {
                'ParameterKey':'HashKeyElementName',
                'ParameterValue':'trackname'
            }
        ]
    )

    return response