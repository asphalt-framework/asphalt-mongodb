import logging
import os

import pytest
from asphalt.core import Context, get_resource_nowait
from motor.motor_asyncio import AsyncIOMotorClient
from pytest import LogCaptureFixture

from asphalt.mongodb import MongoDBComponent

MONGODB_HOSTNAME = os.getenv("MONGODB_HOST", "localhost")

pytestmark = pytest.mark.anyio


async def test_default_client(caplog: LogCaptureFixture) -> None:
    """Test that the client is created and is available on the context."""
    caplog.set_level(logging.INFO, "asphalt.mongodb")
    async with Context():
        await MongoDBComponent().start()
        get_resource_nowait(AsyncIOMotorClient)

    assert len(caplog.messages) == 1
    assert caplog.messages == [
        "Configured MongoDB client (default; hosts={'localhost:27017'})"
    ]
