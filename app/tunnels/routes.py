# -*- coding: utf-8 -*-
"""Module for Tunnel related routes"""

import os
import jinja2
from app.tunnels import bp
from app.services import helpers
from jinja2 import FileSystemLoader
from app.services import ip_address
from flask import jsonify, current_app
from flask_jwt_extended import jwt_required
from app.tunnels.requests import TunnelBody
from app.services import tunnels as tunnel_service
from app.tunnels.exceptions import TunnelNotFoundException
from app.tunnels.responses import TunnelResponse, TunnelPath


@bp.get("/", operation_id="get_tunnel_list", responses={200: {}}, security=[{"jwt": []}])
@jwt_required()
def get_tunnel_list():
    """Get All Tunnels
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

@bp.post("/", operation_id="create_tunnel", responses={}, security=[{"jwt": []}])
@jwt_required()
def create_tunnel(body: TunnelBody):
    """Create Tunnel
    Creates a new tunnel
    """

    tunnel_path = current_app.config["AUTO_PEER_TUNNEL_PATH"] + f"{body.name}.conf"
    interface_path = current_app.config["AUTO_PEER_INTERFACE_PATH"] + f"42-{body.name}"

    if os.path.isfile(tunnel_path) or os.path.isfile(interface_path):
        return {
            "code": 400,
            "message": "Session already exists"
        }, 400

    environment = jinja2.Environment(
        loader=FileSystemLoader("app/templates/"),
        trim_blocks=True,
    )

    tunnel_template = environment.get_template("wg_tunnel.conf.j2")
    tunnel_output = tunnel_template.render(
        body
    )

    loopback_interface = current_app.config["LOOPBACK_INTERFACE"]
    loopback_ips = ip_address.get_loopback_addresses(loopback_interface)

    link_local_ips = {}

    if current_app.config["IPV4_LINK_LOCAL"] != "":
        link_local_ips['ipv4'] = current_app.config["IPV4_LINK_LOCAL"]

    if current_app.config["IPV6_LINK_LOCAL"] != "":
        link_local_ips['ipv6'] = current_app.config["IPV6_LINK_LOCAL"]

    interface_template = environment.get_template("wg_interface.conf.j2")
    interface_output = interface_template.render(
        peer_info=body,
        loopback_ips=loopback_ips,
        link_local_ips=link_local_ips
    )

    with open(tunnel_path, "w", encoding="utf-8") as file:
        file.write(tunnel_output)

    with open(interface_path, "w", encoding="utf-8") as file:
        file.write(interface_output)

    helpers.ifdown(body.name, force=True)
    helpers.ifup(body.name)

    return jsonify(body.model_dump()), 201


@bp.delete("/<id>", operation_id="delete_tunnel", responses={},
           security=[{"jwt": []}])
@jwt_required()
def delete_tunnel(path: TunnelPath):
    """Delete Tunnel
    Deletes a given tunnel
    """

    try:
        details = tunnel_service.get_tunnel_details(path.id)
        current_app.logger.debug(details)

    except TunnelNotFoundException:
        return {
            "code": 404,
            "message": "Tunnel not found"
        }, 404

    tunnel_path = current_app.config["AUTO_PEER_TUNNEL_PATH"] + f"{path.id}.conf"
    interface_path = current_app.config["AUTO_PEER_INTERFACE_PATH"] + f"42-{path.id}"

    os.remove(tunnel_path)
    os.remove(interface_path)

    helpers.ip_link_del(path.id)

    return {
        "code": 200,
        "message": "Session deleted"
    }, 200