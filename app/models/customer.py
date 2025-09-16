from sqlalchemy import Column, String, Integer, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base


class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100))
    address = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())

    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))



    def to_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    orders = relationship("Order", back_populates="customer")

    def __repr__(self):
        return f"<Customer(id={self.id}, fullname='{self.fullname}', phone='{self.phone}')>"
