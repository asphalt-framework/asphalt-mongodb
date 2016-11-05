Configuration
-------------

.. highlight:: yaml

The typical MongoDB configuration using a single database at ``localhost`` on the default port
would look like this::

    components:
      mongodb:

The above configuration creates a :class:`motor.motor_asyncio.AsyncIOMotorClient` instance in the
context, available as ``ctx.mongo`` (resource name: ``default``).

The most important option for specifying the server address(es) is ``host``. It can be either a
host name or a ``mongo://`` URI, as specified by the `MongoDB documentation`_.
For more options, refer to the documentation of the :class:`~pymongo.mongo_client.MongoClient`
class.

If you wanted to connect to ``mongo.example.org`` on port 27020, you would do::

    components:
      mongodb:
        host: mongo://mongo.example.org:27020

To connect to a replica set, you can use a URI like this::

    components:
      mongodb:
        host: mongo://mongo1.example.org,mongo2.example.org:27018/?replicaSet=my_replica_set_name

To connect to two unrelated MongoDB servers, you could use a configuration like::

    components:
      mongodb:
        clients:
          mongo1:
            host: /run/mongodb.sock
          mongo2:
            context_attr: othermongo
            host: mongoserver1.example.org
            ssl: true

This configuration creates two :class:`~motor.motor_asyncio.AsyncIOMotorClient` resources,
``mongo1`` and ``mongo2`` (``ctx.mongo1`` and ``ctx.othermongo``) respectively. The first one
connects using a UNIX socket and the second one uses a TLS protected TCP connection.

.. _MongoDB documentation: https://docs.mongodb.com/manual/reference/connection-string/