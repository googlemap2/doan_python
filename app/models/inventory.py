from turtle import update
from sqlalchemy import (
    Column,
    String,
    Integer,
    BigInteger,
    DateTime,
    ForeignKey,
    CheckConstraint,
    func,
)
from sqlalchemy.orm import relationship
from app.config.database import Base


class Inventory(Base):

    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    supplier = Column(String)
    quantity = Column(Integer, nullable=False)
    quantity_in = Column(Integer, nullable=False)
    price = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    deleted_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_positive"),
        CheckConstraint("quantity_in >= 0", name="check_quantity_in_positive"),
    )
    created_by_user = relationship(
        "User", foreign_keys=[created_by], back_populates="inventories"
    )
    updated_by_user = relationship("User", foreign_keys=[updated_by])
    deleted_by_user = relationship("User", foreign_keys=[deleted_by])
    product = relationship("Product", back_populates="inventories")

    order_item_inventories = relationship(
        "OrderItemInventory", back_populates="inventory"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "quantity_in": self.quantity_in,
            "supplier": self.supplier,
            "price": self.price,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
            "product": self.product.to_dict() if self.product else None,
            "created_by_user": (
                self.created_by_user.to_dict() if self.created_by_user else None
            ),
            "total_price": self.total_price,
        }

    @property
    def total_price(self):
        return self.quantity * self.price

    def __repr__(self):
        return f"<Inventory(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
