"""
Custom exceptions cho authentication và authorization.
"""
from fastapi import HTTPException, status


class InvalidTokenException(HTTPException):
    """
    Exception khi JWT token không hợp lệ.
    """

    def __init__(self, detail: str = "Invalid token"):
        """
        Khởi tạo InvalidTokenException.

        Args:
            detail (str): Chi tiết lỗi.
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class ExpiredTokenException(HTTPException):
    """
    Exception khi JWT token đã hết hạn.
    """

    def __init__(self):
        """
        Khởi tạo ExpiredTokenException.
        """
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InsufficientPermissionException(HTTPException):
    """
    Exception khi user không có đủ quyền.
    """

    def __init__(self, missing_permissions: set[str]):
        """
        Khởi tạo InsufficientPermissionException.

        Args:
            missing_permissions (set[str]): Các quyền bị thiếu.
        """
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing permissions: {missing_permissions}",
        )
