"""
Endpoints cho User CRUD operations.
"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.base.dependency_injection import Injects
from src.auth.dto.token_payload import TokenPayload
from src.auth.dependency.authorization import require_permissions
from src.user.dto.user_dto import (
    UserCreateRequest,
    UserUpdateRequest,
    UserListRequest,
)
from src.user.service.user_service import UserService
from src.user.doc import Tags

router = APIRouter(tags=[Tags.USER], prefix="/users")


@router.post(
    path="",
    summary="Create User",
    description="Create a new user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: UserCreateRequest,
    _: TokenPayload = Depends(require_permissions("user:create")),
    user_service: UserService = Injects("user_service"),
) -> JSONResponse:
    """
    Tạo user mới.

    Args:
        request (UserCreateRequest): Thông tin user cần tạo.
        _ (TokenPayload): Token payload (cần permission user:create).
        user_service (UserService): Service xử lý user.

    Returns:
        JSONResponse: User đã tạo.
    """
    result = await user_service.create(request)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=201)


@router.get(
    path="",
    summary="List Users",
    description="Get paginated list of users",
    status_code=status.HTTP_200_OK,
)
async def list_users(
    request: UserListRequest = Depends(UserListRequest.as_query),
    _: TokenPayload = Depends(require_permissions("user:read")),
    user_service: UserService = Injects("user_service"),
) -> JSONResponse:
    """
    Lấy danh sách users với phân trang.

    Args:
        request (UserListRequest): Request với thông tin phân trang.
        _ (TokenPayload): Token payload (cần permission user:read).
        user_service (UserService): Service xử lý user.

    Returns:
        JSONResponse: Danh sách users.
    """
    result = await user_service.get_list(request.target_page, request.page_size)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)


@router.get(
    path="/{user_id}",
    summary="Get User",
    description="Get user by ID",
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    _: TokenPayload = Depends(require_permissions("user:read")),
    user_service: UserService = Injects("user_service"),
) -> JSONResponse:
    """
    Lấy thông tin một user theo ID.

    Args:
        user_id (int): ID của user.
        _ (TokenPayload): Token payload (cần permission user:read).
        user_service (UserService): Service xử lý user.

    Returns:
        JSONResponse: Thông tin user.
    """
    result = await user_service.get_one(user_id)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)


@router.put(
    path="/{user_id}",
    summary="Update User",
    description="Update user by ID",
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    request: UserUpdateRequest,
    _: TokenPayload = Depends(require_permissions("user:update")),
    user_service: UserService = Injects("user_service"),
) -> JSONResponse:
    """
    Cập nhật thông tin user.

    Args:
        user_id (int): ID của user cần update.
        request (UserUpdateRequest): Thông tin cần update.
        _ (TokenPayload): Token payload (cần permission user:update).
        user_service (UserService): Service xử lý user.

    Returns:
        JSONResponse: User đã update.
    """
    result = await user_service.update(user_id, request)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)


@router.delete(
    path="/{user_id}",
    summary="Delete User",
    description="Delete user by ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int,
    _: TokenPayload = Depends(require_permissions("user:delete")),
    user_service: UserService = Injects("user_service"),
) -> None:
    """
    Xóa user theo ID.

    Args:
        user_id (int): ID của user cần xóa.
        _ (TokenPayload): Token payload (cần permission user:delete).
        user_service (UserService): Service xử lý user.
    """
    await user_service.delete(user_id)
    return None
