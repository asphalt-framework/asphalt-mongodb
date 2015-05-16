import logging
from functools import partial
from typing import Dict, Any, Union, List

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorReplicaSetClient
from typeguard import check_argument_types

from asphalt.core import Component, Context, merge_config

logger = logging.getLogger(__name__)


class MongoDBComponent(Component):
    """
    Publishes one or more :class:`~motor.motor_asyncio.AsyncIOMotorClient` resources.

    If ``clients`` is given, a MongoDB client resource will be published for each key in the
    dictionary, using the key as the resource name. Any extra keyword arguments to the component
    constructor will be used as defaults for omitted configuration values.

    If ``clients`` is omitted, a single MongoDB client resource (``default`` / ``ctx.mongo``)
    is published using any extra keyword arguments passed to the component.

    The client(s) will not connect to the target database until they're used for the first time.

    :param clients: a dictionary of resource name ⭢ :meth:`configure_client` arguments
    :param default_client_args: default values for omitted :meth:`configure_client` arguments
    """

    def __init__(self, clients: Dict[str, Dict[str, Any]] = None, **default_client_args):
        assert check_argument_types()
        if not clients:
            default_client_args.setdefault('context_attr', 'mongo')
            clients = {'default': default_client_args}

        self.clients = []
        for resource_name, config in clients.items():
            config = merge_config(default_client_args, config)
            config.setdefault('context_attr', resource_name)
            context_attr, client_cls, client_args = self.configure_client(**config)
            self.clients.append((resource_name, context_attr, client_cls, client_args))

    @classmethod
    def configure_client(cls, context_attr: str,
                         address: Union[str, List[str]] = 'localhost:27017', **client_args):
        """
        Configure a MongoDB client.

        If ``address`` contains a comma (``,``) or is a list, then
        :class:`~motor.motor_asyncio.AsyncIOMotorReplicaSetClient` is used instead of
        :class:`~motor.motor_asyncio.AsyncIOMotorClient`.

        :param context_attr: context attribute of the client (if omitted, the resource name
            will be used instead)
        :param address: either host, host:port, UNIX socket path or a list of such addresses
        :param client_args: extra keyword arguments passed to
            :class:`~pymongo.mongo_client.MongoClient`

        """
        assert check_argument_types()
        if isinstance(address, list):
            address = ','.join(address)

        if ',' in address:
            client_cls = AsyncIOMotorReplicaSetClient
            client_args['hosts_or_uri'] = address
        else:
            client_cls = AsyncIOMotorClient
            client_args['host'] = address

        return context_attr, client_cls, client_args

    @staticmethod
    def shutdown_client(event, client, resource_name):
        client.close()
        logger.info('MongoDB client (%s) shut down', resource_name)

    async def start(self, ctx: Context):
        for resource_name, context_attr, client_cls, client_args in self.clients:
            client = client_cls(**client_args)
            ctx.finished.connect(
                partial(self.shutdown_client, client=client, resource_name=resource_name))
            ctx.publish_resource(client, resource_name, context_attr, types=[AsyncIOMotorClient])

            if client_cls is AsyncIOMotorReplicaSetClient:
                nodes = client_args['hosts_or_uri']
            else:
                nodes = client_args['host']

            logger.info('Configured MongoDB client (%s / ctx.%s; nodes=%r)', resource_name,
                        context_attr, nodes)
