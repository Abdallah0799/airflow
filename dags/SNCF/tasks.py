import requests
import re
import unicodedata

from airflow.decorators import task
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)

from SNCF.bq_schemas import sncf_cleanliness
from utils.gcp.gcs import GCS

URL_FROM_DATA_SOURCE = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/proprete-en-gare/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
BUCKET_NAME = "sncf-aga"
TARGET_FILE_NAME = "proprete_gare"

DATASET_ID = "sncf"
TABLE_ID = "proprete_gare"


def standardize_column_names(name: str) -> str:
    """
    Standardizes a column name by removing accents, converting to snake_case,
    and keeping only alphanumeric characters + underscores.

    Steps:
        1) Normalize Unicode to remove accents
        2) Replace spaces, hyphens, and separators with underscores
        3) Add underscores between camelCase / PascalCase transitions
        4) Convert to lowercase
        5) Remove non-alphanumeric characters (except _)
        6) Collapse multiple underscores
        7) Strip leading/trailing underscores
    """
    # 1)
    name = unicodedata.normalize('NFKD', name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    # 2)
    name = re.sub(r'[\s\-]+', '_', name)
    # 3)
    name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    # 4)
    name = name.lower()
    # 5)
    name = re.sub(r'[^a-z0-9_]', '', name)
    # 6)
    name = re.sub(r'_+', '_', name)
    # 7)
    return name.strip('_')


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
    data = data.rename(columns={col: standardize_column_names(col) for col in data.columns})

    csv_str = data.to_csv(index=False)
    content_bytes = csv_str.encode("utf-8")

    # Write result in gcs
    return gcs_engine.upload(
        "airflow_tasks_results", f"transform_{BUCKET_NAME}_{TARGET_FILE_NAME}.csv", content_bytes
    )


load_to_bigquery = GCSToBigQueryOperator(
    task_id="load_to_bigquery",
    gcp_conn_id="gcp_airflow",
    bucket=BUCKET_NAME,
    source_objects=["transform_{BUCKET_NAME}_{TARGET_FILE_NAME}.csv"],
    destination_project_dataset_table=f"{DATASET_ID}.{TABLE_ID}",
    schema_fields=sncf_cleanliness,
    write_disposition="WRITE_TRUNCATE",
)
