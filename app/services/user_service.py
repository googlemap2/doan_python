from app.config.database import SessionLocal
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.utils.auth import get_password_hash as hash_password


class UserService:
    def __init__(self):
        self.db = SessionLocal()

    def create_user(self, user_data: UserCreate) -> bool:
        if self.check_user_exists(user_data.username):
            return False
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
        return True

    def check_user_exists(self, username: str) -> bool:
        return self.db.query(User).filter(User.username == username).first() is not None

    def get_users(self):
        users = self.db.query(User).all()
        return users
