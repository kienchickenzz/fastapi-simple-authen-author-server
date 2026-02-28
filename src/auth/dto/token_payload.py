"""
DTO chứa thông tin được encode/decode từ JWT token.

TokenPayload đảm bảo type safety khi tạo và parse JWT token.
Permissions được embed trực tiếp trong token để tránh query DB mỗi request.
"""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TokenPayload:
    """
    Payload của JWT token.

    Args:
        sub (str): Subject - User ID dưới dạng string (JWT convention).
        username (str): Tên đăng nhập của user.
        permissions (list[str]): Danh sách permission codes của user.
        exp (int): Expiration timestamp.
        iat (int): Issued at timestamp.
    """

    sub: str
    username: str
    permissions: list[str] = field(default_factory=list)
    exp: int = 0
    iat: int = 0

    @property
    def user_id(self) -> int:
        """
        Lấy user_id dưới dạng int.

        Returns:
            int: User ID.
        """
        return int(self.sub)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dict để truyền vào jwt.encode().

        Returns:
            dict[str, Any]: Dictionary representation.
        """
        return {
            "sub": self.sub,
            "username": self.username,
            "permissions": self.permissions,
            "exp": self.exp,
            "iat": self.iat,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TokenPayload":
        """
        Tạo instance từ decoded JWT dict.

        Args:
            data (dict[str, Any]): Decoded JWT payload.

        Returns:
            TokenPayload: Instance mới.
        """
        return cls(
            sub=data["sub"],
            username=data["username"],
            permissions=data.get("permissions", []),
            exp=data.get("exp", 0),
            iat=data.get("iat", 0),
        )
