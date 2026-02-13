"""
DTO cho Permission endpoints.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_serializer

from src.base.dto.main import PaginatedRequestBase, PaginatedResponseBase, ResponseBase


# === Request DTOs ===
class PermissionCreateRequest(BaseModel):
    """
    Request tạo permission mới.

    Args:
        code (str): Mã permission (e.g. "book:read").
        description (str | None): Mô tả permission.
    """

    code: str
    description: Optional[str] = None


class PermissionListRequest(PaginatedRequestBase):
    """
    Request lấy danh sách permissions với phân trang.
    """

    pass


# === Response DTOs ===
class PermissionResponse(ResponseBase):
    """
    Response cho single permission.

    Args:
        id (int): ID của permission.
        code (str): Mã permission.
        description (str | None): Mô tả permission.
        created_at (datetime): Thời gian tạo.
        updated_at (datetime): Thời gian cập nhật.
    """

    id: int
    code: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dates(self, value: datetime) -> str:
        """Serialize datetime to ISO format string."""
        return value.isoformat() if value else None


class PermissionListResponse(PaginatedResponseBase):
    """
    Response cho danh sách permissions với phân trang.

    Args:
        permissions (list[PermissionResponse]): Danh sách permissions.
    """

    permissions: list[PermissionResponse]
