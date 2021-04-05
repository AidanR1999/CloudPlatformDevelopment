#imports
import logging
import boto3
from botocore.exceptions import ClientError

#creates dynamoDb Table using Cloudformation template
#TAKES name : string
#RETURNS response : object
def create(name):
    #access cloud formation api
    cf = boto3.client('cloudformation')

    #template url
    url = 'https://s3.us-west-2.amazonaws.com/cloudformation-templates-us-west-2/DynamoDB_Table.template'

    try:
        #create table using cloudformation template
        response = cf.create_stack(
            StackName=name,
            TemplateURL=url,
            Parameters=[
                {
                    'ParameterKey':'HashKeyElementName',
                    'ParameterValue':'trackname'
                }
            ]
        )

        #print
        print(name + ' has been created successfully')
        return response

    #print error if stack already exists
    except Exception as e:
        print("Error: Stack already created")