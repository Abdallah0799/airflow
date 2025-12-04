ARG AIRFLOW_VERSION=3.1.0

FROM apache/airflow:${AIRFLOW_VERSION}

# Ensure script has correct permissions
USER root
COPY scripts /opt/airflow/scripts
RUN chmod +x /opt/airflow/scripts/airflow-init-connections.sh

USER airflow 

COPY requirements.txt requirements.txt
COPY airflow-478417-fc7921015d46.json /opt/airflow/

RUN pip install --no-cache-dir -r requirements.txt