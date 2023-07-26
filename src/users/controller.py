from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from sqlalchemy.orm import Session
from src.auth.services import get_current_user
from src.database import get_db
from src.exceptions import ApiException
from src.response import ApiResponse
from src.users.model import User
from src.users.repository import UserRepository
from src.users.schemas import UserCreateSchema, UserOutSchema, UserUpdateSchema
from fastapi_pagination import paginate
from fastapi_pagination.links import Page

router = APIRouter()


@router.get("/", response_model=Page[UserOutSchema], status_code=HTTP_200_OK)
def find_all(db: Session = Depends(get_db)) -> JSONResponse:
    users = UserRepository.find_all(db)
    return ApiResponse.success(status_code=HTTP_200_OK, data=paginate([UserOutSchema.model_validate(user) for user in users]))


@router.get("/{user_id}", response_model=UserOutSchema, status_code=HTTP_200_OK)
def find_by_id(user_id: int, db: Session = Depends(get_db)) -> JSONResponse:
    user = UserRepository.find_by_id(db, user_id)
    if not user:
        raise ApiException(status_code=HTTP_404_NOT_FOUND, msg="User not found")

    return ApiResponse.success(status_code=HTTP_200_OK, data=UserOutSchema.model_validate(user))


@router.post("/", response_model=UserOutSchema, status_code=HTTP_201_CREATED)
def create(request: UserCreateSchema, db: Session = Depends(get_db), _current_user: User = Depends(get_current_user)) -> JSONResponse:
    user = UserRepository.save(db, User(**request.model_dump()))
    return ApiResponse.success(status_code=HTTP_201_CREATED, data=UserOutSchema.model_validate(user))


@router.put("/{user_id}", response_model=UserOutSchema, status_code=HTTP_200_OK)
def update(user_id: int, request: UserUpdateSchema, db: Session = Depends(get_db), _current_user: User = Depends(get_current_user)) -> JSONResponse:
    if not UserRepository.user_exists(db, user_id):
        raise ApiException(status_code=HTTP_404_NOT_FOUND, msg="User not found")

    user = UserRepository.save(db, User(user_id=user_id, **request.model_dump()))
    return ApiResponse.success(status_code=HTTP_200_OK, data=UserOutSchema.model_validate(user))


@router.delete("/{user_id}", status_code=HTTP_200_OK)
def delete(user_id: int, db: Session = Depends(get_db), _current_user: User = Depends(get_current_user)) -> JSONResponse:
    if not UserRepository.user_exists(db, user_id):
        raise ApiException(status_code=HTTP_404_NOT_FOUND, msg="User not found")

    deleted_id = UserRepository.delete_by_id(db, user_id)
    return ApiResponse.success(status_code=HTTP_200_OK, data={deleted_id})
