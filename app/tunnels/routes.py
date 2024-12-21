# -*- coding: utf-8 -*-
"""Module for Tunnel related routes"""

from flask import jsonify
from flask_jwt_extended import jwt_required

from app.services import tunnels as tunnel_service
from app.tunnels import bp
from app.tunnels.exceptions import TunnelNotFoundException
from app.tunnels.responses import TunnelResponse, TunnelPath


@bp.get("/", operation_id="get_tunnel_list", responses={200: {}}, security=[{"jwt": []}])
@jwt_required()
def get_tunnel_list():
    """Get list of tunnels
    Gets list of tunnels from node
    """

    interfaces = tunnel_service.get_tunnels()

    tunnel_list = []

    for interface in interfaces:
        details = tunnel_service.get_tunnel_details(interface)
        details["tunnel_id"] = interface
        tunnel_list.append(TunnelResponse.model_validate(details).model_dump())

    return jsonify(tunnel_list)


@bp.get("/<id>", operation_id="get_tunnel", responses={200: TunnelResponse},
        security=[{"jwt": []}])
@jwt_required()
def get_tunnel(path: TunnelPath):
    """Get Tunnel Details
    Gets details of a tunnel from node
    """

    try:
        details = tunnel_service.get_tunnel_details(path.id)
    except TunnelNotFoundException:
        return {
            "code": 404,
            "message": "Tunnel not found"
        }, 404

    return jsonify(TunnelResponse.model_validate(details).model_dump())
