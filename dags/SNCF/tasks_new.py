import requests

from airflow.decorators import task
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)

from SNCF.bq_schemas import sncf_cleanliness
from utils.gcp.gcs import GCS

URL_FROM_DATA_SOURCE = ""
BUCKET_NAME = ""
TARGET_FILE_NAME = ""

DATASET_ID = ""
TABLE_ID = ""


@task
def upload_source_to_gcs():
    gcs_engine = GCS()

    # Download file from URL
    response = requests.get(URL_FROM_DATA_SOURCE)
    response.raise_for_status()

    gcs_engine.upload(BUCKET_NAME, TARGET_FILE_NAME, response.content)


@task
def extract_and_transform():
    gcs_engine = GCS()

    data = gcs_engine.download(BUCKET_NAME, TARGET_FILE_NAME)

    # Rename columns
    data = data.rename(columns={})

    # Write result in gcs
    return gcs_engine.upload(
        "airflow_tasks_results", f"transform_{BUCKET_NAME}_{TARGET_FILE_NAME}.csv"
    )


load_to_bigquery = GCSToBigQueryOperator(
    task_id="load_to_bigquery",
    bucket=BUCKET_NAME,
    source_objects=["transform_{BUCKET_NAME}_{TARGET_FILE_NAME}.csv"],
    destination_project_dataset_table=f"{DATASET_ID}.{TABLE_ID}",
    schema_fields=sncf_cleanliness,
    write_disposition="WRITE_TRUNCATE",
)
