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
    deleted_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    updated_by = Column(Integer, nullable=True)
    deleted_by = Column(Integer, nullable=True)
    created_by = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    orders = relationship("Order", back_populates="created_by_user")
    inventories = relationship(
        "Inventory",
        foreign_keys="Inventory.created_by",
        back_populates="created_by_user",
    )

    def to_dict(self, exclude_password: bool = True) -> dict:
        data = {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "phone": self.phone,
            "address": self.address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "is_active": self.is_active,
        }

        if not exclude_password:
            data["password"] = self.password

        return data

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', fullname='{self.fullname}')>"
