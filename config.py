# pylint: disable=too-few-public-methods
# -*- coding: utf-8 -*-
"""Module providing config to Flask App"""

import os
from pathlib import Path
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
    """Class for App Config"""

    AGENT_VERSION = Path("version.txt").read_text(encoding="utf-8").strip("\n")
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    NODE_ID = os.environ.get("NODE_ID") or "rt0-test"
    NODE_FQDN = os.environ.get("NODE_FQDN") or "rt0.test.tatk.network"
    PEER_LIMIT = os.environ.get("PEER_LIMIT") or 50
    LOOPBACK_INTERFACE = os.environ.get("LOOPBACK_INTERFACE") or "internal-dummy0"
    PEERING_POLICY = os.environ.get("PEERING_POLICY") or "Open"
    WIREGUARD_ENABLED = bool(os.environ.get("WIREGUARD_ENABLED")) or False
    WIREGUARD_PUBKEY_PATH = (
        os.environ.get("WIREGUARD_PUBKEY_PATH") or "/etc/wireguard/publickey"
    )
    AUTO_PEER_PREFIX = os.environ.get("AUTO_PEER_PREFIX") or "dn42_"
    API_DOCS_ENABLED = bool(os.environ.get("API_DOCS_ENABLED")) or False
    IPV4_LINK_LOCAL = os.environ.get("IPV4_LINK_LOCAL") or ""
    IPV6_LINK_LOCAL = os.environ.get("IPV6_LINK_LOCAL") or ""
