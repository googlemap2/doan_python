from typing import Optional
from fastapi import APIRouter, Query
from fastapi.security import HTTPBearer
from fastapi import Request

from app.controllers.customer_controller import CustomerController
from app.schemas.customer_schema import GetCustomerResponse, GetCustomersResponse


router = APIRouter(prefix="/customer", tags=["customer"])
security = HTTPBearer()
customer_controller = CustomerController()


@router.get("/")
def get_customers(
    name: str | None = Query(None, description="Filter by customer name"),
    phone: str | None = Query(None, description="Filter by customer phone number"),
    address: str | None = Query(None, description="Filter by customer address"),
    email: str | None = Query(None, description="Filter by customer email"),
) -> GetCustomersResponse:
    return customer_controller.get_customers(
        name=name,
        phone=phone,
        address=address,
        email=email,
    )


@router.get("/{phone}", response_model=GetCustomerResponse)
def get_customer(phone: str) -> GetCustomerResponse:
    return customer_controller.get_customer(phone=phone)

@router.put("/{phone}", response_model=GetCustomerResponse)
def update_customer(phone: str, request: Request):
    user_id = getattr(request.state, "user_id", None)
    return customer_controller.update_customer(phone=phone, user_id=user_id)
