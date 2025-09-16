from typing import Optional
from pydantic import BaseModel
from app.schemas.product_schema import Product
from app.schemas.base_schema import ResponseType
from app.schemas.user_schema import User
class Inventory(BaseModel):
    id: int
    product_id: int
    quantity: int
    quantity_in: int
    supplier: str
    price: int
    created_at: str
    created_by: int
    product: Product
    total_price: int
    created_by_user: User

class ImportWarehouse(BaseModel):
    product_id: int
    quantity: int
    supplier: str
    price: int

class UpdateInventory(BaseModel):
    quantity: int
    supplier: str
    price: int

class InventoryProduct(BaseModel):
    product_id: int
    product: Product
    quantity_in: int
    total_quantity: int

class ImportWarehouseResponse(ResponseType[Inventory]):
    pass

class GetInventoryProductResponse(ResponseType[InventoryProduct]):
    pass

class GetInventoriesResponse(ResponseType[list[Inventory]]):
    pass

class GetInventoryResponse(ResponseType[Inventory]):
    pass
