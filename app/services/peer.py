# pylint: disable=unspecified-encoding
# -*- coding: utf-8 -*-
"""Module providing services to get Peer related information from the node"""

from flask import current_app

from app.peers.exceptions import PeerNotFoundException
from app.services import helpers


def get_peers() -> list:
    """
    Returns the list of automatic BGP peers on the node.

            Returns:
                    peers (list): List of peers
    """

    peer_command = helpers.run_command("birdc show protocols")
    peers = helpers.parse_protocols_output(peer_command)

    peers = [
        peer
        for peer in peers
        if peer[1] == "BGP"
           and peer[0].startswith(current_app.config["AUTO_PEER_PREFIX"])
    ]

    return peers


def get_peer_detail(peer) -> dict:
    """
    Fetches the detailed information about a Bird Peer

            Returns:
                    peers (dict): List of peers
    """

    peer_command = helpers.run_command(f"birdc show protocols all {peer}")

    if "CF_SYM_UNDEFINED" in peer_command:
        raise PeerNotFoundException("Peer not found")

    return helpers.parse_bgp_info(peer_command)
