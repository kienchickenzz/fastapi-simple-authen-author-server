"""
DTO chứa thông tin được decode từ JWT token.
"""
from dataclasses import dataclass


@dataclass
class TokenPayload:
    """
    Payload được extract từ JWT token.

    Args:
        user_id (int): ID của user trong database.
        permissions (set[str]): Danh sách permission codes của user.
    """

    user_id: int
    permissions: set[str]
