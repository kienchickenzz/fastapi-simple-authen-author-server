"""
Model đại diện cho bảng books trong database.
"""
from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.base.database.model.base import Base


class Book(Base):
    """
    Model book trong hệ thống.

    Args:
        title (str): Tiêu đề sách.
        author (str): Tác giả.
        isbn (str | None): Mã ISBN, unique.
        description (str | None): Mô tả sách.
        quantity (int): Số lượng tồn kho.
    """

    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    isbn: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
