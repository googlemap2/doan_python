import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.order_item_schema import OrderItem
from app.schemas.customer_schema import Customer, CustomerCreateOrder
from app.schemas.base_schema import ResponseType


class Order(BaseModel):
    id: uuid.UUID
    code: str
    customer_id: int
    created_at: str
    created_by: int
    updated_at: Optional[str] = None
    updated_by: Optional[int] = None
    customer: Customer
    order_items: list[OrderItem]

    class Config:
        from_attributes = True


class OrderItemCreateOrder(BaseModel):
    product_id: int
    quantity: int


class CreateOrder(BaseModel):
    order_item: list[OrderItemCreateOrder]
    customer: CustomerCreateOrder


class CreateOrderResponse(ResponseType[Optional[Order]]):
    pass
