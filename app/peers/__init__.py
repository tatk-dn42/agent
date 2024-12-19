# pylint: disable=wrong-import-position
# ruff: noqa: E402, F401
# -*- coding: utf-8 -*-
"""Module for Peering related routes"""

from flask_openapi3 import APIBlueprint, Tag


peer_tag = Tag(name="peers", description="Peers")

bp = APIBlueprint("peers", __name__, url_prefix="/api/peers", abp_tags=[peer_tag])

from app.peers import routes
