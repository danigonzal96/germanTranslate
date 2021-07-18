'''
05/07/2021
Writer:dgonzalez
This function has been designed to be used from AWS Lambda.

It has been designed to be trigger from an S3 Bucket and it will handle '.txt' files.
Finally the function will make a request to AWS Comprehend to know in wich language is the inforation of the file.

The function Role needs permissions to access the S3 bucket and AWS Comprehend.

As an output, it will return the following atributes:
- statusCode
- objectName
- bucketName
- text
- language
- lenguageScore
'''


import json
import boto3


def lambda_handler(event, context):

    # Set up the AWS Boto3 cilenst required
    s3_client = boto3.client('s3')
    comprehend_client = boto3.client('comprehend')

    # Get the object and bucket Names
    objectName = event['Records'][0]['s3']['object']['key']
    bucketName = event['Records'][0]['s3']['bucket']['name']

    # Get and Transform the text from binary into a string
    s3Response = s3_client.get_object(
        Bucket=bucketName,
        Key=objectName,
    )

    binaryText = s3Response['Body'].read()
    textToComprehend = bytearray(binaryText).decode('utf-8')

    # Call the Comprehend API and check the lenguage of the text
    comprehendResponse = comprehend_client.detect_dominant_language(
        Text=textToComprehend,
    )

    # Get the result of the Comprehend API request
    language = comprehendResponse['Languages'][0]['LanguageCode']
    languageScore = comprehendResponse['Languages'][0]['Score']

    return {
        'statusCode': 200,
        'objectName': objectName,
        'bucketName': bucketName,
        'text': textToComprehend,
        'language': language,
        'lenguageScore': languageScore,
    }
