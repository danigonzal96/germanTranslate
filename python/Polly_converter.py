'''
06/07/2021
Writer:dgonzalez
This function has been designed to be used from AWS Lambda.

'''

import json
import boto3
import os

polly_client = boto3.client('polly')
s3_client = boto3.client('s3')


def lambda_handler(event, context):

    if event['responsePayload']['sourceLenguage'] == 'de':
        pollyText = event['responsePayload']['sourceText']
    elif event['responsePayload']['targetLenguage'] == 'de':
        pollyText = event['responsePayload']['translatedText']

    response = polly_client.synthesize_speech(
        Engine='neural',
        LanguageCode='de-DE',
        OutputFormat='mp3',
        SampleRate='22050',
        Text=pollyText,
        TextType='text',
        VoiceId='Vicki'
    )

    fileName = '/tmp/' + event['responsePayload']['objectName']+'.mp3'
    file = open(fileName, 'wb')
    file.write(response['AudioStream'].read())
    file.close()

    objectName = event['responsePayload']['objectName']+'.mp3'
    s3_response = s3_client.upload_file(fileName,
                                        event['responsePayload']['bucketName'],
                                        objectName)

    return {
        'statusCode': 200,
        'body': 'Your audio file is waiting for you in your bucket'
    }
