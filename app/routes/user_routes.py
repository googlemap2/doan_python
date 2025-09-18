from fastapi import APIRouter, Query, Request
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
def login_user(user_data: UserLogin) -> TokenResponse:
    """Đăng nhập người dùng và trả về token JWT"""
    return user_controller.login_user(user_data)


@router.post("/", response_model=CreateUserResponse)
def create_user(user_data: UserCreate) -> CreateUserResponse:
    """Tạo mới người dùng"""
    return user_controller.create_user(user_data)


@router.get("/{id}", response_model=GetUserResponse)
def get_user(id: int) -> GetUserResponse:
    """Lấy thông tin người dùng theo id"""
    return user_controller.get_user(id)


@router.get("/", response_model=GetUsersResponse)
def get_users(
    username: str | None = Query(None),
    phone: str | None = Query(None),
    address: str | None = Query(None),
    fullname: str | None = Query(None),
) -> GetUsersResponse:
    """Lấy danh sách người dùng với các bộ lọc tùy chọn"""
    return user_controller.get_users(
        username=username, phone=phone, address=address, fullname=fullname
    )


@router.put("/{id}", response_model=GetUserResponse)
def update_user(id: int, user_data: UserUpdate, request: Request) -> GetUserResponse:
    """Cập nhật thông tin người dùng"""
    user_id = getattr(request.state, "user_id", None)
    return user_controller.update_user(id, user_data, user_id=user_id)


@router.delete("/{id}", response_model=GetUserResponse)
def delete_user(id: int, request: Request) -> GetUserResponse:
    """Xóa người dùng"""
    user_id = getattr(request.state, "user_id", None)
    return user_controller.delete_user(id, user_id=user_id)
