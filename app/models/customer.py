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

    created_by_user = relationship("User", foreign_keys=[created_by])
    updated_by_user = relationship("User", foreign_keys=[updated_by])
    orders = relationship("Order", back_populates="customer")

    def to_dict(self):
        return {
            "id": self.id,
            "fullname": self.fullname,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "created_by_user": (
                self.created_by_user.to_dict() if self.created_by_user else None
            ),
            "updated_by_user": (
                self.updated_by_user.to_dict() if self.updated_by_user else None
            ),
        }

    orders = relationship("Order", back_populates="customer")

    def calculate_monthly_sales(self, month: int, year: int) -> float:
        """Tính doanh số mua hàng trong tháng"""
        total_sales = 0
        for order in self.orders:
            if (
                order.created_at
                and order.created_at.month == month
                and order.created_at.year == year
            ):
                for item in order.order_items:
                    total_sales += item.quantity * item.price
        return total_sales

    def calculate_monthly_sales_by_product(self, month: int, year: int) -> list:
        """Thống kê doanh số mua sản phẩm trong tháng"""
        sales_by_product = []
        for order in self.orders:
            if (
                order.created_at
                and order.created_at.month == month
                and order.created_at.year == year
            ):
                for item in order.order_items:
                    product_id = item.product_id
                    sales_amount = item.quantity * item.price
                    find_product = next(
                        (
                            prod
                            for prod in sales_by_product
                            if prod["product_id"] == product_id
                        ),
                        None,
                    )
                    if find_product:
                        find_product["total_sales"] += sales_amount
                    else:
                        sales_by_product.append(
                            {
                                "product_id": product_id,
                                "product_name": (
                                    item.product.name if item.product else None
                                ),
                                "product_code": (
                                    item.product.code if item.product else None
                                ),
                                "total_sales": sales_amount,
                            }
                        )
        return sales_by_product

    def __repr__(self):
        return f"<Customer(id={self.id}, fullname='{self.fullname}', phone='{self.phone}')>"
