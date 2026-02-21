"""
Module định nghĩa model UserRole cho junction table.
Quản lý quan hệ many-to-many giữa User và Role.
"""
from sqlalchemy import ForeignKey, UniqueConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.base.database.model.base import Base


class UserRole(Base):
    """
    Junction table model cho quan hệ User-Role.

    Một User có thể có nhiều Roles và một Role
    có thể được gán cho nhiều Users.

    Attributes:
        user_id (int): Foreign key đến users.id.
        role_id (int): Foreign key đến roles.id.
    """
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )
