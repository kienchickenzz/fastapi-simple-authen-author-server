"""
Module đăng ký dependencies cho Permission service.

PermissionModule là một module độc lập, không phụ thuộc vào module nào khác.

LƯU Ý QUAN TRỌNG:
Module này PHẢI được khởi tạo TRƯỚC các modules sau:
- RoleModule: cần permission_repository để query permissions của role
- AuthModule: cần permission_repository để query permissions của user

Vì vậy, trong AppInitializer._modules, PermissionModule phải đứng trước
RoleModule và AuthModule.
"""

from dataclasses import dataclass

from src.base.module import IModule, ModuleContext, ModuleDependencies
from src.permission.database.repository.permission_repository import PermissionRepository
from src.permission.service.permission_service import PermissionService


@dataclass
class PermissionModule(IModule):
    """
    Module khởi tạo Permission service và repository.

    Dependencies được cung cấp:
        - permission_repository: PermissionRepository instance
        - permission_service: PermissionService instance

    Cross-module dependencies: Không có (module độc lập)

    Modules phụ thuộc vào module này:
        - RoleModule
        - AuthModule
    """

    _repository: PermissionRepository | None = None
    _service: PermissionService | None = None

    async def initialize(self, context: ModuleContext) -> ModuleDependencies:
        """
        Khởi tạo PermissionRepository và PermissionService.

        Args:
            context (ModuleContext): Chứa db_engine và config

        Returns:
            ModuleDependencies: permission_repository và permission_service
        """
        self._repository = PermissionRepository(engine=context.db_engine)
        self._service = PermissionService(permission_repository=self._repository)

        return ModuleDependencies(
            services={"permission_service": self._service},
            repositories={"permission_repository": self._repository},
        )
