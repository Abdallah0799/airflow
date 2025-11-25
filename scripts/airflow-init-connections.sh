# Create connections
/entrypoint airflow connections add 'gcp_airflow' \
  --conn-type google_cloud_platform \
  --conn-extra "{\"extra__google_cloud_platform__project\": \"$GCP_PROJECT_ID\", \"extra__google_cloud_platform__key_path\": \"gcp-key.json\"}" 2>/dev/null || echo "Connection gcp_airflow already exists"
