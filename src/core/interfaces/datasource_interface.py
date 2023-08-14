# TODO: Needed ASAP

from httpx import AsyncClient

from .base_interface import BaseInterface


class Datasource:
    data: dict

    def __init__(self, data: dict):
        self.data = data

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return repr(self.data)


class DatasourceInterface(BaseInterface):
    def __init__(self, http_client: AsyncClient):
        super().__init__(http_client)

    async def get_datasource(self) -> Datasource:
        pass
