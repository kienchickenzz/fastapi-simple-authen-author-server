"""
Module đăng ký dependencies cho Auth service.

AuthModule có CROSS-MODULE DEPENDENCY với UserModule:
- AuthService cần UserRepository để xác thực user

Vì vậy, AuthModule PHẢI được khởi tạo SAU UserModule trong danh sách modules
của AppInitializer. UserRepository sẽ được lấy từ context.shared_repositories.
"""

from dataclasses import dataclass

from src.base.module import IModule, ModuleContext, ModuleDependencies
from src.auth.database.repository.token_repository import TokenRepository
from src.auth.repository.permission_repository import PermissionRepository
from src.auth.service.token_service import TokenService
from src.auth.service.auth_service import AuthService


@dataclass
class AuthModule(IModule):
    """
    Module khởi tạo Auth services và repositories.

    Dependencies được cung cấp:
        - token_repository: TokenRepository instance
        - permission_repository: PermissionRepository instance
        - token_service: TokenService instance
        - auth_service: AuthService instance

    Cross-module dependencies:
        - user_repository: Lấy từ UserModule qua shared_repositories
          (UserModule PHẢI khởi tạo trước AuthModule)
    """

    _token_repository: TokenRepository | None = None
    _permission_repository: PermissionRepository | None = None
    _token_service: TokenService | None = None
    _auth_service: AuthService | None = None

    async def initialize(self, context: ModuleContext) -> ModuleDependencies:
        """
        Khởi tạo Auth services và repositories.

        QUAN TRỌNG: Method này yêu cầu "user_repository" đã có trong
        context.shared_repositories. Điều này đảm bảo bởi thứ tự
        khởi tạo modules trong AppInitializer.

        Args:
            context (ModuleContext): Chứa db_engine, config, và shared_repositories

        Returns:
            ModuleDependencies: token_repository, token_service, auth_service

        Raises:
            KeyError: Nếu user_repository chưa có trong shared_repositories
                (do thứ tự khởi tạo modules sai)
        """
        # =================================================================
        # CROSS-MODULE DEPENDENCY: Lấy UserRepository từ module trước
        # UserModule phải được khởi tạo trước AuthModule
        # =================================================================
        user_repository = context.shared_repositories["user_repository"]

        # Khởi tạo repositories của module này
        self._token_repository = TokenRepository(engine=context.db_engine)
        self._permission_repository = PermissionRepository(engine=context.db_engine)

        # Khởi tạo services
        # TokenService chỉ cần config (cho JWT secret)
        self._token_service = TokenService(config=context.config)

        # AuthService cần cả UserRepository (cross-module) và các dependencies local
        self._auth_service = AuthService(
            user_repository=user_repository,
            token_service=self._token_service,
            token_repository=self._token_repository,
        )

        return ModuleDependencies(
            services={
                "token_service": self._token_service,
                "auth_service": self._auth_service,
            },
            repositories={
                "token_repository": self._token_repository,
                "permission_repository": self._permission_repository,
            },
        )
