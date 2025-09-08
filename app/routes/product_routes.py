from itertools import product
from urllib import response
from fastapi import APIRouter
from fastapi.security import HTTPBearer

from app.controllers.product_controller import ProductController
from app.schemas.product_schema import CreateProduct


router = APIRouter(prefix="/product", tags=["product"])
security = HTTPBearer()
product_controller = ProductController()


@router.post("/")
def create_product(product_data: CreateProduct):
    return product_controller.create_product(product_data)
