"""
Endpoints cho Authentication operations.
"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.base.dependency_injection import Injects
from src.auth.dto.auth_dto import (
    SignUpRequest,
    SignInRequest,
)
from src.auth.service.auth_service import AuthService
from src.auth.doc import Tags

router = APIRouter(tags=[Tags.AUTH], prefix="/auth")
security = HTTPBearer()


@router.post(
    path="/sign-up",
    summary="Sign Up",
    description="Register a new user account",
    status_code=status.HTTP_201_CREATED,
)
async def sign_up(
    request: SignUpRequest,
    auth_service: AuthService = Injects("auth_service"),
) -> JSONResponse:
    """
    Đăng ký user mới.

    Args:
        request (SignUpRequest): Thông tin đăng ký.
        auth_service (AuthService): Service xử lý authentication.

    Returns:
        JSONResponse: Thông tin user đã tạo.
    """
    result = await auth_service.sign_up(request)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=201)


@router.post(
    path="/sign-in",
    summary="Sign In",
    description="Authenticate and get access token",
    status_code=status.HTTP_200_OK,
)
async def sign_in(
    request: SignInRequest,
    auth_service: AuthService = Injects("auth_service"),
) -> JSONResponse:
    """
    Đăng nhập và lấy access token.

    Args:
        request (SignInRequest): Thông tin đăng nhập.
        auth_service (AuthService): Service xử lý authentication.

    Returns:
        JSONResponse: Access token.
    """
    result = await auth_service.sign_in(request)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)


@router.post(
    path="/sign-out",
    summary="Sign Out",
    description="Logout and invalidate access token",
    status_code=status.HTTP_200_OK,
)
async def sign_out(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Injects("auth_service"),
) -> JSONResponse:
    """
    Đăng xuất và vô hiệu hóa token.

    Args:
        credentials (HTTPAuthorizationCredentials): Bearer token.
        auth_service (AuthService): Service xử lý authentication.

    Returns:
        JSONResponse: Thông báo thành công.
    """
    result = await auth_service.sign_out(credentials.credentials)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)
