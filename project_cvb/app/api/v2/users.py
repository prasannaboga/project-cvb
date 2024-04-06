from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def index():
  return [{"username": "prasanna"}, {"username": "kumar"}, {"username": "v2"}]
