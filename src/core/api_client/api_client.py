from httpx import AsyncClient
from httpx import Auth
from httpx import Response
from httpx import URL

from src.core.api_client.components.dashboards_component import DashBoardsComponent
from src.core.api_client.components.datasource_component import DatasourceComponent
from src.core.api_client.components.folders_component import FoldersComponent
from src.core.api_client.components.organizations_component import (
    OrganizationsComponent,
)


class ApiClient:
    def __init__(self, base_url: URL, auth: Auth, organization_id: int = 1):
        self.__http_client = AsyncClient(
            base_url=base_url,
            auth=auth,
            event_hooks={
                "response": [self.__raise_on_4xx_5xx],
            },
            headers={"X-Grafana-Org-Id": str(organization_id)},
        )

    @property
    def dashboards(self) -> DashBoardsComponent:
        dashboards_interface = DashBoardsComponent(http_client=self.__http_client)
        return dashboards_interface

    @property
    def folders(self) -> FoldersComponent:
        folders_interface = FoldersComponent(http_client=self.__http_client)
        return folders_interface

    @property
    def data_sources(self) -> DatasourceComponent:
        data_sources_interface = DatasourceComponent(http_client=self.__http_client)
        return data_sources_interface

    @property
    def organizations(self) -> OrganizationsComponent:
        organizations_interface = OrganizationsComponent(http_client=self.__http_client)
        return organizations_interface

    @staticmethod
    async def __raise_on_4xx_5xx(response: Response):
        response.raise_for_status()
