from typing import List

from google.oauth2 import service_account
from google.cloud.exceptions import NotFound


class BaseGCP():
    """
    Base GCP class that handles authentication for Google Cloud Platform services.
    """
    def __init__(self, service_account_infos: str = None, scopes: List[str] = None) -> None:
        """
        Initialize GCP credentials.

        Args:
            service_account_infos (dict, optional): Service account JSON as a Python dict.
            scopes (List[str], optional): List of OAuth scopes.
        """
        try:
            if service_account_infos:
                self.credentials = service_account.Credentials.from_service_account_info(
                    info=service_account_infos,
                    scopes=scopes,
                )
            else:
                self.credentials = None

        except Exception as e:
            print(f"Erreur lors de la connexion avec le compte de service : {e}")
            raise
