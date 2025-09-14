from pydantic import BaseModel
from app.schemas.product_schema import Product
from app.schemas.base_schema import ResponseType

class Inventory(BaseModel):
    id: int
    product_id: int
    quantity: int
    supplier: str
    price: int
    created_at: str
    created_by: int
    product: Product

class ImportWarehouse(BaseModel):
    product_id: int
    quantity: int
    supplier: str
    price: int

class ImportWarehouseResponse(ResponseType[Inventory]):
    pass
