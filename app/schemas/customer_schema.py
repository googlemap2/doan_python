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
