"""
OpenAPI documentation tags cho Role module.
"""

from src.base.doc import Tag, TagEnum


class Tags(TagEnum):
    """Tags cho Role endpoints."""

    ROLE = Tag(name="Role", description="Role management endpoints")
