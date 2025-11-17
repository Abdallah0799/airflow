# 1. Fetch file from url and load it to GCS bucket
# => custom code
# 2. Extract file from GCS, rename columns
# 3. Create BigQuery dataset if it doesn't exist
# 4. Load transformed data to BigQuery with airflow operator