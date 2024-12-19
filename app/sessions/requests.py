# -*- coding: utf-8 -*-
"""Module for Session related exceptions"""
from pydantic import BaseModel, Field


class SessionBody(BaseModel):
    session_id: str = Field(None, description="ID of peering session")
    interface_id: str = Field(None, description="ID of interface to create session on")
    remote_address: str = Field(None, description="Remote address to establish peering session with")
    remote_as: int = Field(None, description="Remote ASN to establish peering session with")
