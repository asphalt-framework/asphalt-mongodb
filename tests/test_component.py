import os

import pytest
from asphalt.core import Context, get_resource_nowait
from motor.motor_asyncio import AsyncIOMotorClient

from asphalt.mongodb import MongoDBComponent

MONGODB_HOSTNAME = os.getenv("MONGODB_HOST", "localhost")

pytestmark = pytest.mark.anyio


async def test_default_client() -> None:
    """Test that the client is created and is available on the context."""
    async with Context():
        await MongoDBComponent().start()
        get_resource_nowait(AsyncIOMotorClient)
