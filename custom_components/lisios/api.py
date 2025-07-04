"""Lisios API client."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import aiohttp


API_URL = "https://stbl.lisios-ops.de/v1"


class LisiosApiClient:
    """Lisios API client."""

    _token: str | None

    def __init__(
        self,
        session: aiohttp.ClientSession,
        token: str | None = None,
    ) -> None:
        """Initialize."""
        self._session = session
        self._token = token

    async def login(self, username: str, password: str) -> str:
        """Login to the Lisios API and return the access token."""
        url = f"{API_URL}/app/users/login"
        json = {"email": username, "password": password}
        async with self._session.post(url, json=json) as resp:
            resp.raise_for_status()
            json = await resp.json()
            token: str = json["access_token"]
            self._token = token
            return token

    async def me(self) -> Any:
        """Get the current user's data."""
        url = f"{API_URL}/app/users/me"
        headers = {"Authorization": f"Bearer {self._token}"}
        async with self._session.get(url, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def device_data(self, device_id: str) -> Any:
        """Get data for a specific device."""
        url = f"{API_URL}/devices"
        params = {"device_id": device_id}
        headers = {"Authorization": f"Bearer {self._token}"}
        async with self._session.get(url, params=params, headers=headers) as resp:
            resp.raise_for_status()
            return await resp.json()
