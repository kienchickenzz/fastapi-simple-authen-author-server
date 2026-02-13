"""
Aggregation router cho Auth module.
"""
from fastapi import APIRouter

from src.auth.endpoint.auth_endpoint import router as auth_router

main_router = APIRouter(prefix="/api")
main_router.include_router(auth_router)
