"""
Repository để quản lý user-role assignments trong database.
"""

from sqlalchemy.ext.asyncio import AsyncEngine

from src.base.database.repository.base import Repository
from src.auth.database.model.user_role import UserRole
from src.auth.database.model.role import Role


class UserRoleRepository(Repository[UserRole]):
    """
    Repository cho UserRole junction table.

    Args:
        engine (AsyncEngine): SQLAlchemy async engine.
    """

    def __init__(self, engine: AsyncEngine):
        """
        Khởi tạo UserRoleRepository.

        Args:
            engine (AsyncEngine): SQLAlchemy async engine.
        """
        super().__init__(engine, UserRole)

    async def assign_role(self, user_id: int, role_id: int) -> UserRole:
        """
        Gán role cho user.

        Args:
            user_id (int): ID của user.
            role_id (int): ID của role.

        Returns:
            UserRole: Record vừa tạo.
        """
        values = {
            "user_id": user_id,
            "role_id": role_id,
        }
        return await self.create(values)

    async def has_role(self, user_id: int, role_id: int) -> bool:
        """
        Kiểm tra user đã có role chưa.

        Args:
            user_id (int): ID của user.
            role_id (int): ID của role.

        Returns:
            bool: True nếu user đã có role.
        """
        sql = """
            SELECT 1 FROM user_roles
            WHERE user_id = :user_id AND role_id = :role_id
            LIMIT 1
        """
        results = await self.fetch_sql(sql, {
            "user_id": user_id,
            "role_id": role_id,
        })
        return len(results) > 0

    async def count_users_with_role(self, role_name: str) -> int:
        """
        Đếm số users có role theo tên role.

        Args:
            role_name (str): Tên role (e.g. "Admin").

        Returns:
            int: Số lượng users có role này.
        """
        sql = """
            SELECT COUNT(*) as count
            FROM user_roles ur
            JOIN roles r ON r.id = ur.role_id
            WHERE r.name = :role_name
        """
        results = await self.fetch_sql(sql, {"role_name": role_name})
        if not results:
            return 0
        return results[0]["count"]

    async def remove_role(self, user_id: int, role_id: int) -> bool:
        """
        Xóa role khỏi user.

        Args:
            user_id (int): ID của user.
            role_id (int): ID của role.

        Returns:
            bool: True nếu xóa thành công.
        """
        sql = """
            DELETE FROM user_roles
            WHERE user_id = :user_id AND role_id = :role_id
        """
        row_count = await self.execute_sql(sql, {
            "user_id": user_id,
            "role_id": role_id,
        })
        return row_count > 0

    async def get_roles_by_user_id(self, user_id: int) -> list[Role]:
        """
        Lấy danh sách roles của một user.

        Args:
            user_id (int): ID của user.

        Returns:
            list[Role]: Danh sách roles của user.
        """
        sql = """
            SELECT r.id, r.name, r.description, r.created_at, r.updated_at
            FROM roles r
            JOIN user_roles ur ON ur.role_id = r.id
            WHERE ur.user_id = :user_id
        """
        results = await self.fetch_sql(sql, {"user_id": user_id})
        return [Role(**dict(row)) for row in results]
