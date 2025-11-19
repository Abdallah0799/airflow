from typing import List
import pandas as pd
import io

from google.cloud import storage

from utils.gcp import BaseGCP


class GCS(BaseGCP):
    def __init__(self, service_account_infos: str = None, scopes: List[str] = None) -> None:
        super().__init__(service_account_infos, scopes)
        self.client = storage.Client(credentials=self.credentials)

    def upload(self, bucket_name: str, file_name: str, file_content: bytes) -> str:
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        blob.upload_from_string(file_content)

        print(f"File uploaded to gs://{bucket_name}/{file_name}")
        return f"gs://{bucket_name}/{file_name}"
    
    def download(self, bucket_name: str, file_name: str) -> pd.DataFrame:
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        # Read file content
        file_content = blob.download_as_bytes()

        # Determine file type and read accordingly
        if file_name.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_content))
        elif file_name.endswith('.json'):
            df = pd.read_json(io.BytesIO(file_content))
        elif file_name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(file_content))
        else:
            # Default to CSV
            df = pd.read_csv(io.BytesIO(file_content))
        
        return df
