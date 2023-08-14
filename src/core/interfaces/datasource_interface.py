from typing import AsyncIterable

from httpx import AsyncClient
from httpx import Response

from .base_interface import BaseInterface


class Datasource:
    data: dict

    def __init__(self, data: dict):
        self.data = data

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return repr(self.data)

    @property
    def datasource_id(self):
        return self.data["id"]

    @property
    def darasource_uid(self):
        return self.data["uid"]

    @property
    def name(self):
        return self.data["name"]

    @property
    def organization_id(self):
        return self.data["orgId"]


class DatasourceInterface(BaseInterface):
    def __init__(self, http_client: AsyncClient):
        super().__init__(http_client)

    @staticmethod
    async def __datasource_factory(response: Response) -> Datasource:
        return Datasource(data=response.json())

    async def get_datasource_by_id(self, ds_id: int) -> Datasource:
        r = await self._http_client.get(f"/api/datasources/{ds_id}")
        return await self.__datasource_factory(response=r)

    async def get_datasource_by_uid(self, ds_uid: str) -> Datasource:
        r = await self._http_client.get(f"/api/datasources/uid/{ds_uid}/")
        return await self.__datasource_factory(response=r)

    async def get_datasource_by_name(self) -> Datasource:
        # TODO: Should be implemented
        pass

    async def get_all_datasources(self) -> AsyncIterable[Datasource]:
        # TODO: Should be implemented
        pass
