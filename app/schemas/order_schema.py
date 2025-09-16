from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.base_schema import ResponseType


class OrderItemCreateOrder(BaseModel):
    product_id: int
    quantity: int

class CustomerCreateOrder(BaseModel):
    fullname: str
    phone: str
    address: str
    email: str

class CreateOrder(BaseModel):
    order_item: list[OrderItemCreateOrder]
    customer: CustomerCreateOrder