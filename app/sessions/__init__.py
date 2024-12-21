# pylint: disable=wrong-import-position
# ruff: noqa: E402, F401
# -*- coding: utf-8 -*-
"""Module for Session related routes"""

from flask_openapi3 import APIBlueprint, Tag

session_tag = Tag(name="sessions", description="BGP Sessions")

bp = APIBlueprint("sessions", __name__, url_prefix="/api/sessions", abp_tags=[session_tag])

from app.sessions import routes
from app.sessions import requests
from app.sessions import responses
from app.sessions import exceptions
