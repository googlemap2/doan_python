from typing import Optional
from fastapi import APIRouter, Query
from fastapi.security import HTTPBearer
from app.controllers.order_controller import OrderController
from fastapi import Request
from app.schemas.order_schema import (CreateOrder)

router = APIRouter(prefix="/order", tags=["order"])
security = HTTPBearer()
order_controller = OrderController()


@router.post("/")
def create_order(order_data: CreateOrder, request: Request):
    user_id = getattr(request.state, "user_id", None)
    return order_controller.create_order(order_data, user_id)
