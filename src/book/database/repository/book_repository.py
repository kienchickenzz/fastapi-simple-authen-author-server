"""
Repository để thao tác với bảng books.
"""
from sqlalchemy.ext.asyncio import AsyncEngine

from src.base.database.repository.base import Repository
from src.book.database.model.book import Book


class BookRepository(Repository[Book]):
    """
    Repository cho Book entity.

    Args:
        engine (AsyncEngine): SQLAlchemy async engine.
    """

    def __init__(self, engine: AsyncEngine):
        """
        Khởi tạo BookRepository.

        Args:
            engine (AsyncEngine): SQLAlchemy async engine.
        """
        super().__init__(engine, Book)

    async def get_by_isbn(self, isbn: str) -> Book | None:
        """
        Tìm book theo ISBN.

        Args:
            isbn (str): ISBN cần tìm.

        Returns:
            Book | None: Book nếu tìm thấy, None nếu không.
        """
        sql = "SELECT * FROM books WHERE isbn = :isbn"
        results = await self.fetch_sql(sql, {"isbn": isbn})
        if not results:
            return None
        return Book(**dict(results[0]))

    async def delete(self, book_id: int) -> bool:
        """
        Xóa book theo id.

        Args:
            book_id (int): ID của book cần xóa.

        Returns:
            bool: True nếu xóa thành công.
        """
        sql = "DELETE FROM books WHERE id = :book_id"
        row_count = await self.execute_sql(sql, {"book_id": book_id})
        return row_count > 0
