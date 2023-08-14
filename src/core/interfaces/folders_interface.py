from typing import AsyncIterable

from httpx import AsyncClient
from httpx import HTTPStatusError

from .base_interface import BaseInterface
from .dashboards_interface import DashBoardsInterface


class Folder:
    data: dict

    def __init__(self, data: dict, http_client: AsyncClient):
        self.data = data
        self.__http_client = http_client

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return repr(self.data)

    @property
    def folder_id(self) -> int:
        return self.data["id"]

    @property
    def folder_uid(self) -> str:
        return self.data["uid"]

    @property
    def title(self) -> str:
        return self.data["title"]

    @property
    def dashboards(self) -> DashBoardsInterface:
        dashboards_interface = DashBoardsInterface(http_client=self.__http_client, folder_id=self.folder_id)
        return dashboards_interface


class FoldersInterface(BaseInterface):
    def __init__(self, http_client: AsyncClient):
        super().__init__(http_client)

    async def get_all_folders(self) -> AsyncIterable[Folder]:
        # TODO: implement pagination
        # https://grafana.com/docs/grafana/latest/developers/http_api/folder/#get-all-folders
        # Get General folder

        yield await self.get_folder_by_id(folder_id=0)

        r = await self._http_client.get("/api/folders/")
        for folder in r.json():
            yield await self.get_folder_by_uid(folder["uid"])

    async def get_folder_by_id(
            self,
            folder_id: int,
    ) -> Folder:
        r = await self._http_client.get(f"/api/folders/id/{folder_id}")
        return Folder(data=r.json(), http_client=self._http_client)

    async def get_folder_by_uid(
            self,
            uid: str,
    ) -> Folder:
        if uid == "":
            return await self.get_folder_by_id(0)
        r = await self._http_client.get(f"/api/folders/{uid}")
        return Folder(data=r.json(), http_client=self._http_client)

    async def create_folder(
            self,
            folder: Folder,
    ) -> Folder:
        if folder.folder_uid == "" or folder.folder_id == 0:
            return await self.get_folder_by_id(folder_id=0)
        json_payload = {
            "uid": folder.folder_uid,
            "title": folder.title,
        }
        headers = {
            **self._http_client.headers,
            "Content-Type": "application/json",
        }
        try:
            r = await self._http_client.post(
                url="/api/folders",
                json=json_payload,
                headers=headers,
            )
            return Folder(data=r.json(), http_client=self._http_client)
        except HTTPStatusError as err:
            if err.response.status_code == 412:
                # TODO: Forward an implicit call to update_folder
                # For now, we are just ignore the updates and forward call to get_folder_by_uid
                return await self.get_folder_by_uid(folder.folder_uid)
            else:
                err.response.raise_for_status()
