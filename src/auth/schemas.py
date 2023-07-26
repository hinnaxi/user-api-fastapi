from pydantic import BaseModel
from dataclasses import dataclass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


@dataclass
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
