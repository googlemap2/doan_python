from typing import Optional
from h11 import Response
from pydantic import BaseModel

from app.schemas.base_schema import ResponseType


class Customer(BaseModel):
    id: int
    fullname: str
    phone: str
    address: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True


class CustomerCreateOrder(BaseModel):
    fullname: str
    phone: str
    address: Optional[str] = None
    email: Optional[str] = None


class GetCustomersResponse(ResponseType[list[Customer]]):
    pass
