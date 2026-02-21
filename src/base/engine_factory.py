"""
Module quản lý việc tạo và quản lý database engines.
Cung cấp EngineFactory để tạo async SQLAlchemy engines với cấu hình phù hợp.
"""
from threading import Lock
from types import TracebackType
from typing import Dict, Optional, Type
from uuid import uuid4

from asyncpg import Connection  # type: ignore[import]
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.config import Config


class EngineFactory:
    """
    Encapsulates the configurations required by data-platform to establish direct
    access to either data-platform or RDS.

    To create engines you will need the following environment variables:
        <<database_identifier>>_HOST
        <<database_identifier>>_PORT
        <<database_identifier>>_NAME
        <<database_identifier>>_USER
        <<database_identifier>>_PASSWORD

    Where <<database_identifier>> is the prefix to uniquely indentify the engine you want to create.
    This factory is already context managed by FastAPIInitializer, so it can be used straight away:

    >>> class MyInitializer(Initializer):
    ...     def __init__(self, app: FastAPI) -> None:
    ...         super().__init__(app)
    ...         self.my_repository: MyRepository
    ...
    ...     async def __aenter__(self) -> MyInitializer:
    ...         await super().__aenter__()
    ...         engine = self.engine_factory.create_engine("MY_DB")
    ...         self.my_repository = MyRepository(engine)
    ...
    ...     async def __aexit__(
    ...         self,
    ...         exc_type: Optional[Type[BaseException]],
    ...         exc_val: Optional[BaseException],
    ...         exc_tb: Optional[TracebackType]
    ...     ) -> None:
    ...          await super().__aexit__(exc_type, exc_val, exc_tb)

    This factory guarantees that only one engine will be created per repository, and you will
    be able to retrieve the engine as many times as you want.
    """

    def __init__(self, *, config: Config):
        """
        Khởi tạo EngineFactory.

        Args:
            config (Config): Config instance để đọc database credentials.
        """
        self._config = config
        self._engine_init_lock: Lock = Lock()
        self._engines: Dict[str, AsyncEngine] = {}

    async def __aenter__(self) -> "EngineFactory":
        """
        Async context manager entry point.

        Returns:
            EngineFactory: Self instance.
        """
        return self

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        """
        Async context manager exit point. Dispose tất cả engines.

        Args:
            exc_type (Optional[Type[BaseException]]): Exception type nếu có.
            exc_val (Optional[BaseException]): Exception value nếu có.
            exc_tb (Optional[TracebackType]): Traceback nếu có.
        """
        for database_identifier, engine in self._engines.items():
            await engine.dispose()

    def create_engine(self, database_identifier: str) -> AsyncEngine:
        """
        Tạo hoặc lấy engine đã tồn tại cho database identifier.

        Thread-safe method đảm bảo chỉ tạo một engine cho mỗi identifier.

        Args:
            database_identifier (str): Prefix để tìm config
                (e.g., "DB" sẽ tìm DB_HOST, DB_PORT, ...).

        Returns:
            AsyncEngine: SQLAlchemy async engine instance.
        """
        with self._engine_init_lock:
            if database_identifier not in self._engines:
                self._engines[database_identifier] = self._create_no_pool_engine(database_identifier.upper())

        return self._engines[database_identifier]

    def _create_no_pool_engine(self, database_identifier: str) -> AsyncEngine:
        """
        Tạo async engine không sử dụng connection pool.

        Engine được cấu hình để tương thích với pgbouncer trong
        transaction/statement pool mode bằng cách disable prepared statements.

        Args:
            database_identifier (str): Prefix để tìm config
                (e.g., "DB" sẽ tìm DB_HOST, DB_PORT, ...).

        Returns:
            AsyncEngine: SQLAlchemy async engine với NullPool.
        """
        db_host = self._config.require_config(f"{database_identifier}_HOST")
        db_port = self._config.require_config(f"{database_identifier}_PORT")
        db_name = self._config.require_config(f"{database_identifier}_NAME")
        db_user = self._config.require_config(f"{database_identifier}_USER")
        db_password = self._config.require_config(f"{database_identifier}_PASSWORD")
        url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        # Data-platform configure DBs in a way that services can't have connection pools,
        # since connections are closed and returned as soon as the query is completed.
        # We should not allow any pooling nor caching in our engine otherwise we will see
        # errors in staging/production -> pgbouncer with pool_mode set to "transaction" or
        # "statement" does not support prepared statements properly.
        return create_async_engine(
            url=url,
            echo=False,
            poolclass=NullPool,
            connect_args={
                "server_settings": {"application_name": "test"},
                "statement_cache_size": 0,
                "prepared_statement_cache_size": 0,
                "connection_class": _CConnection,
            },
        )


# Necessary hack to handle data-platform no pooling configuration,
# see https://github.com/sqlalchemy/sqlalchemy/issues/6467#issuecomment-864943824
class _CConnection(Connection):
    """
    Custom Connection class để xử lý unique ID generation.

    Workaround cho vấn đề với asyncpg và SQLAlchemy khi
    không sử dụng connection pooling.
    """

    def _get_unique_id(self, prefix: str) -> str:
        """
        Tạo unique ID cho prepared statements.

        Args:
            prefix (str): Prefix cho unique ID.

        Returns:
            str: Unique ID string với format __asyncpg_{prefix}_{uuid}__.
        """
        return f"__asyncpg_{prefix}_{uuid4()}__"
