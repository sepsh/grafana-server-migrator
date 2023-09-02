from httpx import AsyncClient
from httpx import HTTPStatusError

from .base_interface import BaseInterface
from .datasource_interface import DatasourceInterface
from .folders_interface import FoldersInterface


class Organization:
    data: dict

    def __init__(self, data: dict, http_client: AsyncClient):
        self.data = data
        self.__http_client = http_client

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return repr(self.data)

    @property
    def name(self) -> str:
        return self.data["name"]

    @property
    def org_id(self) -> int:
        return self.data["id"]

    @property
    def folders(self) -> FoldersInterface:
        folders_interface = FoldersInterface(http_client=self.__http_client)
        return folders_interface

    @property
    def datasources(self) -> DatasourceInterface:
        datasource_interface = DatasourceInterface(http_client=self.__http_client)
        return datasource_interface


class OrganizationsInterface(BaseInterface):
    def __init__(self, http_client: AsyncClient):
        super().__init__(http_client)

    async def get_current_organization(self) -> Organization:
        r = await self._http_client.get("/api/org")
        organization = Organization(
            data=r.json(),
            http_client=self._http_client,
        )
        return organization

    async def get_all_organizations(self):
        r = await self._http_client.get(url="/api/orgs")
        for organization_data in r.json():
            organization = await self.get_organization_by_id(organization_data["id"])
            yield organization

    async def get_organization_by_id(self, org_id: int) -> Organization:
        r = await self._http_client.get(url=f"/api/orgs/{org_id}")
        organization = await self.__organization_factory(org_data=r.json())
        return organization

    async def get_organization_by_name(self, org_name: str) -> Organization:
        r = await self._http_client.get(url=f"/api/orgs/name/{org_name}")
        organization = await self.__organization_factory(org_data=r.json())
        return organization

    async def create_organization(self, org_name: str) -> Organization:
        json_payload = {
            "name": org_name
        }
        try:
            r = await self._http_client.post(
                url="/api/orgs/",
                json=json_payload,
                headers={
                    "Content-Type": "application/json"
                }
            )
            return await self.get_organization_by_name(org_name=org_name)
        except HTTPStatusError as err:
            if err.response.status_code == 409:
                # TODO: Forward an implicit call to update_organization
                # For now, we are just ignore the updates and forward call to get_folder_by_uid
                return await self.get_organization_by_name(org_name=org_name)
            else:
                err.response.raise_for_status()

    async def deploy_organization(self, organization: Organization):
        """
        Clone an existing organization.
        """
        return await self.create_organization(org_name=organization.name)

    async def __organization_factory(self, org_data: dict) -> Organization:
        org_id = org_data["id"]
        headers = {
            k: v
            for k, v in self._http_client.headers.items()
            if k != "x-grafana-org-id"
        }
        org_http_client = AsyncClient(
            base_url=self._http_client.base_url,
            auth=self._http_client.auth,
            event_hooks=self._http_client.event_hooks,
            headers={**headers, "X-Grafana-Org-Id": str(org_id)},
        )
        organization = Organization(data=org_data, http_client=org_http_client)
        return organization
