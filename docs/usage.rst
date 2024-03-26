Using the MongoDB client
========================

The MongoDB clients made available in the context are objects compatible with the
:class:`~motor.motor_asyncio.AsyncIOMotorClient` API. As such, refer to Motor's
`asyncio tutorial`_ and `api documentation`_ for details.

An example demonstrating the use of the client in Asphalt::

    from asphalt.core import inject, resource

    @inject
    async def handler(*, mongodb: AsyncIOMotorClient = resource() -> None:
        # Insert a document to somecollection in somedb
        collection = mongodb.somedb.somecollection
        document = {'key': 'value'}
        obj_id = await collection.insert(document)

        # Delete the document
        await collection.remove(obj_id)

.. _asyncio tutorial: https://motor.readthedocs.io/en/stable/tutorial-asyncio.html
.. _api documentation: https://motor.readthedocs.io/en/stable/api/index.html
