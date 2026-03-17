import json
import boto3
import os

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566", region_name="us-east-1")
table = dynamodb.Table('FileMetadata')

def handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])

        if 'Records' in body:
            for s3_rec in body['Records']:
                file_name = s3_rec['s3']['object']['key']
                file_size = s3_rec['s3']['object']['size']

        print(f"Processing: {file_name} ({file_size} bytes)")

        table.put_item(Item={
           'FileName': file_name,
           'Size': str(file_size),
           'Status': 'PROCESSED'
        })
    return {"statusCode": 200, "body": "Success"}
