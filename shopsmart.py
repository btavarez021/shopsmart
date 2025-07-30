import boto3
from dotenv import load_dotenv
import os
from botocore.exceptions import ClientError


load_dotenv(dotenv_path="/home/bxt058y/projects/shopsmart-etl/.env")  # loads .env from current directory

def s3_client():
    s3_client = boto3.client(
        's3',
        aws_access_key_id= os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    return s3_client

def list_s3_objects(s3_client, bucket_name):

    try:
        # List objects in your bucket
        response = s3_client.list_objects_v2(Bucket='shopsmart-etl')
        print(response)
        contents = response.get('Contents', [])
        if not contents:
            print(f"No objects found in bucket '{bucket_name}'.")
        for obj in response.get('Contents', []):
            print(obj['Key'])

    except ClientError as e:
        print(f"Error accessing bucket: {e}")




s3_client = s3_client()
list_s3_objects(s3_client, bucket_name = 'shopsmart-etl')