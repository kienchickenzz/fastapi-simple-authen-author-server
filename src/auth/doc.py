"""
OpenAPI documentation tags cho Auth module.
"""
from src.base.doc import Tag, TagEnum


class Tags(TagEnum):
    """Tags cho Auth endpoints."""

    AUTH = Tag(name="Auth", description="Authentication endpoints (sign in/up/out)")
