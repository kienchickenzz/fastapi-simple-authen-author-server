"""
Endpoints cho Book CRUD operations.
"""
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.base.dependency_injection import Injects
from src.auth.dto.token_payload import TokenPayload
from src.auth.dependency.authorization import require_permissions
from src.book.dto.book_dto import (
    BookCreateRequest,
    BookUpdateRequest,
    BookListRequest,
)
from src.book.service.book_service import BookService
from src.book.doc import Tags

router = APIRouter(tags=[Tags.BOOK], prefix="/books")


@router.post(
    path="",
    summary="Create Book",
    description="Create a new book",
    status_code=status.HTTP_201_CREATED,
)
async def create_book(
    request: BookCreateRequest,
    _: TokenPayload = Depends(require_permissions("book:create")),
    book_service: BookService = Injects("book_service"),
) -> JSONResponse:
    """
    Tạo book mới.

    Args:
        request (BookCreateRequest): Thông tin book cần tạo.
        _ (TokenPayload): Token payload (cần permission book:create).
        book_service (BookService): Service xử lý book.

    Returns:
        JSONResponse: Book đã tạo.
    """
    result = await book_service.create(request)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=201)


@router.get(
    path="",
    summary="List Books",
    description="Get paginated list of books",
    status_code=status.HTTP_200_OK,
)
async def list_books(
    request: BookListRequest = Depends(BookListRequest.as_query),
    _: TokenPayload = Depends(require_permissions("book:read")),
    book_service: BookService = Injects("book_service"),
) -> JSONResponse:
    """
    Lấy danh sách books với phân trang.

    Args:
        request (BookListRequest): Request với thông tin phân trang.
        _ (TokenPayload): Token payload (cần permission book:read).
        book_service (BookService): Service xử lý book.

    Returns:
        JSONResponse: Danh sách books.
    """
    result = await book_service.get_list(request.target_page, request.page_size)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)


@router.get(
    path="/{book_id}",
    summary="Get Book",
    description="Get book by ID",
    status_code=status.HTTP_200_OK,
)
async def get_book(
    book_id: int,
    _: TokenPayload = Depends(require_permissions("book:read")),
    book_service: BookService = Injects("book_service"),
) -> JSONResponse:
    """
    Lấy thông tin một book theo ID.

    Args:
        book_id (int): ID của book.
        _ (TokenPayload): Token payload (cần permission book:read).
        book_service (BookService): Service xử lý book.

    Returns:
        JSONResponse: Thông tin book.
    """
    result = await book_service.get_one(book_id)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)


@router.put(
    path="/{book_id}",
    summary="Update Book",
    description="Update book by ID",
    status_code=status.HTTP_200_OK,
)
async def update_book(
    book_id: int,
    request: BookUpdateRequest,
    _: TokenPayload = Depends(require_permissions("book:update")),
    book_service: BookService = Injects("book_service"),
) -> JSONResponse:
    """
    Cập nhật thông tin book.

    Args:
        book_id (int): ID của book cần update.
        request (BookUpdateRequest): Thông tin cần update.
        _ (TokenPayload): Token payload (cần permission book:update).
        book_service (BookService): Service xử lý book.

    Returns:
        JSONResponse: Book đã update.
    """
    result = await book_service.update(book_id, request)
    return JSONResponse(content=result.model_dump(mode="json"), status_code=200)


@router.delete(
    path="/{book_id}",
    summary="Delete Book",
    description="Delete book by ID",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_book(
    book_id: int,
    _: TokenPayload = Depends(require_permissions("book:delete")),
    book_service: BookService = Injects("book_service"),
) -> None:
    """
    Xóa book theo ID.

    Args:
        book_id (int): ID của book cần xóa.
        _ (TokenPayload): Token payload (cần permission book:delete).
        book_service (BookService): Service xử lý book.
    """
    await book_service.delete(book_id)
    return None
