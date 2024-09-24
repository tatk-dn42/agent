import re


def parse_protocols_output(contents):
    output = []

    for line in contents:
        line = line.strip("\n")
        output.append(re.split(r"\s+(?=\S)", line, maxsplit=6))

    return output


def get_peer_count() -> int:
    with open("/app/bird_output", "rt") as input_file:
        peers = parse_protocols_output(input_file)

    peers = [peer for peer in peers if peer[1] == "BGP" and peer[0].startswith("dn42")]

    return len(peers)
