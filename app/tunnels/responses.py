# pylint: disable=too-few-public-methods
# -*- coding: utf-8 -*-
"""Module for Tunnel related responses/models"""
from enum import Enum

from pydantic import BaseModel, Field


class TunnelType(str, Enum):
    """Class for TunnelType Enum"""

    WIREGUARD = "wireguard"


class WgPeerResponse(BaseModel):
    """Class for WgPeerResponse schema"""

    endpoint: str = Field("", description="Endpoint of Peer")
    handshake: str = Field("", description="Last Handshake")
    public_key: str = Field("", description="Public Key of Peer")
    allowed_ips: list = [str]
    transfer: dict = {"sent": str, "received": str}


class TunnelResponse(BaseModel):
    """Class for TunnelResponse schema"""

    tunnel_id: str = Field("", description="ID of Tunnel")
    interface_id: str = Field("", description="ID of Interface")
    tunnel_type: TunnelType = TunnelType.WIREGUARD
    port: int = Field("", description="Listen Port")
    public_key: str = Field("", description="Public Key")
    peer: dict = WgPeerResponse()


class TunnelPath(BaseModel):
    """Path class for searching tunnels"""

    id: str = Field(..., description='Tunnel ID')
