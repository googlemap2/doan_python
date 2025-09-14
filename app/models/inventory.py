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
    created_by = Column(Integer, ForeignKey("users.id"))

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_positive"),
        CheckConstraint("quantity_in >= 0", name="check_quantity_in_positive"),
    )

    product = relationship("Product", back_populates="inventories")
    created_by_user = relationship("User", back_populates="inventories")
    order_item_inventories = relationship(
        "OrderItemInventory", back_populates="inventory"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "supplier": self.supplier,
            "price": self.price,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
            "product": self.product.to_dict() if self.product else None,
        }

    def __repr__(self):
        return f"<Inventory(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
