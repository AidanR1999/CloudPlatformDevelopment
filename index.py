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

#get queue url
queueUrl = _sqsQueueManager.getUrl(queueName)

#upload audio files
for i in range(5):
    fileName = "Audio" + str(i + 1) + ".mp3"
    
    #if(i != 0):
    #    time.sleep(30)
    
    success = _s3BucketManager.uploadFile(
        "audio-bucket-" + studentId,
        fileName,
        "./audioTracks/"
    )

    if(success):
        _sqsQueueManager.sendMessage(fileName, queueUrl)
    else:
        print("upload failed, moving to next audio file")