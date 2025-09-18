from typing import Optional
from fastapi import APIRouter, Query
from fastapi.security import HTTPBearer
from app.controllers.order_controller import OrderController
from fastapi import Request
from app.schemas.order_schema import (
    CreateOrder,
    CreateOrderResponse,
    GetOrderResponse,
    GetOrdersResponse,
    UpdateOrder,
)

router = APIRouter(prefix="/order", tags=["order"])
security = HTTPBearer()
order_controller = OrderController()


@router.post("/")
def create_order(order_data: CreateOrder, request: Request) -> CreateOrderResponse:
    user_id = getattr(request.state, "user_id", None)
    return order_controller.create_order(order_data, user_id)


@router.get("/", response_model=GetOrdersResponse)
def get_orders(
    customer_name: str | None = Query(None, description="Filter by customer name"),
    order_code: str | None = Query(None, description="Filter by order code"),
    product_name: str | None = Query(None, description="Filter by product name"),
    product_code: str | None = Query(None, description="Filter by product code"),
    username: str | None = Query(None, description="Filter by username"),
) -> GetOrdersResponse:
    return order_controller.get_orders(
        customer_name=customer_name,
        order_code=order_code,
        product_name=product_name,
        product_code=product_code,
        username=username,
    )


@router.get("/{order_code}", response_model=GetOrderResponse)
def get_order(order_code: str) -> GetOrderResponse:
    return order_controller.get_order(order_code)


@router.put("/{order_code}", response_model=GetOrderResponse)
def update_order(order_code: str, order_data: UpdateOrder, request: Request) -> GetOrderResponse:
    user_id = getattr(request.state, "user_id", None)
    return order_controller.update_order(order_code, order_data, user_id)
