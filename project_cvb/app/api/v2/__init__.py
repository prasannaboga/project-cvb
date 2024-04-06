from fastapi import APIRouter
from .users import router as users_router

v2_router = APIRouter()
v2_router.include_router(users_router, prefix="/users")