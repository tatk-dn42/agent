# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel
"""Module for Flask Web App"""

import logging

import sentry_sdk
from flask_openapi3 import OpenAPI, Info

from app.meta import bp as meta_bp
from app.sessions import bp as peers_bp
from app.tunnels import bp as tunnels_bp
from config import Config


def create_app(config_class=Config):
    """Flask App Factory Instance"""

    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        traces_sample_rate=1.0,
        _experiments={
            "continuous_profiling_auto_start": True,
        },
    )

    info = Info(
        title="TATK Network Agent",
        version=Config.AGENT_VERSION,
        summary="Agent for auto-peering within TATK Network",
        contact={
            "name": "TATK Network",
            "email": "noc@tatk.network",
            "url": "https://tatk.network/contact",
        },
    )

    jwt = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }

    security_schemes = {"jwt": jwt}

    app = OpenAPI(
        __name__, doc_prefix="/api", info=info, security_schemes=security_schemes,
        doc_ui=Config.API_DOCS_ENABLED
    )

    app.config.from_object(config_class)

    # Initialize Flask extensions here
    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    from flask_jwt_extended import JWTManager
    jwt = JWTManager(app)

    # Register routes here
    app.register_api(meta_bp)
    app.register_api(peers_bp)
    app.register_api(tunnels_bp)

    return app
