ARG AIRFLOW_VERSION=3.1.0

FROM apache/airflow:${AIRFLOW_VERSION}

USER airflow 

COPY requirements.txt requirements.txt
COPY scripts /opt/airflow/scripts

RUN pip install --no-cache-dir -r requirements.txt