"""
OpenAPI documentation tags cho User module.
"""
from src.base.doc import Tag, TagEnum


class Tags(TagEnum):
    """Tags cho User endpoints."""

    USER = Tag(name="User", description="User management endpoints")
