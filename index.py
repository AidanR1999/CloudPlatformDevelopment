import json
import managers.s3BucketManager as _s3BucketManager
import managers.sqsQueueManager as _sqsQueueManager
import managers.dynamoDbManager as _dynamoDbManager

#get student ID from app secrets
file = open('appsecrets.json')
secrets = json.load(file)
studentId = secrets['studentId']

bucket = _s3BucketManager.create("audio-bucket-" + studentId)
queue = _sqsQueueManager.create("audio-queue-" + studentId)
table = _dynamoDbManager.create("audio-table-" + studentId)