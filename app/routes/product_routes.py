from itertools import product
from typing import Optional
from urllib import response
from fastapi import APIRouter, Query, Request
from fastapi.security import HTTPBearer

from app.controllers.product_controller import ProductController
from app.schemas.product_schema import (
    CreateProduct,
    CreateProductResponse,
    GetProductsResponse,
)


router = APIRouter(prefix="/product", tags=["product"])
security = HTTPBearer()
product_controller = ProductController()


@router.post("/", response_model=CreateProductResponse)
def create_product(
    product_data: CreateProduct,
    request: Request,
):
    user_id = getattr(request.state, "user_id", None)
    return product_controller.create_product(product_data, user_id)


@router.get("/", response_model=GetProductsResponse)
def get_products(
    name: Optional[str] = Query(None, description="Filter by product name"),
    code: Optional[str] = Query(None, description="Filter by product code"),
    color: Optional[str] = Query(None, description="Filter by product color"),
    capacity: Optional[str] = Query(None, description="Filter by product capacity"),
):
    return product_controller.get_products(
        name=name, code=code, color=color, capacity=capacity
    )
