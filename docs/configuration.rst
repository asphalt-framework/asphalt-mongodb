Configuration
-------------

.. highlight:: yaml

The typical MongoDB configuration using a single database at ``localhost`` on the
default port would look like this::

    components:
      mongodb:

The above configuration creates a :class:`motor.motor_asyncio.AsyncIOMotorClient`
resource in the context (resource name: ``default``).

The most important option for specifying the server address(es) is ``host``. It can be
either a host name, a ``hostname:port`` combination or a ``mongo://`` URI, as specified
by the `MongoDB documentation`_. For more options, refer to the documentation of the
:class:`~pymongo.mongo_client.MongoClient` class.

If you wanted to connect to ``mongo.example.org`` on port 27020, you would do::

    components:
      mongodb:
        host: mongo.example.org:27020

To connect to a replica set, you can use a URI like this::

    components:
      mongodb:
        host: mongo2.example.org:27018/?replicaSet=my_replica_set_name

.. _MongoDB documentation: https://docs.mongodb.com/manual/reference/connection-string/
