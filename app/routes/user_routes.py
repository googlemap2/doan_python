from urllib import response
from fastapi import APIRouter, Query
from fastapi.security import HTTPBearer

from app.controllers.user_controller import UserController
from app.schemas.user_schema import (
    CreateUserResponse,
    GetUserResponse,
    GetUsersResponse,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserUpdate,
)

router = APIRouter(prefix="/user", tags=["user"])
security = HTTPBearer()
user_controller = UserController()


@router.post("/login", response_model=TokenResponse)
def login_user(user_data: UserLogin):
    return user_controller.login_user(user_data)


@router.post("/", response_model=CreateUserResponse)
def create_user(user_data: UserCreate):
    return user_controller.create_user(user_data)


@router.get("/", response_model=GetUsersResponse)
def get_users(
    username: str | None = Query(None, description="Filter by username"),
    phone: str | None = Query(None, description="Filter by phone number"),
    address: str | None = Query(None, description="Filter by address"),
    fullname: str | None = Query(None, description="Filter by full name"),
):
    return user_controller.get_users(
        username=username, phone=phone, address=address, fullname=fullname
    )

@router.put("/{username}", response_model=GetUserResponse)
def update_user(username: str, user_data: UserUpdate):
    return user_controller.update_user(username, user_data)

@router.delete("/{username}", response_model=GetUserResponse)
def delete_user(username: str):
    return user_controller.delete_user(username)