from sqlalchemy import Boolean, Column, String, DateTime, func, Integer
from sqlalchemy.orm import relationship
from app.config.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    fullname = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    address = Column(String(50), nullable=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    updated_by = Column(Integer, nullable=True)
    deleted_by = Column(Integer, nullable=True)
    created_by = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    orders = relationship(
        "Order", foreign_keys="Order.created_by", back_populates="created_by_user"
    )
    inventories = relationship(
        "Inventory",
        foreign_keys="Inventory.created_by",
        back_populates="created_by_user",
    )

    def to_dict(self, exclude_password: bool = True) -> dict:
        data = {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "phone": self.phone,
            "address": self.address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "is_active": self.is_active,
        }

        if not exclude_password:
            data["password"] = self.password

        return data

    def calculate_monthly_sales(self, month: int, year: int) -> float:
        """Tính doanh số bán hàng trong tháng"""
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
        """Thống kê doanh số bán sản phẩm trong tháng"""
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

    def calculate_monthly_inventory_cost(self, month: int, year: int) -> float:
        """Tính số tiền nhập kho của lô hàng đã bán trong tháng"""
        total_cost = 0
        for order in self.orders:
            if (
                order.created_at
                and order.created_at.month == month
                and order.created_at.year == year
            ):
                for item in order.order_items:
                    for item_inv in item.order_item_inventories:
                        inventory = item_inv.inventory
                        total_cost += item_inv.quantity * inventory.price
        return total_cost

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', fullname='{self.fullname}')>"
