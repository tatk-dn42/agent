import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class Config:
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
    