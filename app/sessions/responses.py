# pylint: disable=too-few-public-methods
# -*- coding: utf-8 -*-
"""Module for Session related responses/models"""
from pydantic import BaseModel, Field


class ChannelResponse(BaseModel):
    """Class for ChannelResponse schema"""

    state: str = Field("DOWN", description="State of channel")
    table: str = Field("master4", description="Routing table of channel")
    preference: int = Field(100, description="Preference of channel")
    filter: dict = Field(
        {"input": "", "output": ""}
    )


class SessionResponse(BaseModel):
    """Class for SessionResponse schema"""

    session_id: str = Field("", description="ID of Session")
    interface_id: str = Field("", description="ID of Network Interface")
    remote_as: int = Field("", description="Remote AS Number")
    local_as: int = Field("", description="Local AS Number")
    remote_address: str = Field("", description="Remote neighbor address")
    local_address: str = Field("", description="Local address")
    bgp_state: str = Field("", description="State of BGP Session")
    admin_down: bool = Field(False, description="Is BGP session administratively down")

    ipv4: dict = ChannelResponse()
    ipv6: dict = ChannelResponse()


class SessionPath(BaseModel):
    """Path class for searching sessions"""

    id: str = Field(..., description='Session ID')
