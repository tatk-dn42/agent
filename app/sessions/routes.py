# -*- coding: utf-8 -*-
"""Module for Session related routes"""

import os

import jinja2
from flask import jsonify, current_app
from flask_jwt_extended import jwt_required
from jinja2 import FileSystemLoader

from app.services import helpers
from app.services import peer as peer_service
from app.sessions import bp
from app.sessions.exceptions import SessionNotFoundException
from app.sessions.requests import SessionBody
from app.sessions.responses import SessionPath, SessionResponse


@bp.get("/", operation_id="get_session_list", responses={200: {}}, security=[{"jwt": []}])
@jwt_required()
def get_session_list():
    """Get list of sessions
    Gets list of BGP sessions from node
    """

    peers = peer_service.get_peers()
    peer_list = []

    for peer in peers:
        details = peer_service.get_peer_detail(peer[0])
        details["session_id"] = peer[0]
        peer_list.append(SessionResponse.model_validate(details).model_dump())

    return jsonify(peer_list)


@bp.get("/<id>", operation_id="get_session", responses={200: SessionResponse},
        security=[{"jwt": []}])
@jwt_required()
def get_session(path: SessionPath):
    """Get Session Details
    Gets details of BGP session from node
    """

    try:
        peer_detail = peer_service.get_peer_detail(path.id)
        peer_detail["session_id"] = path.id
    except SessionNotFoundException:
        return {
            "code": 404,
            "message": "Session not found"
        }, 404

    return jsonify(SessionResponse.model_validate(peer_detail).model_dump())


@bp.post("/<id>/disable", operation_id="disable_session", responses={}, security=[{"jwt": []}])
@jwt_required()
def disable_session(path: SessionPath):
    """Disable session
    Disables given BGP session
    """

    try:
        peer = peer_service.get_peer_detail(path.id)
    except SessionNotFoundException:
        return {
            "code": 404,
            "message": "Session not found"
        }, 404

    if peer["bgp_state"] == "Down":
        return {
            "code": 422,
            "message": "Session is already disabled"
        }, 422

    helpers.run_bird_command(f"disable {path.id}", restricted=False)

    return {
        "code": 200,
        "message": "Session has been disabled"
    }, 200


@bp.post("/<id>/enable", operation_id="enable_session", responses={}, security=[{"jwt": []}])
@jwt_required()
def enable_session(path: SessionPath):
    """Enable session
    Enables given BGP session
    """

    try:
        peer = peer_service.get_peer_detail(path.id)
    except SessionNotFoundException:
        return {
            "code": 404,
            "message": "Session not found"
        }, 404

    if peer["bgp_state"] != "Down":
        return {
            "code": 422,
            "message": "Session is already enabled"
        }, 422

    helpers.run_bird_command(f"enable {path.id}", restricted=False)

    return {
        "code": 200,
        "message": "Session has been enabled"
    }, 200


@bp.post("/<id>/restart", operation_id="restart_session", responses={}, security=[{"jwt": []}])
@jwt_required()
def restart_session(path: SessionPath):
    """Restart session
    Restart given BGP session
    """

    try:
        peer_service.get_peer_detail(path.id)
    except SessionNotFoundException:
        return {
            "code": 404,
            "message": "Session not found"
        }, 404

    helpers.run_bird_command(f"restart {path.id}", restricted=False)

    return {
        "code": 200,
        "message": "Session has been restarted"
    }, 200


@bp.post("/<id>/reload", operation_id="reload_session", responses={}, security=[{"jwt": []}])
@jwt_required()
def reload_session(path: SessionPath):
    """Reload session
    Reload given BGP session
    """

    try:
        peer_service.get_peer_detail(path.id)
    except SessionNotFoundException:
        return {
            "code": 404,
            "message": "Session not found"
        }, 404

    helpers.run_bird_command(f"reload {path.id}", restricted=False)

    return {
        "code": 200,
        "message": "Session has been reloaded"
    }, 200


@bp.post("/", operation_id="create_session", responses={}, security=[{"jwt": []}])
@jwt_required()
def create_session(body: SessionBody):
    """Create session
    Creates a new session
    """

    # TODO: Check if interface exists

    path = current_app.config["AUTO_PEER_SESSION_PATH"] + f"/{body.session_id}.conf"

    if os.path.isfile(path):
        return {
            "code": 400,
            "message": "Session already exists"
        }, 400

    dn42_communities = helpers.get_dn42_communities(body.remote_address, body.interface_id)

    if not dn42_communities:
        return {
            "code": 400,
            "message": "Something went wrong when generating the community values, please try again"
        }, 400

    environment = jinja2.Environment(loader=FileSystemLoader("app/templates/"))
    template = environment.get_template("peer.conf.j2")
    output = template.render(
        body,
        latency=dn42_communities["latency"],
        bandwidth=dn42_communities["bandwidth"],
        encryption=dn42_communities["encryption"]
    )

    with open(path, "w", encoding="utf-8") as file:
        file.write(output)

    config_check = helpers.run_bird_command("configure check", restricted=False)

    if "Configuration OK" in config_check:
        helpers.run_bird_command("configure", restricted=False)

    else:
        os.remove(path)

        return {
            "code": 400,
            "message": "The config could not be parsed, please try again"
        }, 400

    return jsonify(body.model_dump()), 201


@bp.delete("/<id>", operation_id="delete_session", responses={},
           security=[{"jwt": []}])
@jwt_required()
def delete_session(path: SessionPath):
    """Delete Session
    Deletes a given session
    """

    try:
        peer_detail = peer_service.get_peer_detail(path.id)
        peer_detail["session_id"] = path.id
    except SessionNotFoundException:
        return {
            "code": 404,
            "message": "Session not found"
        }, 404

    file_path = current_app.config["AUTO_PEER_SESSION_PATH"] + f"/{path.id}.conf"

    helpers.run_bird_command(f"disable {path.id}", restricted=False)
    os.remove(file_path)

    config_check = helpers.run_bird_command("configure check", restricted=False)

    if "Configuration OK" in config_check:
        helpers.run_bird_command("configure", restricted=False)

    else:
        return {
            "code": 500,
            "message": "Something went wrong when deleting the session, please try again"
        }, 500

    return {
        "code": 200,
        "message": "Session deleted"
    }, 200
