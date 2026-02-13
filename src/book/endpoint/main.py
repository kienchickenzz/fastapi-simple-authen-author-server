"""
Aggregation router cho Book module.
"""
from fastapi import APIRouter

from src.book.endpoint.book_endpoint import router as book_router

main_router = APIRouter(prefix="/api")
main_router.include_router(book_router)
