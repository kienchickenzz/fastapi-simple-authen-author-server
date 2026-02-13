"""
Repository để thao tác với bảng tokens.
"""
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncEngine

from src.base.database.repository.base import Repository
from src.auth.database.model.token import Token


class TokenRepository(Repository[Token]):
    """
    Repository cho Token entity.

    Args:
        engine (AsyncEngine): SQLAlchemy async engine.
    """

    def __init__(self, engine: AsyncEngine):
        """
        Khởi tạo TokenRepository.

        Args:
            engine (AsyncEngine): SQLAlchemy async engine.
        """
        super().__init__(engine, Token)

    async def create_token(self, user_id: int, token: str, expired_at: datetime) -> Token:
        """
        Tạo token mới với trạng thái active.

        Args:
            user_id (int): ID của user.
            token (str): JWT token string.
            expired_at (datetime): Thời gian hết hạn.

        Returns:
            Token: Token record đã tạo.
        """
        values = {
            "user_id": user_id,
            "token": token,
            "is_active": True,
            "expired_at": expired_at,
        }
        return await self.create(values)

    async def deactivate_token(self, token: str) -> bool:
        """
        Vô hiệu hóa token (set is_active=False).

        Args:
            token (str): JWT token cần deactivate.

        Returns:
            bool: True nếu deactivate thành công.
        """
        sql = "UPDATE tokens SET is_active = FALSE WHERE token = :token AND is_active = TRUE"
        row_count = await self.execute_sql(sql, {"token": token}, fetch=False)
        return row_count > 0 if isinstance(row_count, int) else False

    async def is_token_active(self, token: str) -> bool:
        """
        Kiểm tra token có active không.

        Args:
            token (str): JWT token cần kiểm tra.

        Returns:
            bool: True nếu token active và chưa hết hạn.
        """
        sql = """
            SELECT 1 FROM tokens
            WHERE token = :token
            AND is_active = TRUE
            AND expired_at > NOW()
            LIMIT 1
        """
        results = await self.execute_sql(sql, {"token": token})
        return len(results) > 0 if not isinstance(results, int) else False

    async def deactivate_all_user_tokens(self, user_id: int) -> int:
        """
        Vô hiệu hóa tất cả tokens của user (logout all devices).

        Args:
            user_id (int): ID của user.

        Returns:
            int: Số lượng tokens đã deactivate.
        """
        sql = "UPDATE tokens SET is_active = FALSE WHERE user_id = :user_id AND is_active = TRUE"
        row_count = await self.execute_sql(sql, {"user_id": user_id}, fetch=False)
        return row_count if isinstance(row_count, int) else 0

    async def cleanup_expired(self) -> int:
        """
        Xóa các tokens đã hết hạn.

        Returns:
            int: Số lượng tokens đã xóa.
        """
        sql = "DELETE FROM tokens WHERE expired_at < NOW()"
        row_count = await self.execute_sql(sql, fetch=False)
        return row_count if isinstance(row_count, int) else 0

    def handle_sql_error(self, error_code: str, error_message: str, exc: Exception) -> None:
        """
        Xử lý SQL errors.

        Args:
            error_code (str): Mã lỗi PostgreSQL.
            error_message (str): Thông báo lỗi.
            exc (Exception): Exception gốc.
        """
        raise exc
