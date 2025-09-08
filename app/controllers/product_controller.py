from annotated_types import T
from app.schemas.product_schema import CreateProduct
from app.services.product_service import ProductService
from app.config.database import SessionLocal
from app.utils.helpers import ResponseHelper


class ProductController:

    def __init__(self):
        self.db = SessionLocal()
        self.product_service = ProductService()

    def create_product(self, product_data: CreateProduct):
        product = self.product_service.create_product(product_data)
        if product:
            return ResponseHelper.response_data(
                data=product, message="Product created successfully"
            )
        return ResponseHelper.response_data(False, message="Failed to create product")
