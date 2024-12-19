# pylint: disable=too-many-branches
# -*- coding: utf-8 -*-
"""Module providing helper functions for processing"""

import ipaddress
import re
import shlex
import subprocess


def run_bird_command(command, timeout=3, restricted=True):
    """
        Runs a Bird command and retrieves the output.

                Parameters:
                        command (str): Bird command to run
                        timeout (int): Command timeout in seconds
                        restricted (bool): Whether to run command in restricted mode

                Returns:
                        output (str): Command output
        """
    try:
        bird_prefix = 'birdc -r ' if restricted else 'birdc '
        command = bird_prefix + command

        output = (
            subprocess.check_output(shlex.split(command), timeout=timeout, stderr=subprocess.STDOUT)
            .decode('utf-8')
            .strip()
        )
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8').strip()
    return output

def parse_protocols_output(contents):
    """
    Parses the output of the Bird "Protocols" command.

            Parameters:
                    contents: Contents of the command output

            Returns:
                    output (list): List containing list items for each protocol
    """

    output = []

    for line in contents.splitlines():
        line = line.strip("\n")

        if line.startswith("BIRD") or line.startswith("Name") or line.startswith("Access"):
            continue

        output.append(re.split(r"\s+(?=\S)", line, maxsplit=6))

    return output

def parse_bgp_info(contents):
    """
    Parses the output of the Bird "Protocols All" command.

            Parameters:
                    contents (str): Contents of the command output

            Returns:
                    bgp_info (dict): Dict containing protocol info
    """

    lines = contents.split("\n")
    bgp_info = {"timer": {}}
    current_channel = None

    for line in lines:
        line = line.strip()
        if line.startswith("BGP state:"):
            bgp_info["bgp_state"] = line.split(":")[1].strip()
            bgp_info["admin_down"] = line.split(":")[1].strip() == "Down"
        elif line.startswith("Neighbor address:"):
            neighbor_address = line.split(":",1)[1].strip()
            neighbor_address = neighbor_address.split("%")
            bgp_info["remote_address"] = neighbor_address[0]
            bgp_info["interface_id"] = neighbor_address[1]
        elif line.startswith("Neighbor AS:"):
            bgp_info["remote_as"] = int(line.split(":")[1].strip())
        elif line.startswith("Local AS:"):
            bgp_info["local_as"] = int(line.split(":")[1].strip())
        elif line.startswith("Neighbor ID:"):
            bgp_info["neighbor_id"] = line.split(":")[1].strip()
        elif line.startswith("Session:"):
            bgp_info["session"] = line.split(":")[1].strip()
        elif line.startswith("Source address:"):
            bgp_info["local_address"] = line.split(":", 1)[1].strip()
        elif line.startswith("Hold timer:"):
            bgp_info["timer"]["hold"] = line.split(":")[1].strip()
        elif line.startswith("Keepalive timer:"):
            bgp_info["timer"]["keepalive"] = line.split(":")[1].strip()
        elif line.startswith("Send hold timer:"):
            bgp_info["timer"]["send_hold"] = line.split(":")[1].strip()
        elif line.startswith("Channel"):
            current_channel = line.split()[1]
            bgp_info[current_channel] = {"filter": {}}
        elif current_channel:
            if line.startswith("State:"):
                bgp_info[current_channel]["state"] = line.split(":")[1].strip()
            elif line.startswith("Table:"):
                bgp_info[current_channel]["table"] = line.split(":")[1].strip()
            elif line.startswith("Preference:"):
                bgp_info[current_channel]["pref"] = int(
                    line.split(":")[1].strip()
                )
            elif line.startswith("Input filter:"):
                bgp_info[current_channel]["filter"]["input"] = line.split(":")[1].strip()
            elif line.startswith("Output filter:"):
                bgp_info[current_channel]["filter"]["output"] = line.split(":")[1].strip()
            elif line.startswith("Routes:"):
                routes = line.split(":")[1].strip().split(", ")
                bgp_info[current_channel]["routes"] = {
                    "imported": int(routes[0].split()[0]),
                    "exported": int(routes[1].split()[0]),
                    "preferred": int(routes[2].split()[0]),
                }
            elif line.startswith("BGP Next hop:"):
                bgp_info[current_channel]["next_hop"] = line.split(":")[1].strip()

    return bgp_info


def get_dn42_communities(endpoint, source):
    """
    Processes DN42 Endpoint to produce BGP communities.

            Parameters:
                    endpoint (str): Endpoint to check
                    source (str): Source address or interface

            Returns:
                    communities (dict): Dict containing community info
    """

    ping_output = ping(endpoint, interface=source)

    if not ping_output:
        return False

    match float(ping_output["average"]):
        case num if 0 <= num < 2.7:
            latency = 1
        case num if 2.7 <= num < 7.3:
            latency = 2
        case num if 7.3 <= num < 20:
            latency = 3
        case num if 20 <= num < 55:
            latency = 4
        case num if 55 <= num < 148:
            latency = 5
        case num if 148 <= num < 403:
            latency = 6
        case num if 403 <= num < 1097:
            latency = 7
        case num if 1097 <= num < 2981:
            latency = 8
        case _:
            latency = 9

    return {
        "latency": latency,
        "bandwidth": 24,
        "encryption": 34
    }


def ping(host, interface, ping_count=3):
    ip = ipaddress.ip_address(host)

    rtt = {}

    if ip.version == 4:
        output = subprocess.run(["ping", "-c", str(ping_count), "-I", interface, host], capture_output=True)

    elif ip.version == 6:
        output = subprocess.run(["ping6", "-c", str(ping_count), "-I", interface, host], capture_output=True)
    else:
        return False

    if output.returncode != 0:
        # Endpoint unreachable
        return False

    for line in output.stdout.decode("utf-8").split('\n'):
        if line.startswith("rtt"):
            rtt["min"] = line.split('=')[1].split('/')[0].lstrip()
            rtt["max"] = line.split('=')[1].split('/')[1]
            rtt["average"] = line.split('=')[1].split('/')[2]

    return rtt
