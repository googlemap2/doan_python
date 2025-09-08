from operator import is_
from sqlalchemy import (
    Boolean,
    Column,
    String,
    Integer,
    Text,
    BigInteger,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from app.config.database import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    code = Column(String(200), nullable=False, unique=True)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    description = Column(Text)
    price = Column(BigInteger, nullable=False)
    compare_price = Column(BigInteger, nullable=False)
    image_url = Column(Text)
    color = Column(String(50), nullable=False)
    capacity = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))

    brand = relationship("Brand", back_populates="products")
    inventories = relationship("Inventory", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    created_by_user = relationship("User", foreign_keys=[created_by])
    updated_by_user = relationship("User", foreign_keys=[updated_by])

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', code='{self.code}')>"
