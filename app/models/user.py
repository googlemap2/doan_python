from sqlalchemy import Boolean, Column, String, DateTime, func, Integer
from sqlalchemy.orm import relationship
from app.config.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    fullname = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(String(50), nullable=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=True)

    inventories = relationship("Inventory", back_populates="created_by_user")
    orders = relationship("Order", back_populates="created_by_user")

    def to_dict(self, exclude_password: bool = True) -> dict:
        data = {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "phone": self.phone,
            "address": self.address,
            "created_at": self.created_at,
            "is_active": self.is_active,
        }

        if not exclude_password:
            data["password"] = self.password

        return data

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', fullname='{self.fullname}')>"
