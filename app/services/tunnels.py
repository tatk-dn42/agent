# pylint: disable=unspecified-encoding
# -*- coding: utf-8 -*-
"""Module providing services to get tunnel related information from the node"""

import netifaces
from flask import current_app

from app.services import helpers


def get_tunnels() -> list:
    """
    Returns the list of tunnels on the node.

            Returns:
                    tunnels (list): List of tunnels
    """

    tunnels = [
        interface
        for interface in netifaces.interfaces()
        if interface.startswith(current_app.config["AUTO_PEER_PREFIX"].lower())
    ]

    return tunnels


def get_tunnel_details(tunnel: str) -> dict:
    """
        Returns the details of a tunnel on the node.

                Returns:
                        tunnel (dict): Tunnel details
        """

    tunnel_command = helpers.parse_wg_output(helpers.run_wg_command(f"show {tunnel}"))

    return tunnel_command
