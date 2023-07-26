from fastapi import APIRouter, status
from src.users.controller import router as users_router
from src.auth.controller import router as auth_router

api_router = APIRouter()


@api_router.get("/health", status_code=status.HTTP_200_OK, tags=["API"])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
