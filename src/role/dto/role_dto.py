"""
DTO cho Role endpoints.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_serializer

from src.base.dto.main import PaginatedRequestBase, PaginatedResponseBase, ResponseBase
from src.permission.dto.permission_dto import PermissionResponse


# === Request DTOs ===
class RoleCreateRequest(BaseModel):
    """
    Request tạo role mới.

    Args:
        name (str): Tên role.
        description (str | None): Mô tả role.
    """

    name: str
    description: Optional[str] = None


class RoleUpdateRequest(BaseModel):
    """
    Request cập nhật role.

    Args:
        name (str | None): Tên role mới.
        description (str | None): Mô tả mới.
    """

    name: Optional[str] = None
    description: Optional[str] = None


class RoleListRequest(PaginatedRequestBase):
    """
    Request lấy danh sách roles với phân trang.
    """

    pass


class RolePermissionAssignRequest(BaseModel):
    """
    Request gán permission cho role.

    Args:
        permission_id (int): ID của permission cần gán.
    """

    permission_id: int


# === Response DTOs ===
class RoleResponse(ResponseBase):
    """
    Response cho single role.

    Args:
        id (int): ID của role.
        name (str): Tên role.
        description (str | None): Mô tả role.
        created_at (datetime): Thời gian tạo.
        updated_at (datetime): Thời gian cập nhật.
    """

    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dates(self, value: datetime) -> str:
        """Serialize datetime to ISO format string."""
        return value.isoformat() if value else None


class RoleDetailResponse(RoleResponse):
    """
    Response cho role với chi tiết permissions.

    Args:
        permissions (list[PermissionResponse]): Danh sách permissions của role.
    """

    permissions: list[PermissionResponse]


class RoleListResponse(PaginatedResponseBase):
    """
    Response cho danh sách roles với phân trang.

    Args:
        roles (list[RoleResponse]): Danh sách roles.
    """

    roles: list[RoleResponse]


class RolePermissionsResponse(ResponseBase):
    """
    Response cho danh sách permissions của một role.

    Args:
        role_id (int): ID của role.
        permissions (list[PermissionResponse]): Danh sách permissions.
    """

    role_id: int
    permissions: list[PermissionResponse]
