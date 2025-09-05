from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Base schemas
class UserBase(BaseModel):
    username: str
    fullname: Optional[str] = None
    is_active: bool = True


class UserLogin(BaseModel):
    username: str
    password: str


class fullnameUserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    fullname: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    fullname: str
    is_active: Optional[bool] = None
    password: str
    phone: str


class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Response schemas
class User(UserInDB):
    pass


class UserList(BaseModel):
    users: list[User]
    total: int
    page: int
    size: int


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
