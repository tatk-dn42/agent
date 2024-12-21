# pylint: disable=wrong-import-position
# ruff: noqa: E402, F401
# -*- coding: utf-8 -*-
"""Module for Tunnel related routes"""

from flask_openapi3 import APIBlueprint, Tag

tunnel_tag = Tag(name="tunnels", description="Tunnels")

bp = APIBlueprint("tunnels", __name__, url_prefix="/api/tunnels", abp_tags=[tunnel_tag])

from app.tunnels import routes
from app.tunnels import responses
from app.tunnels import exceptions
