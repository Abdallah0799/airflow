from datetime import timedelta
import pendulum

from airflow import DAG

from SNCF.tasks import upload_source_to_gcs, extract_and_transform, load_to_bigquery

default_args = {
    "owner": "sncf_owner",
    # "email": "abdallah.gazal@gmail.com",
    # "email_on_failure": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

DAG_ID = "SNCF"
TIMEZONE = "Europe/Zurich"

with DAG(
    DAG_ID,
    default_args=default_args,
    tags=["sncf"],
    schedule_interval="* 6 * * *",
    start_date=pendulum.now(tz=pendulum.timezone(TIMEZONE)).subtract(days=1),
    max_active_runs=1,
) as dag:
    upload_source_to_gcs_task = upload_source_to_gcs()
    extract_and_transform_task = extract_and_transform()

    upload_source_to_gcs_task >> extract_and_transform_task >> load_to_bigquery
