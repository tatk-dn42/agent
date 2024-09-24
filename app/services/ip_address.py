# pylint: disable=unspecified-encoding
# -*- coding: utf-8 -*-
"""Module providing services to get IP Address related information from the node"""

import netifaces as ni


def get_link_local_address(interface_name: str) -> object:
    """
    Returns an object containing the Link Local IP address of the node.

            Parameters:
                    interface_name (str): Name of the Link Local Interface

            Returns:
                    ip_object (obj): Object containing the Link Local IP address
    """

    # TODO: Handle nodes with or without v4/v6

    ipv4 = ni.ifaddresses(interface_name)[ni.AF_INET][0]["addr"]
    ipv6 = ni.ifaddresses(interface_name)[ni.AF_INET6][0]["addr"]

    ip_object = {
        "ipv4": ipv4,
        "ipv6": ipv6,
    }

    return ip_object
