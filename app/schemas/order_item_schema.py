from typing import Optional
import uuid
from pydantic import BaseModel

from app.models import order_item_inventory
from app.schemas.order_item_inventory_schema import OrderItemInventory
from app.schemas.product_schema import Product


class OrderItem(BaseModel):
    id: uuid.UUID
    product_id: int
    quantity: int
    price: float
    product: Product
    order_item_inventories: list[OrderItemInventory]

    class Config:
        from_attributes = True
