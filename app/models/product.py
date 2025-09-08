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
from app.models import brand


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
    updated_at = Column(DateTime, onupdate=func.current_timestamp())

    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))

    brand = relationship("Brand", back_populates="products")
    inventories = relationship("Inventory", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
    created_by_user = relationship("User", foreign_keys=[created_by])
    updated_by_user = relationship("User", foreign_keys=[updated_by])

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "brand_id": self.brand_id,
            "description": self.description,
            "price": self.price,
            "compare_price": self.compare_price,
            "image_url": self.image_url,
            "color": self.color,
            "capacity": self.capacity,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "brand": self.brand.to_dict() if self.brand else None,
            "created_by_user": (
                self.created_by_user.to_dict() if self.created_by_user else None
            ),
            "updated_by_user": (
                self.updated_by_user.to_dict() if self.updated_by_user else None
            ),
        }

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', code='{self.code}')>"
