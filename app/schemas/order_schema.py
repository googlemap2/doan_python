import uuid
from venv import create
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.order_item_schema import OrderItem
from app.schemas.customer_schema import Customer, CustomerCreateOrder
from app.schemas.base_schema import ResponseType
from app.schemas.user_schema import User


class Order(BaseModel):
    id: uuid.UUID
    code: str
    customer_id: int
    created_at: str
    address_delivery: Optional[str] = None
    phone: Optional[str] = None
    created_by: int
    updated_at: Optional[str] = None
    updated_by: Optional[int] = None
    created_by_user: User
    updated_by_user: Optional[User] = None
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
    address_delivery: Optional[str] = None
    phone: Optional[str] = None


class UpdateOrder(BaseModel):
    address_delivery: Optional[str] = None
    phone: Optional[str] = None


class CreateOrderResponse(ResponseType[Optional[Order]]):
    pass


class GetOrdersResponse(ResponseType[list[Order]]):
    pass


class GetOrderResponse(ResponseType[Order]):
    pass


class MonthlySalesReportSaleProduct(BaseModel):
    product_id: int
    product_name: str
    product_code: str
    total_sales: float


class MonthlySalesReport(BaseModel):
    month: str
    sale_products: list[MonthlySalesReportSaleProduct]
    total_sales: float
    inventory_cost: float
    total_profit: float


class MonthlySalesReportResponse(ResponseType[MonthlySalesReport]):
    pass
