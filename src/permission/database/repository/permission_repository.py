"""
Repository để quản lý permissions trong database.
Cung cấp các operations CRUD và query permissions của user.
"""

from sqlalchemy.ext.asyncio import AsyncEngine

from src.base.database.repository.base import Repository
from src.auth.database.model.permission import Permission


class PermissionRepository(Repository[Permission]):
    """
    Repository để quản lý Permission entities.

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

    async def get_by_code(self, code: str) -> Permission | None:
        """
        Tìm permission theo code.

        Args:
            code (str): Permission code cần tìm (e.g. "book:read").

        Returns:
            Permission | None: Permission nếu tìm thấy, None nếu không.
        """
        sql = "SELECT * FROM permissions WHERE code = :code"
        results = await self.fetch_sql(sql, {"code": code})
        if not results:
            return None
        return Permission(**dict(results[0]))

    async def delete(self, permission_id: int) -> bool:
        """
        Xóa permission theo id.

        Args:
            permission_id (int): ID của permission cần xóa.

        Returns:
            bool: True nếu xóa thành công.
        """
        sql = "DELETE FROM permissions WHERE id = :permission_id"
        row_count = await self.execute_sql(sql, {"permission_id": permission_id})
        return row_count > 0
