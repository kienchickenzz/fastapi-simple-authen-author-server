"""
Service xử lý business logic cho User.
"""
from src.user.database.repository.user_repository import UserRepository
from src.user.database.repository.user_role_repository import UserRoleRepository
from src.role.database.repository.role_repository import RoleRepository
from src.user.dto.user_dto import (
    UserCreateRequest,
    UserUpdateRequest,
    UserResponse,
    UserListResponse,
    UserRoleResponse,
    UserRolesResponse,
)


class UserService:
    """
    Service cho User operations.

    Args:
        user_repository (UserRepository): Repository để truy cập users.
        user_role_repository (UserRoleRepository): Repository để quản lý user-role.
        role_repository (RoleRepository): Repository để truy cập roles.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        user_role_repository: UserRoleRepository,
        role_repository: RoleRepository,
    ):
        """
        Khởi tạo UserService.

        Args:
            user_repository (UserRepository): Repository để truy cập users.
            user_role_repository (UserRoleRepository): Repository để quản lý user-role.
            role_repository (RoleRepository): Repository để truy cập roles.
        """
        self._repository = user_repository
        self._user_role_repository = user_role_repository
        self._role_repository = role_repository

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

    # =========================================================================
    # User-Role Operations
    # =========================================================================

    async def get_roles(self, user_id: int) -> UserRolesResponse:
        """
        Lấy danh sách roles của một user.

        Args:
            user_id (int): ID của user.

        Returns:
            UserRolesResponse: Danh sách roles của user.

        Raises:
            ValueError: Nếu user không tồn tại.
        """
        user = await self._repository.get_one(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        roles = await self._user_role_repository.get_roles_by_user_id(user_id)

        return UserRolesResponse(
            user_id=user_id,
            roles=[
                UserRoleResponse(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                )
                for role in roles
            ],
        )

    async def assign_role(self, user_id: int, role_id: int) -> None:
        """
        Gán role cho user.

        Args:
            user_id (int): ID của user.
            role_id (int): ID của role cần gán.

        Raises:
            ValueError: Nếu user không tồn tại.
            ValueError: Nếu role không tồn tại.
            ValueError: Nếu user đã có role này.
        """
        user = await self._repository.get_one(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        role = await self._role_repository.get_one(role_id)
        if not role:
            raise ValueError(f"Role with id {role_id} not found")

        if await self._user_role_repository.has_role(user_id, role_id):
            raise ValueError(f"User already has role '{role.name}'")

        await self._user_role_repository.assign_role(user_id, role_id)

    async def remove_role(self, user_id: int, role_id: int) -> None:
        """
        Xóa role khỏi user.

        Args:
            user_id (int): ID của user.
            role_id (int): ID của role cần xóa.

        Raises:
            ValueError: Nếu user không tồn tại.
            ValueError: Nếu user không có role này.
        """
        user = await self._repository.get_one(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        removed = await self._user_role_repository.remove_role(user_id, role_id)
        if not removed:
            raise ValueError(f"User does not have role with id {role_id}")
