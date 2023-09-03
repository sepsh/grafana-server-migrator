# TODO: Needed ASAP

from httpx import AsyncClient

from .base_component import BaseComponent


class SettingsComponent(BaseComponent):
    def __init__(self, http_client: AsyncClient):
        super().__init__(http_client)
