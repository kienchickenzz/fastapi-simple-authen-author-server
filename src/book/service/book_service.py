"""
Service xử lý business logic cho Book.
"""
from src.book.database.repository.book_repository import BookRepository
from src.book.dto.book_dto import (
    BookCreateRequest,
    BookUpdateRequest,
    BookResponse,
    BookListResponse,
)


class BookService:
    """
    Service cho Book operations.

    Args:
        book_repository (BookRepository): Repository để truy cập DB.
    """

    def __init__(self, book_repository: BookRepository):
        """
        Khởi tạo BookService.

        Args:
            book_repository (BookRepository): Repository để truy cập DB.
        """
        self._repository = book_repository

    async def create(self, request: BookCreateRequest) -> BookResponse:
        """
        Tạo book mới.

        Args:
            request (BookCreateRequest): Thông tin book cần tạo.

        Returns:
            BookResponse: Book đã tạo.
        """
        values = request.model_dump()
        book = await self._repository.create(values)
        return BookResponse(**book.__dict__)

    async def get_one(self, book_id: int) -> BookResponse:
        """
        Lấy thông tin một book.

        Args:
            book_id (int): ID của book.

        Returns:
            BookResponse: Thông tin book.
        """
        book = await self._repository.get_one(book_id)
        return BookResponse(**book.__dict__)

    async def get_list(self, target_page: int, page_size: int) -> BookListResponse:
        """
        Lấy danh sách books với phân trang.

        Args:
            target_page (int): Trang cần lấy.
            page_size (int): Số lượng mỗi trang.

        Returns:
            BookListResponse: Danh sách books.
        """
        skip = (target_page - 1) * page_size
        books, total = await self._repository.get_multiple(skip=skip, limit=page_size)
        total_pages = (total + page_size - 1) // page_size

        return BookListResponse(
            books=[BookResponse(**b.__dict__) for b in books],
            current_page=target_page,
            total_pages=total_pages,
            page_size=page_size,
        )

    async def update(self, book_id: int, request: BookUpdateRequest) -> BookResponse:
        """
        Cập nhật thông tin book.

        Args:
            book_id (int): ID của book cần update.
            request (BookUpdateRequest): Thông tin cần update.

        Returns:
            BookResponse: Book đã update.
        """
        values = request.model_dump(exclude_unset=True)
        book = await self._repository.update(book_id, values)
        return BookResponse(**book.__dict__)

    async def delete(self, book_id: int) -> bool:
        """
        Xóa book.

        Args:
            book_id (int): ID của book cần xóa.

        Returns:
            bool: True nếu xóa thành công.
        """
        return await self._repository.delete(book_id)
