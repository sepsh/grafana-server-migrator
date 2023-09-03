from typing import AsyncIterable

from httpx import AsyncClient

from .base_component import BaseComponent


class Dashboard:
    data: dict

    def __init__(self, data: dict):
        self.data = data

    def __str__(self):
        return str(self.title)

    def __repr__(self):
        return repr(self.data)

    @property
    def dashboard_uid(self) -> str:
        return self.data["dashboard"]["uid"]

    @property
    def folder_id(self) -> str:
        return self.data["meta"]["folderId"]

    @property
    def folder_uid(self) -> str:
        return self.data["meta"]["folderUid"]

    @property
    def title(self) -> str:
        return self.data["dashboard"]["title"]

    @property
    def striped(self) -> dict[str, dict]:
        # TODO: this function was made in hurry. most certainly needs a rewrite.

        data = self.data
        striped_data = dict()

        # Filter keys to be generated again by grafana
        unneeded_keys = [
            "id",
            # "uid",
            "links",
            "version",
        ]
        striped_data["dashboard"] = {k: v for (k, v) in data["dashboard"].items() if k not in unneeded_keys}

        # Filter keys to be generated again by grafana
        unneeded_keys = [
            "url",
            "expires",
            "created",
            "updated",
            "version",
            "folderId",
            "folderUid",
            "folderUrl",
            "provisioned",
            "provisionedExternalId",
            "publicDashboardAccessToken",
            "publicDashboardUid",
            "publicDashboardEnabled",
        ]
        striped_data["meta"] = {k: v for (k, v) in data["meta"].items() if k not in unneeded_keys}
        return striped_data


class DashBoardsComponent(BaseComponent):
    def __init__(
            self,
            http_client: AsyncClient,
            folder_id: int | None = None,
    ):
        super().__init__(http_client)
        self.folder_id = folder_id

    async def get_all_dashboards(
            self,
            filter_folder_id: list[str | int] | None = None,
    ) -> AsyncIterable[Dashboard]:
        if filter_folder_id is None:
            if self.folder_id is None:
                filter_folder_id = []
            else:
                filter_folder_id = [self.folder_id]
        params = {"type": "dash-db", "folderIds": filter_folder_id}
        r = await self._http_client.get("/api/search", params=params)
        for dashboard in r.json():
            yield await self.get_dashboard(uid=dashboard["uid"])

    async def get_dashboard(
            self,
            uid: str,
    ) -> Dashboard:
        r = await self._http_client.get(f"/api/dashboards/uid/{uid}")
        return Dashboard(data=r.json())

    async def create_dashboard(
            self,
            dashboard: Dashboard,
            folder_uid: str | None = None,
    ) -> Dashboard:
        json_payload = {
            **dashboard.striped,
            "folderUid": dashboard.folder_uid,
            "overwrite": True,
        }
        if folder_uid is not None:
            json_payload["folderUid"] = folder_uid
        headers = {
            **self._http_client.headers,
            "Content-Type": "application/json",
        }
        r = await self._http_client.post(
            url="/api/dashboards/db/",
            json=json_payload,
            headers=headers,
        )
        new_uid = r.json()["uid"]
        new_dashboard = await self.get_dashboard(uid=new_uid)
        return new_dashboard
