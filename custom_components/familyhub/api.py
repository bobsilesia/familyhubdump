import json
from typing import Optional

import aiohttp

BASE_URL = "https://api.smartthings.com/v1"


class SmartThingsClient:
    def __init__(
        self,
        token: str,
        refresh_token: Optional[str] = None,
        token_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ):
        self._token = token
        self._refresh_token = refresh_token
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def _refresh(self):
        if not (
            self._refresh_token
            and self._token_url
            and self._client_id
            and self._client_secret
        ):
            return
        session = await self._get_session()
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }
        async with session.post(self._token_url, data=data) as resp:
            if resp.status == 200:
                j = await resp.json()
                self._token = j.get("access_token", self._token)
                self._refresh_token = j.get(
                    "refresh_token",
                    self._refresh_token,
                )
                self._headers["Authorization"] = f"Bearer {self._token}"

    async def get_device_status(self, device_id: str) -> dict:
        session = await self._get_session()
        async with session.get(
            f"{BASE_URL}/devices/{device_id}/status",
            headers=self._headers,
        ) as resp:
            if resp.status == 401:
                await self._refresh()
                return await self.get_device_status(device_id)
            return await resp.json()

    async def execute(self, device_id: str, commands: list[dict]) -> dict:
        session = await self._get_session()
        payload = {"commands": commands}
        async with session.post(
            f"{BASE_URL}/devices/{device_id}/commands",
            headers=self._headers,
            data=json.dumps(payload),
        ) as resp:
            if resp.status == 401:
                await self._refresh()
                return await self.execute(device_id, commands)
            return await resp.json()

    async def get_snapshot_image(self, device_id: str) -> Optional[bytes]:
        try:
            await self.execute(
                device_id,
                [
                    {
                        "component": "main",
                        "capability": "execute",
                        "command": "execute",
                        "arguments": [{"x": {"viewInside": True}}],
                    }
                ],
            )
        except Exception:
            pass
        status = await self.get_device_status(device_id)
        url = None
        try:
            url = status["components"]["main"]["camera"]["snapshot"]["value"]
        except Exception:
            url = None
        if not url:
            return None
        session = await self._get_session()
        async with session.get(url, headers=self._headers) as resp:
            if resp.status != 200:
                return None
            return await resp.read()

    async def upload_media(
        self,
        device_id: str,
        content: bytes,
        filename: str,
        content_type: str = "image/jpeg",
    ) -> dict:
        session = await self._get_session()
        form = aiohttp.FormData()
        form.add_field(
            "file",
            content,
            filename=filename,
            content_type=content_type,
        )
        async with session.post(
            f"{BASE_URL}/devices/{device_id}/media",
            headers={"Authorization": f"Bearer {self._token}"},
            data=form,
        ) as resp:
            if resp.status == 401:
                await self._refresh()
                return await self.upload_media(
                    device_id,
                    content,
                    filename,
                    content_type,
                )
            return await resp.json()
