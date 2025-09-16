from annotated_types import T
from app.schemas.product_schema import (
    CreateProduct,
    CreateProductResponse,
    GetProductsResponse,
    UpdateProductResponse,
    UpdateProduct,
    GetProductResponse
)
from app.services.product_service import ProductService
from app.config.database import SessionLocal
from app.utils.helpers import ResponseHelper


class ProductController:

    def __init__(self):
        self.db = SessionLocal()
        self.product_service = ProductService()

    def create_product(
        self, product_data: CreateProduct, user_id: int
    ) -> CreateProductResponse:
        result = self.product_service.create_product(product_data, user_id)
        return result

    def get_products(
        self,
        name: str | None,
        code: str | None,
        color: str | None,
        capacity: str | None,
    ) -> GetProductsResponse:
        products = self.product_service.get_products(name=name, code=code, color=color, capacity=capacity)
        return products
    
    def get_product(self, product_id: int) -> GetProductResponse:
        product = self.product_service.get_product_by_id(product_id)
        return product  

    def update_product(self, product_id: int, product_data: UpdateProduct, user_id: int) -> UpdateProductResponse:
        updated_product = self.product_service.update_product(product_id, product_data, user_id)
        return updated_product

    def delete_product(self, product_id: int, user_id: int) -> UpdateProductResponse:
        deleted_product = self.product_service.delete_product(product_id, user_id)
        return deleted_product
