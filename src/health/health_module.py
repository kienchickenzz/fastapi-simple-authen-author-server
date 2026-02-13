"""
Module đăng ký dependencies cho Health check service.

HealthModule là một module độc lập, không phụ thuộc vào module nào khác.
Có thể được khởi tạo ở bất kỳ vị trí nào trong danh sách modules.
"""

from dataclasses import dataclass

from src.base.module import IModule, ModuleContext, ModuleDependencies
from src.health.database.repository.health import HealthCheckRepository
from src.health.service.health_check import HealthCheckService


@dataclass
class HealthModule(IModule):
    """
    Module khởi tạo Health check service và repository.

    Dependencies được cung cấp:
        - health_check_repository: HealthCheckRepository instance
        - health_check_service: HealthCheckService instance

    Cross-module dependencies: Không có (module độc lập)
    """

    _repository: HealthCheckRepository | None = None
    _service: HealthCheckService | None = None

    async def initialize(self, context: ModuleContext) -> ModuleDependencies:
        """
        Khởi tạo HealthCheckRepository và HealthCheckService.

        Args:
            context (ModuleContext): Chứa db_engine và config

        Returns:
            ModuleDependencies: health_check_repository và health_check_service
        """
        self._repository = HealthCheckRepository(engine=context.db_engine)
        self._service = HealthCheckService(health_check_repository=self._repository)

        return ModuleDependencies(
            services={"health_check_service": self._service},
            repositories={"health_check_repository": self._repository},
        )
