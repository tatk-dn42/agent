# pylint: disable=too-few-public-methods
# -*- coding: utf-8 -*-
"""Module for Peer related responses/models"""
from pydantic import BaseModel, Field


class ChannelResponse(BaseModel):
    """Class for ChannelResponse schema"""

    state: str = Field("DOWN", description="State of channel")
    table: str = Field("master4", description="Routing table of channel")
    preference: int = Field(100, description="Preference of channel")
    filter: dict = Field(
        {"input": "", "output": ""}
    )


class PeerResponse(BaseModel):
    """Class for PeerResponse schema"""

    peer_id: str = Field("dn42_blah", description="ID of Peer")
    interface_id: str = Field("dn42-blah", description="ID of Network Interface")
    remote_as: int = Field("64665", description="Remote AS Number")
    local_as: int = Field("64665", description="Local AS Number")
    remote_address: str = Field("10.20.30.40", description="Remote neighbor address")
    local_address: str = Field("10.20.30.40", description="Local address")
    bgp_state: str = Field("Idle", description="State of BGP Session")
    admin_down: bool = Field(False, description="Is BGP session administratively down")

    ipv4: dict = ChannelResponse()
    ipv6: dict = ChannelResponse()

class PeerPath(BaseModel):
    """Path class for searching peers"""

    id: str = Field(..., description='Peer ID')
