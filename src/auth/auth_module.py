"""
Module đăng ký dependencies cho Auth service.

AuthModule có CROSS-MODULE DEPENDENCIES:
- UserRepository từ UserModule (để xác thực user)
- PermissionRepository từ PermissionModule (đã được inject, không cần đăng ký lại)

Vì vậy, AuthModule PHẢI được khởi tạo SAU UserModule và PermissionModule
trong danh sách modules của AppInitializer.
"""

from dataclasses import dataclass

from src.base.module import IModule, ModuleContext, ModuleDependencies
from src.auth.database.repository.token_repository import TokenRepository
from src.auth.service.token_service import TokenService
from src.auth.service.auth_service import AuthService


@dataclass
class AuthModule(IModule):
    """
    Module khởi tạo Auth services và repositories.

    Dependencies được cung cấp:
        - token_repository: TokenRepository instance
        - token_service: TokenService instance
        - auth_service: AuthService instance

    Cross-module dependencies (lấy từ shared_repositories):
        - user_repository: Từ UserModule (để xác thực credentials)
        - permission_repository: Từ PermissionModule (để fetch permissions khi sign-in)

    LƯU Ý: AuthService cần permission_repository để embed permissions vào JWT token
    khi user sign-in. Điều này cho phép resource servers authorize mà không cần
    query database.
    """

    _token_repository: TokenRepository | None = None
    _token_service: TokenService | None = None
    _auth_service: AuthService | None = None

    async def initialize(self, context: ModuleContext) -> ModuleDependencies:
        """
        Khởi tạo Auth services và repositories.

        QUAN TRỌNG: Method này yêu cầu các dependencies sau đã có trong
        context.shared_repositories:
        - "user_repository" (từ UserModule)
        - "permission_repository" (từ PermissionModule)

        Điều này đảm bảo bởi thứ tự khởi tạo modules trong AppInitializer.

        Args:
            context (ModuleContext): Chứa db_engine, config, và shared_repositories

        Returns:
            ModuleDependencies: token_repository, token_service, auth_service

        Raises:
            KeyError: Nếu dependencies chưa có trong shared_repositories
                (do thứ tự khởi tạo modules sai)
        """
        # =================================================================
        # CROSS-MODULE DEPENDENCIES
        # UserModule và PermissionModule phải được khởi tạo trước AuthModule
        # =================================================================
        user_repository = context.shared_repositories["user_repository"]
        permission_repository = context.shared_repositories["permission_repository"]

        # Khởi tạo repositories của module này
        self._token_repository = TokenRepository(engine=context.db_engine)

        # Khởi tạo services
        # TokenService chỉ cần config (cho JWT secret)
        self._token_service = TokenService(config=context.config)

        # AuthService cần UserRepository và PermissionRepository (cross-module)
        # để fetch permissions khi sign-in và embed vào JWT token
        self._auth_service = AuthService(
            user_repository=user_repository,
            token_service=self._token_service,
            token_repository=self._token_repository,
            permission_repository=permission_repository,
        )

        return ModuleDependencies(
            services={
                "token_service": self._token_service,
                "auth_service": self._auth_service,
            },
            repositories={
                "token_repository": self._token_repository,
                # Không đăng ký permission_repository ở đây
                # vì PermissionModule đã làm điều đó
            },
        )
