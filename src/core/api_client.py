from httpx import AsyncClient
from httpx import Auth
from httpx import URL


class ApiClient:
    def __init__(self, base_url: URL, auth: Auth, organization_id: int = 1):
        self.__http_client = AsyncClient(
            base_url=base_url,
            auth=auth,
            headers={
                "X-Grafana-Org-Id": str(organization_id)
            }
        )
