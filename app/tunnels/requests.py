# pylint: disable=too-few-public-methods
# -*- coding: utf-8 -*-
"""Module for Tunnel related requests"""
from enum import Enum
from pydantic import BaseModel, Field

class TunnelBody(BaseModel):
    """Class for TunnelBody schema"""

    name: str = Field(None, description="Name of tunnel")
    protocol: str = Field("wireguard", description="Protocol of tunnel")
    local_port: int = Field(51820, description="Local port of tunnel")
    remote_port: int = Field(51820, description="Remote port of tunnel")
    endpoint: str = Field("", description="Remote endpoint of tunnel")
    public_key: str = Field("", description="Remote public key of tunnel")
    pre_shared_key: str = Field("", description="Pre shared key of tunnel")
    allowed_ips: str = Field("0.0.0.0/0, ::/0", description="Allowed IPs of tunnel")
    mtu: int = Field(1280, description="MTU of tunnel")

    ip_addresses: dict | None = Field(
        default=None,
        description="IP addresses for the tunnel (optional)"
    )
