from google.cloud import bigquery

sncf_cleanliness = [
        bigquery.SchemaField("id", "INT64"),
        bigquery.SchemaField("created_at", "TIMESTAMP"),
        bigquery.SchemaField("updated_at", "TIMESTAMP"),
        bigquery.SchemaField("order_date", "TIMESTAMP"),
        bigquery.SchemaField("status", "STRING"),
        bigquery.SchemaField("customer_id", "INT64"),
        bigquery.SchemaField("amount", "FLOAT64"),
        bigquery.SchemaField("total_items", "INT64")
    ]
