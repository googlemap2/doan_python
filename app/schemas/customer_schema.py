import email
from typing import Optional
from venv import create
from h11 import Response
from pydantic import BaseModel

from app.schemas.base_schema import ResponseType
from app.schemas.user_schema import User


class Customer(BaseModel):
    id: int
    fullname: str
    phone: str
    address: Optional[str] = None
    email: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None
    created_by_user: User
    updated_by_user: Optional[User] = None

    class Config:
        from_attributes = True


class CustomerCreateOrder(BaseModel):
    fullname: str
    phone: str
    address: Optional[str] = None
    email: Optional[str] = None


class GetCustomersResponse(ResponseType[list[Customer]]):
    pass


class GetCustomerResponse(ResponseType[Customer]):
    pass


class MonthlySalesReportSaleProduct(BaseModel):
    product_id: int
    product_name: str
    product_code: str
    total_sales: float

    class Config:
        from_attributes = True


class MonthlySalesReport(BaseModel):
    customer_name: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    sale_products: list[MonthlySalesReportSaleProduct]
    total_sales: float

    class Config:
        from_attributes = True


class MonthlySalesReportResponse(ResponseType[list[MonthlySalesReport]]):
    pass
