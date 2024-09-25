# pylint: disable=too-few-public-methods
# -*- coding: utf-8 -*-
"""Module for Metadata related responses/models"""

from enum import Enum
from pydantic import BaseModel, Field


class PeeringPolicy(str, Enum):
    """Class for PeeringPolicy Enum"""

    OPEN = "Open"
    SELECTIVE = "Selective"
    CLOSED = "Closed"


class InfoResponse(BaseModel):
    """Class for InfoResponse schema"""

    id: str = Field("rt0.test", description="ID of node")
    fqdn: str = Field(
        "rt0.test.tatk.network", description="Fully qualified domain name of node"
    )
    agent_version: str = Field("1.0.0", description="Version of agent installed")
    current_peers: int = Field(24, description="Number of peers")
    peer_limit: int = Field(50, description="Maximum peers")
    loopback_ips: dict = Field(
        {"ipv4": "127.0.0.1", "ipv6": "::1"}
    )
    link_local_ips: dict = Field(
        {"ipv4": "203.0.113.123", "ipv6": "2001:0db8:0000:0000:0000:0000:0000:0000"}
    )
    peering_policy: PeeringPolicy = PeeringPolicy.OPEN
    protocols: dict = Field({"wireguard": {"enabled": True, "public_key": ""}})
