from typing import Optional
import uuid
from pydantic import BaseModel

from app.models import inventory
from app.schemas.inventory_schema import Inventory
from app.schemas.product_schema import Product


class OrderItemInventory(BaseModel):
    quantity: int
    inventory: Inventory

    class Config:
        from_attributes = True
