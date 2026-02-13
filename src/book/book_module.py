"""
Module đăng ký dependencies cho Book service.

BookModule là một module độc lập, không phụ thuộc vào module nào khác.
Có thể được khởi tạo ở bất kỳ vị trí nào trong danh sách modules.
"""

from dataclasses import dataclass

from src.base.module import IModule, ModuleContext, ModuleDependencies
from src.book.database.repository.book_repository import BookRepository
from src.book.service.book_service import BookService


@dataclass
class BookModule(IModule):
    """
    Module khởi tạo Book service và repository.

    Dependencies được cung cấp:
        - book_repository: BookRepository instance
        - book_service: BookService instance

    Cross-module dependencies: Không có (module độc lập)
    """

    _repository: BookRepository | None = None
    _service: BookService | None = None

    async def initialize(self, context: ModuleContext) -> ModuleDependencies:
        """
        Khởi tạo BookRepository và BookService.

        Args:
            context (ModuleContext): Chứa db_engine và config

        Returns:
            ModuleDependencies: book_repository và book_service
        """
        self._repository = BookRepository(engine=context.db_engine)
        self._service = BookService(book_repository=self._repository)

        return ModuleDependencies(
            services={"book_service": self._service},
            repositories={"book_repository": self._repository},
        )
