from fastapi import APIRouter

users_router = APIRouter()


@users_router.get("/")
async def index():
  return [{"username": "prasanna"}, {"username": "kumar"}]
