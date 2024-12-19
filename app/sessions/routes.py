# -*- coding: utf-8 -*-
"""Module for Session related routes"""

from flask import jsonify
from flask_jwt_extended import jwt_required

from app.services import helpers
from app.services import peer as peer_service
from app.sessions import bp
from app.sessions.exceptions import SessionNotFoundException
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
