"""
Module định nghĩa model HealthCheck.
Sử dụng để lưu trữ và kiểm tra kết nối database.
"""
from src.base.database.model.base import Base


class HealthCheck(Base):
    """
    Model để kiểm tra health của database connection.

    Table này chỉ chứa các trường cơ bản từ Base (id, created_at, updated_at)
    và được sử dụng để verify database connectivity.
    """

    __tablename__ = "health_check"

    def __repr__(self) -> str:
        return "HealthCheck()"
