#imports
import json
import time
import os
import managers.s3BucketManager as _s3BucketManager
import managers.sqsQueueManager as _sqsQueueManager

#get student ID from app secrets
file = open('appsecrets.json')
secrets = json.load(file)
studentId = secrets['studentId']

#define dir
dir = "./audioTracks/"
files = os.listdir(dir)

#define resource names
bucketName = "audio-bucket-" + studentId
queueName = "audio-queue-" + studentId
tableName = "audio-table-" + studentId

#get queue url
queueUrl = _sqsQueueManager.getUrl(queueName)

#upload all audio files
for i in range(len(files)):
    #define fileName
    fileName = files[i]
    
    #sleep for 30 seconds
    if(i != 0):
        time.sleep(30)
    
    #upload file to bucket
    success = _s3BucketManager.uploadFile(
        "audio-bucket-" + studentId,
        fileName,
        dir
    )

    #send message on successful upload
    if(success):
        _sqsQueueManager.sendMessage(fileName, queueUrl)
    else:
        print("upload failed, moving to next audio file")

print('Upload complete')