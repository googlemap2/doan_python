from fastapi import HTTPException, status
from app.models import user
from app.models.user import User
from app.schemas.user_schema import (
    CreateUserResponse,
    GetUserResponse,
    GetUsersResponse,
    TokenResponse,
    UserCreate,
    UserLogin,
)
from app.utils.auth import create_access_token, verify_password
from app.config.database import SessionLocal
from app.utils.auth import get_password_hash as hash_password
from app.services.user_service import UserService
from app.utils.helpers import ResponseHelper


class UserController:

    def __init__(self):
        self.db = SessionLocal()
        self.user_service = UserService()

    def login_user(self, user_data: UserLogin) -> TokenResponse:
        return self.user_service.login_user(user_data)

    def create_user(self, user_data: UserCreate) -> CreateUserResponse:
        return self.user_service.create_user(user_data)

    def get_users(
        self,
        username: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        fullname: str | None = None,
    ) -> GetUsersResponse:
        users = self.user_service.get_users(
            username=username, phone=phone, address=address, fullname=fullname
        )
        return users

    def get_user(self, id: int) -> GetUserResponse:
        return self.user_service.get_user(id)

    def update_user(self, id: int, user_data) -> GetUserResponse:
        return self.user_service.update_user(id, user_data)

    def delete_user(self, id: int) -> GetUserResponse:
        return self.user_service.delete_user(id)
