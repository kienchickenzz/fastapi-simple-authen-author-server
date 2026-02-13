"""
DTO cho Auth endpoints.
"""
from pydantic import BaseModel, EmailStr

from src.base.dto.main import ResponseBase


# === Request DTOs ===
class SignUpRequest(BaseModel):
    """
    Request đăng ký user mới.

    Args:
        username (str): Tên đăng nhập.
        email (EmailStr): Email.
        password (str): Mật khẩu.
    """

    username: str
    email: EmailStr
    password: str


class SignInRequest(BaseModel):
    """
    Request đăng nhập.

    Args:
        username (str): Tên đăng nhập.
        password (str): Mật khẩu.
    """

    username: str
    password: str


# === Response DTOs ===
class SignUpResponse(ResponseBase):
    """
    Response sau khi đăng ký thành công.

    Args:
        id (int): ID của user mới.
        username (str): Tên đăng nhập.
        email (str): Email.
    """

    id: int
    username: str
    email: str


class SignInResponse(ResponseBase):
    """
    Response sau khi đăng nhập thành công.

    Args:
        access_token (str): JWT access token.
        token_type (str): Loại token (Bearer).
    """

    access_token: str
    token_type: str = "Bearer"


class SignOutResponse(ResponseBase):
    """
    Response sau khi đăng xuất thành công.

    Args:
        message (str): Thông báo.
    """

    message: str
