"""
OpenAPI documentation tags cho Permission module.
"""

from src.base.doc import Tag, TagEnum


class Tags(TagEnum):
    """Tags cho Permission endpoints."""

    PERMISSION = Tag(name="Permission", description="Permission management endpoints")
