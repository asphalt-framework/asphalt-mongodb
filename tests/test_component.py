import logging
import os

import pytest
from asphalt.core import Context, require_resource
from motor.motor_asyncio import AsyncIOMotorClient
from pytest import LogCaptureFixture

from asphalt.mongodb import MongoDBComponent

MONGODB_HOSTNAME = os.getenv("MONGODB_HOST", "localhost")

pytestmark = pytest.mark.anyio


async def test_default_client(caplog: LogCaptureFixture) -> None:
    """Test that the client is created and is available on the context."""
    caplog.set_level(logging.INFO, "asphalt.mongodb")
    async with Context() as ctx:
        await MongoDBComponent().start(ctx)
        require_resource(AsyncIOMotorClient)

    assert len(caplog.messages) == 2
    assert caplog.messages == [
        "Configured MongoDB client (default; hosts={'localhost:27017'})",
        "MongoDB client (default) shut down",
    ]
