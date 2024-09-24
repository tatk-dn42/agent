# -*- coding: utf-8 -*-
"""Module for Flask Web App"""

from flask_openapi3 import OpenAPI, Info

from config import Config
from app.meta import bp as main_bp


def create_app(config_class=Config):
    """Flask App Factory Instance"""

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

    bearer_scheme = {
        "type": "http",
        "scheme": "bearer",
        "description": "API Key used for authorisation",
    }

    security_schemes = {"api_key": bearer_scheme}

    app = OpenAPI(
        __name__, doc_prefix="/api", info=info, security_schemes=security_schemes
    )

    app.config.from_object(config_class)

    # Initialize Flask extensions here

    # Register routes here
    app.register_api(main_bp)

    return app
