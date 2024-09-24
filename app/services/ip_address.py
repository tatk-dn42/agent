import netifaces as ni


def get_link_local_address(interface_name: str) -> object:

    ipv4 = ni.ifaddresses(interface_name)[ni.AF_INET][0]["addr"]
    ipv6 = ni.ifaddresses(interface_name)[ni.AF_INET6][0]["addr"]

    ip_object = {
        "ipv4": ipv4,
        "ipv6": ipv6,
    }

    return ip_object
