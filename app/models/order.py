from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    code = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_date = Column(DateTime, server_default=func.current_timestamp())
    user_id = Column(Integer, ForeignKey("users.id"))

    customer = relationship("Customer", back_populates="orders")
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return (
            f"<Order(id={self.id}, code='{self.code}', customer_id={self.customer_id})>"
        )
