"""
Main application initializer module.

AppInitializer là orchestrator chính, điều phối việc khởi tạo tất cả
service modules theo đúng thứ tự dependencies.

Pattern: Composite Initializer
- Kế thừa từ Initializer base (setup app, validate, engine)
- Điều phối các IModule để đăng ký dependencies
- Quản lý cross-module dependencies qua shared_repositories
"""

from types import TracebackType
from typing import Optional, Type, Any

from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi import FastAPI

from src.base.initializer import State, Initializer
from src.base.module import IModule, ModuleContext

# =============================================================================
# IMPORT MODULES
# Các modules được import ở đây, thứ tự import không quan trọng.
# Thứ tự khởi tạo được định nghĩa trong self._modules.
# =============================================================================
from src.user.user_module import UserModule
from src.auth.auth_module import AuthModule
from src.book.book_module import BookModule
from src.health.health_module import HealthModule
from src.permission.permission_module import PermissionModule
from src.role.role_module import RoleModule
from src.admin.bootstrap import AdminBootstrap


class AppState(State):
    """
    Application state chứa tất cả services và repositories.

    State này được inject vào request.state, cho phép endpoints
    truy cập dependencies qua Injects("dependency_name").
    """

    # Database
    db_engine: AsyncEngine

    # Services
    user_service: Any
    auth_service: Any
    token_service: Any
    book_service: Any
    health_check_service: Any
    permission_service: Any
    role_service: Any

    # Repositories
    user_repository: Any
    token_repository: Any
    permission_repository: Any
    book_repository: Any
    health_check_repository: Any
    role_repository: Any
    role_permission_repository: Any


class AppInitializer(Initializer):
    """
    Main initializer kế thừa từ Initializer base.

    Điều phối khởi tạo tất cả modules theo thứ tự dependencies.
    Xử lý cross-module dependencies qua ModuleContext.shared_repositories.
    """

    def __init__(self, app: FastAPI) -> None:
        """
        Khởi tạo AppInitializer.

        Args:
            app (FastAPI): FastAPI application instance
        """
        super().__init__(app=app)

        # =================================================================
        # ĐỊNH NGHĨA THỨ TỰ KHỞI TẠO MODULES
        #
        # THỨ TỰ RẤT QUAN TRỌNG khi có cross-module dependencies!
        #
        # Quy tắc:
        # 1. Modules độc lập (không phụ thuộc module khác) có thể đặt
        #    ở bất kỳ vị trí nào trong nhóm độc lập
        # 2. Modules có dependencies PHẢI đặt SAU modules mà nó phụ thuộc
        #
        # Dependency Graph hiện tại:
        # - BookModule: Độc lập
        # - HealthModule: Độc lập
        # - PermissionModule: Độc lập
        # - RoleModule: Phụ thuộc PermissionModule (cần permission_repository)
        # - UserModule: Phụ thuộc RoleModule (cần role_repository)
        # - AuthModule: Phụ thuộc UserModule (cần user_repository)
        #
        # Nếu thêm module mới có dependencies, hãy cập nhật thứ tự này!
        # =================================================================
        self._modules: list[IModule] = [
            # --- Modules độc lập (khởi tạo trước) ---
            BookModule(),       # Cung cấp: book_repository, book_service
            HealthModule(),     # Cung cấp: health_check_repository, health_check_service
            PermissionModule(), # Cung cấp: permission_repository, permission_service
                                # PHẢI trước RoleModule

            # --- Modules có cross-dependencies (khởi tạo sau) ---
            RoleModule(),       # Yêu cầu: permission_repository (từ PermissionModule)
                                # Cung cấp: role_repository, role_permission_repository, role_service

            UserModule(),       # Yêu cầu: role_repository (từ RoleModule)
                                # Cung cấp: user_repository, user_role_repository, user_service

            AuthModule(),       # Yêu cầu: user_repository (từ UserModule)
                                # Cung cấp: token_repository, token_service, auth_service
        ]

    async def __aenter__(self) -> AppState:
        """
        Khởi tạo application.

        Flow:
        1. Gọi lớp cha để setup app, validate OpenAPI, khởi tạo engine
        2. Tạo DB engine từ EngineFactory
        3. Khởi tạo từng module theo thứ tự, thu thập dependencies
        4. Cập nhật shared_repositories sau mỗi module để modules sau sử dụng
        5. Trả về AppState chứa tất cả dependencies

        Returns:
            AppState: State chứa tất cả services và repositories
        """
        # =================================================================
        # BƯỚC 1: Gọi lớp cha
        # Initializer.__aenter__() thực hiện:
        # - _setup_app(): Set version, debug mode
        # - _validate_openapi(): Validate OpenAPI spec
        # - _validate_endpoints(): Đảm bảo có /health và /
        # - engine_factory.__aenter__(): Khởi tạo database connections
        # =================================================================
        state = await super().__aenter__()

        # =================================================================
        # BƯỚC 2: Tạo DB engine
        # =================================================================
        db_engine = self.engine_factory.create_engine("DB")

        # =================================================================
        # BƯỚC 3: Tạo ModuleContext
        # Context này được truyền xuống tất cả modules, chứa:
        # - db_engine: Để tạo repositories
        # - config: Để đọc configuration
        # - shared_repositories: Dict rỗng ban đầu, sẽ được cập nhật
        #   sau mỗi module để modules sau có thể sử dụng
        # =================================================================
        context = ModuleContext(
            db_engine=db_engine,
            config=self.config,
            shared_repositories={},
        )

        # =================================================================
        # BƯỚC 4: Khởi tạo từng module và thu thập dependencies
        # =================================================================
        all_services: dict[str, Any] = {}
        all_repositories: dict[str, Any] = {}

        for module in self._modules:
            # Module.initialize() trả về ModuleDependencies
            # chứa services và repositories của module đó
            deps = await module.initialize(context)

            # Thu thập vào collections chung
            all_services.update(deps.services)
            all_repositories.update(deps.repositories)

            # =============================================================
            # QUAN TRỌNG: Cập nhật shared_repositories
            # Sau khi một module khởi tạo xong, repositories của nó
            # được thêm vào shared_repositories để modules sau có thể
            # sử dụng (cross-module dependencies).
            #
            # Ví dụ: Sau khi UserModule khởi tạo, user_repository được
            # thêm vào shared_repositories. AuthModule khởi tạo sau
            # sẽ lấy user_repository từ đây.
            # =============================================================
            context.shared_repositories.update(deps.repositories)

        # =================================================================
        # BƯỚC 5: Bootstrap Admin User
        # Kiểm tra và tạo admin user từ environment variables nếu:
        # 1. Chưa có admin nào trong database
        # 2. Có đủ ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD trong env
        #
        # Nếu thiếu config hoặc đã có admin, sẽ skip và log thông tin.
        # =================================================================
        await AdminBootstrap.run(db_engine=db_engine, config=self.config)

        # =================================================================
        # BƯỚC 6: Trả về AppState
        # Merge state từ lớp cha với tất cả dependencies đã thu thập
        # =================================================================
        return AppState(
            **state,
            db_engine=db_engine,
            **all_services,
            **all_repositories,
        )

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """
        Shutdown application.

        Gọi shutdown() của từng module theo thứ tự ngược lại,
        sau đó gọi lớp cha để cleanup engine.

        Args:
            exc_type: Exception type nếu có
            exc_val: Exception value nếu có
            exc_tb: Exception traceback nếu có
        """
        # Shutdown modules theo thứ tự ngược (LIFO)
        # Module khởi tạo sau sẽ shutdown trước
        for module in reversed(self._modules):
            await module.shutdown()

        # Gọi lớp cha để cleanup EngineFactory
        await super().__aexit__(exc_type, exc_val, exc_tb)
