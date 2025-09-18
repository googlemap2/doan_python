from turtle import update
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func, UUID
from sqlalchemy.orm import relationship
from app.config.database import Base
from uuid import uuid4


class Order(Base):

    __tablename__ = "orders"

    id = Column(UUID, primary_key=True, default=uuid4)
    code = Column(String)
    phone = Column(String)
    address_delivery = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    updated_by = Column(Integer, ForeignKey("users.id"))
    created_by = Column(Integer, ForeignKey("users.id"))

    customer = relationship("Customer", back_populates="orders")
    created_by_user = relationship(
        "User", 
        foreign_keys=[created_by],
        back_populates="orders"
    )
    updated_by_user = relationship(
        "User", 
        foreign_keys=[updated_by]
    )
    order_items = relationship("OrderItem", back_populates="order")

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "customer_id": self.customer_id,
            "address_delivery": self.address_delivery,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "updated_by": self.updated_by,
            "customer": self.customer.to_dict() if self.customer else None,
            "created_by_user": (
                self.created_by_user.to_dict() if self.created_by_user else None
            ),
            "updated_by_user": (
                self.updated_by_user.to_dict() if self.updated_by_user else None
            ),
            "order_items": [item.to_dict() for item in self.order_items],
        }

    def __repr__(self):
        return (
            f"<Order(id={self.id}, code='{self.code}', customer_id={self.customer_id})>"
        )
