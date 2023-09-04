from abc import ABC

from httpx import AsyncClient
from pydantic import BaseModel


class BaseDataModel(BaseModel):
    data: dict


class BaseComponent(ABC):
    _http_client: AsyncClient

    def __init__(self, http_client: AsyncClient):
        self._http_client = http_client
