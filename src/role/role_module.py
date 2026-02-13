"""
Module đăng ký dependencies cho Role service.

RoleModule có CROSS-MODULE DEPENDENCY với PermissionModule:
- RoleService cần PermissionRepository để verify permission tồn tại khi assign

Vì vậy, RoleModule PHẢI được khởi tạo SAU PermissionModule trong danh sách
modules của AppInitializer. PermissionRepository sẽ được lấy từ
context.shared_repositories.
"""

from dataclasses import dataclass

from src.base.module import IModule, ModuleContext, ModuleDependencies
from src.role.database.repository.role_repository import RoleRepository
from src.role.database.repository.role_permission_repository import RolePermissionRepository
from src.role.service.role_service import RoleService


@dataclass
class RoleModule(IModule):
    """
    Module khởi tạo Role service và repositories.

    Dependencies được cung cấp:
        - role_repository: RoleRepository instance
        - role_permission_repository: RolePermissionRepository instance
        - role_service: RoleService instance

    Cross-module dependencies:
        - permission_repository: Lấy từ PermissionModule qua shared_repositories
          (PermissionModule PHẢI khởi tạo trước RoleModule)
    """

    _role_repository: RoleRepository | None = None
    _role_permission_repository: RolePermissionRepository | None = None
    _service: RoleService | None = None

    async def initialize(self, context: ModuleContext) -> ModuleDependencies:
        """
        Khởi tạo Role repositories và service.

        QUAN TRỌNG: Method này yêu cầu "permission_repository" đã có trong
        context.shared_repositories. Điều này đảm bảo bởi thứ tự
        khởi tạo modules trong AppInitializer.

        Args:
            context (ModuleContext): Chứa db_engine, config, và shared_repositories

        Returns:
            ModuleDependencies: role_repository, role_permission_repository, role_service

        Raises:
            KeyError: Nếu permission_repository chưa có trong shared_repositories
                (do thứ tự khởi tạo modules sai)
        """
        # =================================================================
        # CROSS-MODULE DEPENDENCY: Lấy PermissionRepository từ module trước
        # PermissionModule phải được khởi tạo trước RoleModule
        # =================================================================
        permission_repository = context.shared_repositories["permission_repository"]

        # Khởi tạo repositories của module này
        self._role_repository = RoleRepository(engine=context.db_engine)
        self._role_permission_repository = RolePermissionRepository(engine=context.db_engine)

        # Khởi tạo service
        self._service = RoleService(
            role_repository=self._role_repository,
            role_permission_repository=self._role_permission_repository,
            permission_repository=permission_repository,
        )

        return ModuleDependencies(
            services={"role_service": self._service},
            repositories={
                "role_repository": self._role_repository,
                "role_permission_repository": self._role_permission_repository,
            },
        )
