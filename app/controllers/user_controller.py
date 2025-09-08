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
        user = self.db.query(User).filter(User.username == user_data.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        if not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        access_token = create_access_token(data={"sub": user.username})
        return ResponseHelper.response_data(
            data={"access_token": access_token, "token_type": "bearer"},
            message="Login successful",
        )

    def create_user(self, user_data: UserCreate) -> CreateUserResponse:
        if self.user_service.create_user(user_data):
            return ResponseHelper.response_data(message="User created successfully")
        return ResponseHelper.response_data(
            message="User creation failed", success=False
        )

    def get_users(self) -> GetUsersResponse:
        users = self.user_service.get_users()
        return ResponseHelper.response_data(
            data=users, message="Users retrieved successfully"
        )

    def get_user(self, username: str) -> GetUserResponse:
        user = self.user_service.get_user(username)
        if not user:
            return ResponseHelper.response_data(message="User not found", success=False)
        return ResponseHelper.response_data(
            data=user, message="User retrieved successfully"
        )

    def update_user(self, username: str, user_data) -> GetUserResponse:
        user = self.user_service.update_user(username, user_data)
        if not user:
            return ResponseHelper.response_data(message="User not found", success=False)
        return ResponseHelper.response_data(
            data=user, message="User updated successfully"
        )
