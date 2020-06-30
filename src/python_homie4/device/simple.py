#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import importlib
from .base import BaseDevice
from ..node import BaseNode
from .helpers import generate_device_id
import logging

logger = logging.getLogger(__name__)


class SimpleDevice(BaseDevice):
    """A simple device, which starts with no nodes.
    """

    def __init__(self, device_id=None, name=None,
                 *, node=None, node_init={}, **kwargs):
        """Initializes a SimpleDevice without any nodes.

        Parameters
        ----------
        device_id : str
            Device ID for MQTT topic.

        name : str
            Human readable name of device.

        """
        super().__init__(device_id, name, **kwargs)

    def update_node(self, name, value):
        """Updates the node with `name` with `value`.

        """
        self.get_node(name).update_value(value)
        logger.debug(f"Node '{name}' updated to '{value}'")

    @staticmethod
    def node_from_name(name: str, **kwargs):
        """Returns a new node, which was created from the `name` of the node.

        For example, `node` value of "integer" will return a node of type
        'IntegerNode'. 

        An 'AttributeError' is raised, if the node cannot be created from the `name`.

        Parameters
        ----------
        name : str
            Identifier of the specific class of the node, which should be created.
            For example, `name` of "integer" or "Integer" will be expanded to return
            an instance of 'IntegerNode'.

        **kwargs
            Additional keyword arguments are directly passed to the initializer of
            the node.

        Raises
        ------
        AttributeError
            If the node cannot be created from the given `name`.

        """
        try:
            node_module_name = "node"
            node_id = str(name).lower()   # Ignore all uppercase letters
            # Convert to CamelCase
            node_name = node_id[0].upper() + node_id[1:].lower()

            node_module = importlib.import_module("..."+node_module_name, package=__name__)   # noqa: E501

            node_class_name = node_name + "Node"   # noqa: E501
            Node = getattr(node_module, node_class_name)

            node_obj = Node(node_id, node_name,
                            type_=node_id, **kwargs)

        except ImportError as e:
            logger.error(f"Could not import module with name "
                         + f"'{node_module_name}'. Reason: {e}.")
            raise AttributeError(f"Could not import module with name "
                                 + f"'{node_module_name}'. Reason: {e}.")

        return node_obj