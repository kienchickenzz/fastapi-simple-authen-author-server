"""
DTO cho User endpoints.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_serializer

from src.base.dto.main import PaginatedRequestBase, PaginatedResponseBase, ResponseBase


# === Request DTOs ===
class UserCreateRequest(BaseModel):
    """
    Request tạo user mới.

    Args:
        username (str): Tên đăng nhập.
        email (EmailStr): Email.
        password (str): Mật khẩu.
    """

    username: str
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    """
    Request cập nhật user.

    Args:
        username (str | None): Tên đăng nhập mới.
        email (EmailStr | None): Email mới.
        is_active (bool | None): Trạng thái hoạt động.
    """

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class UserListRequest(PaginatedRequestBase):
    """
    Request lấy danh sách users với phân trang.
    """

    pass


# === Response DTOs ===
class UserResponse(ResponseBase):
    """
    Response cho single user.

    Args:
        id (int): ID của user.
        username (str): Tên đăng nhập.
        email (str): Email.
        is_active (bool): Trạng thái hoạt động.
        created_at (datetime): Thời gian tạo.
        updated_at (datetime): Thời gian cập nhật.
    """

    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dates(self, value: datetime) -> str:
        """Serialize datetime to ISO format string."""
        return value.isoformat() if value else None


class UserListResponse(PaginatedResponseBase):
    """
    Response cho danh sách users với phân trang.

    Args:
        users (list[UserResponse]): Danh sách users.
    """

    users: list[UserResponse]


# === User-Role DTOs ===
class UserRoleAssignRequest(BaseModel):
    """
    Request gán role cho user.

    Args:
        role_id (int): ID của role cần gán.
    """

    role_id: int


class UserRoleResponse(ResponseBase):
    """
    Response cho single role của user.

    Args:
        id (int): ID của role.
        name (str): Tên role.
        description (str | None): Mô tả role.
    """

    id: int
    name: str
    description: Optional[str]


class UserRolesResponse(ResponseBase):
    """
    Response cho danh sách roles của một user.

    Args:
        user_id (int): ID của user.
        roles (list[UserRoleResponse]): Danh sách roles.
    """

    user_id: int
    roles: list[UserRoleResponse]
