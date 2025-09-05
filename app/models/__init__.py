# Import all models to ensure they are registered with SQLAlchemy
from .base import Base
from .user import User
from .brand import Brand
from .product import Product
from .customer import Customer
from .inventory import Inventory
from .order import Order
from .order_item import OrderItem
from .order_item_inventory import OrderItemInventory

# Export all models
__all__ = [
    "Base",
    "User",
    "Brand",
    "Product",
    "Customer",
    "Inventory",
    "Order",
    "OrderItem",
    "OrderItemInventory",
]
