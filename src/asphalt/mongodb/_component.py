from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from asphalt.core import Component, add_resource
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBComponent(Component):
    """
    Creates an :class:`~motor.motor_asyncio.AsyncIOMotorClient` resource.

    The client will not connect to the target database until it's used for the first
    time.

    :param client_args: a dictionary of keyword arguments to pass to
        :class:`~motor.motor_asyncio.AsyncIOMotorClient`
    """

    def __init__(self, *, client_args: Mapping[str, Any] | None = None):
        options = client_args or {}
        self._client = AsyncIOMotorClient(**options)

    async def start(self) -> None:
        add_resource(
            self._client,
            description="MongoDB client",
            teardown_callback=self._client.close,
        )
