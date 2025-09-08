from typing import Optional

from pydantic import BaseModel

from app.schemas.base_schema import ResponseType


class CreateProduct(BaseModel):
    name: str
    description: str
    price: float
    brand_id: int
    color: str
    capacity: str
    image_url: Optional[str] = None
    compare_price: Optional[float] = None
    code: str
    is_active: Optional[bool] = False


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    brand_id: int
    color: str
    capacity: str
    image_url: Optional[str] = None
    compare_price: Optional[float] = None
    code: str
    is_active: Optional[bool] = False
    created_at: str
    updated_at: Optional[str] = None
    created_by: int
    updated_by: Optional[int] = None


class CreateProductResponse(ResponseType[Product]):
    pass
