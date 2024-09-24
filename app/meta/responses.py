from pydantic import BaseModel, Field
from enum import Enum


class PeeringPolicy(str, Enum):
    open = "Open"
    selective = "Selective"
    closed = "Closed"


class InfoResponse(BaseModel):
    id: str = Field("rt0.test", description="ID of node")
    fqdn: str = Field(
        "rt0.test.tatk.network", description="Fully qualified domain name of node"
    )
    current_peers: int = Field(24, description="Number of peers")
    peer_limit: int = Field(50, description="Maximum peers")
    link_local_ips: dict = Field(
        {"ipv4": "203.0.113.123", "ipv6": "2001:0db8:0000:0000:0000:0000:0000:0000"}
    )
    peering_policy: PeeringPolicy = PeeringPolicy.open
    protocols: dict = Field({"wireguard": {"enabled": True, "public_key": ""}})
