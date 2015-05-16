Configuration
-------------

.. highlight:: yaml

The typical MongoDB configuration using a single database at ``localhost`` on the default port
would look like this::

    components:
      mongodb:

The above configuration creates a :class:`motor.motor_asyncio.AsyncIOMotorClient` instance in the
context, available as ``ctx.mongo`` (resource name: ``default``).

If you wanted to connect to ``mongo.example.org`` on port 27020, you would do::

    components:
      mongodb:
        address: mongo.example.org:27020

To connect to a replica set, specify the ``replicaSet`` option and give the node addresses as a
list::

    components:
      mongodb:
        replicaSet: my_replica_set_name
        address:
          - mongo1.example.org
          - mongo2.example.org:27018

To connect to two unrelated MongoDB servers, you could use a configuration like::

    components:
      mongodb:
        clients:
          mongo1:
            address: /run/mongodb.sock
          mongo2:
            address: mongoserver1.example.org
            ssl: true

This configuration creates two :class:`~motor.motor_asyncio.AsyncIOMotorClient` resources,
``mongo1`` and ``mongo2`` (``ctx.mongo1`` and ``ctx.mongo2``) respectively. The first one connects
using a UNIX socket and the second one uses an TLS protected TCP connection on the default port.

.. seealso:: Connection options:
    :meth:`~asphalt.mongodb.component.MongoDBComponent.configure_client`
