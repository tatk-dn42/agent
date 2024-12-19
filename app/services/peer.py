# pylint: disable=unspecified-encoding
# -*- coding: utf-8 -*-
"""Module providing services to get Peer related information from the node"""

from flask import current_app

from app.services import helpers
from app.sessions.exceptions import SessionNotFoundException


def get_peers() -> list:
    """
    Returns the list of automatic BGP sessions on the node.

            Returns:
                    sessions (list): List of sessions
    """

    peer_command = helpers.run_bird_command("show protocols")
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
                    sessions (dict): List of sessions
    """

    peer_command = helpers.run_bird_command(f"show protocols all {peer}")

    if "CF_SYM_UNDEFINED" in peer_command:
        raise SessionNotFoundException("Session not found")

    return helpers.parse_bgp_info(peer_command)
