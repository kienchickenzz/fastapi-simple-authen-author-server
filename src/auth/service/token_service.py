"""
Service xử lý encode/decode JWT token.

Token chứa thông tin user và permissions để resource servers
có thể authorize mà không cần query database.
"""
from datetime import datetime, timedelta, timezone

import jwt

from src.config import Config
from src.auth.dto.token_payload import TokenPayload


class TokenService:
    """
    Service để tạo và xác thực JWT token.

    Args:
        config (Config): Configuration chứa JWT secret và settings.
    """

    def __init__(self, config: Config):
        """
        Khởi tạo TokenService.

        Args:
            config (Config): Configuration object.
        """
        self._secret_key = config.require_config("JWT_SECRET_KEY")
        self._algorithm = config.require_config("JWT_ALGORITHM")
        self._expire_minutes = config.require_int("JWT_EXPIRE_MINUTES")

    def encode(self, user_id: int, username: str, permissions: list[str]) -> str:
        """
        Tạo JWT token với user info và permissions.

        Args:
            user_id (int): ID của user.
            username (str): Tên đăng nhập của user.
            permissions (list[str]): Danh sách permission codes.

        Returns:
            str: JWT token string.
        """
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self._expire_minutes)

        # Tạo TokenPayload instance để đảm bảo type safety
        payload = TokenPayload(
            sub=str(user_id),
            username=username,
            permissions=permissions,
            exp=int(expire.timestamp()),
            iat=int(now.timestamp()),
        )

        return jwt.encode(payload.to_dict(), self._secret_key, algorithm=self._algorithm)

    def decode(self, token: str) -> TokenPayload:
        """
        Decode JWT token và trả về TokenPayload.

        Args:
            token (str): JWT token string.

        Returns:
            TokenPayload: Payload chứa user info và permissions.

        Raises:
            jwt.ExpiredSignatureError: Khi token hết hạn.
            jwt.InvalidTokenError: Khi token không hợp lệ.
        """
        payload_dict = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        return TokenPayload.from_dict(payload_dict)

    def get_expiration(self, token: str) -> datetime:
        """
        Lấy thời gian hết hạn từ token.

        Args:
            token (str): JWT token.

        Returns:
            datetime: Thời gian hết hạn.
        """
        payload = self.decode(token)
        return datetime.fromtimestamp(payload.exp, tz=timezone.utc)
