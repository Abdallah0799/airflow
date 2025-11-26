# Airflow (WIP 🏗)

This repository contains a standard **Apache Airflow** application packaged with **Docker** and **Docker Compose**.  
It includes a custom Airflow image.

It will be used to orchestrate various data workflows.

The current focus is on ingesting and processing **open SNCF datasets**.  
The initial objective is to determine the *“best French train stations”* using multiple KPIs.

## 🗄️ Architecture Overview

Extracted data is stored and processed using **Google Cloud Platform (GCP)**:

- **Cloud Storage** → Raw data (CSV files, logs, etc.)
- **BigQuery** → Cleaned and transformed analytics-ready tables
-  **Looker Studio** → Visualization

Airflow handles ingestion, transformation, and orchestration through DAGs defined in this project.

---

## ⚙️ Environment Variables

To run the project, ensure you have the required environment variables configured.

### Base variables

```env
AIRFLOW_UID=5000
AIRFLOW__CORE__EXECUTOR=CeleryExecutor
AIRFLOW__CORE__LOAD_EXAMPLES=False
AIRFLOW__CORE__AUTH_MANAGER=airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager
AIRFLOW__CORE__EXECUTION_API_SERVER_URL=http://airflow-apiserver:8080/execution/
AIRFLOW_CONFIG=/opt/airflow/config/airflow.cfg

# Apache Airflow configuration
AIRFLOW__API__AUTH_BACKENDS=airflow.api.auth.backend.basic_auth,airflow.api.auth.backend.session
AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=True
AIRFLOW__CORE__DEFAULT_TIMEZONE=Europe/Zurich
AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
AIRFLOW__CORE__TEST_CONNECTION=Enabled

AIRFLOW__DATABASE__LOAD_DEFAULT_CONNECTIONS=False
AIRFLOW__DATABASE__SQL_ALCHEMY_POOL_SIZE=0

AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK=True
AIRFLOW__WEBSERVER__BASE_URL=http://airflow.colibrys.com:8080

_AIRFLOW_DB_MIGRATE=True
_AIRFLOW_WWW_USER_CREATE=True
_AIRFLOW_WWW_USER_USERNAME=admin
_AIRFLOW_WWW_USER_PASSWORD=admin

AIRFLOW__SECRETS__BACKEND=airflow.providers.google.cloud.secrets.secret_manager.CloudSecretManagerBackend
```
## 🔐 Private / Required Secrets

These must be added manually (**do not commit secrets to git**):

```env
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN
AIRFLOW__CELERY__RESULT_BACKEND
GOOGLE_APPLICATION_CREDENTIALS
AIRFLOW__SECRETS__BACKEND_KWARGS
AIRFLOW__CORE__FERNET_KEY
```

Additionally, place your **GCP service account `.json` file** at the project root and point `GOOGLE_APPLICATION_CREDENTIALS` to it.

---

## 🧭 Quickstart

1. Add the private environment variables listed above (e.g., via a `.env` file or your shell environment).
2. Place your GCP service account JSON in the project root.
3. Build and start the project:

```bash
docker compose up --build -d
```

Open the Airflow web UI at the configured AIRFLOW__WEBSERVER__BASE_URL (default: http://airflow.colibrys.com:8080).
