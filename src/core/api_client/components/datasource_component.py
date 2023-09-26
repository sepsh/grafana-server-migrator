from typing import AsyncIterable

from httpx import AsyncClient
from httpx import HTTPStatusError
from httpx import Response
from pydantic import computed_field

from .base_component import BaseComponent, BaseDataModel


class Datasource(BaseDataModel):
    @computed_field
    @property
    def datasource_id(self) -> dict:
        return self.data["id"]

    @computed_field
    @property
    def datasource_uid(self) -> str:
        return self.data["uid"]

    @computed_field
    @property
    def name(self) -> str:
        return self.data["name"]

    @computed_field
    @property
    def organization_id(self) -> str:
        return self.data["orgId"]

    @computed_field
    @property
    def striped(self) -> dict:
        unneeded_keys = ["id"]
        return {k: v for (k, v) in self.data.items() if k not in unneeded_keys}


class DatasourceComponent(BaseComponent):
    def __init__(self, http_client: AsyncClient):
        super().__init__(http_client)

    @staticmethod
    async def __datasource_factory(response: Response) -> Datasource:
        return Datasource(data=response.json())

    async def get_datasource_by_id(self, datasource_id: int) -> Datasource:
        r = await self._http_client.get(f"/api/datasources/{datasource_id}")
        return await self.__datasource_factory(response=r)

    async def get_datasource_by_uid(self, datasource_uid: str) -> Datasource:
        r = await self._http_client.get(f"/api/datasources/uid/{datasource_uid}/")
        return await self.__datasource_factory(response=r)

    async def get_datasource_by_name(self, datasource_name: str) -> Datasource:
        r = await self._http_client.get(f"/api/datasources/name/{datasource_name}")
        return await self.__datasource_factory(response=r)

    async def create_data_source(self, data_source: Datasource):
        headers = {
            **self._http_client.headers,
            "Content-Type": "application/json",
        }
        json_payload = {**data_source.striped}
        try:
            r = await self._http_client.post(
                url="/api/datasources",
                headers=headers,
                json=json_payload,
            )
            return Datasource(data=r.json())
        except HTTPStatusError as err:
            if err.response.status_code != 409:
                err.response.raise_for_status()
            ds = await self.get_datasource_by_uid(
                datasource_uid=data_source.datasource_uid
            )
            return ds

    async def get_all_datasources(self) -> AsyncIterable[Datasource]:
        r = await self._http_client.get("/api/datasources/")
        for datasource in r.json():
            datasource_uid = datasource["uid"]
            yield await self.get_datasource_by_uid(datasource_uid=datasource_uid)
