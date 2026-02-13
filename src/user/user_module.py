"""
Module đăng ký dependencies cho User service.

UserModule là một module độc lập, không phụ thuộc vào module nào khác.
Vì vậy nó có thể được khởi tạo đầu tiên trong danh sách modules.
"""

from dataclasses import dataclass

from src.base.module import IModule, ModuleContext, ModuleDependencies
from src.user.database.repository.user_repository import UserRepository
from src.user.service.user_service import UserService


@dataclass
class UserModule(IModule):
    """
    Module khởi tạo User service và repository.

    Dependencies được cung cấp:
        - user_repository: UserRepository instance
        - user_service: UserService instance

    Cross-module dependencies: Không có (module độc lập)
    """

    _repository: UserRepository | None = None
    _service: UserService | None = None

    async def initialize(self, context: ModuleContext) -> ModuleDependencies:
        """
        Khởi tạo UserRepository và UserService.

        Args:
            context (ModuleContext): Chứa db_engine và config

        Returns:
            ModuleDependencies: user_repository và user_service
        """
        self._repository = UserRepository(engine=context.db_engine)
        self._service = UserService(user_repository=self._repository)

        return ModuleDependencies(
            services={"user_service": self._service},
            repositories={"user_repository": self._repository},
        )
