#imports
import json
import time
import managers.s3BucketManager as _s3BucketManager
import managers.sqsQueueManager as _sqsQueueManager
import managers.dynamoDbManager as _dynamoDbManager

#get student ID from app secrets
file = open('appsecrets.json')
secrets = json.load(file)
studentId = secrets['studentId']


#define resource names
bucketName = "audio-bucket-" + studentId
queueName = "audio-queue-" + studentId
tableName = "audio-table-" + studentId

#create resources required
bucket = _s3BucketManager.create(bucketName)
queue = _sqsQueueManager.create(queueName)
table = _dynamoDbManager.create(tableName)