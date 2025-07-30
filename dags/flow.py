from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import boto3
from botocore.exceptions import ClientError
import os

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def get_s3_client():
    s3_client = boto3.client('s3')

    return s3_client

def check_files_exist_in_s3(local_dir, bucket_name, s3_prefix='data/'):
    s3 = get_s3_client()  # This uses AWS credentials from environment or ~/.aws/credentials

    for filename in os.listdir(local_dir):
        if filename.endswith('.csv') and os.path.isfile(os.path.join(local_dir, filename)):
            s3_key = f"{s3_prefix}{filename}" if s3_prefix else filename
            print("S3KEY: ", s3_key)
            try:
                s3.head_object(Bucket=bucket_name, Key=s3_key)
                print(f"✅ {filename} exists in bucket '{bucket_name}'")
            except s3.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print(f"❌ {filename} NOT found in bucket '{bucket_name}'")
                else:
                    raise

# Example usage
local_directory = '/mnt/c/Users/Benny/projects/sales_data_pipeline'
bucket = 'shopsmart-etl'

with DAG(
    dag_id='shopsmart_etl_dag',
    default_args=default_args,
    description='Ingest data from S3 using Airbyte HTTP call into Snowflake, then model the data with dbt',
    schedule_interval='@daily',
    start_date=datetime.now() - timedelta(days=1),
    catchup=False
) as dag:

    start = EmptyOperator(task_id='start')

    trigger_s3_files_exist = PythonOperator(
        task_id='trigger_s3_files_exist',
        python_callable=check_files_exist_in_s3,
        op_kwargs={
        'local_dir': local_directory,
        'bucket_name': bucket,
        's3_prefix': 'data/'  # optional
    }
    )

    trigger_airbyte_sync = SimpleHttpOperator(
    task_id='trigger_airbyte_connection',
    http_conn_id='airbyte_api',
    endpoint='api/v1/connections/sync',
    method='POST',
    data='{"connectionId": ""}',
    response_check=lambda response: response.status_code == 200,
    log_response=True,
)

    end = EmptyOperator(task_id='end')

    start >> trigger_s3_files_exist >> trigger_airbyte_sync >> end
