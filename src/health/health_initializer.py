from types import TracebackType
from typing import Optional, Type

from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi import FastAPI

from src.base.initializer import State, Initializer
from src.health.database.repository.health_check.main import HealthCheckRepository
from src.health.service.health_check.main import HealthCheckService
from src.auth.service.token_service import TokenService
from src.auth.service.auth_service import AuthService
from src.auth.repository.permission_repository import PermissionRepository
from src.auth.database.repository.token_repository import TokenRepository
from src.user.database.repository.user_repository import UserRepository
from src.user.service.user_service import UserService
from src.book.database.repository.book_repository import BookRepository
from src.book.service.book_service import BookService


class ServiceState(State):
    # Services
    health_check_service: HealthCheckService
    token_service: TokenService
    auth_service: AuthService
    user_service: UserService
    book_service: BookService
    # Repositories
    db_engine: AsyncEngine
    health_check_repository: HealthCheckRepository
    permission_repository: PermissionRepository
    token_repository: TokenRepository
    user_repository: UserRepository
    book_repository: BookRepository

class HealthInitializer(Initializer):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app=app)

    async def __aenter__(self) -> ServiceState:
        state = await super().__aenter__()

        # DB engine
        db_engine = self.engine_factory.create_engine("DB")

        # Initialize utilities

        # Initialize repositories
        health_check_repository = HealthCheckRepository(engine=db_engine)

        # Initialize services/tools
        health_check_service = HealthCheckService(
            health_check_repository=health_check_repository,
        )

        # User repository (needed by auth service)
        user_repository = UserRepository(engine=db_engine)

        # Auth services
        token_service = TokenService(config=self.config)
        permission_repository = PermissionRepository(engine=db_engine)
        token_repository = TokenRepository(engine=db_engine)
        auth_service = AuthService(
            user_repository=user_repository,
            token_service=token_service,
            token_repository=token_repository,
        )

        # User services
        user_service = UserService(user_repository=user_repository)

        # Book services
        book_repository = BookRepository(engine=db_engine)
        book_service = BookService(book_repository=book_repository)

        return ServiceState(
            **state,
            db_engine=db_engine,
            health_check_repository=health_check_repository,
            health_check_service=health_check_service,
            token_service=token_service,
            auth_service=auth_service,
            permission_repository=permission_repository,
            token_repository=token_repository,
            user_repository=user_repository,
            user_service=user_service,
            book_repository=book_repository,
            book_service=book_service,
        )

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        await super().__aexit__(exc_type, exc_val, exc_tb)
        # self.logger.info("detector_service_stopped")
