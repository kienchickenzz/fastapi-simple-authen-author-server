"""
Module đăng ký dependencies cho User service.

UserModule phụ thuộc vào RoleModule để validate role khi gán cho user.
Vì vậy RoleModule phải được khởi tạo TRƯỚC UserModule trong AppInitializer.
"""

from dataclasses import dataclass

from src.base.module import IModule, ModuleContext, ModuleDependencies
from src.user.database.repository.user_repository import UserRepository
from src.user.database.repository.user_role_repository import UserRoleRepository
from src.user.service.user_service import UserService


@dataclass
class UserModule(IModule):
    """
    Module khởi tạo User service và repositories.

    Dependencies được cung cấp:
        - user_repository: UserRepository instance
        - user_role_repository: UserRoleRepository instance
        - user_service: UserService instance

    Cross-module dependencies:
        - role_repository (từ RoleModule): Để validate role khi gán cho user
    """

    _user_repository: UserRepository | None = None
    _user_role_repository: UserRoleRepository | None = None
    _service: UserService | None = None

    async def initialize(self, context: ModuleContext) -> ModuleDependencies:
        """
        Khởi tạo UserRepository, UserRoleRepository và UserService.

        Args:
            context (ModuleContext): Chứa db_engine, config và shared_repositories

        Returns:
            ModuleDependencies: user_repository, user_role_repository và user_service
        """
        # Lấy role_repository từ shared (RoleModule phải khởi tạo trước)
        role_repository = context.shared_repositories["role_repository"]

        self._user_repository = UserRepository(engine=context.db_engine)
        self._user_role_repository = UserRoleRepository(engine=context.db_engine)

        self._service = UserService(
            user_repository=self._user_repository,
            user_role_repository=self._user_role_repository,
            role_repository=role_repository,
        )

        return ModuleDependencies(
            services={"user_service": self._service},
            repositories={
                "user_repository": self._user_repository,
                "user_role_repository": self._user_role_repository,
            },
        )
