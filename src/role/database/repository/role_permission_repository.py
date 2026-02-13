"""
Repository để quản lý role-permission assignments trong database.
"""

from sqlalchemy.ext.asyncio import AsyncEngine

from src.base.database.repository.base import Repository
from src.auth.database.model.role_permission import RolePermission
from src.auth.database.model.permission import Permission


class RolePermissionRepository(Repository[RolePermission]):
    """
    Repository cho RolePermission junction table.

    Args:
        engine (AsyncEngine): SQLAlchemy async engine.
    """

    def __init__(self, engine: AsyncEngine):
        """
        Khởi tạo RolePermissionRepository.

        Args:
            engine (AsyncEngine): SQLAlchemy async engine.
        """
        super().__init__(engine, RolePermission)

    async def get_permissions_by_role_id(self, role_id: int) -> list[Permission]:
        """
        Lấy tất cả permissions của một role.

        Args:
            role_id (int): ID của role.

        Returns:
            list[Permission]: Danh sách Permission entities.
        """
        sql = """
            SELECT p.*
            FROM permissions p
            JOIN role_permissions rp ON rp.permission_id = p.id
            WHERE rp.role_id = :role_id
            ORDER BY p.code
        """
        results = await self.fetch_sql(sql, {"role_id": role_id})
        return [Permission(**dict(row)) for row in results]

    async def assign_permission(self, role_id: int, permission_id: int) -> RolePermission:
        """
        Gán permission cho role.

        Args:
            role_id (int): ID của role.
            permission_id (int): ID của permission.

        Returns:
            RolePermission: Record vừa tạo.
        """
        values = {
            "role_id": role_id,
            "permission_id": permission_id,
        }
        return await self.create(values)

    async def remove_permission(self, role_id: int, permission_id: int) -> bool:
        """
        Xóa permission khỏi role.

        Args:
            role_id (int): ID của role.
            permission_id (int): ID của permission.

        Returns:
            bool: True nếu xóa thành công.
        """
        sql = """
            DELETE FROM role_permissions
            WHERE role_id = :role_id AND permission_id = :permission_id
        """
        row_count = await self.execute_sql(sql, {
            "role_id": role_id,
            "permission_id": permission_id,
        })
        return row_count > 0

    async def has_permission(self, role_id: int, permission_id: int) -> bool:
        """
        Kiểm tra role đã có permission chưa.

        Args:
            role_id (int): ID của role.
            permission_id (int): ID của permission.

        Returns:
            bool: True nếu role đã có permission.
        """
        sql = """
            SELECT 1 FROM role_permissions
            WHERE role_id = :role_id AND permission_id = :permission_id
            LIMIT 1
        """
        results = await self.fetch_sql(sql, {
            "role_id": role_id,
            "permission_id": permission_id,
        })
        return len(results) > 0
