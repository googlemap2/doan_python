from typing import Optional
import uuid
from pydantic import BaseModel

from app.schemas.product_schema import Product


class OrderItem(BaseModel):
    id: uuid.UUID
    product_id: int
    quantity: int
    price: float
    product: Product

    class Config:
        from_attributes = True
