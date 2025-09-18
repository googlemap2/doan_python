from typing import Optional
from urllib import response
from fastapi import APIRouter, Query
from fastapi.security import HTTPBearer
from app.controllers.order_controller import OrderController
from fastapi import Request
from app.schemas.order_schema import (
    CreateOrder,
    CreateOrderResponse,
    GetOrderResponse,
    GetOrdersResponse,
    MonthlySalesReportResponse,
    UpdateOrder,
)

router = APIRouter(prefix="/order", tags=["order"])
security = HTTPBearer()
order_controller = OrderController()


@router.post("/")
def create_order(order_data: CreateOrder, request: Request) -> CreateOrderResponse:
    """Tạo mới đơn hàng"""
    user_id = getattr(request.state, "user_id", None)
    return order_controller.create_order(order_data, user_id)


@router.get("/", response_model=GetOrdersResponse)
def get_orders(
    customer_name: str | None = Query(None),
    order_code: str | None = Query(None),
    product_name: str | None = Query(None),
    product_code: str | None = Query(None),
    username: str | None = Query(None),
) -> GetOrdersResponse:
    """Lấy danh sách đơn hàng với các bộ lọc tùy chọn"""
    return order_controller.get_orders(
        customer_name=customer_name,
        order_code=order_code,
        product_name=product_name,
        product_code=product_code,
        username=username,
    )


@router.get("/{order_code}", response_model=GetOrderResponse)
def get_order(order_code: str) -> GetOrderResponse:
    """Lấy thông tin đơn hàng theo mã đơn hàng"""
    return order_controller.get_order(order_code)


@router.put("/{order_code}", response_model=GetOrderResponse)
def update_order(
    order_code: str, order_data: UpdateOrder, request: Request
) -> GetOrderResponse:
    """Cập nhật thông tin đơn hàng"""
    user_id = getattr(request.state, "user_id", None)
    return order_controller.update_order(order_code, order_data, user_id)


@router.get("/sales/report_monthly", response_model=MonthlySalesReportResponse)
def get_monthly_sales_report(
    month: int,
    year: int,
    username: str | None = Query(None),
) -> MonthlySalesReportResponse:
    """Báo cáo doanh số bán hàng theo tháng, có thể lọc theo username người tạo đơn hàng"""
    return order_controller.get_monthly_sales_report(username, month, year)
