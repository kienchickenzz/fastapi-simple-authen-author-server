"""
Repository để thao tác với bảng users.
"""
from sqlalchemy.ext.asyncio import AsyncEngine

from src.base.database.repository.base import Repository
from src.auth.database.model.user import User


class UserRepository(Repository[User]):
    """
    Repository cho User entity.

    Args:
        engine (AsyncEngine): SQLAlchemy async engine.
    """

    def __init__(self, engine: AsyncEngine):
        """
        Khởi tạo UserRepository.

        Args:
            engine (AsyncEngine): SQLAlchemy async engine.
        """
        super().__init__(engine, User)

    async def get_by_username(self, username: str) -> User | None:
        """
        Tìm user theo username.

        Args:
            username (str): Username cần tìm.

        Returns:
            User | None: User nếu tìm thấy, None nếu không.
        """
        sql = "SELECT * FROM users WHERE username = :username"
        results = await self.execute_sql(sql, {"username": username})
        if not results or isinstance(results, int):
            return None
        return User(**dict(results[0]))

    async def get_by_email(self, email: str) -> User | None:
        """
        Tìm user theo email.

        Args:
            email (str): Email cần tìm.

        Returns:
            User | None: User nếu tìm thấy, None nếu không.
        """
        sql = "SELECT * FROM users WHERE email = :email"
        results = await self.execute_sql(sql, {"email": email})
        if not results or isinstance(results, int):
            return None
        return User(**dict(results[0]))

    async def delete(self, user_id: int) -> bool:
        """
        Xóa user theo id.

        Args:
            user_id (int): ID của user cần xóa.

        Returns:
            bool: True nếu xóa thành công.
        """
        sql = "DELETE FROM users WHERE id = :user_id"
        row_count = await self.execute_sql(sql, {"user_id": user_id}, fetch=False)
        return row_count > 0

    def handle_sql_error(self, error_code: str, error_message: str, exc: Exception) -> None:
        """
        Xử lý SQL errors.

        Args:
            error_code (str): Mã lỗi PostgreSQL.
            error_message (str): Thông báo lỗi.
            exc (Exception): Exception gốc.
        """
        raise exc
