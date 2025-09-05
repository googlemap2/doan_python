from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.utils.auth import get_password_hash, verify_password
from app.utils.helpers import check_exists, PaginationHelper


class UserController:
    """Controller for User operations"""

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, page: int = 1, size: int = 10, search: Optional[str] = None):
        """Get paginated list of users"""
        query = self.db.query(User)

        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                (User.username.ilike(search_filter))
                | (User.email.ilike(search_filter))
                | (User.full_name.ilike(search_filter))
            )

        return PaginationHelper.paginate(query, page, size)

    def create_user(self, user_data: UserCreate) -> User:
        """Create new user"""
        # Check if username already exists
        if check_exists(self.db, User, "username", user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        # Check if email already exists
        if check_exists(self.db, User, "email", user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            is_active=user_data.is_active,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Update user"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        # Check username uniqueness if being updated
        if user_data.username and user_data.username != db_user.username:
            if check_exists(
                self.db, User, "username", user_data.username, exclude_id=user_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered",
                )

        # Check email uniqueness if being updated
        if user_data.email and user_data.email != db_user.email:
            if check_exists(
                self.db, User, "email", user_data.email, exclude_id=user_id
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

        # Update fields
        for field, value in user_data.dict(exclude_unset=True).items():
            if field == "password":
                setattr(db_user, "hashed_password", get_password_hash(value))
            else:
                setattr(db_user, field, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        self.db.delete(db_user)
        self.db.commit()
        return True

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user = self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
