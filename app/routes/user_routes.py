from fastapi import APIRouter
from fastapi.security import HTTPBearer

from app.controllers.user_controller import UserController
from app.schemas.user_schema import TokenResponse, UserCreate, UserLogin

router = APIRouter(prefix="/user", tags=["user"])
security = HTTPBearer()


@router.post("/login", response_model=TokenResponse)
def login_user(user_data: UserLogin):
    controller = UserController()
    return controller.login_user(user_data)


@router.post("/")
def create_user(user_data: UserCreate):
    controller = UserController()
    return controller.create_user(user_data)


@router.get("/")
def get_users():
    controller = UserController()
    return controller.get_users()
