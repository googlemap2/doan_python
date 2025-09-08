import code
from app.config.database import SessionLocal
from app.models.brand import Brand
from app.models.product import Product
from app.schemas.product_schema import (
    CreateProduct,
    CreateProductResponse,
)
from app.utils.helpers import ResponseHelper


class ProductService:
    def __init__(self):
        self.db = SessionLocal()

    def create_product(
        self, product_data: CreateProduct, user_id: int
    ) -> CreateProductResponse:
        if self.check_product_code_exists(product_data.code):
            return ResponseHelper.response_data(
                success=False, message="Product code already exists"
            )
        if not self.check_brand_exists(product_data.brand_id):
            return ResponseHelper.response_data(
                success=False, message="Brand does not exist"
            )
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            code=product_data.code,
            brand_id=product_data.brand_id,
            color=product_data.color,
            capacity=product_data.capacity,
            image_url=product_data.image_url,
            compare_price=product_data.compare_price or product_data.price,
            is_active=product_data.is_active,
            created_by=user_id,
        )
        self.db.add(product)
        self.db.commit()
        return ResponseHelper.response_data(
            success=True, message="Product created successfully", data=product.to_dict()
        )

    def check_product_code_exists(self, code: str) -> bool:
        return self.db.query(Product).filter(Product.code == code).first() is not None

    def check_brand_exists(self, brand_id: int) -> bool:
        return self.db.query(Brand).filter(Brand.id == brand_id).first() is not None

    def get_products(self):
        products = self.db.query(Product).all()
        return products
