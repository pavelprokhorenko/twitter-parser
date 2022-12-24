from asyncio import AbstractEventLoop
from collections.abc import Mapping
from typing import Any, Union

from aiohttp import ClientResponse, ClientSession
from aiohttp.typedefs import StrOrURL
from orjson import dumps


class AsyncHTTPClient:
    """
    HTTP client for asynchronous requests to outer API.
    """

    __slots__ = ["_client_session"]

    def __init__(self) -> None:
        self._client_session: ClientSession | None = None

    async def connect(self, loop: AbstractEventLoop) -> None:
        """
        Create active HTTP session.
        """
        self._client_session = ClientSession(
            loop=loop, json_serialize=lambda data: dumps(data, default=str).decode()
        )

    async def close(self) -> None:
        """
        Close HTTP session.
        """
        await self._client_session.close()

    async def get(
        self,
        url: StrOrURL,
        *,
        json: Union[Mapping[str, Any], None] = None,
        headers: Union[Mapping[str, Any], None] = None,
        cookies: Union[Mapping[str, Any], None] = None,
        **kwargs
    ) -> Any:
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        async with self._client_session.get(
            url, json=json, headers=headers, cookies=cookies, **kwargs
        ) as response:
            response: ClientResponse
            return await response.json()

    async def post(
        self,
        url: StrOrURL,
        *,
        json: Union[Mapping[str, Any], None] = None,
        headers: Union[Mapping[str, Any], None] = None,
        cookies: Union[Mapping[str, Any], None] = None,
        **kwargs
    ) -> Any:
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        async with self._client_session.post(
            url, json=json, headers=headers, cookies=cookies, **kwargs
        ) as response:
            response: ClientResponse
            return await response.json()


async_http_client = AsyncHTTPClient()
