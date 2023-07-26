import logging
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from sqlalchemy.orm import Session
from src.auth.repository import AuthRepository
from src.auth.schemas import Token
from src.auth.services import AuthService, TokenService, get_current_user
from src.database import get_db
from src.exceptions import ApiException
from src.response import ApiResponse
from src.users.model import User
from src.users.schemas import UserCreateSchema, UserOutSchema

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/signup", response_model=UserOutSchema, status_code=HTTP_201_CREATED)
async def register(request: UserCreateSchema, db: Session = Depends(get_db)) -> JSONResponse:
    if await AuthRepository.user_exists(db, username=request.username):
        raise ApiException(status_code=HTTP_400_BAD_REQUEST, msg="Username already exist")
    try:
        user = AuthRepository.save(db, User(**request.model_dump()))
    except Exception as e:
        logger.error(e)
        raise ApiException(status_code=HTTP_400_BAD_REQUEST, msg="", errors=e.args)

    return ApiResponse.success(status_code=HTTP_201_CREATED, data=UserOutSchema.model_validate(user))


@router.post("/login", response_model=Token, status_code=HTTP_200_OK)
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> JSONResponse:
    user = await AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise ApiException(status_code=HTTP_401_UNAUTHORIZED, msg="Incorrect username or password")

    data = {
        "access_token": TokenService.create_access_token(user.username),
        "token_type": "bearer"
    }
    return ApiResponse.success(status_code=HTTP_200_OK, data=data)


@router.get("/me", response_model=UserOutSchema, status_code=HTTP_200_OK)
async def get_me(current_user: User = Depends(get_current_user)) -> JSONResponse:
    return ApiResponse.success(status_code=HTTP_200_OK, data=UserOutSchema.model_validate(current_user))
