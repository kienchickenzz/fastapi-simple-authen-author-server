"""
OpenAPI documentation tags cho Book module.
"""
from src.base.doc import Tag, TagEnum


class Tags(TagEnum):
    """Tags cho Book endpoints."""

    BOOK = Tag(name="Book", description="Book management endpoints")
