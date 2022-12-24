from asyncio import AbstractEventLoop, get_event_loop
from os import system

from fastapi.applications import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run

from app.api.endpoints.routers import api_router
from app.async_client import async_http_client
from settings import Settings, settings


class Service:
    __slots__ = ["_loop", "_settings", "_asgi_app"]

    def __init__(self, service_settings: Settings) -> None:
        """
        Initiation ASGI app.
        """
        self._loop: AbstractEventLoop | None = None
        self._settings = service_settings

        middleware = [
            Middleware(
                CORSMiddleware,
                allow_origins=self._settings.service.origins,
                allow_credentials=True,
                allow_methods=["POST"],
                allow_headers=["*"],
            ),
        ]

        self._asgi_app = FastAPI(
            middleware=middleware,
            on_startup=[self._open_connections],
            on_shutdown=[self._close_connections],
        )
        self._asgi_app.include_router(api_router)

    def get_app(self) -> FastAPI:
        """
        Get ASGI app.
        """
        return self._asgi_app

    def serve(self, path_to_app: str) -> None:
        """
        Start service.
        """
        if self._settings.service.debug:
            run(
                path_to_app,
                host=self._settings.service.host,
                port=self._settings.service.port,
                reload=True,
                use_colors=True,
            )
        else:
            system(
                f"uvicorn {path_to_app} --host"
                f" {self._settings.service.host} --port"
                f" {self._settings.service.port} --workers"
                f" {self._settings.service.workers}"
            )

    def _update_event_loop(self) -> None:
        """
        Initiation current event loop.
        """
        if not self._loop:
            self._loop = get_event_loop()

        self._loop.set_debug(self._settings.service.debug)

    async def _open_connections(self) -> None:
        """
        Open connections to all necessary services.
        """
        await async_http_client.connect(self._loop)

    async def _close_connections(self) -> None:
        """
        Close connections to all necessary services.
        """
        await async_http_client.close()


service = Service(service_settings=settings)
