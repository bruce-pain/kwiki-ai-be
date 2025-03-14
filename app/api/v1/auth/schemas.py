from typing import Annotated, Optional

from pydantic import BaseModel, StringConstraints
from app.core.base.schema import BaseResponseModel


class RegisterRequest(BaseModel):
    password: Optional[str] = None
    username: Annotated[str, StringConstraints(max_length=70)]


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class TokenRefreshResponse(BaseResponseModel):
    access_token: str


class AuthResponseData(BaseModel):
    id: str
    username: str


class AuthResponse(BaseResponseModel):
    access_token: str
    refresh_token: str
    data: AuthResponseData
