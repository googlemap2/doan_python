from typing import Optional
from fastapi import APIRouter, Query
from fastapi.security import HTTPBearer
from fastapi import Request

from app.controllers.customer_controller import CustomerController
from app.schemas.customer_schema import (
    GetCustomerResponse,
    GetCustomersResponse,
    MonthlySalesReportResponse,
)


router = APIRouter(prefix="/customer", tags=["customer"])
security = HTTPBearer()
customer_controller = CustomerController()


@router.get("/")
def get_customers(
    name: str | None = Query(None),
    phone: str | None = Query(None),
    address: str | None = Query(None),
    email: str | None = Query(None),
) -> GetCustomersResponse:
    """Lấy danh sách khách hàng với các bộ lọc"""
    return customer_controller.get_customers(
        name=name,
        phone=phone,
        address=address,
        email=email,
    )


@router.get("/{phone}", response_model=GetCustomerResponse)
def get_customer(phone: str) -> GetCustomerResponse:
    """Lấy thông tin khách hàng theo số điện thoại"""
    return customer_controller.get_customer(phone=phone)


@router.put("/{phone}", response_model=GetCustomerResponse)
def update_customer(phone: str, request: Request) -> GetCustomerResponse:
    """Cập nhật thông tin khách hàng"""
    user_id = getattr(request.state, "user_id", None)
    return customer_controller.update_customer(phone=phone, user_id=user_id)


@router.get("/sales/report_monthly", response_model=MonthlySalesReportResponse)
def get_monthly_sales_report(
    month: int,
    year: int,
) -> MonthlySalesReportResponse:
    """Lấy báo cáo doanh số bán hàng theo tháng"""
    return customer_controller.get_monthly_sales_report(month, year)
