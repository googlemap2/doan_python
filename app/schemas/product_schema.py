from typing import Optional
from venv import create

from pydantic import BaseModel

from app.schemas.base_schema import ResponseType
from app.schemas.brand_schema import Brand
from app.schemas.user_schema import UserBase


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

class UpdateProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    brand_id: Optional[int] = None
    color: Optional[str] = None
    capacity: Optional[str] = None
    image_url: Optional[str] = None
    compare_price: Optional[float] = None
    is_active: Optional[bool] = None


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
    brand: Brand
    created_by_user: Optional[UserBase] = None
    updated_by_user: Optional[UserBase] = None


class CreateProductResponse(ResponseType[Product]):
    pass

class UpdateProductResponse(ResponseType[Product]):
    pass


class GetProductsResponse(ResponseType[list[Product]]):
    pass

class GetProductResponse(ResponseType[Product]):
    pass
