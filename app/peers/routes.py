# -*- coding: utf-8 -*-
"""Module for Peering related routes"""

from flask import jsonify
from flask_jwt_extended import jwt_required

from app.peers import bp
from app.peers.exceptions import PeerNotFoundException
from app.peers.responses import PeerResponse, PeerPath
from app.services import helpers
from app.services import peer as peer_service


@bp.get("/", operation_id="get_peers_list", responses={200: {}})
@jwt_required()
def get_peers_list():
    """Get list of peers
    Gets list of peers from node
    """

    peers = peer_service.get_peers()
    peer_list = []

    for peer in peers:
        details = peer_service.get_peer_detail(peer[0])
        details["peer_id"] = peer[0]
        # peer_list.append(PeerResponse.model_validate(details).model_dump())
        peer_list.append(details)

    return jsonify(peer_list)


@bp.get("/<id>", operation_id="get_peer", responses={200: PeerResponse})
@jwt_required()
def get_peer(path: PeerPath):
    """Get peer
    Gets details of peer from node
    """

    try:
        peer_detail = peer_service.get_peer_detail(path.id)
    except PeerNotFoundException:
        return {
            "code": 404,
            "message": "Peer not found"
        }, 404

    return jsonify(PeerResponse.model_validate(peer_detail).model_dump())


@bp.post("/<id>/disable", operation_id="disable_peer", responses={})
@jwt_required()
def disable_peer(path: PeerPath):
    """Disable peer
    Disables given peer
    """

    try:
        peer = peer_service.get_peer_detail(path.id)
    except PeerNotFoundException:
        return {
            "code": 404,
            "message": "Peer not found"
        }, 404

    if peer["bgp_state"] == "Down":
        return {
            "code": 422,
            "message": "Peer is already disabled"
        }, 422

    helpers.run_bird_command(f"disable {path.id}", restricted=False)

    return {
        "code": 200,
        "message": "Peer has been disabled"
    }, 200

@bp.post("/<id>/enable", operation_id="enable_peer", responses={})
@jwt_required()
def enable_peer(path: PeerPath):
    """Enable peer
    Enables given peer
    """

    try:
        peer = peer_service.get_peer_detail(path.id)
    except PeerNotFoundException:
        return {
            "code": 404,
            "message": "Peer not found"
        }, 404

    if peer["bgp_state"] != "Down":
        return {
            "code": 422,
            "message": "Peer is already enabled"
        }, 422

    helpers.run_bird_command(f"enable {path.id}", restricted=False)

    return {
        "code": 200,
        "message": "Peer has been enabled"
    }, 200


@bp.post("/<id>/restart", operation_id="restart_peer", responses={})
@jwt_required()
def restart_peer(path: PeerPath):
    """Restart peer
    Restart given peer
    """

    try:
        peer = peer_service.get_peer_detail(path.id)
    except PeerNotFoundException:
        return {
            "code": 404,
            "message": "Peer not found"
        }, 404

    helpers.run_bird_command(f"restart {path.id}", restricted=False)

    return {
        "code": 200,
        "message": "Peer has been restarted"
    }, 200


@bp.post("/<id>/reload", operation_id="reload_peer", responses={})
@jwt_required()
def reload_peer(path: PeerPath):
    """Reload peer
    Reload given peer
    """

    try:
        peer = peer_service.get_peer_detail(path.id)
    except PeerNotFoundException:
        return {
            "code": 404,
            "message": "Peer not found"
        }, 404

    helpers.run_bird_command(f"reload {path.id}", restricted=False)

    return {
        "code": 200,
        "message": "Peer has been reloaded"
    }, 200
