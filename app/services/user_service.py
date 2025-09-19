from datetime import datetime
from fastapi import HTTPException, status
from app.config.database import SessionLocal
from app.models.user import User
from app.schemas.user_schema import (
    CreateUserResponse,
    GetUserResponse,
    TokenResponse,
    UserCreate,
    UserLogin,
    GetUsersResponse,
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
        """Đăng nhập người dùng và trả về token JWT"""
        user = self.db.query(User).filter(User.username == user_data.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tên đăng nhập hoặc mật khẩu không đúng",
            )

        if not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tên đăng nhập hoặc mật khẩu không đúng",
            )

        access_token = create_access_token(data={"sub": user.username})
        return ResponseHelper.response_data(
            data={"access_token": access_token, "token_type": "bearer"},
        )

    def create_user(self, user_data: UserCreate) -> CreateUserResponse:
        """Tạo mới người dùng"""
        if self.check_user_exists(user_data.username):
            return ResponseHelper.response_data(
                message="Người dùng đã tồn tại", success=False
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
        return ResponseHelper.response_data(data=new_user.to_dict())

    def check_user_exists(self, username: str) -> bool:
        """Kiểm tra người dùng đã tồn tại chưa"""
        return self.db.query(User).filter(User.username == username).first() is not None

    def get_users(
        self,
        username: str | None = None,
        phone: str | None = None,
        address: str | None = None,
        fullname: str | None = None,
    ) -> GetUsersResponse:
        """Lấy danh sách người dùng với các bộ lọc tùy chọn"""
        query = self.db.query(User)
        query = query.filter(User.is_active == True)
        query = query.filter(User.deleted_at == None)
        if username:
            query = query.filter(User.username == username)
        if phone:
            query = query.filter(User.phone == phone)
        if address:
            query = query.filter(User.address.ilike(f"%{address}%"))
        if fullname:
            query = query.filter(User.fullname.ilike(f"%{fullname}%"))
        users = query.all()
        return ResponseHelper.response_data(
            data=[user.to_dict() for user in users],
        )

    def get_user(self, id: int) -> GetUserResponse:
        """Lấy thông tin người dùng theo id"""
        user = self.db.query(User).filter(User.id == id).first()
        if user:
            return ResponseHelper.response_data(
                data=user.to_dict(),
            )
        return ResponseHelper.response_data(
            success=False, message="Không tìm thấy người dùng"
        )

    def update_user(self, id: int, user_data, user_id: int) -> GetUserResponse:
        """Cập nhật thông tin người dùng"""
        user = self.db.query(User).filter(User.id == id).first()
        if not user:
            return ResponseHelper.response_data(
                message="Không tìm thấy người dùng", success=False
            )
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
        user.updated_by = user_id
        self.db.commit()
        return ResponseHelper.response_data(data=user.to_dict())

    def delete_user(self, id: int, user_id: int) -> GetUserResponse:
        """Xóa người dùng"""
        user = self.db.query(User).filter(User.id == id).first()
        if not user:
            return ResponseHelper.response_data(
                message="Không tìm thấy người dùng", success=False
            )
        user.is_active = False
        user.deleted_at = datetime.now()
        user.deleted_by = user_id
        user.updated_by = user_id
        self.db.commit()
        return ResponseHelper.response_data(data=user.to_dict())
