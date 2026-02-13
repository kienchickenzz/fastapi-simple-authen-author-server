"""
Aggregation router cho User module.
"""
from fastapi import APIRouter

from src.user.endpoint.user_endpoint import router as user_router

main_router = APIRouter(prefix="/api")
main_router.include_router(user_router)
