"""
DTO cho Book endpoints.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_serializer

from src.base.dto.main import PaginatedRequestBase, PaginatedResponseBase, ResponseBase


# === Request DTOs ===
class BookCreateRequest(BaseModel):
    """
    Request tạo book mới.

    Args:
        title (str): Tiêu đề sách.
        author (str): Tác giả.
        isbn (str | None): Mã ISBN.
        description (str | None): Mô tả sách.
        quantity (int): Số lượng tồn kho.
    """

    title: str
    author: str
    isbn: Optional[str] = None
    description: Optional[str] = None
    quantity: int = 0


class BookUpdateRequest(BaseModel):
    """
    Request cập nhật book.

    Args:
        title (str | None): Tiêu đề mới.
        author (str | None): Tác giả mới.
        isbn (str | None): Mã ISBN mới.
        description (str | None): Mô tả mới.
        quantity (int | None): Số lượng mới.
    """

    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None


class BookListRequest(PaginatedRequestBase):
    """
    Request lấy danh sách books với phân trang.
    """

    pass


# === Response DTOs ===
class BookResponse(ResponseBase):
    """
    Response cho single book.

    Args:
        id (int): ID của book.
        title (str): Tiêu đề sách.
        author (str): Tác giả.
        isbn (str | None): Mã ISBN.
        description (str | None): Mô tả sách.
        quantity (int): Số lượng tồn kho.
        created_at (datetime): Thời gian tạo.
        updated_at (datetime): Thời gian cập nhật.
    """

    id: int
    title: str
    author: str
    isbn: Optional[str]
    description: Optional[str]
    quantity: int
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dates(self, value: datetime) -> str:
        """Serialize datetime to ISO format string."""
        return value.isoformat() if value else None


class BookListResponse(PaginatedResponseBase):
    """
    Response cho danh sách books với phân trang.

    Args:
        books (list[BookResponse]): Danh sách books.
    """

    books: list[BookResponse]
