"""
Service để tạo và quản lý admin users.
"""

import hashlib
import logging

from sqlalchemy.ext.asyncio import AsyncEngine

from src.user.database.repository.user_repository import UserRepository
from src.user.database.repository.user_role_repository import UserRoleRepository
from src.role.database.repository.role_repository import RoleRepository


logger = logging.getLogger("app")


class AdminService:
    """
    Service để tạo admin user.

    Cung cấp logic tạo user mới và gán Admin role.
    """

    ADMIN_ROLE_NAME = "admin"

    def __init__(
        self,
        user_repository: UserRepository,
        user_role_repository: UserRoleRepository,
        role_repository: RoleRepository,
    ):
        """
        Khởi tạo AdminService.

        Args:
            user_repository (UserRepository): Repository để tạo user.
            user_role_repository (UserRoleRepository): Repository để gán role.
            role_repository (RoleRepository): Repository để query role.
        """
        self._user_repository = user_repository
        self._user_role_repository = user_role_repository
        self._role_repository = role_repository

    async def create_admin(
        self,
        username: str,
        email: str,
        password: str,
    ) -> int:
        """
        Tạo user mới và gán Admin role.

        Args:
            username (str): Username cho admin.
            email (str): Email cho admin.
            password (str): Password (sẽ được hash).

        Returns:
            int: ID của user vừa tạo.

        Raises:
            ValueError: Nếu username đã tồn tại.
            ValueError: Nếu email đã tồn tại.
            ValueError: Nếu Admin role không tồn tại trong DB.
        """
        # Kiểm tra username đã tồn tại chưa
        existing_user = await self._user_repository.get_by_username(username)
        if existing_user:
            raise ValueError(f"Username '{username}' already exists")

        # Kiểm tra email đã tồn tại chưa
        existing_email = await self._user_repository.get_by_email(email)
        if existing_email:
            raise ValueError(f"Email '{email}' already exists")

        # Kiểm tra Admin role tồn tại
        admin_role = await self._role_repository.get_by_name(self.ADMIN_ROLE_NAME)
        if not admin_role:
            raise ValueError(
                f"Admin role not found in database. "
                f"Please run seed_data.sql first to create roles and permissions."
            )

        # Hash password
        password_hash = self._hash_password(password)

        # Tạo user
        user = await self._user_repository.create({
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "is_active": True,
        })

        # Gán Admin role
        await self._user_role_repository.assign_role(user.id, admin_role.id)

        logger.info(f"Admin user created: {username} (id={user.id})")

        return user.id

    async def has_any_admin(self) -> bool:
        """
        Kiểm tra có user nào với Admin role không.

        Returns:
            bool: True nếu có ít nhất 1 admin.
        """
        count = await self._user_role_repository.count_users_with_role(self.ADMIN_ROLE_NAME)
        return count > 0

    def _hash_password(self, password: str) -> str:
        """
        Hash password sử dụng SHA256.

        Args:
            password (str): Password cần hash.

        Returns:
            str: Password đã hash.
        """
        # TODO: Sử dụng bcrypt hoặc argon2 trong production
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    async def create_instance(cls, db_engine: AsyncEngine) -> "AdminService":
        """
        Factory method để tạo AdminService instance.

        Tạo các repositories cần thiết và trả về service instance.
        Dùng cho CLI command khi không có context từ AppInitializer.

        Args:
            db_engine (AsyncEngine): Database engine.

        Returns:
            AdminService: Service instance.
        """
        user_repository = UserRepository(engine=db_engine)
        user_role_repository = UserRoleRepository(engine=db_engine)
        role_repository = RoleRepository(engine=db_engine)

        return cls(
            user_repository=user_repository,
            user_role_repository=user_role_repository,
            role_repository=role_repository,
        )
