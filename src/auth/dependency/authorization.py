"""
Dependency để kiểm tra quyền truy cập của user.

Permissions được lấy trực tiếp từ JWT token, không query database.
"""
from typing import Callable

from fastapi import Depends

from src.auth.dto.token_payload import TokenPayload
from src.auth.dependency.authentication import get_current_user
from src.auth.exception.auth_exception import InsufficientPermissionException


def require_permissions(*required: str) -> Callable[..., TokenPayload]:
    """
    Tạo dependency để kiểm tra user có đủ permissions hay không.

    Permissions được check từ token.permissions (không query DB).

    Args:
        *required (str): Danh sách permission codes cần thiết.

    Returns:
        Callable: Dependency function trả về TokenPayload nếu đủ quyền.

    Example:
        @router.post("/books")
        async def create_book(
            user: TokenPayload = Depends(require_permissions("book:create"))
        ):
            return {"created_by": user.user_id}
    """

    async def checker(
        user: TokenPayload = Depends(get_current_user),
    ) -> TokenPayload:
        """
        Kiểm tra permissions của user từ token.

        Args:
            user (TokenPayload): Thông tin user từ JWT (đã có permissions).

        Returns:
            TokenPayload: Trả về user nếu đủ quyền.

        Raises:
            InsufficientPermissionException: Khi thiếu quyền.
        """
        user_permissions = set(user.permissions)
        required_permissions = set(required)

        missing = required_permissions - user_permissions
        if missing:
            raise InsufficientPermissionException(missing)

        return user

    return checker
