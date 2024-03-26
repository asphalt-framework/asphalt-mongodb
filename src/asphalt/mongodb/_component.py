from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from asphalt.core import Component, add_resource
from motor.motor_asyncio import AsyncIOMotorClient

logger = logging.getLogger("asphalt.mongodb")


class MongoDBComponent(Component):
    """
    Creates an :class:`~motor.motor_asyncio.AsyncIOMotorClient` resource.

    The client will not connect to the target database until it's used for the first
    time.

    :param client_args: a dictionary of keyword arguments to pass to
        :class:`~motor.motor_asyncio.AsyncIOMotorClient`
    :param resource_name: default values for omitted
        :class:`~motor.motor_asyncio.AsyncIOMotorClient` arguments
    """

    def __init__(
        self,
        *,
        client_args: Mapping[str, Any] | None = None,
        resource_name: str = "default",
    ):
        options = client_args or {}
        self._client = AsyncIOMotorClient(**options)
        self.resource_name = resource_name

    async def start(self) -> None:
        add_resource(
            self._client,
            self.resource_name,
            description="MongoDB client",
            teardown_callback=self._client.close,
        )
        hosts = {
            f"{host}:{port}"
            for host, port in self._client.topology_description.server_descriptions()
        }
        logger.info(
            "Configured MongoDB client (%s; hosts=%r)",
            self.resource_name,
            hosts,
        )
