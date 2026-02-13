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
        - user_repository: Từ UserModule
        - permission_repository: Từ PermissionModule (đã đăng ký, dùng cho authentication)

    LƯU Ý: AuthModule không đăng ký permission_repository vì PermissionModule
    đã làm điều đó. AuthModule chỉ cần đảm bảo PermissionModule khởi tạo trước.
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
        # permission_repository đã được PermissionModule đăng ký,
        # không cần lấy ra ở đây vì AuthService không cần nó trực tiếp.
        # Tuy nhiên, authentication dependency cần nó và đã được inject qua Injects().

        # Khởi tạo repositories của module này
        self._token_repository = TokenRepository(engine=context.db_engine)

        # Khởi tạo services
        # TokenService chỉ cần config (cho JWT secret)
        self._token_service = TokenService(config=context.config)

        # AuthService cần UserRepository (cross-module) và các dependencies local
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
                # Không đăng ký permission_repository ở đây
                # vì PermissionModule đã làm điều đó
            },
        )
