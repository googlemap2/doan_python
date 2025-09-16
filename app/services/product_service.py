import code
from app.config.database import SessionLocal
from app.models.brand import Brand
from app.models.product import Product
from app.schemas.product_schema import (
    CreateProduct,
    CreateProductResponse,
    UpdateProductResponse,
    UpdateProduct,
    GetProductResponse,
    GetProductsResponse,
)
from app.utils.helpers import ResponseHelper
from datetime import datetime


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

    def get_product_by_id(self, product_id: int) -> GetProductResponse:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product:
            return ResponseHelper.response_data(
                success=True,
                message="Product retrieved successfully",
                data=product.to_dict(),
            )
        return ResponseHelper.response_data(success=False, message="Product not found")

    def get_products(
        self,
        name: str | None,
        code: str | None,
        color: str | None,
        capacity: str | None,
    ) -> GetProductsResponse:
        query = self.db.query(Product)
        query = query.filter(Product.deleted_at == None)
        if name:
            query = query.filter(Product.name.ilike(f"%{name}%"))
        if code:
            query = query.filter(Product.code == code)
        if color:
            query = query.filter(Product.color.ilike(f"%{color}%"))
        if capacity:
            query = query.filter(Product.capacity.ilike(f"%{capacity}%"))
        products = query.all()
        return ResponseHelper.response_data(
            success=True,
            message="Products retrieved successfully",
            data=[product.to_dict() for product in products],
        )

    def update_product(
        self, product_id: int, product_data: UpdateProduct, user_id: int
    ) -> UpdateProductResponse:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return ResponseHelper.response_data(
                success=False, message="Product not found"
            )
        if product_data.brand_id is not None:
            product.brand_id = product_data.brand_id
            if not self.check_brand_exists(product_data.brand_id):
                return ResponseHelper.response_data(
                    success=False, message="Brand does not exist"
                )
        if product_data.name is not None:
            product.name = product_data.name
        if product_data.description is not None:
            product.description = product_data.description
        if product_data.price is not None:
            product.price = product_data.price
        if product_data.color is not None:
            product.color = product_data.color
        if product_data.capacity is not None:
            product.capacity = product_data.capacity
        if product_data.image_url is not None:
            product.image_url = product_data.image_url
        if product_data.compare_price is not None:
            product.compare_price = product_data.compare_price
        if product_data.is_active is not None:
            product.is_active = product_data.is_active
        product.updated_by = user_id
        product.updated_at = datetime.now()
        self.db.commit()
        return ResponseHelper.response_data(
            success=True, message="Product updated successfully", data=product.to_dict()
        )

    def check_product_exists(self, product_id: int) -> bool:
        return (
            self.db.query(Product)
            .filter(Product.id == product_id)
            .filter(Product.deleted_at == None)
            .first()
            is not None
        )

    def delete_product(self, product_id: int, user_id: int) -> UpdateProductResponse:
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return ResponseHelper.response_data(
                success=False, message="Product not found"
            )
        product.is_active = False
        product.updated_by = user_id
        product.updated_at = datetime.now()
        product.deleted_at = datetime.now()
        product.deleted_by = user_id
        self.db.commit()
        return ResponseHelper.response_data(
            success=True, message="Product deleted successfully", data=product.to_dict()
        )
