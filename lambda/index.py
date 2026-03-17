import json
import boto3
import os

# Use the internal hostname provided by LocalStack environment
# If not found, it falls back to 'localhost' (for manual testing)
ls_host = os.environ.get('LOCALSTACK_HOSTNAME', 'localhost')
endpoint_url = f"http://{ls_host}:4566"

# Initialize DynamoDB with the correct INTERNAL endpoint
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url, region_name="us-east-1")
table = dynamodb.Table('FileMetadata')

def handler(event, context):
    print("--- Lambda Triggered ---")
    for record in event['Records']:
        try:
            # Parse SQS body which contains the S3 record
            body = json.loads(record['body'])
            
            if 'Records' in body:
                for s3_rec in body['Records']:
                    file_name = s3_rec['s3']['object']['key']
                    file_size = s3_rec['s3']['object']['size']
                    
                    print(f"SRE LOG: Processing {file_name} ({file_size} bytes)")
                    
                    # Write to DynamoDB
                    table.put_item(Item={
                        'FileName': file_name,
                        'Size': str(file_size),
                        'Status': 'PROCESSED'
                    })
                    print(f"SRE LOG: Successfully saved {file_name} to DynamoDB")
        except Exception as e:
            print(f"SRE ERROR: {str(e)}")
            raise e
    return {"statusCode": 200}
