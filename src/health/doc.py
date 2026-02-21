"""
Module định nghĩa OpenAPI tags cho Health module.
Cung cấp tags để nhóm các endpoints health check trong Swagger documentation.
"""
from src.base.doc import Tag, TagEnum


class Tags(TagEnum):
    """
    Enum chứa các tags cho Health module.

    Tags được sử dụng để nhóm các endpoints trong OpenAPI/Swagger documentation,
    giúp tổ chức và phân loại các API endpoints theo chức năng.
    """

    HEALTH = Tag(name="Health")
