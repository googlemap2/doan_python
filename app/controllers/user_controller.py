from fastapi import HTTPException, status
from app.models import user
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.auth import create_access_token, verify_password
from app.config.database import SessionLocal
from app.utils.auth import get_password_hash as hash_password
from app.services.user_service import UserService
from app.utils.helpers import ResponseHelper


class UserController:

    def __init__(self):
        self.db = SessionLocal()
        self.user_service = UserService()

    def login_user(self, user_data: UserLogin) -> str:
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
        return ResponseHelper.success(
            data={"access_token": access_token, "token_type": "bearer"},
            message="Login successful",
        )

    def create_user(self, user_data: UserCreate):
        if self.user_service.createUser(user_data):
            return {"success": True, "message": "User created successfully"}
        return {"success": False, "message": "User creation failed"}
