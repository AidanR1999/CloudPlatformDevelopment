import json
import s3BucketManager
import sqsQueueManager
import dynamoDbManager

#get student ID from app secrets
file = open('appsecrets.json')
secrets = json.load(file)
studentId = secrets['studentId']

bucket = s3BucketManager.create("audio-bucket-" + studentId)
queue = sqsQueueManager.create("audio-queue-" + studentId)
table = dynamoDbManager.create("audio-table-" + studentId)