from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.config.database import Base


class OrderItemInventory(Base):

    __tablename__ = "order_item_inventories"

    id = Column(Integer, primary_key=True)
    order_item_id = Column(UUID(as_uuid=True), ForeignKey("order_items.id"))
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    quantity = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "quantity > 0", name="check_order_item_inventory_quantity_positive"
        ),
    )

    order_item = relationship("OrderItem", back_populates="order_item_inventories")
    inventory = relationship("Inventory", back_populates="order_item_inventories")

    def __repr__(self):
        return f"<OrderItemInventory(id={self.id}, order_item_id={self.order_item_id}, inventory_id={self.inventory_id})>"
