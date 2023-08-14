from httpx import AsyncClient
from httpx import Auth
from httpx import Response
from httpx import URL


class ApiClient:
    def __init__(self, base_url: URL, auth: Auth, organization_id: int = 1):
        self.__http_client = AsyncClient(
            base_url=base_url,
            auth=auth,
            event_hooks={
                "response": [self.__raise_on_4xx_5xx],
            },
            headers={
                "X-Grafana-Org-Id": str(organization_id)
            }
        )

    @staticmethod
    async def __raise_on_4xx_5xx(response: Response):
        response.raise_for_status()

