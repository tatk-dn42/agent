# pylint: disable=unspecified-encoding
# -*- coding: utf-8 -*-
"""Module providing services to get IP Address related information from the node"""

import netifaces


def get_loopback_addresses(interface_name: str) -> object:
    """
    Returns an object containing the Loopback addresses of the node.

            Parameters:
                    interface_name (str): Name of the Loopback Interface

            Returns:
                    ip_object (obj): Object containing the Loopback IP address
    """

    # TODO: Handle nodes with or without v4/v6

    ipv4 = netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0]["addr"]
    ipv6 = netifaces.ifaddresses(interface_name)[netifaces.AF_INET6][0]["addr"]

    ip_object = {
        "ipv4": ipv4,
        "ipv6": ipv6,
    }

    return ip_object
