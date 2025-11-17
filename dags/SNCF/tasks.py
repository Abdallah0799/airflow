import requests
import pandas as pd

from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

from utils.gcp.gcs import GCS

@task
def upload_source_to_gcs():
    gcs_engine = GCS()
    
    # Get URL from DAG configuration or use default
    url = context['dag_run'].conf.get('url') if context['dag_run'].conf else context['params'].get('url')
    bucket_name = context['params']['bucket_name']
    file_name = context['params']['file_name']

    # Download file from URL
    response = requests.get(url)
    response.raise_for_status()

    gcs_engine.upload(bucket_name, file_name, response.content)

@task
def extract_and_transform():
    gcs_engine = GCS()

    bucket_name = context['params']['bucket_name']
    file_name = context['params']['file_name']

    data = gcs_engine.download(bucket_name, file_name)

    # transform
    data = data.rename(columns={})

    # write result in gcs
    return gcs_engine.upload("airflow_tasks_results", f"transform_{bucket_name}_{file_name}")

# Task 3: Create BigQuery dataset if it doesn't exist
create_dataset = BigQueryCreateEmptyDatasetOperator(
    task_id='create_bigquery_dataset',
    dataset_id='{{ params.dataset_id }}',
    dag=dag
)

load_to_bigquery = GCSToBigQueryOperator(
    task_id='load_to_bigquery',
    bucket='{{ params.bucket_name }}',
    source_objects=['transformed_{{ params.file_name.split(".")[0] }}.csv'],
    destination_project_dataset_table='{{ params.dataset_id }}.{{ params.table_id }}',
    schema_fields=None,  # Auto-detect schema
    write_disposition='WRITE_TRUNCATE',
    autodetect=True,
    dag=dag
)