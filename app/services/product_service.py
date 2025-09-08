import code
from app.config.database import SessionLocal
from app.models import brand
from app.models.product import Product
from app.schemas.product_schema import CreateProduct


class ProductService:
    def __init__(self):
        self.db = SessionLocal()

    def create_product(self, product_data: CreateProduct):
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
        )
        self.db.add(product)
        self.db.commit()
        return product
