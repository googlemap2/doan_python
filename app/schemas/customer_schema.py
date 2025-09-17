from typing import Optional
from pydantic import BaseModel


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
