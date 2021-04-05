#imports
import boto3
import json
import urllib3

#begin transcription job for audio
#TAKES fileName : string, objectUri: string
#RETURNS job : object
def transcribe(fileName, objectUri):
    #get client
    transcribe = boto3.client('transcribe')
    
    #check if job exists
    try:
        job = getJob(fileName)
        
        #delete job
        transcribe.delete_transcription_job(
            TranscriptionJobName=fileName
        )
    except Exception as e:
        print(e)
    
    #if not, start job
    response = transcribe.start_transcription_job(
        TranscriptionJobName=fileName,
        LanguageCode='en-GB',
        Media={
            'MediaFileUri': objectUri
        }
    )
    
    return response
    
#retrieves job details from AWS Transcribe
#TAKES name : string
#RETURNS job : object
def getJob(name):
    #get client
    transcribe = boto3.client('transcribe')
    
    #retreives job
    res = transcribe.get_transcription_job(
        TranscriptionJobName=name    
    )
    
    return res

#retrieves results from transcription
#TAKES job : object
#RETURNS text : string
def getTranscription(job):
    #get job output
    uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
    
    #load data using get request
    http = urllib3.PoolManager()
    req = http.request('GET', uri)
    req = json.loads(req.data)
    
    #extract text
    text = req['results']['transcripts'][0]['transcript']
    
    return text
    
#performs sentiment analysis on text using AWS comprehend
#TAKES text : string
#RETURNS res : object
def sentimentAnalysis(text):
    #get client
    comprehend = boto3.client('comprehend')
    
    #begin analysis
    res = comprehend.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    
    return res

#sends SMS message to specified phone number
#TAKES phoneNo : string, fileName : string
#RETURNS res : object
def sendSMS(phoneNo, fileName):
    #get client
    sns = boto3.client('sns')
    
    #create message
    message = fileName + ' was analysed as NEGATIVE'
    
    #send SMS
    res = sns.publish(
            PhoneNumber=phoneNo,
            Message=message
        )
    return res
    
#adds results from analysis to db
#TAKES fileName : string, result : string, tableName : string
#RETURNS void
def addResultToDb(fileName, result, tableName):
    #get resource
    db = boto3.resource('dynamodb')
    
    #retrieve table
    table = db.Table(tableName)
    
    #put item in table
    try:
        table.put_item(
            Item={
                'trackname':fileName,
                'sentiment':result
            }
        )
    #ignore if item already exists
    except Exception as e:
        print(e)