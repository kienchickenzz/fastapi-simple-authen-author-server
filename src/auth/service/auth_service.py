"""
Service xử lý authentication logic.
"""
import hashlib

from src.auth.dto.auth_dto import (
    SignUpRequest,
    SignUpResponse,
    SignInRequest,
    SignInResponse,
    SignOutResponse,
)
from src.auth.service.token_service import TokenService
from src.auth.database.repository.token_repository import TokenRepository
from src.auth.exception.auth_exception import InvalidTokenException
from src.user.database.repository.user_repository import UserRepository


class AuthService:
    """
    Service cho authentication operations.

    Args:
        user_repository (UserRepository): Repository để truy cập users.
        token_service (TokenService): Service để tạo/verify JWT.
        token_repository (TokenRepository): Repository để quản lý tokens.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        token_service: TokenService,
        token_repository: TokenRepository,
    ):
        """
        Khởi tạo AuthService.

        Args:
            user_repository (UserRepository): Repository để truy cập users.
            token_service (TokenService): Service để tạo/verify JWT.
            token_repository (TokenRepository): Repository để quản lý tokens.
        """
        self._user_repository = user_repository
        self._token_service = token_service
        self._token_repository = token_repository

    async def sign_up(self, request: SignUpRequest) -> SignUpResponse:
        """
        Đăng ký user mới.

        Args:
            request (SignUpRequest): Thông tin đăng ký.

        Returns:
            SignUpResponse: Thông tin user đã tạo.
        """
        password_hash = self._hash_password(request.password)
        values = {
            "username": request.username,
            "email": request.email,
            "password_hash": password_hash,
            "is_active": True,
        }
        user = await self._user_repository.create(values)
        return SignUpResponse(
            id=user.id,
            username=user.username,
            email=user.email,
        )

    async def sign_in(self, request: SignInRequest) -> SignInResponse:
        """
        Đăng nhập và trả về JWT token.

        Args:
            request (SignInRequest): Thông tin đăng nhập.

        Returns:
            SignInResponse: Access token.

        Raises:
            InvalidTokenException: Khi credentials không hợp lệ.
        """
        user = await self._user_repository.get_by_username(request.username)
        if not user:
            raise InvalidTokenException("Invalid username or password")

        if not self._verify_password(request.password, user.password_hash):
            raise InvalidTokenException("Invalid username or password")

        if not user.is_active:
            raise InvalidTokenException("User is inactive")

        # Tạo JWT token
        # TODO: Thêm claims như permissions vào token, hiện tại chỉ có user_id
        access_token = self._token_service.encode(user.id)
        expired_at = self._token_service.get_expiration(access_token)

        # Lưu token vào database với trạng thái active
        await self._token_repository.create_token(
            user_id=user.id,
            token=access_token,
            expired_at=expired_at,
        )

        return SignInResponse(access_token=access_token)

    async def sign_out(self, token: str) -> SignOutResponse:
        """
        Đăng xuất bằng cách deactivate token.

        Args:
            token (str): JWT token cần invalidate.

        Returns:
            SignOutResponse: Thông báo thành công.
        """
        await self._token_repository.deactivate_token(token)
        return SignOutResponse(message="Successfully signed out")

    async def is_token_active(self, token: str) -> bool:
        """
        Kiểm tra token có active không.

        Args:
            token (str): JWT token cần kiểm tra.

        Returns:
            bool: True nếu token active.
        """
        return await self._token_repository.is_token_active(token)

    def _hash_password(self, password: str) -> str:
        """
        Hash password sử dụng SHA256.

        Args:
            password (str): Password cần hash.

        Returns:
            str: Password đã hash.
        """
        # TODO: Sử dụng bcrypt hoặc argon2 trong production
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify password với hash.

        Args:
            password (str): Password cần verify.
            password_hash (str): Hash để so sánh.

        Returns:
            bool: True nếu password khớp.
        """
        return self._hash_password(password) == password_hash
