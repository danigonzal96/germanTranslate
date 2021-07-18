'''
05/07/2021
Writer:dgonzalez
This function has been designed to be used from AWS Lambda.

The function will take the arguments form an other Lambda function ('checkLanguage.py').
It will use the outputs form that function to translate the content from spanish to german and from german to spanish.
If the content is not in german nor spanish, it will translate it into english.

The function Role needs permissions to access the AWS Translete Service.

As an output, it will return the following atributes:
- statusCode
- sourceText
- translatedText
- sourceLenguage
- targetLenguage
'''


import json
import boto3


def lambda_handler(event, context):

    # Set up the AWS Boto3 cilenst required
    translate_client = boto3.client('translate')

    # Language Logic
    if event['responsePayload']['language'] == 'de':
        targetLenguageCode = 'es'
    elif event['responsePayload']['language'] == 'es':
        targetLenguageCode = 'de'
    else:
        targetLenguageCode = 'en'

    # Call the Translate API and check the lenguage of the text
    translateResponse = translate_client.translate_text(
        Text=event['responsePayload']['text'],
        SourceLanguageCode=event['responsePayload']['language'],
        TargetLanguageCode=targetLenguageCode
    )

    # Get the result of the Translate API request
    translatedText = translateResponse['TranslatedText']
    sourceLanguage = translateResponse['SourceLanguageCode']
    targetLanguage = translateResponse['TargetLanguageCode']

    return {
        'statusCode': 200,
        'sourceText': event['responsePayload']['text'],
        'objectName': event['responsePayload']['objectName'],
        'bucketName': event['responsePayload']['bucketName'],
        'translatedText': translatedText,
        'sourceLenguage': sourceLanguage,
        'targetLenguage': targetLanguage,
    }
