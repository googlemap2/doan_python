from sqlalchemy import (
    Boolean,
    Column,
    String,
    Integer,
    Text,
    BigInteger,
    DateTime,
    ForeignKey,
    delete,
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
    deleted_at = Column(DateTime, nullable=True)

    created_by = Column(Integer, ForeignKey("users.id"))
    updated_by = Column(Integer, ForeignKey("users.id"))
    deleted_by = Column(Integer, ForeignKey("users.id"))

    brand = relationship("Brand", back_populates="products")
    inventories = relationship("Inventory", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

    created_by_user = relationship("User", foreign_keys=[created_by])
    updated_by_user = relationship("User", foreign_keys=[updated_by])
    deleted_by_user = relationship("User", foreign_keys=[deleted_by])

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
            "deleted_by": self.deleted_by,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "brand": self.brand.to_dict() if self.brand else None,
            "created_by_user": (
                self.created_by_user.to_dict() if self.created_by_user else None
            ),
            "updated_by_user": (
                self.updated_by_user.to_dict() if self.updated_by_user else None
            ),
            "deleted_by_user": (
                self.deleted_by_user.to_dict() if self.deleted_by_user else None
            ),
        }

    def calculate_monthly_sales(self, month: int, year: int) -> float:
        """Tính doanh số bán sản phẩm trong tháng"""
        total_sales = 0
        for item in self.order_items:
            if (
                item.order
                and item.order.created_at
                and item.order.created_at.month == month
                and item.order.created_at.year == year
            ):
                total_sales += item.quantity * item.price
        return total_sales

    def calculate_monthly_sales_by_product(self, month: int, year: int) -> list:
        """Tính doanh số bán sản phẩm trong tháng"""
        sales_data = {}
        for item in self.order_items:
            if (
                item.order
                and item.order.created_at
                and item.order.created_at.month == month
                and item.order.created_at.year == year
            ):
                key = f"{self.name} ({self.code})"
                if key not in sales_data:
                    sales_data[key] = {
                        "product_id": self.id,
                        "product_name": self.name,
                        "product_code": self.code,
                        "total_quantity": 0,
                        "total_sales": 0,
                    }
                sales_data[key]["total_quantity"] += item.quantity
                sales_data[key]["total_sales"] += item.quantity * item.price
        return list(sales_data.values())

    def calculate_monthly_inventory_cost(self, month: int, year: int) -> float:
        """Tính số tiền nhập kho của lô hàng đã bán trong tháng"""
        total_cost = 0
        for item in self.order_items:
            if (
                item.order
                and item.order.created_at
                and item.order.created_at.month == month
                and item.order.created_at.year == year
            ):
                for oi_inv in item.order_item_inventories:
                    if oi_inv.inventory is not None:
                        total_cost += oi_inv.quantity * oi_inv.inventory.price

        return total_cost

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', code='{self.code}')>"
