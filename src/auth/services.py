from src.exceptions import ApiException
from datetime import datetime, timedelta
from typing import Annotated
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from src.auth.repository import AuthRepository
from src.auth.schemas import TokenData
from src.config import settings
from src.database import get_db
from src.users.schemas import UserOutSchema
from src.utils import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
credentials_exception = ApiException(
    status_code=HTTP_401_UNAUTHORIZED,
    msg="Invalid authentication credentials"
)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    token_data = await TokenService.decode_token(token)
    user = await AuthService.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


class TokenService:
    @staticmethod
    def token_response(token: str):
        return {
            "access_token": token
        }

    @staticmethod
    def _create_token(token_type: str, lifetime: timedelta, sub: str, secret_key: str) -> str:
        payload = {}
        expire = datetime.utcnow() + lifetime
        payload["type"] = token_type
        payload["exp"] = expire
        payload["iat"] = datetime.utcnow()
        payload["sub"] = str(sub)

        return jwt.encode(payload, secret_key, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def create_access_token(sub: str) -> token_response:
        return TokenService._create_token(
            token_type="access_token",
            lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXP_MINUTES),
            sub=sub,
            secret_key=settings.JWT_SECRET_KEY
        )

    @staticmethod
    async def decode_token(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                options={"verify_aud": False},
            )

            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception

            token_data = TokenData(username=username)

            return token_data
        except JWTError:
            raise credentials_exception


class AuthService:
    @staticmethod
    async def get_user(db: Session, username: str):
        return AuthRepository.find_by_username(db, username=username)

    @staticmethod
    async def get_current_active_user(current_user: Annotated[UserOutSchema, Depends(get_current_user)]):
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return await current_user

    @staticmethod
    async def authenticate_user(db: Session, username: str, plain_pass: str):
        user = AuthRepository.find_by_username(db, username=username)
        if not user:
            return False
        if not verify_password(plain_pass, user.password):
            return False

        return user
