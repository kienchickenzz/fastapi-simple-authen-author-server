"""
Service xử lý business logic cho User.
"""
from src.user.database.repository.user_repository import UserRepository
from src.user.dto.user_dto import (
    UserCreateRequest,
    UserUpdateRequest,
    UserResponse,
    UserListResponse,
)


class UserService:
    """
    Service cho User operations.

    Args:
        user_repository (UserRepository): Repository để truy cập DB.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Khởi tạo UserService.

        Args:
            user_repository (UserRepository): Repository để truy cập DB.
        """
        self._repository = user_repository

    async def create(self, request: UserCreateRequest) -> UserResponse:
        """
        Tạo user mới.

        Args:
            request (UserCreateRequest): Thông tin user cần tạo.

        Returns:
            UserResponse: User đã tạo.
        """
        # TODO: Hash password trước khi lưu
        values = {
            "username": request.username,
            "email": request.email,
            "password_hash": request.password,  # Cần hash
            "is_active": True,
        }
        user = await self._repository.create(values)
        return UserResponse(**user.__dict__)

    async def get_one(self, user_id: int) -> UserResponse:
        """
        Lấy thông tin một user.

        Args:
            user_id (int): ID của user.

        Returns:
            UserResponse: Thông tin user.
        """
        user = await self._repository.get_one(user_id)
        return UserResponse(**user.__dict__)

    async def get_list(self, target_page: int, page_size: int) -> UserListResponse:
        """
        Lấy danh sách users với phân trang.

        Args:
            target_page (int): Trang cần lấy.
            page_size (int): Số lượng mỗi trang.

        Returns:
            UserListResponse: Danh sách users.
        """
        skip = (target_page - 1) * page_size
        users, total = await self._repository.get_multiple(skip=skip, limit=page_size)
        total_pages = (total + page_size - 1) // page_size

        return UserListResponse(
            users=[UserResponse(**u.__dict__) for u in users],
            current_page=target_page,
            total_pages=total_pages,
            page_size=page_size,
        )

    async def update(self, user_id: int, request: UserUpdateRequest) -> UserResponse:
        """
        Cập nhật thông tin user.

        Args:
            user_id (int): ID của user cần update.
            request (UserUpdateRequest): Thông tin cần update.

        Returns:
            UserResponse: User đã update.
        """
        values = request.model_dump(exclude_unset=True)
        user = await self._repository.update(user_id, values)
        return UserResponse(**user.__dict__)

    async def delete(self, user_id: int) -> bool:
        """
        Xóa user.

        Args:
            user_id (int): ID của user cần xóa.

        Returns:
            bool: True nếu xóa thành công.
        """
        return await self._repository.delete(user_id)
