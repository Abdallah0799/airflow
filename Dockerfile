ARG AIRFLOW_VERSION=3.1.0

FROM apache/airflow:${AIRFLOW_VERSION}

USER airflow 

COPY requirements.txt requirements.txt
COPY scripts /opt/airflow/scripts
COPY airflow-478417-fc7921015d46.json /opt/airflow/

RUN pip install --no-cache-dir -r requirements.txt