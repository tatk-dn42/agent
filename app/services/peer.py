# pylint: disable=unspecified-encoding
# -*- coding: utf-8 -*-
"""Module providing services to get Peer related information from the node"""

import re
from flask import current_app


def parse_protocols_output(contents: str):
    """
    Parses the output of the Bird "Protocols" command.

            Parameters:
                    contents (str): Contents of the command output

            Returns:
                    output (list): List containing list items for each protocol
    """

    output = []

    for line in contents:
        line = line.strip("\n")
        output.append(re.split(r"\s+(?=\S)", line, maxsplit=6))

    return output


def get_peer_count() -> int:
    """
    Returns the count of automatic BGP peers on the node.

            Returns:
                    peers (int): Count of peers
    """

    # TODO: Retrieve information from Bird directly
    with open("/app/bird_output", "rt") as input_file:
        peers = parse_protocols_output(input_file)

    peers = [
        peer
        for peer in peers
        if peer[1] == "BGP"
           and peer[0].startswith(current_app.config["AUTO_PEER_PREFIX"])
    ]

    return len(peers)
