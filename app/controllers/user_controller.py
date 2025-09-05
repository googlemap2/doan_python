from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, UserUpdate
from app.utils.auth import create_access_token, verify_password
from app.utils.helpers import check_exists, PaginationHelper
from app.config.database import SessionLocal


class UserController:

    def __init__(self):
        self.db = SessionLocal()

    def login_user(self, user_data: UserLogin) -> str:
        user = self.db.query(User).filter(User.username == user_data.username).first()
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )
        access_token = create_access_token(data={"sub": user.username})
        return access_token
