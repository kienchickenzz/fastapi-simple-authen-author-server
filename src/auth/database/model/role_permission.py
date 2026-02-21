"""
Module định nghĩa model RolePermission cho junction table.
Quản lý quan hệ many-to-many giữa Role và Permission.
"""
from sqlalchemy import ForeignKey, UniqueConstraint, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.base.database.model.base import Base


class RolePermission(Base):
    """
    Junction table model cho quan hệ Role-Permission.

    Một Role có thể có nhiều Permissions và một Permission
    có thể thuộc về nhiều Roles.

    Attributes:
        role_id (int): Foreign key đến roles.id.
        permission_id (int): Foreign key đến permissions.id.
    """
    __tablename__ = "role_permissions"

    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    )
    permission_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
    )
