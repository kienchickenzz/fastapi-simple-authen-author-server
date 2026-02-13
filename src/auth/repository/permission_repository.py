"""
Repository để query permissions của user từ database.
"""
from sqlalchemy.ext.asyncio import AsyncEngine

from src.base.database.repository.base import Repository
from src.auth.database.model.permission import Permission


class PermissionRepository(Repository[Permission]):
    """
    Repository để truy vấn permissions của user.

    Args:
        engine (AsyncEngine): SQLAlchemy async engine.
    """

    def __init__(self, engine: AsyncEngine):
        """
        Khởi tạo PermissionRepository.

        Args:
            engine (AsyncEngine): SQLAlchemy async engine.
        """
        super().__init__(engine, Permission)

    async def get_permissions_by_user_id(self, user_id: int) -> set[str]:
        """
        Lấy tất cả permission codes của user thông qua roles.

        Args:
            user_id (int): ID của user.

        Returns:
            set[str]: Set các permission codes.
        """
        sql = """
            SELECT DISTINCT p.code
            FROM permissions p
            JOIN role_permissions rp ON rp.permission_id = p.id
            JOIN user_roles ur ON ur.role_id = rp.role_id
            WHERE ur.user_id = :user_id
        """
        results = await self.fetch_sql(sql, {"user_id": user_id})
        return {row["code"] for row in results}
