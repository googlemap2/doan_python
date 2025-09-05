from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from app.config.database import Base


class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100))
    address = Column(Text)

    orders = relationship("Order", back_populates="customer")

    def __repr__(self):
        return f"<Customer(id={self.id}, fullname='{self.fullname}', phone='{self.phone}')>"
