from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, Numeric, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.config.database import Base


class OrderItem(Base):

    __tablename__ = "order_items"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    order_id = Column(UUID, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(12, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_order_item_quantity_positive"),
    )

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
    order_item_inventories = relationship(
        "OrderItemInventory", back_populates="order_item"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": float(self.price) if self.price is not None else None,
            "product": self.product.to_dict() if self.product else None,
            "order_item_inventories": [
                item_inv.to_dict() for item_inv in self.order_item_inventories
            ],
        }

    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, product_id={self.product_id})>"
