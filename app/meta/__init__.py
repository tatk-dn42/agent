from flask_openapi3 import APIBlueprint, Tag

meta_tag = Tag(name="meta", description="Metadata")

bp = APIBlueprint("meta", __name__, url_prefix="/api/meta", abp_tags=[meta_tag])

from app.meta import routes
