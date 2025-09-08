from itertools import product
from urllib import response
from fastapi import APIRouter, Request
from fastapi.security import HTTPBearer

from app.controllers.product_controller import ProductController
from app.schemas.product_schema import (
    CreateProduct,
    CreateProductResponse,
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


@router.get("/")
def get_products():
    return product_controller.get_products()
