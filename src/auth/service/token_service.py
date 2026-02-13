"""
Service xử lý encode/decode JWT token.
"""
from datetime import datetime, timedelta, timezone

import jwt

from src.base.config import Config


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
        self._algorithm = config.get_config("JWT_ALGORITHM", "HS256")
        self._expire_minutes = int(config.get_config("JWT_EXPIRE_MINUTES", "30"))

    def encode(self, user_id: int) -> str:
        """
        Tạo JWT token từ user_id.

        Args:
            user_id (int): ID của user.

        Returns:
            str: JWT token string.
        """
        expire = datetime.now(timezone.utc) + timedelta(minutes=self._expire_minutes)
        payload = {
            "sub": str(user_id),  # PyJWT yêu cầu sub phải là string
            "exp": expire,
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode(self, token: str) -> int:
        """
        Decode JWT token và trả về user_id.

        Args:
            token (str): JWT token string.

        Returns:
            int: User ID từ token.

        Raises:
            jwt.ExpiredSignatureError: Khi token hết hạn.
            jwt.InvalidTokenError: Khi token không hợp lệ.
        """
        payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        return int(payload["sub"])

    def get_expiration(self, token: str) -> datetime:
        """
        Lấy thời gian hết hạn từ token.

        Args:
            token (str): JWT token.

        Returns:
            datetime: Thời gian hết hạn.
        """
        payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        return datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
