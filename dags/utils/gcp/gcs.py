from typing import List

from google.cloud import storage

from utils.gcp import BaseGCP


class GCS(BaseGCP):
    """
    Google Cloud Storage client class, inheriting authentication from BaseGCP.
    """

    def __init__(
        self, service_account_infos: str = None, scopes: List[str] = None
    ) -> None:
        super().__init__(service_account_infos, scopes)
        self.client = storage.Client(credentials=self.credentials)

    def upload(
        self,
        bucket_name: str,
        file_name: str,
        file_content: bytes,
        extension: str,
        content_type="'text/csv'",
    ) -> str:
        """
        Upload a file to a GCS bucket.

        Args:
            bucket_name (str): Name of the GCS bucket.
            file_name (str): Destination filename in the bucket.
            file_content (bytes): Binary content of the file.

        Returns:
            str: gs:// path of the uploaded file.
        """
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(f"{file_name}.{extension}")

        blob.upload_from_string(file_content, content_type=content_type)

        print(f"File uploaded to gs://{bucket_name}/{file_name}.{extension}")
        return f"gs://{bucket_name}/{file_name}.{extension}"
