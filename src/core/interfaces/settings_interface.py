# TODO: Needed ASAP

from httpx import AsyncClient

from .base_interface import BaseInterface


class SettingsInterface(BaseInterface):
    def __init__(self, http_client: AsyncClient):
        super().__init__(http_client)
