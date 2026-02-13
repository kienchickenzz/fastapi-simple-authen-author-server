"""
Repository để quản lý roles trong database.
"""

from sqlalchemy.ext.asyncio import AsyncEngine

from src.base.database.repository.base import Repository
from src.auth.database.model.role import Role


class RoleRepository(Repository[Role]):
    """
    Repository cho Role entity.

    Args:
        engine (AsyncEngine): SQLAlchemy async engine.
    """

    def __init__(self, engine: AsyncEngine):
        """
        Khởi tạo RoleRepository.

        Args:
            engine (AsyncEngine): SQLAlchemy async engine.
        """
        super().__init__(engine, Role)

    async def get_by_name(self, name: str) -> Role | None:
        """
        Tìm role theo name.

        Args:
            name (str): Tên role cần tìm.

        Returns:
            Role | None: Role nếu tìm thấy, None nếu không.
        """
        sql = "SELECT * FROM roles WHERE name = :name"
        results = await self.fetch_sql(sql, {"name": name})
        if not results:
            return None
        return Role(**dict(results[0]))

    async def delete(self, role_id: int) -> bool:
        """
        Xóa role theo id.

        Args:
            role_id (int): ID của role cần xóa.

        Returns:
            bool: True nếu xóa thành công.
        """
        sql = "DELETE FROM roles WHERE id = :role_id"
        row_count = await self.execute_sql(sql, {"role_id": role_id})
        return row_count > 0
