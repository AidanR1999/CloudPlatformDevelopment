#imports 
import json
import helpers as _helpers

#initial function
def lambda_handler(event, context):
    
    #get object location
    location = 'eu-west-2'
    bucket_name  = "audio-bucket-s1911669"
    fileName = event['Records'][0]['body']
    
    #define public URLs
    bucketUri = "https://s3-%s.amazonaws.com/%s/" % (location, bucket_name)
    objectUri = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, fileName)
    
    #other dependencies
    tableName = "audio-table-s1911669"
    phoneNo = "+44ZZZZZZZZZZ"
    
    #begin transcription job
    _helpers.transcribe(fileName, objectUri)
    
    #check if transcribe job is complete
    #loop until job is complete
    while(True):
        #get job
        job = _helpers.getJob(fileName)
        
        #if job complete
        if(job['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED'):
            #get tracscription text
            text = _helpers.getTranscription(job)
            
            #start sentiment analysis
            comp = _helpers.sentimentAnalysis(text)
            result = comp['Sentiment']
            
            #add result to db if result not NEUTRAL
            if result not in ["NEUTRAL"]:
                _helpers.addResultToDb(fileName, result, tableName)
            
            #send text sms if result NEGATIVE
            if result in ["NEGATIVE"]:
                _helpers.sendSMS(phoneNo, fileName)
                
            #break while loop
            break
        
    #return response
    return {
        'statusCode': 200,
        'body': json.dumps(comp)
    }