from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.base_schema import ResponseType




class UserBase(BaseModel):
    username: str
    fullname: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool = True


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    fullname: str
    phone: str
    address: Optional[str] = None
    password: str
    is_active: Optional[bool] = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    fullname: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    fullname: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


# Alias cho backward compatibility
User = UserResponse


class UserList(BaseModel):
    users: list[UserResponse]
    total: int
    page: int
    size: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(ResponseType[Token]):
    pass


class TokenData(BaseModel):
    username: Optional[str] = None
