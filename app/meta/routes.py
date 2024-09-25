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
    loopback_ips = ip_address.get_loopback_addresses(loopback_interface)
    peer_count = peer.get_peer_count()

    protocols = {}
    link_local_ips = {}

    if current_app.config["WIREGUARD_ENABLED"]:
        public_key = Path(current_app.config["WIREGUARD_PUBKEY_PATH"]).read_text(encoding="utf-8")
        protocols["wireguard"] = {
            "enabled": current_app.config["WIREGUARD_ENABLED"],
            "public_key": public_key.strip("\n")
        }

    if current_app.config["IPV4_LINK_LOCAL"] != "":
        link_local_ips['ipv4'] = current_app.config["IPV4_LINK_LOCAL"]

    if current_app.config["IPV6_LINK_LOCAL"] != "":
        link_local_ips['ipv6'] = current_app.config["IPV6_LINK_LOCAL"]

    return jsonify(
        InfoResponse(
            id=current_app.config["NODE_ID"],
            fqdn=current_app.config["NODE_FQDN"],
            agent_version=current_app.config["AGENT_VERSION"],
            current_peers=peer_count,
            peer_limit=current_app.config["PEER_LIMIT"],
            loopback_ips=loopback_ips,
            link_local_ips=link_local_ips,
            peering_policy=current_app.config["PEERING_POLICY"],
            protocols=protocols,
        ).model_dump()
    )
