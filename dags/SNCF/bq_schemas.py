from google.cloud import bigquery

sncf_cleanliness = [
        bigquery.SchemaField("mois", "STRING"),
        bigquery.SchemaField("uic", "STRING"),
        bigquery.SchemaField("nom_gare", "STRING"),
        bigquery.SchemaField("nombre_de_non_conformites", "INT64"),
        bigquery.SchemaField("nombre_d_observations", "INT64"),
        bigquery.SchemaField("taux_de_conformite", "FLOAT64")
    ]
