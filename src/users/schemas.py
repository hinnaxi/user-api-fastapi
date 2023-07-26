from dataclasses import dataclass
from datetime import datetime
from typing import Union
from pydantic import BaseModel, EmailStr, model_validator, Field


class UserBase(BaseModel):
    """User base schema"""
    username: str
    first_name: str
    last_name: str
    email: EmailStr


@dataclass
class UserOutSchema(UserBase):
    """User response schema"""
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Union[datetime, None] = None

    class Config:
        from_attributes = True


@dataclass
class UserCreateSchema(UserBase):
    password: str
    password_confirm: str = Field(exclude=True, title="password_confirm")

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserCreateSchema':
        pw1 = self.password
        pw2 = self.password_confirm
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self


@dataclass
class UserUpdateSchema(UserBase):
    pass
