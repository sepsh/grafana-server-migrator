from httpx import AsyncClient
from httpx import Auth
from httpx import Response
from httpx import URL

from src.core.api_client.interfaces.dashboards_interface import DashBoardsInterface
from src.core.api_client.interfaces.datasource_interface import DatasourceInterface
from src.core.api_client.interfaces.folders_interface import FoldersInterface
from src.core.api_client.interfaces.organizations_interface import OrganizationsInterface


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

    @property
    def dashboards(self) -> DashBoardsInterface:
        dashboards_interface = DashBoardsInterface(http_client=self.__http_client)
        return dashboards_interface

    @property
    def folders(self) -> FoldersInterface:
        folders_interface = FoldersInterface(http_client=self.__http_client)
        return folders_interface

    @property
    def data_sources(self) -> DatasourceInterface:
        data_sources_interface = DatasourceInterface(http_client=self.__http_client)
        return data_sources_interface

    @property
    def organizations(self) -> OrganizationsInterface:
        organizations_interface = OrganizationsInterface(http_client=self.__http_client)
        return organizations_interface

    @staticmethod
    async def __raise_on_4xx_5xx(response: Response):
        response.raise_for_status()