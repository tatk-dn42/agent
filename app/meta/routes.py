# -*- coding: utf-8 -*-
"""Module for Metadata related routes"""

from pathlib import Path
from flask import current_app, jsonify

from app.meta import bp
from app.services import ip_address, peer
from app.meta.responses import InfoResponse


@bp.get("/info", operation_id="get_node_info", responses={200: InfoResponse})
def info():
    """Get node info
    Gets information from node
    """

    loopback_interface = current_app.config["LOOPBACK_INTERFACE"]
    loopback_ips = ip_address.get_link_local_address(loopback_interface)
    peer_count = peer.get_peer_count()

    protocols = {}

    if current_app.config["WIREGUARD_ENABLED"]:
        public_key = Path(current_app.config["WIREGUARD_PUBKEY_PATH"]).read_text()
        protocols["wireguard"] = {
            "enabled": current_app.config["WIREGUARD_ENABLED"],
            "public_key": public_key.strip("\n")
        }

    return jsonify(
        InfoResponse(
            id=current_app.config["NODE_ID"],
            fqdn=current_app.config["NODE_FQDN"],
            current_peers=peer_count,
            peer_limit=current_app.config["PEER_LIMIT"],
            link_local_ips=loopback_ips,
            peering_policy=current_app.config["PEERING_POLICY"],
            protocols=protocols,
        ).model_dump()
    )
