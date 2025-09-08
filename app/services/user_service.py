from fastapi import HTTPException, status
from app.config.database import SessionLocal
from app.models.user import User
from app.schemas.user_schema import (
    CreateUserResponse,
    GetUserResponse,
    TokenResponse,
    UserCreate,
    UserLogin,
)
from app.utils.auth import (
    create_access_token,
    get_password_hash as hash_password,
    verify_password,
)
from app.utils.helpers import ResponseHelper


class UserService:
    def __init__(self):
        self.db = SessionLocal()

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
        if self.check_user_exists(user_data.username):
            return ResponseHelper.response_data(
                message="User already exists", success=False
            )
        user_data.password = hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            password=user_data.password,
            fullname=user_data.fullname,
            is_active=user_data.is_active,
            phone=user_data.phone,
        )
        self.db.add(new_user)
        self.db.commit()
        return ResponseHelper.response_data(message="User created successfully")

    def check_user_exists(self, username: str) -> bool:
        return self.db.query(User).filter(User.username == username).first() is not None

    def get_users(self):
        users = self.db.query(User).all()
        return [user.to_dict() for user in users]

    def get_user(self, username: str):
        user = self.db.query(User).filter(User.username == username).first()
        if user:
            return user.to_dict()
        return None

    def update_user(self, username: str, user_data) -> GetUserResponse:
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            return ResponseHelper.response_data(message="User not found", success=False)
        if user_data.fullname is not None:
            user.fullname = user_data.fullname
        if user_data.phone is not None:
            user.phone = user_data.phone
        if user_data.address is not None:
            user.address = user_data.address
        if user_data.is_active is not None:
            user.is_active = user_data.is_active
        if user_data.password is not None:
            user.password = hash_password(user_data.password)
        self.db.commit()
        return ResponseHelper.response_data(
            data=user.to_dict(), message="User updated successfully"
        )
