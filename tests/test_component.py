import pytest
from asphalt.core import Context
from motor.motor_asyncio import AsyncIOMotorClient

from asphalt.mongodb.component import MongoDBComponent


@pytest.mark.asyncio
async def test_default_client(caplog):
    """Test that the default connection is started and is available on the context."""
    async with Context() as context:
        await MongoDBComponent().start(context)
        assert isinstance(context.mongo, AsyncIOMotorClient)

    records = [record for record in caplog.records if record.name == 'asphalt.mongodb.component']
    records.sort(key=lambda r: r.message)
    assert len(records) == 2
    assert records[0].message == ("Configured MongoDB client (default / ctx.mongo; "
                                  "hosts={'localhost:27017'})")
    assert records[1].message == 'MongoDB client (default) shut down'


@pytest.mark.asyncio
async def test_multiple_clients(caplog):
    """Test that a multiple connection configuration works as intended."""
    async with Context() as context:
        await MongoDBComponent(clients={
            'db1': {'host': 'localhost:27018'},
            'db2': {'host': '/tmp/mongodb.sock', 'ssl': True}
        }).start(context)
        assert isinstance(context.db1, AsyncIOMotorClient)
        assert isinstance(context.db2, AsyncIOMotorClient)

    records = [record for record in caplog.records if record.name == 'asphalt.mongodb.component']
    records.sort(key=lambda r: r.message)
    assert len(records) == 4
    assert records[0].message == ("Configured MongoDB client (db1 / ctx.db1; "
                                  "hosts={'localhost:27018'})")
    assert records[1].message == ("Configured MongoDB client (db2 / ctx.db2; "
                                  "hosts={'/tmp/mongodb.sock'})")
    assert records[2].message == 'MongoDB client (db1) shut down'
    assert records[3].message == 'MongoDB client (db2) shut down'


@pytest.mark.asyncio
async def test_create_remove_document():
    """Test the client against a real MongoDB server."""
    async with Context() as context:
        await MongoDBComponent().start(context)
        collection = context.mongo['testdb']['testcollection']
        document = {'somekey': 'somevalue'}
        document2 = {'otherkey': 7}
        try:
            await collection.insert(document)
            await collection.insert(document2)
            documents = await collection.find().to_list(None)
            assert documents == [document, document2]
        finally:
            await context.mongo.drop_database('testdb')
