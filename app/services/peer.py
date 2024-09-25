# pylint: disable=unspecified-encoding
# -*- coding: utf-8 -*-
"""Module providing services to get Peer related information from the node"""

import re
import subprocess
from flask import current_app


def parse_protocols_output(contents):
    """
    Parses the output of the Bird "Protocols" command.

            Parameters:
                    contents: Contents of the command output

            Returns:
                    output (list): List containing list items for each protocol
    """

    output = []

    for line in contents:
        line = line.decode("utf-8")
        line = line.strip("\n")
        output.append(re.split(r"\s+(?=\S)", line, maxsplit=6))

    return output


def get_peer_count() -> int:
    """
    Returns the count of automatic BGP peers on the node.

            Returns:
                    peers (int): Count of peers
    """

    protocols = subprocess.Popen("birdc -r" + " show protocols" +
                                 "| tail -n+4", shell=True, stdout=subprocess.PIPE)
    peers = parse_protocols_output(protocols.stdout)
    protocols.stdout.close()
    protocols.wait()

    peers = [
        peer
        for peer in peers
        if peer[1] == "BGP"
           and peer[0].startswith(current_app.config["AUTO_PEER_PREFIX"])
    ]

    return len(peers)
